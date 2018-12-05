# Turkish Normalization

## Quick Descriptions

- **turkish_levenshtein:** Adapts Turkish characters to be used with `weighted-levenshtein` module. It also has some utility functions that makes dealing Turkish characters easily
- **turkish_sanitize:** Module to sanitize Turkish strings. It contains several functions that are tailored to be worked with Turkish texts.
- **twitter_tokenize:** Module to tokenize Twitter data. It is tailored to work with _20MilyonTweet_ data from http://www.kemik.yildiz.edu.tr/?id=28
- **utils.py:** Contains some utility functions.
- **test_turkish_levenshtein:** A test program to show some functionalities of the module
- **weighted-levenshtein:** Modified version of https://github.com/infoscout/weighted-levenshtein
- **twitter-scrape:** A folder that contains utility programs to scrape data from Twitter using Twitter API
  - **tweet_grabber:** Module to scrape data from Twitter. It fetches raw tweet objects from Twitter using official Twitter API. It stores the fetched data in a NoSQL database (MongoDB). Twitter credentials and database connection settings can be set via **twitter_config.json**
  - **reshape_db:** Reshapes the twitter data fetched via **twitter_grabber**. The data comes from Twitter doesn't have a unique shape and contains unnecessary attributions for our purposes. Thus, this module removes unnecessary attributions and unifies all tweet data into one shape.

## Requires

- Python 3.6 or greater
- [MongoDB](https://www.mongodb.com/) (Only to scrape data)
- [pipenv](https://pypi.org/project/pipenv/)
- [black](https://pypi.org/project/black/)

## Installation

1. Install `pipenv`
2. Install `MongoDB` (Only to scrape data)
3. Clone this repository `git clone https://github.com/talha252/tur-text-norm.git`
4. Run `pipenv install` on the cloned folder

## Run

1. Run `pipenv shell` to activate virtual environment
2. Run `python3 test_turkish_levenshtein.py <correct-word>` to test Levenshtein distance module
3. Run `python3 ./twitter-scrape/tweet_grabber.py` to fetch data from Twitter
   - Before running script, make sure that MongoDB service is running and Twitter credentials are valid
4. Run `python3 ./twitter-scrape/reshape_db.py` to reshape fetched data

## Tweet Object

Reshaping module creates a new collection for the tweet objects. Each tweet object has the following shape:

### Tweet Object

|Attribute|Type|Description|
|---------|----|-----------|
|tweet_id |String| Unique identifier for the tweet|
|full_text|String| Content of the tweet. It always contains the full content of the tweet never truncated|
|entities|Entity Object| Entities that are parsed from the tweet such as hashtags, mentions etc.|
|user|User Object| User object of the tweet's author. It contains some informations about the user (checkout the table below)
|is_extended|boolean| Boolean value that indicates whether the tweet is bigger 140 chars or not|
|is_retweeted|boolean| Boolean value that indicates whether the tweet is a retweet or not. If this value is true then, the tweet has a **retweet object** (see below).|
|is_quoted|boolean| Boolean value that indicates whether the tweet is a retweet or not. If this value is true then, the tweet has a **quote object** (see below).|
|retweet|Tweet object| Attributes of the original tweet. This attribute is only present if the tweet is a retweet.|
|quote|Tweet object| Attributes of the quoted tweet. This attribute is only present if the tweet is quoted.|

### User Object

|Attribute|Type|Description|
|---------|----|-----------|
|user_id  |String| Unique identifier for the tweet's author.|
|name     |String| Real name of the user|
|screen_name|String| Nickname of the user (user handle)|
|verified|Boolean| Whether the user is verified|
|follower_count|int| Follower count of the user|
|lang|String| The language of the user|

### Retweet & Quote Object

|Attribute|Type|Description|
|---------|----|-----------|
|tweet_id |String| Unique identifier for the **original** tweet|
|full_text|String| Full content of the original tweet.|
|is_extended|boolean| Boolean value that indicates whether the original tweet is bigger 140 chars or not|
|entities|Entity Object| Entities that are parsed from the original tweet such as hashtags, mentions etc.|
|user|User Object| User object of the original tweet's author.

### Entity Object

See https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/entities-object




## Making Contribution

- Always use **black** to reformat written code
- Follow git commit message conventions. You can use `vim` editor for the formatting
