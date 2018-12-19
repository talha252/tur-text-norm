import json
from pymongo import MongoClient
from pprint import pprint

db = None
cfg = None
READ_COLLECTION = None
WRITE_COLLECTION = None

def get_config(path):
    with open(path) as cf:
        return json.load(cf)["database"]

def connect_database(database, host="localhost", port=27017):
    client = MongoClient(f"mongodb://{host}:{port}")
    db = client[database]
    return db

def default_reader():
    _id = cfg["tweet_id"]
    _text = cfg["text"]
    cursor = db[READ_COLLECTION].find({_id: {"$exists": True}}, {_id: 1, _text: 1})
    for res in cursor:
        yield (res[_id], res[_text])

def default_writer(tokenized):
    db[WRITE_COLLECTION].insert_one(tokenized)

if __name__ != "__main__":
    cfg = get_config("./db.json") # TODO: değişecek burası
    db = connect_database(cfg["name"], host=cfg["host"], port=cfg["port"])
    READ_COLLECTION = cfg["readfrom"]
    WRITE_COLLECTION = cfg["writeto"]

