from weighted_levenshtein import dam_lev
import numpy as np

# TODO: add docstrings
# TODO: add type annotations

TURKISH_ENCODING = "iso-8859-9"


def w_ord(src_char):
    return int.from_bytes(src_char.encode(TURKISH_ENCODING), "big")


def tur_enc(src_str):
    return src_str.encode(TURKISH_ENCODING)


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
    delete_adjacent_costs=None,
    substitute_costs=None,
    delete_costs=None,
    adjacent_insert_cost=None
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
