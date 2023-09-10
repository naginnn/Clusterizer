import json

import pandas as pd
from redis.client import Redis
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from settings.database import *
from src.models import AnswersData
from src.service.model import DataProcessor, TrainProc, fresh_learn

e = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def init_data_from_files(path: str):
    files = os.listdir(path)
    data = {
        'question_id': [],
        'question': [],
        'answer': [],
        'count': [],
        'cluster': [],
        'sentiment': [],
        'context_cluster': [],
        'corrected': [],
    }
    for file in files:
        try:
            with open(f"{path}/{file}") as f:
                    json_data = json.loads(f.read())
                    for ans in json_data.get('answers'):
                        data['question_id'].append(json_data.get('id'))
                        data['question'].append(json_data.get('question', ''))
                        data['answer'].append(str(ans.get('answer')))
                        data['count'].append(ans.get('count'))
                        data['cluster'].append(ans.get('cluster'))
                        data['sentiment'].append(ans.get('sentiment'))
                        data['context_cluster'].append(ans.get('context cluster'))
                        data['corrected'].append(ans.get('corrected'))
        except:
            print(file)

    df = pd.DataFrame(data)
    df.dropna()
    df.to_sql(name='answers_data', if_exists='append', con=e, index=False)

if __name__ == '__main__':
    # init_first_train()
    print('start finish')
    init_data_from_files(path=f"{os.getcwd()}/load_data/all")
    print('init finish')
    print('start learn')
    fresh_learn()
    print('finish learn')
