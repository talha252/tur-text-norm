import argparse
import pathlib
import importlib.util
from tokenizer import tokenizer

# TODO: write helps

def make_parser(prog):
    default_io_path = pathlib.PurePath(__file__).parent / "default_io.py"
    token_choices = ["hashtags", "mentions", "emoticons", "urls", "emails", "numbers", "keywords", "punctuations", "words"]
    parser = argparse.ArgumentParser(prog=prog, description="Tokenize tweets")
    parser.add_argument("-r", "--reader", type=str, default=default_io_path)
    parser.add_argument("-o", "--writer", type=str, default=default_io_path)
    parser.add_argument("-t", "--tokens", nargs="*", choices=token_choices, default=token_choices)
    # parser.add_argument("--config", action="store_true")
    parser.add_argument("-v", "--verbose", default=0, action="count")
    return parser

def load_module(filepath):
    module_path = pathlib.Path(filepath)
    abs_path = module_path.resolve()
    module_name = module_path.stem

    spec = importlib.util.spec_from_file_location(module_name, abs_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    parser = make_parser(prog="Twitter Tokenizer")
    args = parser.parse_args()
    # TODO: add function checks and exceptions
    module = load_module(args.writer)
    writer = module.writer
    module = load_module(args.reader)
    reader = module.reader()

    for tweet in reader:
        result = tokenizer(tweet, args.tokens, args.verbose)
        writer(result)

if __name__ == "__main__":
    main()