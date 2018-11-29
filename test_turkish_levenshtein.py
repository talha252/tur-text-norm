import turkish_levenshtein as t_lev
from utils import read_data
from turkish_satinize import turkishCompare

insert_chars = "aeıioöuüğyr"
delete_chars = "aeıioöuüğyr"
substitute_chars = [
    ("ı", "i"),
    ("u", "ü"),
    ("o", "ö"),
    ("g", "ğ"),
    ("q", "g"),
    ("q", "ğ"),
    ("c", "ç"),
    ("s", "ş"),
    ("$", "ş"),
    ("0", "o"),
    ("e", "i"),
]
# ('y', 'ğ')


def write_data(filename, data):
    with open(filename, "w") as fp:
        for r, c, w in data:
            fp.write("%.2f %s - %d\n" % (r, w, c))


if __name__ == "__main__":
    insert_costs = t_lev.initiliaze_costs(insert_chars, 0.1)
    delete_costs = t_lev.initiliaze_costs(delete_chars, 0.1)
    substitute_costs = t_lev.initiliaze_costs(substitute_chars, 0.1)
    vocab = read_data("./data/vocab_with_count.txt")
    vocab_list = list(vocab)
    target_word = "geliyorum"
    # TODO: pre grouping can be done
    source_words = filter(lambda w: turkishCompare(target_word[0], w[0]), vocab_list)
    results = t_lev.turkish_levenshtein(
        source_words,
        target_word,
        threshold=2.0,
        insert_costs=insert_costs,
        delete_costs=delete_costs,
        substitute_costs=substitute_costs,
    )
    result_list = []
    for dist, word in results:
        count = vocab[word]
        if dist == -1:
            print('Word: %s - No Result!' % word)
            continue
        result_list.append((dist, count, word))
        print("Word: %s - Score: %f" % (word, dist))

    # sort result based on distance & count of the word
    result_list = sorted(result_list, key=lambda k: (k[0], -k[1]))
    write_data("./results/%s_results.txt" % target_word, result_list)
