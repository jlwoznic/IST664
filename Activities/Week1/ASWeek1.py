# Author: Joyce Woznica
# Async: Week 1

import nltk

# bring up the ability to download different collections from nltk
#nltk.download()

# import a corpus
from nltk.corpus import brown
from nltk.corpus import gutenberg
brown.words()

# discussion of lists and things in python

# what are the corpuses
import nltk.corpus
dir(nltk.corpus)
print("\nAvailable corpus names:")
print(dir(nltk.corpus))

nltk.corpus.gutenberg.fileids()
file0 = nltk.corpus.gutenberg.fileids()[0]
emmatext = nltk.corpus.gutenberg.raw(file0)
type(emmatext)
len(emmatext)
emmatext[:120]
# tokenize
emmatokens = nltk.word_tokenize(emmatext)
emmatokens[:50]
emmawords = [w.lower() for w in emmatokens]
len(emmawords)
emmawords[:50]
emmavocab = sorted(set(emmawords))
emmavocab[:50]

# filter out punctuation - later

emmawords.count('love')
emmawords.count('the')
emmawords.count('bath')
emmawords.count('emma')

# creating a dictionary
from nltk import FreqDist

fdist = FreqDist(emmawords)
fdist["emma"]
fdistkeys = list(fdist.keys())
fdistkeys[:50]

# most common/frequent words
topkeys = fdist.most_common(40)
type(topkeys)
str(topkeys)
for pair in topkeys:
    print(pair)
    
# need to be careful when comparing texts - long book and short books
# need to normalize by length

numwords = len(emmawords)
topkeysnorm = [(word, freq/numwords) for (word, freq) in topkeys]
for pair in topkeysnorm:
    print(pair)
    
# for question
# get text for Sense and Sensibility
sensetext = nltk.corpus.gutenberg.raw('austen-sense.txt')
# toeknize
sensetokens = nltk.word_tokenize(sensetext)
sensewords = [w.lower() for w in sensetokens]

fdistSense = FreqDist(sensewords)
fdistSensekeys = list(fdistSense.keys())
fdistSensekeys[:50]

# most common/frequent words
topkeys = fdistSense.most_common(30)
type(topkeys)
str(topkeys)
for pair in topkeys:
    print(pair)