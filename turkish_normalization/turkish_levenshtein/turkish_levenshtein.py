import numpy as np
from . import lev_encoding
from .weighted_levenshtein import dam_lev
from turkish_normalization.utils.turkish_sanitize import turkish_spesific_chars as tsc
# TODO: add docstrings
# TODO: add type annotations

# TURKISH_ENCODING = "iso-8859-9"
# TURKISH_ENCODING = "lev-turkish"
TURKISH_ENCODING = "ascii"

START_POS = 64 - len(tsc)
assert START_POS > 32 # printable character begin
ascii_translate_table = {ord(t_c):chr(a_c) for a_c, t_c in enumerate(tsc, start=START_POS)}

def w_ord(src_char):
    return ord(tur_enc(src_char))
    # try:
    #     return int.from_bytes(src_char.encode(TURKISH_ENCODING), "big")
    # except:
    #     return 0

def tur_enc(src_str):
    try:
        res = src_str.encode(TURKISH_ENCODING)
    except UnicodeEncodeError:
        src_str = src_str.translate(ascii_translate_table)
        # try:
        res = src_str.encode(TURKISH_ENCODING)
        # except UnicodeEncodeError:
        #     res = b""
    return res


def initiliaze_costs(chars, costs):
    if not isinstance(costs, list):
        costs = [costs for _ in chars]
    zip_chars = zip(chars, costs)
    if isinstance(chars[0], tuple):
        np_costs = np.ones((256, 256), dtype=np.float64)
        for (o, n), cost in zip_chars:
            np_costs[w_ord(o), w_ord(n)] = cost
    else:
        np_costs = np.ones(256, dtype=np.float64)
        for c, cost in zip_chars:
            np_costs[w_ord(c)] = cost

    return np_costs


def turkish_levenshtein(
    source_words,
    target_word,
    *,
    threshold=None,
    ignore_repeating_char=True,
    insert_costs=None,
    substitute_costs=None,
    delete_costs=None,
    delete_adjacent_costs=None,
):
    # TODO: not sure, word counts belong here
    # dist_list = []
    if threshold is None:
        threshold = np.finfo(np.float64).max
    if ignore_repeating_char:
        delete_repeating_costs = np.zeros(256, dtype=np.float64)

    for word in source_words:
        dist = dam_lev(
            word,
            target_word,
            threshold=threshold,
            encoding=TURKISH_ENCODING,
            insert_costs=insert_costs,
            substitute_costs=substitute_costs,
            delete_costs=delete_costs,
            delete_adjacent_costs=delete_adjacent_costs,
            delete_repeating_costs=delete_repeating_costs,
        )
        yield (dist, word)
        # dist_list.append((dist, word))
    # return dist_list
