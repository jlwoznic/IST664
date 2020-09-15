# Author: Joyce Woznica
# Readings - Chapter 1, Chapter 2

import nltk

# bring up the ability to download different collections from nltk
nltk.download()

# import the book
from nltk.book import *

text1
text2

# search the text
text1.concordance("monstrous")

# my turn
text3.concordance("begat")
text2.concordance("Willoughby")
text2.concordance("Elinor")

# similar
text1.similar("monstrous")
text2.similar("monstrous")
text2.similar("love")

# common contexts
text2.common_contexts(["monstrous","very"])

# disperson plot
text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])

# generate
text3.generate()

# length
len(text3)
# sort alphabetically
sort(set(text3))

len(sort(set(text3)))
len(set(text3)) / len(text3)
text3.count("smote")
100 * text4.count('a') / len(text4)

# define functions
def lexical_diversity(text):
    return len(set(text)) / len(text)

def percentage(count, total):
    return 100 * count / total


lexical_diversity(text3)
lexical_diversity(text5)
percentage(4, 5)
percentage(text4.count('a'), len(text4))

# start with Chapter 2




