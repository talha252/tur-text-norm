import re
import json
from collections import defaultdict


whole_data = "./veri/20milyontweet/all_tweets.txt"
data_pattern = re.compile(r".* - @.* - (?P<tweet>.*)")
token_specifications = [
    ("HASHTAG", r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))#([A-Za-z_]+[A-Za-z0-9-_]+)"),
    ("MENTION", r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z_]+[A-Za-z0-9-_]+){1,15}"),
    ("EMOTICON", r"((:|;|=)+(\'|-)?(\)|\(|d|D|p|P|\))+|(\(|\)|\\)+(:|=)|<3)"),
    (
        "URLS",
        r"(?:http|ftp|https)://(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",
    ),
    ("EMAIL", r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"),
    ("NUMBER", r"\d+(\.\d*)?"),
    ("KEYWORDS", r"(RT|DM)"),
    ("PUNCTUATION", r'[\.\?\!,;\'"]+'),
    ("WORD", r"\w+(\'\w+)?"),
    ("MISMATCH", r"\S+"),
]

# TODO: içinde sayı geçen usernamelerde çöküyor

word_set = defaultdict(int)
tok_pattern = re.compile("|".join("(?P<%s>%s)" % pair for pair in token_specifications))

with open(whole_data, encoding="iso8859-9") as tweet_file:
    word_count = 0
    for line in tweet_file:
        ret = data_pattern.match(line)
        if ret is None:
            continue
        tweet_text = ret.group("tweet")
        print("Tweet %d" % current)
        for mo in tok_pattern.finditer(tweet_text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == "WORD":
                word_set[value] += 1
                word_count += 1

json_file = open("./data/vocab_with_count.txt", "w")
word_list = list(word_set)
print("Total Processed Word: %d" % word_count)
print("Total Unique Word: %d" % len(word_list))
json.dump(word_set, json_file, indent=4, ensure_ascii=False, sort_keys=True)
json_file.close()
