# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages
from Cython.Build import cythonize


install_requires = [
    "cython>=0.29.3",
    "numpy>=1.16.0",
    "pymongo>=3.7.2",
    "python-twitter>=3.5",
    "redis>=3.0.1",
    "toml>=0.10.0",
    "unidecode>=1.0.23",
]

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="turkish_normalization",
    version="0.0.1a",
    description="A complete text normalizer framework for Turkish language",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/talha252/tur-text-norm",
    author="Talha Çolakoğlu",
    author_email="talhacolakoglu@gmail.com",
    license="GPL v3.0+",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: Turkish",
        "Operating System :: OS Independent",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
    ],
    keywords="turkish text normalization",
    packages=find_packages(include=["turkish_normalization"]),
    install_requires=install_requires,
    setup_requires=["setuptools >= 18.0", "cython"],
    python_requires=">=3.6,<4.0",
    entry_points={
        "console_scripts": [
            "tweet-grabber=turkish_normalization.twitter_scrape.tweet_grabber:main"
        ]
    },
    ext_modules=cythonize(
        "turkish_normalization/turkish_levenshtein/weighted_levenshtein/clev.pyx"
    ),
)
