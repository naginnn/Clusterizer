import pickle
import time
import zlib

import redis
from nltk.corpus import stopwords
from nltk import sent_tokenize, regexp_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
import nltk

from src.models import Clusters
from src.service.bad_word_filter import MatRemover

pd.options.mode.chained_assignment = None
import re
from sqlalchemy import select, create_engine, update, bindparam
from sqlalchemy.dialects.postgresql import insert
from tqdm import tqdm
from functools import lru_cache
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

import pymorphy2
# import jamspell

from settings.database import DATABASE_URL, DATABASE_SYNC_URL
from src.models import AnswersData
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import os
tqdm.pandas()

############
nltk.download('stopwords')
nltk.download('punkt')

class DataProcessor:
    def __init__(self, df_data):
        self._df_data = df_data
        model_path = f"{os.getcwd()}/src/service/bin"
        self.nlp = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
        # self.corrector = jamspell.TSpellCorrector()
        # loaded = self.corrector.LoadLangModel('bin//ru_small.bin')
        # if not loaded:
        #     print('Sentence corrector model not loaded!')

    def __replace_text(self):
        print('replacing symbols')

        self._df_data = self._df_data.dropna(subset=['answer'])

        self._df_data['corrected'] = self._df_data['answer'].astype(str).str.replace('_x000D_', ' ')
        self._df_data['corrected'] = self._df_data['corrected'].str.replace('\n', ' ')
        self._df_data['corrected'] = self._df_data['corrected'].str.replace('\t', ' ')
        self._df_data = self._df_data[self._df_data['corrected'].str.contains(r'[a-zA-Zа-яА-Я]+')]
        self._df_data['corrected'] = self._df_data['corrected'].str.lower()

    @lru_cache(maxsize=None)
    def _fix_sentense(self, sentense):
        return self.corrector.FixFragment(sentense)

    def __fix_all_sentenses(self):
        print('Fixing grammar')
        self._df_data['corrected'] = self._df_data['corrected'].progress_apply(lambda x: self._fix_sentense(x))

    def __replacing_abbrs(self):
        print('Replacing abbrs')
        for row_abbr in tqdm(self._df_abbr.itertuples(), total=self._df_abbr.shape[0]):
            regex = re.compile(r"\b{}\b".format(row_abbr.abbr_short), re.IGNORECASE)
            self._df_data['corrected'] = regex.sub(row_abbr.abbr_full, self._df_data['corrected'])

    @lru_cache(maxsize=None)
    def __normalize_one_token(self, morph, word: str) -> str:
        """
        Нормализация одного слова
        """
        return (morph.parse(word)[0].normal_form)

    def __tokenize_n_lemmatize(self, text, morph, stop_words=None, normalize: bool = True,
                               regexp: str = r'(?u)\b\w{2,}\b',
                               min_length: int = 2) -> list:
        """
        Функция вызывает функцию нормализации и функцию удаления стоп-слов
        """
        words = [w for sent in sent_tokenize(text) for w in regexp_tokenize(sent, regexp)]
        if normalize:
            words = [self.__normalize_one_token(morph, word) for word in words]
        if stopwords:
            stop_words = set(stop_words)
            words = [word for word in words if word not in stop_words and len(word) >= min_length]
        return words

    def __tokenize_lemmatize(self):
        morph = pymorphy2.MorphAnalyzer()
        stop_r = stopwords.words('russian')
        proc_data = self._df_data[['id', 'question', 'answer', 'count', 'corrected', 'sentiment']]
        print('Tokenizing and lemmatizing')
        proc_data.corrected = proc_data.corrected.progress_apply(
            lambda x: ' '.join(self.__tokenize_n_lemmatize(text=x, morph=morph, stop_words=stop_r)))
        proc_data = proc_data.dropna(subset=['corrected'])
        proc_data.reset_index(drop=True, inplace=True)
        return proc_data

    def __replace_mat(self):
        mat_filter = MatRemover()
        self._df_data['corrected'] = self._df_data['corrected'].progress_apply(lambda x: mat_filter.search(x))


    def __make_mood(self):
        self._df_data['sentiment'] = self._df_data['answer'].progress_apply(lambda x: self.nlp(x)[0]['label'])

    def full_processing(self):
        self.__make_mood()
        self.__replace_text()
        self.__replace_mat()
        # self.__fix_all_sentenses()
        # self.__cutting_description()
        # self.__replacing_abbrs()
        proc_data = self.__tokenize_lemmatize()
        return proc_data

class TrainProc:

    def __init__(self, proc_data: pd.DataFrame, session, key: str = 'models'):
        self._proc_data = proc_data
        self.__redis = redis.Redis(
        host='redis', port=6379, health_check_interval=10,
        socket_timeout=10, socket_keepalive=True,
        socket_connect_timeout=10, retry_on_timeout=True)
        self.key = key
        self.session = session

    def _save_train_data(self, **kwargs):
        print('Saving data to Redis')
        start = time.time()
        for kw in kwargs.keys():
            s = zlib.compress(pickle.dumps(kwargs[kw]))
            self.__redis.set(kw, s)
        print(time.time() - start)

    def _column_update(self, column):
        print('Saving data to DataBase')
        start = time.time()
        self.session.execute(
            update(AnswersData),
            self._proc_data[['id', column]].to_dict(orient='records'), )
        self.session.commit()
        print(time.time() - start)

    def train(self, redis_save=True, db_save=True):
        print('Fitting model')
        stop_r = stopwords.words('russian')

        embedder = SentenceTransformer('distiluse-base-multilingual-cased-v1')
        answer_embeddings = embedder.encode(self._proc_data.corrected, show_progress_bar=True)
        num_clusters = 10
        clustering_model = KMeans(n_clusters=num_clusters)
        clustering_model.fit(answer_embeddings)
        cluster_assignment = clustering_model.labels_
        self._proc_data['cluster'] = cluster_assignment

        clustered_sentences = [[] for i in range(num_clusters)]
        for sentence_id, cluster_id in enumerate(cluster_assignment):
            clustered_sentences[cluster_id].append(self._proc_data.corrected[sentence_id])

        idf_vector = TfidfVectorizer(stop_words=stop_r)
        # proc_data_vector = idf_vector.fit_transform(self._proc_data.answer).toarray()
        cluster_names = []
        for i, cluster in enumerate(clustered_sentences):
            idfed_cluster = idf_vector.fit_transform(cluster)
            importance = np.argsort(np.asarray(idfed_cluster.sum(axis=0)).ravel())[::-1]
            tfidf_feature_names = np.array(idf_vector.get_feature_names_out())
            cluster_features = tfidf_feature_names[importance[:2]]
            cluster_name = {'cluster': i, 'name': '/'.join(cluster_features)}

            cluster_names.append(cluster_name)
            # print("Cluster ", i + 1, cluster_features)
            print(cluster_name)
            # print("")
        for cluster_name in cluster_names:
            stmt = insert(Clusters).values(**cluster_name)
            stmt = stmt.on_conflict_do_update(
                constraint='clusters_cluster_key',
                set_=dict(name=cluster_name['name'])
            )
            self.session.execute(stmt)
        self.session.commit()
        # WRITE TO DB
        cluster_mapping = {x['cluster']: x['name'] for x in cluster_names}
        self._proc_data['context_cluster'] = self._proc_data['cluster'].apply(lambda x: cluster_mapping[x])
        # SAVE TO REDIS
        data = dict(vectorizer=idf_vector, embedder=embedder,
                    clustering_model=clustering_model, cluster_names=cluster_names)
        if db_save:
            self._column_update('cluster')
            self._column_update('corrected')
            self._column_update('sentiment')
            self._column_update('context_cluster')
        if redis_save:
            save_data = {self.key: data}
            self._save_train_data(**save_data)
        return data

class PredictProc:

    def __init__(self, key, session, model_data=None):
        self.session = session
        self.learning = False
        self.key = key
        self.__redis = redis.Redis(
            host='redis', port=6379, health_check_interval=10,
            socket_timeout=10, socket_keepalive=True,
            socket_connect_timeout=10, retry_on_timeout=True
        )
#
#     def _save_train_data(self, **kwargs):
#         print('Saving data to Redis')
#         start = time.time()
#         for kw in kwargs.keys():
#             s = zlib.compress(pickle.dumps(kwargs[kw]))
#             self.__redis.set(kw, s)
#         print(time.time() - start)
#
    def _database_insert(self, df):
        print('Saving data to DataBase')
        start = time.time()
        df.to_sql()
        print(time.time() - start)

    def _load_train_data(self, *args):
        print('Loading Redis data')
        train_data = {}
        start = time.time()
        try:
            for name in args:
                train_data = pickle.loads(zlib.decompress(self.__redis.get(name)))
        except:
            raise Exception(f'No data with keys {args} in Redis')
        print(time.time() - start)
        return train_data

    def _encode_answer(self, processed_df):
        return {"question": processed_df['question'][0],
                'answers': processed_df[
                    ['answer', 'count', 'corrected', 'cluster', 'context_cluster', 'sentiment']].to_dict('records')}

    def predict(self, json_data: dict = None, always_load_redis_data=True) -> dict:

        if not json_data:
            raise Exception('No input data!')

        start = time.time()
        if always_load_redis_data:
            self._train_data = self._load_train_data(self.key)
        else:
            if hasattr(self, '_train_data'):
                print('Using saved data!')
            else:
                self._train_data = self._load_train_data(self.key)

        vectorizer = self._train_data['vectorizer']
        embedder = self._train_data['embedder']
        clustering_model = self._train_data['clustering_model']

        print(time.time() - start)
        print('Start processing data!')

        if vectorizer is None or embedder is None or clustering_model is None:
            raise Exception('No loaded model present, load or fit first')

        data = {
            'question': [],
            'answer': [],
            'count': [],
            'id': []
        }

        for ans in json_data.get('answers'):
            data['question'].append(json_data.get('question', ''))
            data['answer'].append(str(ans.get('answer')))
            data['count'].append(ans.get('count'))
            data['id'].append(0)

        cluster_list = self.session.execute(select(Clusters.cluster, Clusters.name)).all()
        cluster_dict = {cluster_list[i][0]: cluster_list[i][1] for i in range(len(cluster_list))}

        df = pd.DataFrame(data)
        processed_df = DataProcessor(df_data=df).full_processing()
        encoded_answer = embedder.encode(processed_df.corrected, show_progress_bar=False)
        cluster_num = clustering_model.predict(encoded_answer)
        processed_df['cluster'] = cluster_num
        processed_df['context_cluster'] = processed_df['cluster'].apply(lambda x: cluster_dict[x])
        return self._encode_answer(processed_df)


engine = create_engine(DATABASE_SYNC_URL)
session = Session(engine)
def fresh_learn(redis_save=True, db_save=True):
    #df_data = pd.read_csv('model//all3.csv')
    global engine
    global session
    engine = create_engine(DATABASE_SYNC_URL)
    session = Session(engine)
    try:
        query = select(AnswersData.id, AnswersData.question_id, AnswersData.question, AnswersData.answer, AnswersData.count)
        df_data =  pd.read_sql(query, engine)
    except:
        engine = create_engine(DATABASE_SYNC_URL)
        session = Session(engine)
        query = select(AnswersData.id, AnswersData.question_id, AnswersData.question, AnswersData.answer, AnswersData.count)
        df_data =  pd.read_sql(query, engine)
    data_processor = DataProcessor(df_data=df_data)
    processed_data = data_processor.full_processing()

    train_model = TrainProc(proc_data=processed_data, session=session)
    train_model.train(redis_save=redis_save, db_save=db_save)

predictor = PredictProc(key='models', session=session)
def predict(json_data):
    global predictor
    global session
    try:
        return predictor.predict(json_data,  always_load_redis_data=False)
    except:
        print('no data')
        predictor = PredictProc(key='models', session=session)
        return predictor.predict(json_data, always_load_redis_data=False)

# json_data = {
#     "id": 6596,
#     "question": "Как Вы провели лето?",
#     "answers": [
#         {
#             "answer": "Харошо",
#             "count": 1
#         },
#         {
#             "answer": "Good",
#             "count": 1
#         },
#         {
#             "answer": "Хуёво бла бла бла психаванный",
#             "count": 1
#         }
#         ]
#         }
#
# print(predict(json_data=json_data))