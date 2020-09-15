h# Author: Joyce Woznica
# Async: Week 2 Lab

# Import packages
import nltk
import nltk, re, string, collections
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk import FreqDist

# Read in the Emma Text
file0 = nltk.corpus.gutenberg.fileids()[0]
emmatext = nltk.corpus.gutenberg.raw(file0)
emmatokens = nltk.word_tokenize(emmatext) 
emmawords = [w.lower( ) for w in emmatokens]
# show the number of words and print the first 110 words
print(len(emmawords))
print(emmawords[ :110])

# Frequency Distribution for Emma
ndist = FreqDist(emmawords)
nitems = ndist.most_common(30)
for item in nitems:
    print (item[0], '\t', item[1])

# Digression on Tokens
emmawords2 = nltk.corpus.gutenberg.words('austen-emma.txt')
emmawords2lowercase = [w.lower() for w in emmawords2]

# length of these entities
len(emmawords)
len(emmawords2lowercase)

# compare emmawords and emmawords2
print(emmawords[:160])
print(emmawords2lowercase[:160])

# Dictionaries
emptydict = dict()
phonedict = {'Bailey':'32-16','Char':'15-18', 'Dave': '20-15'} 
# get value for Bailey
phonedict['Bailey']

# add item to index
phonedict['Avi'] = '41-54'
phonedict

# looking at the various values
phonedict.keys()
phonedict.values()
phonedict.items()

# looking when indexing is not valid
'Char' in phonedict
'Dave' not in phonedict

for pair in phonedict.items():
    print(pair)

# defining functions
# the function doublesum takes 2 numbers as parameters, either int or float
#  and returns a result which is the sum of those numbers multiplied by 2
def doublesum (x, y):
    result = 2 * (x + y)
    return result

# use function
doublesum(3, 5)
num = doublesum(3.4, 2)
num
    
# another function 
# this function takes a string and a list of words as parameters.
# It will return all the words in the list that contain the string as a substring
#**Note: My version takes out duplicates **
def searchstring (substring, wordlist):
    # initialize the result
    result = [ ]
    #  loop over all the words
    for word in wordlist:
        # test each word if it contains the substring
        if substring in word:
            # add it to the result
            # you can add a check here to make sure the word
            # doesn't already exist
            if word not in result:
                result.append(word)
    return result

# use the function
searchstring('zz', emmawords)

# multiple assignments
name, phone, location = ('Zack', '22-15', 'Room 159')
name
phone
location

# for removing token (regular expressions)
import re

# this regular expression pattern matches any word that contains all non-alphabetical
#   lower-case characters [^a-z]+
# the beginning ^ and ending $ require the match to begin and end on a word boundary 
pattern = re.compile('^[^a-z]+$')

nonAlphaMatch = pattern.match('**')

#  if it matched, print a message
if nonAlphaMatch: 'matched non-alphabetical'

# function that takes a word and returns true if it consists only
#   of non-alphabetic characters
def alpha_filter(w):
  # pattern to match a word of non-alphabetical characters
    pattern = re.compile('^[^a-z]+$')
    if (pattern.match(w)):
        return True
    else:
        return False

# let's test this filter on emmawords
alphaemmawords = [w for w in emmawords if not alpha_filter(w)]
print(len(alphaemmawords))
print(alphaemmawords[:100])

nltkstopwords = nltk.corpus.stopwords.words('english')
print(len(nltkstopwords))
print(nltkstopwords)

print(emmawords[:100])
print(emmawords[15300:15310])

# contractions and other non-words to add
morestopwords = ['could','would','might','must','need','sha','wo','y',"'s","'d",
                 "'ll","'t","'m","'re","'ve"]

stopwords = nltkstopwords + morestopwords
print(len(stopwords))
print(stopwords)

stoppedemmawords = [w for w in alphaemmawords if not w in stopwords]
print(len(stoppedemmawords))

emmadist = FreqDist(stoppedemmawords)
emmaitems = emmadist.most_common(30)
for item in emmaitems:
  print(item)

# Bigrams
emmabigrams = list(nltk.bigrams(emmawords))
print(emmabigrams[:20])

# get the measures
bigram_measures = nltk.collocations.BigramAssocMeasures()
# do not remove puncutation before doing this!!!
finder = BigramCollocationFinder.from_words(emmawords)
scored = finder.score_ngrams(bigram_measures.raw_freq)
print(type(scored))
first = scored[0]
print(type(first), first)

# look at the top 30 scored bigrams
for bscore in scored[:30]:
    print (bscore)
    
# Now we can apply our word filter to remove the punctuation
finder.apply_word_filter(alpha_filter)
scored = finder.score_ngrams(bigram_measures.raw_freq)
for bscore in scored[:30]:
    print (bscore)

# now apply stopwords
finder.apply_word_filter(lambda w: w in stopwords)
scored = finder.score_ngrams(bigram_measures.raw_freq)
for bscore in scored[:30]:
    print (bscore)

# Try something else
# remove words that only occur with a frequency 
# over some minimum threshold
finder2 = BigramCollocationFinder.from_words(emmawords)
finder2.apply_freq_filter(2)
scored = finder2.score_ngrams(bigram_measures.raw_freq)
for bscore in scored[:20]:
    print (bscore)

# remove small words
finder2.apply_ngram_filter(lambda w1, w2: len(w1) < 2)
scored = finder2.score_ngrams(bigram_measures.raw_freq)
for bscore in scored[:20]:
    print (bscore)

# mutual information and other scorers
finder3 = BigramCollocationFinder.from_words(emmawords)
scored = finder3.score_ngrams(bigram_measures.pmi)
for bscore in scored[:30]:
    print (bscore)

