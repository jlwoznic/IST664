#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 18:48:42 2020

@author: joycewoznica
"""

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

#print(os.getcwd())

#change path
#os.chdir('/users/joycewoznica/Syracuse/IST664/HW/HW2/ContactFinder')

#print(os.getcwd())

my_email_pattern = r'''
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


my_phone_pattern = r'''
                         # pattern for phone
        \(?(\d{3})\)?    # area code is 3 digits, e.g. (650), 650
        [ -]?            # separator is - or space or nothing, e.g. 650-XXX, 650 XXX, (650)XXX
        (\d{3})          # trunk is 3 digits, e.g. 800
        [ -]             # separator is - or space
        (\d{4})          # rest of number is 4 digits, e.g. 0987
        \D+              # should have at least one non digit character at the end
        #(\d{3})-(\d{3})-(\d{4})'
        
        '''
""" 

"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        # match email
        matches = re.findall(my_email_pattern ,line, re.VERBOSE|re.I)
        for m in matches:
            email = ""
            if len(m[-1]) != 0:
                email = '%s@%s' % (m[-1], m[-2])
            else:
                if m[1] == "Server":
                    # skip "server at" sentence
                    continue
                email = '%s@%s.%s' % (m[1].replace("-", ""), 
                                      m[6].replace(";", ".")
                                          .replace(" dot ", ".")
                                          .replace("-", "")
                                          .replace(" ", "."), 
                                      m[-4].replace("-", ""))
            res.append((name,'e',email))
            
        # match phone number
        matches = re.findall(my_phone_pattern, line, re.VERBOSE)
        for m in matches:
            phone = '%s-%s-%s' % m
            res.append((name, 'p', phone))
            
    return res

"""
You should not need to edit this function, nor should you alter
its interface as it will be called directly by the submit script
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter(indent=4)
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print ('True Positives (%d): ' % len(tp))
    pp.pprint(list(tp))
    print ('False Positives (%d): ' % len(fp))
    pp.pprint(list(fp))
    print ('False Negatives (%d): ' % len(fn))
    pp.pprint(list(fn))
    print ('Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn)))

"""
You should not need to edit this function.
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)


if __name__ == '__main__':
    print ('Assuming ContactFinder.py called in directory with data folder')
    main('data/dev', 'data/devGOLD')
    
# 
# New Pass
    my_email_pattern = r'''
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


my_phone_pattern = r'''
                         # pattern for phone
        \(?(\d{3})\)?    # area code is 3 digits, e.g. (650), 650
        [ -]?            # separator is - or space or nothing, e.g. 650-XXX, 650 XXX, (650)XXX
        (\d{3})          # trunk is 3 digits, e.g. 800
        [ -]             # separator is - or space
        (\d{4})          # rest of number is 4 digits, e.g. 0987
        \D+              # should have at least one non digit character at the end
        #(\d{3})-(\d{3})-(\d{4})'
        
        '''
""" 

"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        # match email
        matches = re.findall(my_email_pattern ,line, re.VERBOSE|re.I)
        for m in matches:
            email = ""
            if len(m[-1]) != 0:
                email = '%s@%s' % (m[-1], m[-2])
            else:
                if m[1] == "Server":
                    # skip "server at" sentence
                    continue
                email = '%s@%s.%s' % (m[1].replace("-", ""), 
                                      m[6].replace(";", ".")
                                          .replace(" dot ", ".")
                                          .replace("-", "")
                                          .replace(" ", "."), 
                                      m[-4].replace("-", ""))
            res.append((name,'e',email))
            
        # match phone number
        matches = re.findall(my_phone_pattern, line, re.VERBOSE)
        for m in matches:
            phone = '%s-%s-%s' % m
            res.append((name, 'p', phone))
            
    return res

"""
You should not need to edit this function, nor should you alter
its interface as it will be called directly by the submit script
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter(indent=4)
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print ('True Positives (%d): ' % len(tp))
    pp.pprint(list(tp))
    print ('False Positives (%d): ' % len(fp))
    pp.pprint(list(fp))
    print ('False Negatives (%d): ' % len(fn))
    pp.pprint(list(fn))
    print ('Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn)))

"""
You should not need to edit this function.
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)


if __name__ == '__main__':
    print ('Assuming ContactFinder.py called in directory with data folder')
    main('data/dev', 'data/devGOLD')
    
## Another Pass
    epatterns = []
epatterns.append('([A-Za-z0-9._-]+)\s*(\(f.*y.*)?(?:@| at | AT |&#x40;|WHERE)\s*([A-Za-z0-9._-]+)\s?(?:.| dot | DOT | dt | DOM )(-?e-?d-?u|EDU|edu|com|COM)')
epatterns.append('([A-Za-z.]+)\s?\<del\>@([A-Za-z.]+)(?:.| dot | DOT | dt | DOM )(edu|EDU|com|COM)') #s? is whitespace cahracter
epatterns.append('([A-Za-z.]+)\s*\<at symbol\>\s*([A-Za-z.]+)(?:.| dot | DOT | dt | DOM )(edu|EDU|com|COM)')
#epatterns.append('([A-Za-z.]+) at ([A-Za-z;]+)edu')
epatterns.append('([A-Za-z.]+) at ([A-Za-z.]+) cs standford edu')
epatterns.append('([A-Za-z.]+) at ([A-Za-z.]+) robotics.standford.edu')
epatterns.append('([A-Za-z0-9._]{2,})\s+at\s+([A-Za-z0-9._]+)\s*dot\s*edu')

#epatterns.append('[^@]+@[^@]+\.[^@]+') #generalized email capture
#epatterns.append('[\w\.-]+@[\w\.-]+(\.[\w]+)+')
#epatterns.append('([A-Za-z.]+) [at]+ ([A-Za-z.]+)\.edu\s[A-Za-z.]+\s\d+')
#'obfuscate\(\'(\w+)\.(\w+)\',\'(\w+)\'\)
#Summary: tp=110, fp=0, fn=7

#regex used
#"|" Matches Either Or
#[A-Za-z0-9._-] maches any upper or lower case letter or number case insensitive
#\ match non whitespace
#?:.| dot | DOT | dt | DOM any or all match for "."
#'[\w\.-]+@[\w\.-]+(\.[\w]+)+' matches any alhanumeric character and underscores


ppatterns = []
ppatterns.append('[\(|\[]?(\d{3})[\)|\]]?\s?[-]?(\d{3})\s?[-]?(\d{4})\D+[\s|,|\<|}|^;]')
ppatterns.append('[\(|\[]?(\d{3})[\)|\]]?\s?[-]?(\d{3})\s?[-]?(\d{4})\D+$')

#final Summary: tp=72, fp=0, fn=45
""" 

"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        for epat in epatterns:
            # each epat has 2 sets of parentheses so each match will have 2 items in a list
            
            matches = re.findall(epat,line)
            for m in matches:
                m = tuple(x for x in m if x!='')
                if(len(m)==2):
                    m=(m[0],m[1],'edu')
                if(len(m)==4):
                    m=(m[0],m[2],m[3])
                if(len(m)>3):
                    m=(m[1],m[6],'edu')
                if(m[0]=='Server'or m[0]=='funding' or m[0]=='Talk'):
                    continue
                email = '%s@%s.%s' % m
                email=email.replace("-", "")
                email=email.replace("\<del\>", "")
                email=email.replace("..", ".")
                res.append((name,'e',email))
    
    
        for ppat in ppatterns:
            # each ppat has 3 sets of parentheses so each match will have 3 items in a list
            line.replace('<p[^>]*>[\n\t\r]*|<\/p[^>]*>','""')
            matches = re.findall(ppat,line)
            for m in matches:
                if 'id' in line: # after adding this Summary: tp=94, fp=0, fn=23
                    continue;
                phone = '%s-%s-%s' % m
                phone=phone.replace("(","")
                phone=phone.replace(")","")
                phone=phone.replace(" ","")
                phone=phone.replace("[","")
                phone=phone.replace("]","")
                res.append((name,'p',phone))
    return res

"""
You should not edit this function.
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        #, encoding='latin-1'
        f = open(path,'r', encoding='latin-1')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    print ('Guesses (%d): ' % len(guess_set))
    pp.pprint(guess_set)
    print ('Gold (%d): ' % len(gold_set))
    pp.pprint(gold_set)
    print ('True Positives (%d): ' % len(tp))
    pp.pprint(tp)
    print ('False Positives (%d): ' % len(fp))
    pp.pprint(fp)
    print ('False Negatives (%d): ' % len(fn))
    pp.pprint(fn)
    print ('Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn)))

"""
You should not edit this function.
It takes in the string path to the data directory and the gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

if __name__ == '__main__':
    print ('Assuming ContactFinder.py called in directory with data folder')
    main('data/dev', 'data/devGOLD')
    