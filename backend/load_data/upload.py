import json
import os

import pandas as pd


def get_data_from_files(path: str):
    files = os.listdir(dir_name)
    data = {
        'id': [],
        'question': [],
        'answer': [],
        'count': [],
        'cluster': [],
        'sentiment': [],
        'context cluster': [],
        'corrected': [],
    }
    for file in files:
        with open(f'labeled/{dir_name}') as f:
            try:
                json_data = json.loads(f.read())
                for ans in json_data.get('answers'):
                    data['id'].append(json_data.get('id'))
                    data['question'].append(json_data.get('question'))
                    data['answer'].append(ans.get('answer'))
                    data['count'].append(ans.get('count'))
                    data['cluster'].append(ans.get('cluster'))
                    data['sentiment'].append(ans.get('sentiment'))
                    data['context cluster'].append(ans.get('context cluster'))
                    data['corrected'].append(ans.get('corrected'))
            except:
                print(file)
                continue

    df = pd.DataFrame(data)


if __name__ == '__main__':
    dir_name = 'labeled'
    files = os.listdir(dir_name)
    data = {
        'id': [],
        'question': [],
        'answer': [],
        'count': [],
        'cluster': [],
        'sentiment': [],
        'context cluster': [],
        'corrected': [],
                       }
    # data = {}
    for file in files:
        with open(f'labeled/{dir_name}') as f:
            try:
                jj = json.loads(f.read())
                for answ in jj.get('answers'):
                    data['id'].append(jj.get('id'))
                    data['question'].append(jj.get('question'))
                    data['answer'].append(answ.get('answer'))
                    data['count'].append(answ.get('count'))
                    data['cluster'].append(answ.get('cluster'))
                    data['sentiment'].append(answ.get('sentiment'))
                    data['context cluster'].append(answ.get('context cluster'))
                    data['corrected'].append(answ.get('corrected'))
            except:
                print(file)
                continue

    df = pd.DataFrame(data)
    df.to_csv('labeled3.csv')

