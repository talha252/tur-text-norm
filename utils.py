import json


def read_data(filename):
    with open(filename) as fp:
        return json.load(fp)
