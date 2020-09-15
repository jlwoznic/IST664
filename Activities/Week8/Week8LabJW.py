# Author: Joyce Woznica
# Lab - Week 8
#
import nltk

# get movie review
from nltk.corpus import sentence_polarity
import random

# get the sentence corpus and look at some sentences
# had to download nltk sentence_polarity
nltk.download('sentence_polarity')

sentences = sentence_polarity.sents()
print(len(sentences))
print(type(sentences))
print(sentence_polarity.categories())
# sentences are already tokenized, print the first four sentences
for sent in sentences[:4]:
    print(sent)

# look at the sentences by category to see how many positive and negative
pos_sents = sentence_polarity.sents(categories='pos')
print(len(pos_sents))
neg_sents = sentence_polarity.sents(categories='neg')
print(len(neg_sents))

## setup the movie reviews sentences for classification
# create a list of documents, each document is one sentence as a list of words paired with category
documents = [(sent, cat) for cat in sentence_polarity.categories() 
	for sent in sentence_polarity.sents(categories=cat)]

# look at the first and last documents - consists of all the words in the review
# followed by the category
print(documents[0])
print(documents[-1])
# randomly reorder documents
random.shuffle(documents)


# get all words from all movie_reviews and put into a frequency distribution
#   note lowercase, but no stemming or stopwords
all_words_list = [word for (sent,cat) in documents for word in sent]
all_words = nltk.FreqDist(all_words_list)
# get the 2000 most frequently appearing keywords in the corpus
word_items = all_words.most_common(2000)
word_features = [word for (word,count) in word_items]
print(word_features[:50])


# define features (keywords) of a document for a BOW/unigram baseline
# each feature is 'contains(keyword)' and is true or false depending
# on whether that keyword is in the document
def document_features(document, word_features):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['V_{}'.format(word)] = (word in document_words)
    return features

# get features sets for a document, including keyword features and category feature
featuresets = [(document_features(d, word_features), c) for (d, c) in documents]

# the feature sets are 2000 words long so you may not want to look at one
featuresets[0]

# training using naive Baysian classifier, training set is approximately 90% of data
train_set, test_set = featuresets[1000:], featuresets[:1000]
classifier = nltk.NaiveBayesClassifier.train(train_set)
# evaluate the accuracy of the classifier
nltk.classify.accuracy(classifier, test_set)

# 8/25 - Accuracy: .76

# the accuracy result may vary since we randomized the documents

# show which features of classifier are most informative
classifier.show_most_informative_features(30)

####   adding features   ####
# First run the program in the file Subjectivity.py to load the subjectivity lexicon
# copy and paste the definition of the readSubjectivity functions

# create a path to where the subjectivity file resides on your disk
# this example is for my mac
# nancymacpath = "/Users/njmccrac1/AAAdocs/research/subjectivitylexicon/hltemnlp05clues/subjclueslen1-HLTEMNLP05.tff"

# create your own path to the subjclues file
SLpath = "/Users/joycewoznica/Syracuse/IST664/Activities/Week8/subjclueslen1-HLTEMNLP05.tff"

# import the Subjectivity program as a module to use the function
# need to find this code JW
# could not get this to work
#import Subjectivity

def readSubjectivity(path):
    flexicon = open(path, 'r')
    # initialize an empty dictionary
    sldict = { }
    for line in flexicon:
        fields = line.split()   # default is to split on whitespace
        # split each field on the '=' and keep the second part as the value
        strength = fields[0].split("=")[1]
        word = fields[2].split("=")[1]
        posTag = fields[3].split("=")[1]
        stemmed = fields[4].split("=")[1]
        polarity = fields[5].split("=")[1]
        if (stemmed == 'y'):
            isStemmed = True
        else:
            isStemmed = False
        # put a dictionary entry with the word as the keyword
        #     and a list of the other values
        sldict[word] = [strength, posTag, isStemmed, polarity]
    return sldict

#SL = Subjectivity.readSubjectivity(SLpath)
# or copy the readSubjectivity function into your session and cal the fn
SL = readSubjectivity(SLpath)

# how many words are in the dictionary
len(SL.keys())

# look at words in the dictionary
print(SL['absolute'])
print(SL['shabby'])
# note what happens if the word is not there
print(SL['dog'])

# use multiple assignment to get the 4 items
strength, posTag, isStemmed, polarity = SL['absolute']
print(polarity)

# define features that include word counts of subjectivity words
# negative feature will have number of weakly negative words +
#    2 * number of strongly negative words
# positive feature has similar definition
#    not counting neutral words
def SL_features(document, word_features, SL):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['V_{}'.format(word)] = (word in document_words)
    # count variables for the 4 classes of subjectivity
    weakPos = 0
    strongPos = 0
    weakNeg = 0
    strongNeg = 0
    for word in document_words:
        if word in SL:
            strength, posTag, isStemmed, polarity = SL[word]
            if strength == 'weaksubj' and polarity == 'positive':
                weakPos += 1
            if strength == 'strongsubj' and polarity == 'positive':
                strongPos += 1
            if strength == 'weaksubj' and polarity == 'negative':
                weakNeg += 1
            if strength == 'strongsubj' and polarity == 'negative':
                strongNeg += 1
            features['positivecount'] = weakPos + (2 * strongPos)
            features['negativecount'] = weakNeg + (2 * strongNeg)      
    return features

SL_featuresets = [(SL_features(d, word_features, SL), c) for (d, c) in documents]

# show just the two sentiment lexicon features in document 0
print(documents[0])
print(SL_featuresets[0][0]['positivecount'])
print(SL_featuresets[0][0]['negativecount'])

# this gives the label of document 0
SL_featuresets[0][1]
# number of features for document 0
len(SL_featuresets[0][0].keys())

# retrain the classifier using these features
train_set, test_set = SL_featuresets[1000:], SL_featuresets[:1000]
classifier = nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)

# 8/25 - Accuracy: .784


###  Negation words
# Negation words "not", "never" and "no"
# Not can appear in contractions of the form "doesn't"
for sent in list(sentences)[:50]:
   for word in sent:
     if (word.endswith("n't")):
       print(sent)

# this list of negation words includes some "approximate negators" like hardly and rarely
negationwords = ['no', 'not', 'never', 'none', 'nowhere', 'nothing', 'noone', 'rather', 'hardly', 'scarcely', 'rarely', 'seldom', 'neither', 'nor']

# One strategy with negation words is to negate the word following the negation word
#   other strategies negate all words up to the next punctuation
# Strategy is to go through the document words in order adding the word features,
#   but if the word follows a negation words, change the feature to negated word
# Start the feature set with all 2000 word features and 2000 Not word features set to false
def NOT_features(document, word_features, negationwords):
    features = {}
    for word in word_features:
        features['V_{}'.format(word)] = False
        features['V_NOT{}'.format(word)] = False
    # go through document words in order
    for i in range(0, len(document)):
        word = document[i]
        if ((i + 1) < len(document)) and ((word in negationwords) or (word.endswith("n't"))):
            i += 1
            features['V_NOT{}'.format(document[i])] = (document[i] in word_features)
        else:
            features['V_{}'.format(word)] = (word in word_features)
    return features

# define the feature sets
NOT_featuresets = [(NOT_features(d, word_features, negationwords), c) for (d, c) in documents]
# show the values of a couple of example features
print(NOT_featuresets[0][0]['V_NOTcare'])
print(NOT_featuresets[0][0]['V_always'])

train_set, test_set = NOT_featuresets[1000:], NOT_featuresets[:1000]
classifier = nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features(30)

# 8/25 - Accuracy: .772


### Bonus python text for the Question, define a stop word list ###



# now re-run one of the feature set definitions with the new_word_features instead of word_features

# Exercise
# Let’s try using a stopword list to prune the word features. We’ll start with the NLTK stop word list, 
# but we’ll remove some of the negation words, or parts of words, that our negation filter uses. 
# This list is still pretty large.

# (In this question the python parts are preceded by the prompt >>> .)

stopwords = nltk.corpus.stopwords.words('english')
print(len(stopwords))
print(stopwords)

# remove some negation words 
negationwords.extend(['ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn'])
negationwords.extend(["ain't", "aren't", "couldn't", "didn't", "doesn't", "hadn't", 
                      "hasn't", "haven't", "isn't", "mightn't", "mustn't", "needn't", 
                      "shan't", "shouldn't", "wasn't", "weren't", "won't", "wouldn't"])


newstopwords = [word for word in stopwords if word not in negationwords]
print(len(newstopwords))
print(newstopwords)

# remove stop words from the all words list
new_all_words_list = [word for (sent,cat) in documents for word in sent if word not in newstopwords]

# continue to define a new all words dictionary, get the 2000 most common as new_word_features
new_all_words = nltk.FreqDist(new_all_words_list)
new_word_items = new_all_words.most_common(2000)

new_word_features = [word for (word,count) in new_word_items]
print(new_word_features[:30])


# Now choose to re-run one of the classifiers with the word_features having stop words removed. 
# Noting that the definition of the feature functions uses the word_features variable, choose to 
# redefine either

# 1) featuresets

featuresets = [(document_features(d, new_word_features), c) for (d, c) in documents]

# the feature sets are 2000 words long so you may not want to look at one
featuresets[0]

# training using naive Baysian classifier, training set is approximately 90% of data
train_set, test_set = featuresets[1000:], featuresets[:1000]
classifier = nltk.NaiveBayesClassifier.train(train_set)

# evaluate the accuracy of the classifier
nltk.classify.accuracy(classifier, test_set)

# 8/25 - Accuracy: .759

# the accuracy result may vary since we randomized the documents

# show which features of classifier are most informative
classifier.show_most_informative_features(30)


# 2) SL_featuresets

SL_featuresets = [(SL_features(d, new_word_features, SL), c) for (d, c) in documents]

# show just the two sentiment lexicon features in document 0
print(documents[0])
print(SL_featuresets[0][0]['positivecount'])
print(SL_featuresets[0][0]['negativecount'])

# this gives the label of document 0
SL_featuresets[0][1]
# number of features for document 0
len(SL_featuresets[0][0].keys())

# retrain the classifier using these features
train_set, test_set = SL_featuresets[1000:], SL_featuresets[:1000]
classifier = nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)

# 8/25 - Accuracy: .763

classifier.show_most_informative_features(30)

# 3) NOT_featuresets

# define the feature sets
NOT_featuresets = [(NOT_features(d, new_word_features, negationwords), c) for (d, c) in documents]
# show the values of a couple of example features
print(NOT_featuresets[0][0]['V_NOTcare'])
print(NOT_featuresets[0][0]['V_always'])

train_set, test_set = NOT_featuresets[1000:], NOT_featuresets[:1000]
classifier = nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)

# 8/25 - Accuracy: .779

classifier.show_most_informative_features(30)


# Re-run the training and test sets, train the classifier, and report on classifier accuracy in the 
# discussion. Be sure to post the baseline accuracy that you got for that type of feature set when you 
# first ran it and the new accuracy score with stopwords removed.

# Another option would be to redefine the SL_features function to have just one numeric feature that 
# would subtract the number of negative words from positive words. Again you would post a baseline 
# accuracy score for the original SL_features and a new accuracy score for the new definition of features.

