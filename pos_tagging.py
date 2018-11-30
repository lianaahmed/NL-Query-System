# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():

    # List that stores each word and tag in tuple form
    wordTuples = []
    output = []
    with open("sentences.txt", "r") as f:
        for line in f:
            line = line.split(" ")
            for word in line:
                word = word.split("|")
                if word not in wordTuples and (word[1] == 'NN' or word[1] == 'NNS'):
                    wordTuples.append(word)

    #Index variable
    i = 0

    for (word, tag) in wordTuples:
        i += 1
        for (w, t) in wordTuples[i:]:
            if word == w and t != tag:
                output.append(word)

    return output
                
unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""    
    if s.endswith("men"):
        return s[:-2] + "an"
    elif s in unchanging_plurals_list:
        return s
    else:
        # If the stem is have, its 3s form is has.
        if re.match(r"has", s):
            return "have"
        elif re.match(r"is", s):
            return "are"
        elif re.match(r"does", s):
            return "do"
        elif re.match(r"fizzes", s):
            return "fizz"
        elif re.match(r"bathes", s):
            return "bathe"
        elif re.match(r"analyses", s):
            return "analyse"
        elif re.match(r"dazes", s):
            return "daze"
        # If the stem ends in o,x,ch,sh,ss or zz, add es (goes, boxes, attaches, washes,
        # dresses, fizzes).
        elif re.match(r"(\w*)([ox]|ch|zz|s[hs])es", s):
            stem = s[:-2]
        # If the stem ends in se or ze but not in sse or zze, add s (loses, dazes, lapses,
        # analyses).
        elif re.match(r"(\w*)([^s]s|[^z]z)es", s):
            stem = s[:-1]
        # If the stem is of the form Xie where X is a single letter other than a vowel,
        # simply add s (dies, lies, ties - note that this doesn't account for unties)

        elif re.match(r"[bcdfghjklmnpqrstvwxyz]ies", s):
            stem = s[:-1]

        # If the stem ends in y preceded by a non-vowel and contains at least three
        # letters, change the y to ies (flies, tries, unifies).
        elif re.match(r"(\w*)ies", s):
            stem = s[:-3] + "y"

        # If the stem ends in anything except s,x,y,z,ch,sh or a vowel, simply add s
        # (eats, tells, shows).
        elif re.match(r"(\w*)[^aeiousxyz(ch)(sh)]s", s):
            stem = s[:-1]

        # If the stem ends in y preceded by a vowel, simply add s (pays, buys).
        elif re.match(r"(\w*)[aeiou]ys", s):
            stem = s[:-1]
        
        # If the stem ends in e not preceded by i,o,s,x,z,ch,sh, just add s (likes, hates,
        # bathes).
        elif re.match(r"(\w*)([^iosxz]|[^cs]h)es", s):
            stem = s[:-1]
 
        else:
            stem = ""

        return stem

def verbCheck1(v, wd):
    return 

def nounCheck1(n, wd):
    return 

# def checkV(v, wd):
#     return v == ()

# def checkN(n, wd):
#     return n == ()

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    
    allTags = []
    verbs = ['I', 'T']
    others = ['P', 'A']
    nouns = ['N', 'Np', 'Ns']
    
    for (word, tag) in function_words_tags:
        if word == wd:
            allTags.append(tag)
            break

    # proper nouns and adjectives
    for c in others:
        if wd in lx.getAll(c):
            allTags.append(c)

    # verbs
    for c in verbs:
        if wd in lx.getAll(c) or verb_stem(wd) in lx.getAll(c):
            if verb_stem(wd):
                allTags.append(c + 's')
            else:
                allTags.append(c + 'p')

    # nouns
    if wd in lx.getAll(nouns[0]) or noun_stem(wd) in lx.getAll(nouns[0]):
        if wd in unchanging_plurals_list:
            allTags.append(nouns[2])
            allTags.append(nouns[1])
        elif noun_stem(wd):
            allTags.append(nouns[1])
        else:
            allTags.append(nouns[2])

    return allTags





def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])                                                                                
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.