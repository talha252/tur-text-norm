import sys
import twitter
from os import path
from turkish_normalization.utils import connect_database, get_config

# TODO: parametretize et, stopword path ve config dosyalarını ordan al
# TODO: constantları modülün içerisinden çıkar

def read_stopwords(path):
    with open(path) as fp:
        content = fp.read()
        return content.split()

mdir = path.dirname(path.realpath(__file__))

TWITTER_CONFIG_FILE = path.join(mdir, "twitter_config.toml")
STOPWORDS_PATH = "./data/stopwords.txt"
stopwords = read_stopwords(STOPWORDS_PATH)

cfg = get_config(TWITTER_CONFIG_FILE)
api = twitter.Api(**cfg.credentials)
DATABASE_NAME = cfg.database.name
COLLECTION = cfg.database.raw_collection
LANGUAGES = ["tr"]


def main():
    count = 1
    db = connect_database(DATABASE_NAME)
    for tweet in api.GetStreamFilter(track=stopwords, languages=LANGUAGES):
        db[COLLECTION].insert_one(tweet)
        print("Scraped Tweet: %d" % count)
        count += 1


if __name__ == "__main__":
    main()
