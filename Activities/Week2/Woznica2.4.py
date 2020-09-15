# Author: Joyce Woznica
# Async: Week 2

# Choose one of the following groups of bigrams below (A, B, or C) and 
# compute the bigram predictive probabilities, where for a bigram “w1 w2”, 
# this is the probability that w2 follows w1 in the corpus. 
# Recall that the definition of the bigram probability (from slide 9 in the lecture), 
# for a bigram "w1 w2", P(w2 | w1) = count of "w1 w2" / count of w1.

# Here is an example similar to the first group. 
# Suppose that we want to compute the bigram probability of "we bear". 
# We can count to see that there is only one occurrence of the bigram "we bear", 
# but there are 21 occurrences of the first word "we". So the bigram probability 
# is the ratio 1/21. (This makes sense because the probability that the word 
# “bear” follows the word “we” in this document is 1/21.) Please leave your answer 
# in the form of the fraction "1/21" and not compute the decimal fraction.

#Ignore capitalization in your counting.

# A. we ,
#    we will
#    we know

# B. our people
#    our journey

# C. believe that
#
#4. apply re filter  
#5. remove stopwords  
#6. remove low frequency words  
#7. repeat steps 4-6 with pmi  

#------------------------- Import packages
import nltk
from nltk import FreqDist
from nltk import word_tokenize 
import os
from io import StringIO
from nltk import bigrams
from nltk.collocations import *
from nltk.corpus import stopwords
import re
from nltk.util import ngrams
# must install this: pip install docx2txt
import docx2txt

# Set input directory and file
# Note: Had to resave as a .docx first
InputDir = "/Users/joycewoznica/Syracuse/IST664/Activities/Week2/"
inputFile = 'nlp_lecture_exercise_bigram_predictive_probabilities.docx'
fullPath = InputDir + inputFile

# Read document 
inputText = docx2txt.process(fullPath)

# Convert document to tokens 
spTokens = word_tokenize(inputText)
# remove header information and just take speech information
speech = spTokens[22:]

# Create an empty list for the words
lcSpeech = []
# Build list of words
for word in speech: 
    word = word.lower()
    lcSpeech.append(word)

# Create a dictionary with the lowercased words
wordsDist = FreqDist(lcSpeech)

# Now look at bigrams of "our people" and "our journey"
bMeasures = nltk.collocations.BigramAssocMeasures()

# Create the biggram finder and then the score based on frequency
bFinder = BigramCollocationFinder.from_words(lcSpeech)
fScores = bFinder.score_ngrams(bMeasures.raw_freq)

# fScores provide the words and their frequency.
# note: should remove punctuation
print(type(fScores))
first = fScores[0]
print(type(first))
print(first)

# Sort these scores by decreating frequency for top 45
for score in fScores[:45]:
    print(score)

# This function removes punctuation and non alpha characters
def remove_punc(word):
  # pattern to match word of non-alphabetical characters
  mPattern = re.compile('^[^a-z]+$')
  if (mPattern.match(word)):
    return True
  else:
    return False

# Take out all punctuation and redo bigrams
bFinder.apply_word_filter(remove_punc)
nScores = bFinder.score_ngrams(bMeasures.raw_freq)
for score in nScores[:45]:
    print(score)

# Get rid of standard stopwords
myStopwords = set(stopwords.words('english'))
# need to remove 'that' from stopwords since looking for 'believe that'
myStopwords.remove('that')
print(myStopwords)
bFinder.apply_word_filter(lambda word: word in myStopwords)
fScores = bFinder.score_ngrams(bMeasures.raw_freq)
for score in fScores[:45]:
    print(score)

# Find the frequency number for "believe that"
# come up with fraction


# Not sure what this does to help us
# apply a filter (on a new finder) to remove low frequency words
bFinder.apply_freq_filter(5)
lfScores = bFinder.score_ngrams(bMeasures.raw_freq)
for score in lfScores[:45]:
    print(score)

### pointwise mutual information
bFinder3 = BigramCollocationFinder.from_words(lcSpeech)
pmScores = bFinder3.score_ngrams(bMeasures.pmi)
for score in pmScores[:45]:
    print(score)

