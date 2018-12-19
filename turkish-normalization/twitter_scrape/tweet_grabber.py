import sys
import twitter
from os import path
from turkish_normalization.utils import connect_database, get_twitter_config


def read_stopwords(path):
    with open(path) as fp:
        content = fp.read()
        return content.split()


TWITTER_CONFIG_FILE = "./twitter_config.json"
STOPWORDS_PATH = "../data/stopwords.txt"
stopwords = read_stopwords(STOPWORDS_PATH)

cf = get_twitter_config(TWITTER_CONFIG_FILE)
api = twitter.Api(**cf["credentials"])
DATABASE_NAME = cf["database"]["name"]
COLLECTION = cf["database"]["raw_collection"]
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
