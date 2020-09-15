#!/usr/bin/env python
# coding: utf-8

# In[3]:





# In[2]:


import nltk


# In[52]:


my_grammar = nltk.PCFG.fromstring("""
    S -> NP VP [1.0]
    VP -> VBD TO NP [0.2] | VB DT R [0.2] | VB [0.2] | VBZ DT J [0.2] | VBZ R [0.2] 
    R ->  RB R J [0.5] | RB [0.5] 
    J -> JJ NP [0.5] | JJ TO VP [0.5]
    NP -> NNP [0.15] | NN R [0.15] | NNP JJ NP [0.1] | NNP CC NP [0.15] | NN [0.15] | NNS [0.15] | PRP MD [0.15]
    NN -> "Today" [0.2] |"day" [0.4] | "month" [0.4]
    NNP -> "Mary" [0.2] | "France" [0.4] | "Bob" [0.4]
    NNS -> "Birds" [1.0]
    CC -> "and" [1.0]
    JJ -> "last" [0.4] | "able" [0.4] |"nice" [0.2] 
    DT -> "a" [0.5] | "that" [0.5]
    TO -> "to" [1.0]
    VBZ -> "is" [0.5] | "are" [0.5]
    VBD -> "went" [1.0]
    VB -> "fly" [0.5] | "say" [0.5]
    RB -> "not" [0.25] | "necessarily" [0.25] | "again" [0.5]
    PRP -> "You" [1.0]
    MD -> "can" [1.0]
  
    """)


# In[41]:


rd_parser = nltk.RecursiveDescentParser(my_grammar)


# In[42]:


sent5list = 'Today is a nice day'.split()
for tree in rd_parser.parse(sent5list):
   print (tree)


# In[43]:


sent4list= 'Bob and Mary went to France last month again'.split()
for tree in rd_parser.parse(sent4list):
   print (tree)


# In[44]:


sent3list= 'You can say that again'.split()
for tree in rd_parser.parse(sent3list):
   print (tree)


# In[9]:


sent2list= 'Birds are not necessarily able to fly'.split()
for tree in rd_parser.parse(sent2list):
   print (tree)


# In[10]:


# Three sentences from above grammar


# In[12]:


sent2list= 'Bob and Mary say that again'.split()
for tree in rd_parser.parse(sent2list):
   print (tree)


# In[13]:


sent2list= 'Birds went to France last month again'.split()
for tree in rd_parser.parse(sent2list):
   print (tree)


# In[14]:


sent2list= 'went Today to France'.split()
for tree in rd_parser.parse(sent2list):
   print (tree)


# In[15]:


# Probability


# In[60]:


prob_grammar = nltk.PCFG.fromstring("""
    S -> NP VP [1.0]
    VP -> | VBD TO NP [0.2] | VB DT R [0.2] | VB [0.2] | VBZ DT J [0.2] | VBZ R [0.2] 
    R ->  RB R J [0.5] | RB [0.5] 
    J -> JJ NP [0.5] | JJ TO VP [0.5]
    NP -> NNP [0.15] | NN R [0.15] | NNP JJ NP [0.1] | NNP CC NP [0.15] | NN [0.15] | NNS [0.15] | PRP MD [0.15]
    NN -> "Today" [0.2] |"day" [0.4] | "month" [0.4]
    NNP -> "Mary" [0.2] | "France" [0.4] | "Bob" [0.4]
    NNS -> "Birds" [1.0]
    CC -> "and" [1.0]
    JJ -> "last" [0.4] | "able" [0.2] |"nice" [0.4] 
    DT -> "a" [0.5] | "that" [0.5]
    TO -> "to" [1.0]
    VBZ -> "is" [0.5] | "are" [0.5]
    VBD -> "went" [1.0]
    VB -> "fly" [0.5] | "say" [0.5]
    RB -> "not" [0.25] | "necessarily" [0.25] | "again" [0.5]
    PRP -> "You" [1.0]
    MD -> "can" [1.0]
  
    """)


# In[61]:


v_parser = nltk.ViterbiParser(prob_grammar)


# In[62]:


sent5list = 'Today is a nice day'.split()
for tree in v_parser.parse(sent5list):
   print (tree)


# In[63]:


sent4list= 'Bob and Mary went to France last month again'.split()
for tree in v_parser.parse(sent4list):
   print (tree)


# In[64]:


sent3list= 'You can say that again'.split()
for tree in v_parser.parse(sent3list):
   print (tree)


# In[65]:


sent2list= 'Birds are not necessarily able to fly'.split()
for tree in v_parser.parse(sent2list):
   print (tree)


# In[ ]:




