import re
from collections import defaultdict
from validMention import MENTION_PATTERN, AT_SIGNS
from validHashtag import HASHTAG_PATTERN, HT_SIGNS


EMOTICON_PATTERN = r"((:|;|=)+(\'|-)?(\)|\(|d|D|p|P|\))+|(\(|\)|\\)+(:|=)|<3)"
URL_PATTERN = r"(?:http|ftp|https)://(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
EMAIL_PATTERN = r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"
NUMBER_PATTERN = r"\d+(\.\d*)?"
KEYWORD_PATTERN = r"(RT|rt|rT|Rt|DM)"
PUNCT_PATTERN = r"[\!'#%&'\(\)*\+,\\\-\.\/:;<=>\?@\[\]\^_{|}~\$]+"
WORD_PATTERN = r"\w+(\'\w+)?"
NO_MATCH_PATTERN = r"\S+"
PATTERNS = [
    ("hashtags", HASHTAG_PATTERN),
    ("mentions", MENTION_PATTERN),
    ("emoticons", EMOTICON_PATTERN),
    ("urls", URL_PATTERN),
    ("emails", EMAIL_PATTERN),
    ("numbers",NUMBER_PATTERN),
    ("keywords", KEYWORD_PATTERN),
    ("punctuations", PUNCT_PATTERN),
    ("words", WORD_PATTERN),
    ("NO_MATCH", NO_MATCH_PATTERN),
]
TOKENS_PATTERN = re.compile("|".join("(?P<%s>%s)" % pair for pair in PATTERNS))

def tokenizer(tweet, tokens, verbose=0):
    tweet_id, tweet_text = tweet
    if verbose > 0:
        print(f"Processing Tweet - {tweet_id}")
    if verbose > 1:
        print(f"TWEET TEXT:\"{tweet_text}\"")
    if verbose > 2:
        print("FOUND TOKENS:")

    entities = {token: [] for token in tokens}
    result = {"tweet_id": tweet_id, "text": tweet_text, "entities": entities}

    for mo in TOKENS_PATTERN.finditer(tweet_text):
        kind = mo.lastgroup
        value = mo.group()
        beg, end = mo.span()
        offset = 0
        # eliminate non-capturing group
        if kind == "hashtags":
            offset = re.search(HT_SIGNS, value).start()
        elif kind == "mentions":
            offset = re.search(AT_SIGNS, value).start()
        value = value[offset:]
        beg = beg + offset
        if verbose > 2:
            print(f"{kind} = \"{value}\" ({beg}, {end})")
        if kind in tokens:
            result["entities"][kind].append({"value": value, "indices": (beg, end)})
    return result