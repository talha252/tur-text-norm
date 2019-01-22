from argparse import ArgumentParser

import turkish_normalization.turkish_levenshtein as t_lev
from turkish_normalization.utils import read_data
from turkish_normalization.utils.turkish_satinize import turkishCompare

insert_chars = "aeıioöuüğyr'h"
substitute_chars = [
    ("@", "a"),
    ('æ', 'a'),
    ("€", "e"),
    ("ı", "i"),
    ("e", "i"),
    ("μ", "u"),
    ("μ", "ü"),
    ("u", "ü"),
    ("o", "ö"),
    ("0", "o"),
    ('ø', 'o'),
    ("0", "ö"),
    ('ø', 'ö'),
    ("ß", "b"),
    ("c", "ç"),
    ("g", "ğ"),
    ("q", "g"),
    ("q", "ğ"),
    ("q", "k"),
    ("s", "ş"),
    ("$", "ş"),
    ("$", "s"),
    ("y", "ğ"),
    ("w", "v"),
]

delete_char = "ıi" # sıtandart, tiren 

def make_parser(prog):
    parser = ArgumentParser(prog=prog)
    parser.add_argument("target_word", help="the target word to be reached")
    parser.add_argument("source_words_file", help="Json files that contains possible incorrect words")
    parser.add_argument("result_file", help="Path for the results to be written")
    parser.add_argument("--threshold", type=float, default=None, help="Threshold value for Levenshtein Distance")
    parser.add_argument("--verbose", action="store_true")
    return parser

def write_data(filename, data):
    with open(filename, "w") as fp:
        for r, c, w in data:
            fp.write("%.2f %s - %d\n" % (r, w, c))

def main():
    parser = make_parser('Levenshtein Test')
    args = parser.parse_args()
    insert_costs = t_lev.initiliaze_costs(insert_chars, 0.1)
    substitute_costs = t_lev.initiliaze_costs(substitute_chars, 0.1)
    vocab = read_data(args.source_words_file)
    vocab_list = list(vocab)
    target_word = args.target_word
    # TODO: pre grouping can be done
    source_words = filter(lambda w: turkishCompare(target_word[0], w[0]), vocab_list)
    results = t_lev.turkish_levenshtein(
        source_words,
        target_word,
        threshold=args.threshold,
        insert_costs=insert_costs,
        # delete_costs=delete_costs,
        substitute_costs=substitute_costs,
    )
    result_list = []
    for dist, word in results:
        count = vocab[word]
        result_list.append((dist, count, word))
        if not args.verbose:
            continue

        if dist == -1:
            print("Word: %s - No Result!" % word)
            continue
        print("Word: %s - Score: %f" % (word, dist))

    # sort result based on distance & count of the word
    result_list = sorted(result_list, key=lambda k: (k[0], -k[1]))
    write_data(args.result_file, result_list)


if __name__ == "__main__":
    main()
    
