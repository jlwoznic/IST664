# Author: Joyce Woznica
# Lab - Week 6

import nltk
from nltk.corpus import wordnet as wn

# Pick a word
nervous = wn.synsets('nervous')

# Show lemma names
for i in range(len(nervous)): 
    print(nervous[i], ': ', nervous[i].lemma_names())
    
# Show definitions
for i in range(len(nervous)): 
    print(nervous[i], ': ', nervous[i].definition())
    
# Show examples
for i in range(len(nervous)): 
    print(nervous[i], ': ', nervous[i].examples())
    
# Pick a sysnet of the word and explore hypernums
nervous[1].hypernyms() # comes up empty

# Review paths
nervous[1].hypernym_paths()

# Look at sentiment
from nltk.corpus import sentiwordnet as swn

nervous = wn.synsets('nervous')
print(nervous)

nervoussent = swn.senti_synset('nervous.s.01')
print(nervoussent)

print(nervoussent.pos_score())
print(nervoussent.neg_score())
print(nervoussent.obj_score())

anxioussent = swn.senti_synset('anxious.s.02')
print(anxioussent)

print(anxioussent.pos_score())
print(anxioussent.neg_score())
print(anxioussent.obj_score())
