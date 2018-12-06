import json
from pymongo import MongoClient


def read_data(filename):
    with open(filename) as fp:
        return json.load(fp)

def write_json(filename, data):
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False, sort_keys=True)
        
def get_twitter_config(path):
    with open(path) as cf:
        return json.load(cf)

def connect_database(database, host="localhost", port=27017):
    client = MongoClient(f"mongodb://{host}:{port}")
    db = client[database]
    return db
