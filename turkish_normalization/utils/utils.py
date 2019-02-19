import toml
import json
from .attr_dict import Attrdict
from pymongo import MongoClient
from functools import singledispatch
from pathlib import Path

def create_folder(*paths):
    path = Path(*paths).mkdir(parents=True, exist_ok=True)

def read_data(filename):
    with open(filename) as fp:
        return json.load(fp)

def write_json(filename, data):
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False, sort_keys=True)

def read_toml(path):
    with open(path) as cf:
        tml = toml.load(cf)
        return Attrdict(**tml)

@singledispatch
def get_config(path):
    if not path.suffix == ".toml":
        raise ValueError("Config file should be TOML file")
    return read_toml(path)

@get_config.register(str)
def _(path):
    if not path.endswith(".toml"):
        raise ValueError("Config file should be TOML file")
    return read_toml(path)


def connect_database(database, host="localhost", port=27017):
    client = MongoClient(f"mongodb://{host}:{port}")
    db = client[database]
    return db
