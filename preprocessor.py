# CIS439 -- Checkpoint 1
# Author: Will Wylie
# Python 3.10.5
# Using NLTK || Citation:
# Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.
# Installation: https://www.nltk.org/install.html#installing-nltk

# Before running this script, you must install the nltk library as well
# as the wordnet and punkt packages. This can be done by running the
# following commands in the python shell after nltk installation:

# import nltk
# nltk.download('wordnet')
# nltk.download('punkt')

import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

GLOBAL_DICT = dict()

# Article to hold content and process it
class Article:
    def __init__(self, content=''):
        self.__content = content # Raw article content
        self.__tokens = [] # Tokenized content from nltk word_tokenize
        self.__local_dict = [] # Local dictionary for the from filtered lemmatized tokens
    
    def __preprocess(self):
        # Remove markdown
        self.__content = re.sub(r'!.*\|', '', self.__content)
        self.__content = re.sub(r'#.*;', '', self.__content)
        # Remove url
        self.__content = re.sub(r'https://en.wikipedia.org/wiki\?curid=\d+', '', self.__content)

    def process(self):
        global GLOBAL_DICT
        # Preprocess the article content (remove markdown and url)
        self.__preprocess()
        # Tokenize the content
        self.__tokens = word_tokenize(self.__content)
        # Lemmatize the tokens
        lemmatizer = WordNetLemmatizer()
        for token in self.__tokens:
            word = lemmatizer.lemmatize(token).lower()
            # Weed out poorly lemmatized words
            if not word[0].isalpha() or any(sign in word for sign in ['=', '.', '+', '/']):
                continue
            # Manipulate global dictionary
            if word in GLOBAL_DICT: # If the word is already in the dictionary
                GLOBAL_DICT[word][0] += 1 # Increment word count element
            else:
                GLOBAL_DICT[word] = [1, 0] # Add the word to global dictionary (word count, article count)
            # Local dictionary only contains a single instance of each word
            # Used for document frequency (0 in [1, 0] in global dictionary)
            if word not in self.__local_dict:
                GLOBAL_DICT[word][1] += 1 # Increment doc freq element since
                                            # the word is new to this article
                self.__local_dict.append(word)

    def get_dict(self):
        return self.__local_dict[:10]

def main():
    global GLOBAL_DICT
    # Open the file
    input = open('tiny_wikipedia.txt', 'r')
    if input is None:
        print('Error: File not found')
        return
    print('Opened file\n')

    # List to hold the articles
    articles = []
    while True:
        line = input.readline() # Read a line
        if not line:
            break # End of file
        block = Article(line) # Create a new article block
        block.process() # Process the article (tokenize, lemmatize, etc.)
        print('Pulled tokens: ', block.get_dict())
        articles.append(block) # Add the article to the list
    # Close input
    input.close()
    # Sort the dictionary alphabetically
    print('Sorting dictionary alphabetically')
    GLOBAL_DICT = {k: GLOBAL_DICT[k] for k in sorted(GLOBAL_DICT, key=str.lower)}
    # Write the dictionary to a file
    dictionary = open('dictionary.txt', 'w')
    print('Writing dictionary to "dictionary.txt"')
    word_code = 0
    local_dict = {} # For keeping track of word codes
    for key in GLOBAL_DICT:
        local_dict[key] = word_code
        dictionary.write(str(word_code) + ' ' + key + '\n')
        word_code += 1
    # Close dictionary
    dictionary.close()
    # Sort the dictionary by "global-term-frequency"
    print('Sorting dictionary by global term frequency')
    GLOBAL_DICT = {k: GLOBAL_DICT[k] for k in sorted(GLOBAL_DICT, key=lambda x: GLOBAL_DICT[x][0], reverse=True)}
    #Write to unigram file
    unigram = open('unigram.txt', 'w')
    print('Writing unigram to "unigram.txt"')
    # Write the unigram to a file
    # Format: <word-code> <word> <document-frequency> <global-term-frequency>
    for key in GLOBAL_DICT:
        unigram.write(str(local_dict[key]) + key + ' ' + str(GLOBAL_DICT[key][1]) + ' ' + str(GLOBAL_DICT[key][0]) + '\n')
    unigram.close()

main()