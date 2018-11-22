# Turkish Normalization

## Quick Descriptions

- **turkish_levenshtein:** Adapts Turkish characters to be used with `weighted-levenshtein` module. It also has some utility functions that makes dealing Turkish characters easily
- **turkish_sanitize:** Module to sanitize Turkish strings. It contains several functions that are tailored to be worked with Turkish texts.
- **twitter_tokenize:** Module to tokenize Twitter data. It is tailored to work with _20MilyonTweet_ data from http://www.kemik.yildiz.edu.tr/?id=28
- **utils.py:** Contains some utility functions.
- **test_turkish_levenshtein:** A test program to show some functionalities of the module
- **weighted-levenshtein:** Modified version of https://github.com/infoscout/weighted-levenshtein

## Requires

- Python 3.6 or greater
- [pipenv](https://pypi.org/project/pipenv/)
- [black](https://pypi.org/project/black/)

## Installation

1. Install `pipenv`
2. Clone this repository `git clone https://github.com/talha252/tur-text-norm.git`
3. Run `pipenv install` on the cloned folder

## Run

1. Run `pipenv shell` to activate virtual environment
2. Run `python3 test_turkish_levenshtein.py <correct-word>`

## Making Contribution

- Always use **black** to reformat written code
- Follow git commit message conventions. You can use `vim` editor for the formatting
