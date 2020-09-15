# Author: Joyce Woznica
# Subject: Homework 1 - Comparing Corpora with Corpus Statistics

# Import packages
import nltk
import nltk.corpus
from nltk import FreqDist
from nltk import word_tokenize 
import os
from io import StringIO
from nltk import bigrams
from nltk.collocations import *
from nltk.corpus import stopwords
import re
from nltk.util import ngrams
import string
import collections


import nltk
import nltk, re, string, collections
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk import FreqDist

# 2) Pick a file from the gutenberg corpus
#    My Selection: Sense and Sensibility
myFile = 'austen-sense.txt'
myText = nltk.corpus.gutenberg.raw(myFile)

# 3) Tokenize the Text
myTokens = nltk.word_tokenize(myText)
# 4) Convert to lowercase
myWords = [w.lower() for w in myTokens]
# check the length of the list of words
len(myWords)

#4. apply re filter  
#5. remove stopwords  
#6. remove low frequency words  
#7. repeat steps 4-6 with pmi  

# 5) Create the bigram association measure
bMeasures = nltk.collocations.BigramAssocMeasures()

# 6) Create the biggram finder and then the scores
bFinder = BigramCollocationFinder.from_words(myWords)
fScores = bFinder.score_ngrams(bMeasures.raw_freq)

# Review the scores
print(type(fScores))
first = fScores[0]
print(type(first))
print(first)

#Look at the top 20 scores
for score in fScores[:20]:
    print(score)
# NOTE: lots of punctuation in the bigrams, very few words

# This function removes punctuation and non alpha characters
# it is the filter from the coursematerial (I renamed it)
def remove_punc_filter(word):
  # pattern to match word of non-alphabetical characters
  mPattern = re.compile('^[^a-z]+$')
  if (mPattern.match(word)):
    return True
  else:
    return False

# Take out all punctuation and redo bigrams
bFinder.apply_word_filter(remove_punc_filter)
nScores = bFinder.score_ngrams(bMeasures.raw_freq)
for score in nScores[:20]:
    print(score)
# NOTE: Much better results, both words, but these are non meaning words

# Get rid of standard stopwords
myStopwords = set(stopwords.words('english'))

# need to remove 'that' from stopwords since looking for 'believe that'
print(myStopwords)
bFinder.apply_word_filter(lambda word: word in myStopwords)
fScores = bFinder.score_ngrams(bMeasures.raw_freq)
for score in fScores[:20]:
    print(score)
# NOTE: Now we see things that make sense - the mostly names here 
#       but interesting use of "dare say" and "said elinor"

# apply a filter (on a new finder) to remove low frequency words
bFinder.apply_freq_filter(5)
fScores = bFinder.score_ngrams(bMeasures.raw_freq)
for score in lfScores[:20]:
    print(score)
# NOTE: Nothing different now

# mutual information PMI (Pointwise Mutual Information)
# scores high things that only go together
bFinder = BigramCollocationFinder.from_words(myWords)
bFinder.apply_word_filter(lambda word: word in myStopwords)
bFinder.apply_word_filter(remove_punc_filter)
bFinder.apply_freq_filter(5)
fScores = bFinder.score_ngrams(bMeasures.pmi)
for score in fScores[:20]:
    print(score)
# NOTE: Seems to show lots of locations as a result, money, contractions and then some others.
