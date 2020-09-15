# Author: Joyce Woznica
# Subject: Homework 1 - Comparing Corpora with Corpus Statistics
# Date: 7/20/2020
# Corpus1 = Black Beauty by Anna Sewell (noted by "bb" in the program)
# Corpus2 = King of the Wind by Marguerite Henry (noted by "kw" in the program)

# Examine the text in the documents that you chose and decide how to process the words, 
# i.e. decide on tokenization and whether to use all lower case, stopwords or lemmatization.  
# •	list the top 50 words by frequency (normalized by the length of the document)
# •	list the top 50 bigrams by frequencies, and
# •	list the top 50 bigrams by their Mutual Information scores (using min frequency 5)

# Note that you may wish to modify the stop word list, based on your question in Task 3.  
# To complete this part:
# a)	Briefly state why you chose the processing options that you did.
# b)	Are there any problems with the word or bigram lists that you found? 
#       Could you get a better list of bigrams? 
# c)	How are the top 50 bigrams by frequency different from the top 50 bigrams scored by 
#       Mutual Information?
# d)	If you modify the stop word list, or expand the methods of filtering, describe that here.
# e)	You may choose to also run top trigram lists, and include them in the analysis in part 3.

# Describe a problem or question that is based on the difference between the two documents.  
# In the case of literary works, for example, this could be how to characterize the style between 
# two authors or two works of different classes.  
# Another example would be to compare the informal text in blogs with more formal text.  
# Or you can do a topic related comparison that selects words (as in the SOTU speeches example).  
# You could also make a comparison of similar text but at two different times. 

# Now answer the question you have chosen by giving a discussion of the comparison of the texts.  
# Using one or more of the types of measures that you ran in the first task, i.e. word frequencies, 
# bigram frequencies, or bigram mutual information, make a comparison of the two documents to 
# answer the problem or question.  For this analysis, you will want to choose or to revise data 
# that will be applicable for your question. You may wish to hand pick out particular examples of 
# word frequencies, bigram frequencies or mutual information scores that contribute evidence for 
# your comparison, or combine examples into categories.  

# Make sure you include the following in your report:
# a)	Clearly describe the problem or question you are trying to address through the comparison 
#       between the two selected documents.
# b)	Present and explain insights or conclusions based on the comparison to answer the question 
#       (do not just report numbers). 

# Import packages
import nltk, re, string, collections
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.collocations import *
from nltk.metrics import BigramAssocMeasures
from nltk import FreqDist
from nltk import bigrams 
from nltk.util import ngrams
from nltk.probability import DictionaryProbDist

# for plotting
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

# Read in the text files for each book selected
textDir = "/Users/joycewoznica/Syracuse/IST664/HW/HW1/"
bbFile = 'blackbeautyF.txt'
kwFile = 'kingofthewind.txt'
bbLoc = textDir + bbFile
kwLoc = textDir + kwFile
bbtext = open(bbLoc, 'r')
kwtext = open(kwLoc, 'r')

# create a dictionary for each book to gather data about how tokens
# are decreased with each step 'Initial', 'Tokens', 'NoPunct', 'NoStop', 'NoSmall'
bbDict = dict()
kwDict = dict()

# replace newlines with spaces
bbRaw = bbtext.read().replace("\n", " ")
bbtext.close()
bbDict['Initial'] = len(bbRaw)
kwRaw = kwtext.read().replace("\n", " ")
kwtext.close()
kwDict['Initial'] = len(kwRaw)
# tokenize using nlkt.word_tokenize to create a list of each individual token
# from each text
# bbTokens -> Black Beauty Tokens
# kwTokens -> King of the Wind Tokens
bbTokens = nltk.word_tokenize(bbRaw)
kwTokens = nltk.word_tokenize(kwRaw)

# Need to strip from 0 - 113 of the tokens from Black Beauty
# since these are the Gutenberg introduction
# review the text files for cleaniness
# Describe this in the document
bbTokens = bbTokens[114:]
# no need to do this for King of the Wind

# Now we need to convert the tokens to all lowercase
bbWords = [w.lower() for w in bbTokens]
kwWords = [w.lower() for w in kwTokens]
# check the length of the list of words
bbDict['Tokens'] = len(bbWords)
kwDict['Tokens'] = len(kwWords)

# **skip this or is this the frequency for bigrams?
bbBigram = ngrams(bbTokens,2)
freq_dist = nltk.FreqDist(bbBigram)
prob_dist = nltk.MLEProbDist(freq_dist)
numBigrams = freq_dist.N()

bbTrigram = ngrams(bbTokens,3)
Tfreq_dist = nltk.FreqDist(bbTrigram)
Tprob_dist = nltk.MLEProbDist(Tfreq_dist)
numTrigrams = Tfreq_dist.N()

# Bigrams - Black Beauty
bbBigramList = list(nltk.bigrams(bbWords))
print(bbBigramList[:30])
# Bigrams - King of the Wind
kwBigramList = list(nltk.bigrams(kwWords))
print(kwBigramList[:30])

# Trigrams - Black Beauty
bbTrigramList = list(nltk.trigrams(bbWords))
print(bbTrigramList[:30])
# Trigrams - King of the Wind
kwTrigramList = list(nltk.trigrams(kwWords))
print(kwTrigramList[:30])
# **

# remove punctuation
# Function to remove punctuation and non-alphabetic characters
def remove_punc_filter(word):
    # pattern to match word of non-alphabetical characters
    mPattern = re.compile('^[^a-z]+$')
    if (mPattern.match(word)):
        return True
    else:
        return False
    
# remove punctuation from both bb and kw words
abbWords = [w for w in bbWords if not remove_punc_filter(w)]
akwWords = [w for w in kwWords if not remove_punc_filter(w)]
bbDict['NoPunc'] = len(abbWords)
abbWords[:25]
kwDict['NoPunc'] = len(akwWords)
akwWords[:25]

# remove stop words
stopWords = nltk.corpus.stopwords.words('english')
len(stopWords)
# for Black Beauty
# add some additional stop words after review of the words
bbmoreStopWords = ["'d", "n't", "ca", "'ll", "'t", "'m", "'re", "'ve",
                   "would", "could", "might", "one", "'s"]
bbstopWords = stopWords + bbmoreStopWords
len(bbstopWords)
sbbWords = [w for w in abbWords if not w in bbstopWords]
bbDict['NoStop'] = len(sbbWords)

# for King of the Wind
# need additional stop words for contractions 
# need to deal with the fact the apostrophe uses different characters
kwmoreStopWords = ["n't", "'d", "n't", "ca", "'ll", "'t", "'m", "'re", "'ve",
                   "would", "could", "might", "one", "'s", "’s", "´s"]

kwstopWords = stopWords + kwmoreStopWords
len(kwstopWords)
skwWords = [w for w in akwWords if not w in kwstopWords]
kwDict['NoStop'] = len(skwWords)

## MAYBE USE THIS?
# remove small words
# elected not to use this
finder2.apply_ngram_filter(lambda w1, w2: len(w1) < 2)
scored = finder2.score_ngrams(bigram_measures.raw_freq)
for bscore in scored[:20]:
    print (bscore)

# need to stem, but realy only want to stem "horse" and "horses"

# First list the top 50 words by frequency (normalized by the length of the document)
bbDist = FreqDist(sbbWords)
bbDist2 = DictionaryProbDist(bbDist, normalize=True)
bbDist2.prob('black')
bbDist2.prob('horse')
bbDist.plot(50)
# need to make second number number / len(sbbWords)
bbItems = bbDist.most_common(50)
# Show the normalized probability
for item in bbItems:
  print(item)

# King of the Wind Frequency Distribution
kwDist = FreqDist(skwWords)
kwDist2 = DictionaryProbDist(kwDist, normalize=True)
kwDist2.prob('said')
kwDist2.prob('agba')
kwDist.plot(50)
# need to make second number number / len(skwWords)
kwItems = kwDist.most_common(50)
for item in kwItems:
  print(item)

# try this
bbtotal = bbDict['NoStop']
kwtotal = kwDict['NoStop']

# Probability in Dictionary.ProbDist is actually No Stop Words for Denominator
for item in kwItems:
    print(item[0], item[1], item[1]/kwtotal)
    
for item in bbItems:
    print(item[0], item[1], item[1]/bbtotal)
    
# Visualize the normalized frequency - Black Beauty
bbTop50DF = pd.DataFrame(bbItems)
bbTop50DF.columns = ['word', 'frequency']
# set a column for normalized frequency
bbTotalLen = bbDict['NoStop']
bbnFreqDF = []
bbnFreqDF = pd.DataFrame(columns=['norm_freq'])

# Loop through to create normalized value
for value in bbTop50DF['frequency']:
    # get the normalized frequency
    normfreq = value/bbTotalLen
    bbnFreqDF = bbnFreqDF.append(pd.DataFrame({'norm_freq': [normfreq]}))
    
# reset the index properly
bbnFreqDF = bbnFreqDF.reset_index()
# remove bad index
bbnFreqDF = bbnFreqDF.drop(['index'], axis=1)
# need to add the columns from the other 
bbTop50DF['norm_freq'] = bbnFreqDF['norm_freq']

# plot with seaborn
fg = sns.catplot(x = "norm_freq", y = "word", hue = "word", dodge=False, 
                    height = 8, aspect = 1, palette="Spectral", kind="bar", data=bbTop50DF)
fg.set_xticklabels(rotation=25, horizontalalignment = 'center', 
                         fontweight = 'light', fontsize = 'medium')
fg._legend.remove()
fg.set(xlabel = "Normalized Frequency", ylabel = "Word", 
       title = "Top 50 Words from BLACK BEAUTY (normalized)")
    
# Visualize the normalized frequency - King of the Wind
kwTop50DF = pd.DataFrame(kwItems)
kwTop50DF.columns = ['word', 'frequency']
# set a column for normalized frequency
kwTotalLen = kwDict['NoStop']
kwnFreqDF = []
kwnFreqDF = pd.DataFrame(columns=['norm_freq'])

# Loop through to create normalized value
for value in kwTop50DF['frequency']:
    # get the normalized frequency
    normfreq = value/kwTotalLen
    kwnFreqDF = kwnFreqDF.append(pd.DataFrame({'norm_freq': [normfreq]}))
    
# reset the index properly
kwnFreqDF = kwnFreqDF.reset_index()
# remove bad index
kwnFreqDF = kwnFreqDF.drop(['index'], axis=1)
# need to add the columns from the other 
kwTop50DF['norm_freq'] = kwnFreqDF['norm_freq']

# plot with seaborn
fg = sns.catplot(x = "norm_freq", y = "word", hue = "word", dodge=False,
                    height = 8, aspect = 1, palette="Spectral", kind="bar", data=kwTop50DF)
fg.set_xticklabels(rotation=45, horizontalalignment = 'right', 
                         fontweight = 'light', fontsize = 'medium')
fg._legend.remove()
fg.set(xlabel = "Normalized Frequency", ylabel = "Word", 
       title = "Top 50 Words from KING OF THE WIND (normalized)")

# Let's start to review what we have working one text at a time
# first create the bigram association measure
bMeasures = nltk.collocations.BigramAssocMeasures()

# Black Beauty (raw)
# create the bigram finder followed by scores
bbFinder = BigramCollocationFinder.from_words(sbbWords)
# remove less frequent words
bbFinder.apply_freq_filter(3)
bbScores = bbFinder.score_ngrams(bMeasures.raw_freq)
# check the top 50 scores
for score in bbScores[:50]:
    print(score)

# Make a nice format for graphing as well as for printing
for score in bbScores[:50]:
    print("Words: ", score[0], "\tScore: ", score[1])

# Visualize the normalized frequency of the bigrams - Black Beauty
bbBig50DF = pd.DataFrame(bbScores[:50])
bbBig50DF.columns = ['words', 'norm_freq']
newbbBig50DF = []
newbbBig50DF = pd.DataFrame(columns=['words_string'])
for item in bbBig50DF['words']:
    (word1, word2) = item
    newword = word1 + ", " + word2
    newbbBig50DF = newbbBig50DF.append(pd.DataFrame({'words_string': [newword]}))

# reset the index properly
newbbBig50DF = newbbBig50DF.reset_index()
# remove bad index
newbbBig50DF = newbbBig50DF.drop(['index'], axis=1)
# need to add the columns from the other 
bbBig50DF['words_string'] = newbbBig50DF['words_string']

# plot with seaborn
fg = sns.catplot(x = "norm_freq", y = "words_string", hue = "words_string", dodge=False, 
                    height = 8, aspect = 1, palette="viridis", kind="bar", 
                    data=bbBig50DF)
fg.set_xticklabels(rotation=25, horizontalalignment = 'center', 
                         fontweight = 'light', fontsize = 'medium')
fg._legend.remove()
fg.set(xlabel = "Bigram Score", ylabel = "Bigrams", 
       title = "Top 50 Bigrams from BLACK BEAUTY")

# King of the Wind (raw)
# create the bigram finder followed by scores
kwFinder = BigramCollocationFinder.from_words(skwWords)
# remove less frequent words
kwFinder.apply_freq_filter(3)
kwScores = kwFinder.score_ngrams(bMeasures.raw_freq)
# check the top 50 scores
for score in kwScores[:50]:
    print(score)

# Make a nice format for graphing as well as for printing
for score in kwScores[:50]:
    print("Words: ", score[0], "\tScore: ", score[1])

# Visualize the normalized frequency of the bigrams - King of the Wind
kwBig50DF = pd.DataFrame(kwScores[:50])
kwBig50DF.columns = ['words', 'norm_freq']
newkwBig50DF = []
newkwBig50DF = pd.DataFrame(columns=['words_string'])
for item in kwBig50DF['words']:
    (word1, word2) = item
    newword = word1 + ", " + word2
    newkwBig50DF = newkwBig50DF.append(pd.DataFrame({'words_string': [newword]}))

# reset the index properly
newkwBig50DF = newkwBig50DF.reset_index()
# remove bad index
newkwBig50DF = newkwBig50DF.drop(['index'], axis=1)
# need to add the columns from the other 
kwBig50DF['words_string'] = newkwBig50DF['words_string']

# plot with seaborn
fg = sns.catplot(x = "norm_freq", y = "words_string", hue = "words_string", dodge=False, 
                    height = 8, aspect = 1, palette="viridis", kind="bar", 
                    data=kwBig50DF)
fg.set_xticklabels(rotation=25, horizontalalignment = 'center', 
                         fontweight = 'light', fontsize = 'medium')
fg._legend.remove()
fg.set(xlabel = "Bigram Score", ylabel = "Bigrams", 
       title = "Top 50 Bigrams from KING OF THE WIND")

## Trigrams
tMeasures = nltk.collocations.TrigramAssocMeasures()

# Black Beauty (raw)
# create the trigram finder followed by scores
bbTFinder = TrigramCollocationFinder.from_words(sbbWords)
# remove less frequent words
bbTFinder.apply_freq_filter(3)
bbTScores = bbTFinder.score_ngrams(tMeasures.raw_freq)
# check the top 50 scores
# Make a nice format for graphing as well as for printing
for score in bbTScores[:50]:
    print("Words: ", score[0], "\tScore: ", score[1])

# King of the Wind (raw)
# create the bigram finder followed by scores
kwTFinder = TrigramCollocationFinder.from_words(skwWords)
# remove less frequent words
kwTFinder.apply_freq_filter(3)
kwTScores = kwTFinder.score_ngrams(tMeasures.raw_freq)
# check the top 50 scores
# Make a nice format for graphing as well as for printing
for score in kwTScores[:50]:
    print("Words: ", score[0], "\tScore: ", score[1])

# Black Beauty (raw)
# create the trigram finder followed by scores
bbTFinder = TrigramCollocationFinder.from_words(sbbWords)
# remove less frequent words
bbTFinder.apply_freq_filter(2)
bbTScores = bbTFinder.score_ngrams(tMeasures.raw_freq)
len(bbTScores)
# check the top 50 scores
# Make a nice format for graphing as well as for printing
for score in bbTScores[:50]:
    print("Words: ", score[0], "\tScore: ", score[1])

# King of the Wind (raw)
# create the bigram finder followed by scores
kwTFinder = TrigramCollocationFinder.from_words(skwWords)
# remove less frequent words
kwTFinder.apply_freq_filter(2)
kwTScores = kwTFinder.score_ngrams(tMeasures.raw_freq)
len(kwTScores)
# check the top 50 scores
# Make a nice format for graphing as well as for printing
for score in kwTScores[:50]:
    print("Words: ", score[0], "\tScore: ", score[1])

# mutual information PMI (Pointwise Mutual Information)
# scores high things that only go together
# PMI Black Beauty (Bigrams)
bbPFinder = BigramCollocationFinder.from_words(sbbWords,window_size = 5)
# play around with Frequency filter
bbPFinder.apply_freq_filter(3)
bbPScores = bbPFinder.score_ngrams(bMeasures.pmi)
bbPMI = bbPFinder.nbest(bMeasures.pmi,50)

# to print out the answers in order using PMI
for item in bbPScores[:50]:
    print(item)

# King of the Wind (raw)
# create the bigram finder followed by scores
# set the frequency filter of 5 or more
kwPFinder = BigramCollocationFinder.from_words(skwWords,window_size = 5)
kwPFinder.apply_freq_filter(5)
kwPScores = kwPFinder.score_ngrams(bMeasures.pmi)
# check the top 50 scores
for score in kwPScores[:50]:
    print(score)


# Trigrams using PMI
bbTPFinder = TrigramCollocationFinder.from_words(sbbWords, window_size = 5)
# finder.nbest(bigram_measures.pmi, 10)
# to print out the answers in order using PMI
bbTPFinder.apply_freq_filter(3)
bbTPMI2 = bbTPFinder.score_ngrams(tMeasures.pmi)
bbTPMI = bbTPFinder.nbest(tMeasures.pmi,50)
for item in bbTPMI2[:50]:
    print(item)

kwTPFinder = TrigramCollocationFinder.from_words(skwWords, window_size = 5)
# finder.nbest(bigram_measures.pmi, 10)
# to print out the answers in order using PMI
kwTPFinder.apply_freq_filter(3)
kwTPMI2 = kwTPFinder.score_ngrams(tMeasures.pmi)
kwTPMI = kwTPFinder.nbest(tMeasures.pmi,50)
for item in kwTPMI2[:50]:
    print(item)



