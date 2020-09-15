ut# Author: Joyce Woznica
# Async: Week 2

import nltk
import nltk, re, string, collections
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

def get_bigrams(myString):
    tokenizer = WordPunctTokenizer()
    tokens = tokenizer.tokenize(myString)
    stemmer = PorterStemmer()
    bigram_finder = BigramCollocationFinder.from_words(tokens)
    bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 500)

    for bigram_tuple in bigrams:
        x = "%s %s" % bigram_tuple
        tokens.append(x)

    result = [' '.join([stemmer.stem(w).lower() for w in x.split()]) for x in tokens if x.lower() not in stopwords.words('english') and len(x) > 8]
    return result


sentence = ["For we, the people, understand that our country."]
text = sentence

for line in sentence:
    features = get_bigrams(line)

text2 = [[word for word in line.split()] for line in text]
bigrams = nltk.bigrams(text2)
print(bigrams)

for item in bigrams:
    print(item)

# first get individual words
tokenized = text.split()
from nltk.util import ngrams
# and get a list of all the bi-grams
esBigrams = ngrams(text, 2)
# get the frequency of each bigram in our corpus
esBigramFreq = collections.Counter(esBigrams)

# what are the ten most popular ngrams in this Spanish corpus?
esBigramFreq.most_common(10)

raw = "For we, the people, understand that our country."

sequence = nltk.tokenize.word_tokenize(raw) 
bigram = ngrams(sequence,2)
freq_dist = nltk.FreqDist(bigram)
prob_dist = nltk.MLEProbDist(freq_dist)
number_of_bigrams = freq_dist.N()

freq_dist



