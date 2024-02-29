Author: Will Wylie
Using:
- Python 3.10.5
- Natural Language Toolkit (NLTK) || Citation:
  - Bird, Steven, Edward Loper and Ewan Klein (2009), "Natural Language Processing with Python." O’Reilly Media Inc.

NLTK Installation
Windows: https://pypi.python.org/pypi/nltk
Mac/Unix: type `pip install --user -U nltk`


Before running this script, you must install the nltk library as well
as the wordnet and punkt packages. This can be done by running the
following commands in the python shell after nltk installation:

import nltk
nltk.download('wordnet')
nltk.download('punkt')