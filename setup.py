# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='tur_text_norm',
    version='0.0.1a',
    description='A complete text normalizer framework for Turkish language',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/talha252/tur-text-norm',
    author='Talha Çolakoğlu',
    author_email='talhacolakoglu@gmail.com',
    license='GPL v3.0+',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: Turkish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
    keywords='turkish text normalization',
    packages=find_packages(include=["tur_text_norm"]),
)
