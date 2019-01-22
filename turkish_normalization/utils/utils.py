import toml
import json
from .attr_dict import Attrdict
from pymongo import MongoClient


def read_data(filename):
    with open(filename) as fp:
        return json.load(fp)

def write_json(filename, data):
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False, sort_keys=True)
        
def get_config(path):
    if not path.endswith(".toml"):
        raise ValueError("Config file should be TOML file")
    with open(path) as cf:
        tml = toml.load(cf)
        return Attrdict(**tml)

def connect_database(database, host="localhost", port=27017):
    client = MongoClient(f"mongodb://{host}:{port}")
    db = client[database]
    return db
