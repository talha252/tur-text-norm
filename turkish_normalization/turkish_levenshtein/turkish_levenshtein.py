import numpy as np
from . import lev_encoding
from . import weighted_levenshtein as wl
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

set_costs = wl.set_costs

def initiliaze_costs(*tuples):
    chars = tuples[0][0][0]
    if isinstance(chars, tuple):
        np_costs = np.ones((256, 256), dtype=np.float64)
        for chars, cost in tuples:
            for f, t in chars:
                np_costs[w_ord(f), w_ord(t)] = cost
    else:
        np_costs = np.ones(256, dtype=np.float64)
        for chars, cost in tuples:
            for c in chars:
                np_costs[w_ord(c)] = cost
    return np_costs


def turkish_levenshtein(
    source_words,
    target_word,
    *,
    threshold=None,
):
    if threshold is None:
        threshold = np.finfo(np.float64).max

    for word in source_words:
        dist = dam_lev(
            word,
            target_word,
            threshold=threshold,
        )
        yield (dist, word)

