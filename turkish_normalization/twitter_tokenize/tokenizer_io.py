from turkish_normalization.utils import get_config, connect_database
from pprint import pprint

db = None
cfg = None
READ_COLLECTION = None
WRITE_COLLECTION = None

cfg = get_config("./db.toml") # TODO: değişecek burası

def default_reader():
    _id = cfg.database.tweet_id
    _text = cfg.database.text
    cursor = db[READ_COLLECTION].find({_id: {"$exists": True}}, {_id: 1, _text: 1})
    for res in cursor:
        try:
            yield (res[_id], res[_text])
        except:
            continue

def default_writer(tokenized):
    tweet_id = tokenized["tweet_id"]
    entities = tokenized["entities"]
    db[WRITE_COLLECTION].update({"_id": tweet_id}, {"$set": 
                                                        {"entities.words": entities["words"],
                                                         "entities.emoticons": entities["emoticons"],
                                                         "entities.keywords": entities["keywords"],
                                                         "entities.emails": entities["emails"]}})
    # db[WRITE_COLLECTION].insert_one(tokenized)

if __name__ != "__main__":
    db = cfg.database
    READ_COLLECTION = db.readfrom
    WRITE_COLLECTION = db.writeto
    db = connect_database(db.name, host=db.host, port=db.port)
    

