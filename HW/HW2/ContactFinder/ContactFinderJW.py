# Author: Joyce Woznica
# Subject: Homework 2 - Regular Expressions
# Date: 8/9/2020

# Part 1 and then Part 3

"""
This program was adapted from the Stanford NLP class SpamLord homework assignment.
    The code has been rewritten and the data modified, nevertheless
    please do not make this code or the data public.
This version has two patterns that were suggested in comments
    in order to get you started .
"""
import sys
import os
import re
import pprint

"""
TODO
For Part 1 of our assignment, add to these two lists of patterns to match
examples of obscured email addresses and phone numbers in the text.
For optional Part 3, you may need to add other lists of patterns.
"""
# email .edu patterns

# each regular expression pattern should have exactly two sets of parentheses.
#   the first parenthesis should be around the someone part
#   the second parenthesis should be around the somewhere part
#   in an email address whose standard form is someone@somewhere.edu
# 
epatterns = []
# Iteration 1
epatterns.append('([A-Za-z]+)@([A-Za-z]+)\.edu') # match A-Z upper/lower cases with .edu
# Iteration 2
epatterns.append('([A-Za-z.]+)@([A-Za-z.]+)\.edu')
# Iteration 3
epatterns.append('([A-Za-z.]+)\s@\s([A-Za-z.]+)\.edu')
# Not so sure about this one - could get too much, but barely gets anything
# Iteration 4
epatterns.append(r'([A-Za-z.]+)\s+@\s+([A-Za-z.]+)\.[A-Za-z]+')
# Iteration 5
epatterns.append(r'([A-Za-z.]+)@([A-Za-z.]+)\.[A-Za-z]+')
# Iteration 6
epatterns.append(r'(\w+)\b.[A-Z].*\b(stanford).[A-Za-z]+.edu')
# Iteration 7
epatterns.append(r'([a-z]+).at <!--.+>.(stanford).+edu')
# Iteration 8
epatterns.append(r'([a-z]+)&#x40;(graphics.stanford).edu')
# Iteration 9
epatterns.append('([A-Za-z.]+)\s<at symbol>\s([A-Za-z.]+)\.edu')   

# JW: Below are the many things that I tried that did not work - 
# and yes, there are repeats of the above in some cases
# do not seem to work
#epatterns.append(r'(\w+)\b.[A-Z].*\b(cs.stanford).[A-Za-z]+.edu')
#epatterns.append(r'([\w.]+)\b.\w.]*\b(stanford).[\w]+/edu')
#epatterns.append(r'^([a-z]+).?\bat\b\s(\W.+).edu+')
#epatterns.append(r'([a-z]+)&#x40;(cs.stanford).edu')  
#epatterns.append(r'([a-z.]+)\b[<\>|(followed by &ldquo;]+.?@([a-z.]+).edu')
#epatterns.append('([A-Za-z.]+)@([A-Za-z.]+)\.com') 
#epatterns.append('([A-Za-z.]+)@([A-Za-z.]+)\.jhu.edu') 
#epatterns.append('([A-Za-z.]+) @ ([A-Za-z.]+)\.edu')
#epatterns.append('([A-Za-z.]+)  @  ([A-Za-z.]+)\.edu')  
#epatterns.append('([A-Za-z.]+)@([A-Za-z.]+)\.EDU')   
#epatterns.append('([A-Za-z.]+) AT ([A-Za-z.]+) DOT edu') 
#epatterns.append('([A-Za-z.]+)\s<at symbol>\s([A-Za-z.]+)\.edu')    
#epatterns.append('([A-Za-z.]+)&#x40;([A-Za-z.]+)\.edu')        
#epatterns.append('([A-Za-z.]+)<del>@([A-Za-z.]+)\.edu')   
#epatterns.append('([A-Za-z.]+) WHERE ([A-Za-z.]+) DOM edu')       
#epatterns.append('([A-Za-z.]+) [at]+ ([A-Za-z.]+)\.edu')
#epatterns.append('([A-Za-z.]+)\s*\<at symbol\>\s*([A-Za-z.]+)(?:.| dot | DOT | dt | DOM )(edu|EDU|com|COM)')
#epatterns.append('([\w-]+|[\w-]+\.[\w-]+)\.edu') 
#epatterns.append('obfuscate\(\'(\w+)\.(\w+)\',\'(\w+)\'\)')
#epatterns.append('obfuscate\(\'(([\w-]+\s*(\.|;|dot|DOM)\s*)+)(-?[eE]-?[dD]-?[uU]|com)\',\'(\w+)\'\)')
#epatterns.append('([A-Za-z.]+)@([A-Za-z.]+)\.com')
#epatterns.append('([A-Za-z.]+) at ([A-Za-z;]+)edu')
#epatterns.append('([A-Za-z.]+) at ([A-Za-z.\s]+) dot edu')


# phone patterns
# each regular expression pattern should have exactly three sets of parentheses.
#   the first parenthesis should be around the area code part XXX
#   the second parenthesis should be around the exchange part YYY
#   the third parenthesis should be around the number part ZZZZ
#   in a phone number whose standard form is XXX-YYY-ZZZZ
ppatterns = []
# Iteration 1
ppatterns.append('(\d{3})-(\d{3})-(\d{4})')
# Iteration 2
ppatterns.append(r'.+(\d{3}).[^0-9](\d{3})[^0-9](\d{4})')
# Iteration 3
ppatterns.append(r'.?(\d{3})[^0-9](\d{3})[^0-9](\d{4})')

# it doesn't help to add the raw version fo the first iteration
#ppatterns.append(r'(\d{3})-(\d{3})-(\d{4})')

""" 
This function takes in a filename along with the file object and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

TODO
For Part 3, if you have added other lists, you should add
additional for loops that match the patterns in those lists
and produce correctly formatted results to append to the res list.
"""
## Original process_filename (overwriting my version)
# JW: First I defined a pattern for matchine email addresses to use
# in this function.
JWemailPattern = r'''
                                                  # pattern for email
        (([\w-]+|[\w-]+\.[\w-]+)                   # hanks,-
        (\s.?\(f.*y.*)?                            # followed by 
        (\s?(@|&.*;)\s?|\s(at|where)\s)            # @, @ , at , where ,&#x40;,
        ([\w-]+|[\w-]+([\.;]|\sdo?t\s|\s)[\w-]+)   # gmail., ics.bjtu, ics;bjtu, ics dot bjtu, -ics-bjtu-
        ([\.;]|\s(do?t|DOM)\s|\s)                  # ., ;, dot , dt , DOM
        (-?e-?d-?u|com)\b)                         # .edu, .com, -e-d-u
        ([A-Za-z.]+)  @  ([A-Za-z.]+)\.edu'        #dabo
        ('([A-Za-z.]+) [at]+ ([A-Za-z.]+)\.edu')   #lam
        ('([A-Za-z.]+) at ([A-Za-z;]+)edu')        #jks
        |
        ('(\w+\.edu)','(\w+)'\))
        '''
# JW: I also defined a pattern for matching phone numbers to use in the 
# altered function below
JWphonePattern = r'''
                         # pattern for phone
        \(?(\d{3})\)?    # area code is 3 digits, e.g. (650), 650
        [ -]?            # separator is - or space or nothing, e.g. 650-XXX, 650 XXX, (650)XXX
        (\d{3})          # trunk is 3 digits, e.g. 800
        [ -]             # separator is - or space
        (\d{4})          # rest of number is 4 digits, e.g. 0987
        \D+              # should have at least one non digit character at the end
        #(\d{3})-(\d{3})-(\d{4})'
        '''
# JW: below is my altered copy of process_filesname
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        # you may modify the line, using something like substitution
        #    before applying the patterns
        # email pattern list
        # JW: Put my patter here to set up matches (email)
        JWmatches = re.findall(JWemailPattern, line, re.VERBOSE|re.I)
        # JW: process through the matches
        for m in JWmatches:
            email = ""
            # building string for email
            if len(m[-1]) != 0:
                email = '%s@%s' % (m[-1], m[-2])
            else:
                if m[1] == "Server":
                    # skip any occurrences of "server at" in line
                    continue
            email = '%s@%s.%s' % (m[1].replace("-", ""), 
                                      m[6].replace(";", ".")
                                          .replace(" dot ", ".")
                                          .replace("-", "")
                                          .replace(" ", "."), 
                                      m[-4].replace("-", ""))
            res.append((name,'e',email))

        # phone pattern list
        # JW: Now work on matches of phone numbers using my phone pattern
        jWmatches = re.findall(JWphonePattern, line, re.VERBOSE)
        for m in JWmatches:
            phone = '%s-%s-%s' % m
            res.append((name, 'p', phone))
    return res



"""
You should not edit this function.
"""
def process_dir(data_path):
    # save complete list of candidates
    guess_list = []
    # save list of filenames
    fname_list = []

    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        fname_list.append(fname)
        path = os.path.join(data_path,fname)
        f = open(path,'r', encoding='latin-1')
        # get all the candidates for this file
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list, fname_list

"""
You should not edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r', encoding='latin-1')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not edit this function.
Given a list of guessed contacts and gold contacts, this function
    computes the intersection and set differences, to compute the true
    positives, false positives and false negatives. 
It also takes a dictionary that gives the guesses for each filename, 
    which can be used for information about false positives. 
Importantly, it converts all of the values to lower case before comparing.
"""
def score(guess_list, gold_list, fname_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    # for each file name, put the golds from that file in a dict
    gold_dict = {}
    for fname in fname_list:
        gold_dict[fname] = [gold for gold in gold_list if fname == gold[0]]

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)

    print ('True Positives (%d): ' % len(tp))
    # print all true positives
    pp.pprint(tp)
    print ('False Positives (%d): ' % len(fp))
    # for each false positive, print it and the list of gold for debugging
    for item in fp:
        fp_name = item[0]
        pp.pprint(item)
        fp_list = gold_dict[fp_name]
        for gold in fp_list:
            s = pprint.pformat(gold)
            print('   gold: ', s)
    print ('False Negatives (%d): ' % len(fn))
    # print all false negatives
    pp.pprint(fn)
    print ('Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn)))

"""
You should not edit this function.
It takes in the string path to the data directory and the gold file
"""
def main(data_path, gold_path):
    guess_list, fname_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list, fname_list)

"""
commandline interface assumes that you are in the directory containing "data" folder
It then processes each file within that data folder and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    print ('Assuming ContactFinder.py called in directory with data folder')
    main('data/dev', 'data/devGOLD')
