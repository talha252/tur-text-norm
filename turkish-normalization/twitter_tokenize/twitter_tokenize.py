import argparse
from tokenizer import tokenizer
from tokenizer_io import default_reader, default_writer

# TODO: write helps

def make_parser(prog):
    token_choices = ["hashtags", "mentions", "emoticons", "urls", "emails", "numbers", "keywords", "punctuations", "words"]
    parser = argparse.ArgumentParser(prog=prog, description="Tokenize tweets")
    parser.add_argument("-r", "--reader", type=str)
    parser.add_argument("-o", "--writer", type=str)
    parser.add_argument("-t", "--tokens", nargs="*", choices=token_choices, default=token_choices)
    # parser.add_argument("--config", action="store_true")
    parser.add_argument("-v", "--verbose", default=0, action="count")
    return parser

def main():
    parser = make_parser(prog="Twitter Tokenizer")
    args = parser.parse_args()
    # TODO: not complete
    if args.writer is None:
        writer = default_writer
    else:
        writer = eval()
    if args.reader is None:
        reader = default_reader()
    else:
        reader = eval()
    print(args.verbose)
    tokenizer(reader, writer, args.tokens, args.verbose)    

if __name__ == "__main__":
    main()