# Author: Joyce Woznica
# Lab 1: Week 3
# Reading Text Files

# import packages
import nltk
import os
os.getcwd()

cpFile = open('/Users/joycewoznica/Syracuse/IST664/Activities/Week3/crimeandpunishment.txt')
cpText = cpFile.read()

# let's create tokens
crimetokens = nltk.word_tokenize(cpText)
newcpText = nltk.Text(crimetokens)
# to see the word 'pass' in context
newcpText.concordance('pass')

#When we are done, we close the file.
cpFile.close()


# Next Lab - Stemming
# For this part, we will use the crime and punishment text from the file.  
# Using one of the full path forms above, read the CrimeAndPunishment file.
crimeFile = open('/Users/joycewoznica/Syracuse/IST664/Activities/Week3/crimeandpunishment.txt')
crimeText = crimeFile.read()

# let's create tokens
crimeTokens = nltk.word_tokenize(crimeText)
len(crimeTokens)
crimeTokens[:100]

# NLTK has two stemmers, Porter and Lancaster, described in section 3.6 of the NLTK book.  
# To use these stemmers, you first create them.
porter = nltk.PorterStemmer()
lancaster = nltk.LancasterStemmer()

# Then we’ll compare how the two stemmers work on a small portion of the tokens.

crimePstem = [porter.stem(t) for t in crimeTokens]
print(crimePstem[:200])

# very severe
crimeLstem = [lancaster.stem(t) for t in crimeTokens]
print(crimeLstem[:200])

# Note that the Lancaster stemmer has lower-cased all the words, and in some cases, 
# it appears to be a little more severe in removing word endings, but in others not.

# The NLTK has a lemmatizer that uses the WordNet on-line thesaurus as a dictionary to 
# look up roots and find the word.

wnl = nltk.WordNetLemmatizer()
crimeLemma = [wnl.lemmatize(t) for t in crimeTokens]
print(crimeLemma[:200])

# Note that the WordNetLemmatizer does not stem verbs and in general, 
# doesn’t stem very severely at all.
# To see the results of more sentences stemmed and lemmatized in the NLTK, 
# you can go to this NLKT stemmer and lemmatization demo page by Jacob Perkins:
#
# http://text-processing.com/demo/stem/


