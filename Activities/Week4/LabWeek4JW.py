# 
# Lab for Week 4
# Author: Joyce Woznica
#

import nltk
from nltk.corpus import gutenberg

# get a corpus
texts = gutenberg.fileids()
print(texts)
senseText = texts[2]
sense = nltk.corpus.gutenberg.raw(senseText)

# get sentences
senseSents = nltk.sent_tokenize(sense)

# do some work on each sentence
# flatten as we go
senseTokens = []
for i in range(len(senseSents)):
    sentLower = senseSents[i].lower()
    sentWords = nltk.word_tokenize(sentLower)
    senseTokens.append(sentWords)
    
# now tag with POS
sensePOS = []
for i in range(len(senseTokens)):
    pos = nltk.pos_tag(senseTokens[i])
    sensePOS.append(pos)

# what do we have now
sensePOS[0][1]

# flatten the list
senseFlat = []
for ilist in sensePOS:
    for item in ilist:
        senseFlat.append(item)
        
sensePairs = nltk.FreqDist(senseFlat)

# get the most common
sensePairs.most_common(50)

taggedPOSlist = []
for i in range(len(senseFlat)):
    tag = senseFlat[i][1]
    taggedPOSlist.append(tag)
    
senseTagFreq = nltk.FreqDist(taggedPOSlist)
senseTagFreq.most_common(50)
