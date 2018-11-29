                                                                                                                                                                                # File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    
    #Lists of POS categories which will store the appropriate word stem
    def __init__(self):
        # Proper names
        self.P = []
        # Common nouns
        self.N = []
        # Adjectivs
        self.A = []
        # Intransitive Verbs
        self.I = []
        # Transitive Verbs
        self.T = []

    # Adds a word into the appropriate POS category
    def add(self, stem, cat):
        if(cat == "P"):
            self.P.append(stem)
        elif(cat == "N"):
            self.N.append(stem)
        elif(cat == "A"):
            self.A.append(stem)
        elif(cat == "I"):
            self.I.append(stem)
        elif(cat == "T"):
            self.T.append(stem)

    # Returns all noun word stems in a category w/o duplicates
    def getAll(self, cat):

        # Sets catList to cat
        if(cat == "P"):
            catList = self.P
        elif(cat == "N"):
            catList = self.N
        elif(cat == "A"):
            catList = self.A
        elif(cat == "I"):
            catList = self.I
        elif(cat == "T"):
            catList = self.T

        noDupesList = []

        # Loops through each value in the given cat List
        for stem in catList:
            # Checks if the word already exists in noDupesList
            # If it doesn't, it is added to noDupesList
            if stem not in noDupesList:
                noDupesList.append(stem)
        
        return noDupesList
        

class FactBase:
    """stores unary and binary relational facts"""
    
    # Creates an empty list to store unary and binary facts
    def __init__(self):
        self.facts = []

    # Adds a tuple containing the predicate and the e1 value 
    #  to the facts list
    def addUnary(self, pred, e1):
        self.facts.append((pred, e1))

    # Adds a tuple containing the predicate, the e1 value and 
    # the e2 value to the facts list
    def addBinary(self, pred, e1, e2):
        self.facts.append((pred, e1, e2))
    
    # Checks if a unary fact already exists in the facts list
    # in form of a tuple           
    # Returns true if found
    # False otherwise
    def queryUnary(self, pred, e1):

        found = False

        for fact in self.facts:
            if(fact == (pred, e1)):
                found = True

        return found

    # Checks if a binary fact already exists in the facts list
    # in form of a tuple
    # Returns true if found
    # False otherwise
    def queryBinary(self, pred, e1, e2):

        found = False

        for fact in self.facts:
            if(fact == (pred, e1, e2)):
                found = True

        return found


import re
from nltk.corpus import brown 
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
  
    # If the stem is have, its 3s form is has.
    if re.match(r"has", s):
        return "have"
    elif re.match(r"is", s):
        return "are"
    elif re.match(r"does", s):
        return "do"
    elif re.match('.*s$', s):

        # If the stem ends in o,x,ch,sh,ss or zz, add es (goes, boxes, attaches, washes,
        # dresses, fizzes).
        if re.match(r".*((o)|(x)|(ch)|(sh)|(ss)|(zz))e", s[:-1]):
            stem = s[:-2]

        # If the stem ends in se or ze but not in sse or zze, add s (loses, dazes, lapses,
        # analyses).
        elif re.match(r".*[^(sse)(zze)](se)|(ze)", s[:-1]):
            stem = s[:-1]

        # If the stem is of the form Xie where X is a single letter other than a vowel,
        # simply add s (dies, lies, ties - note that this doesn't account for unties)

        elif re.match(r"[bcdfghjklmnpqrstvwxyz]ie", s[:-1]):
            stem = s[:-1]

        # If the stem ends in y preceded by a non-vowel and contains at least three
        # letters, change the y to ies (flies, tries, unifies).
        elif re.match(r".*ie", s[:-1]):
            stem = s[:-3] + "y"

        # If the stem ends in anything except s,x,y,z,ch,sh or a vowel, simply add s
        # (eats, tells, shows).
        elif re.match(r".*[^aeiousxyz(ch)(sh)]", s[:-1]):
            stem = s[:-1]

        # If the stem ends in y preceded by a vowel, simply add s (pays, buys).
        elif re.match(r".*[aeiou]y", s[:-1]):
            stem = s[:-1]
        
        # If the stem ends in e not preceded by i,o,s,x,z,ch,sh, just add s (likes, hates,
        # bathes).
        elif re.match(r".*[^iosxz(ch)(sh)]e", s[:-1]):
            stem = s[:-1]
            
        else:
            return ""
    
    else:
        return ""

    if(checkVerb(stem) == True):
        return stem
    else:
        return ""

# Helper function for verb_stems to check if the word passed through is a verb
def checkVerb(s):

    isVerb = False

    # Loops through each word in the corpus and checks if its a verb
    for (word, tag) in brown.tagged_words():
        if word == s and (tag == 'VB' or tag == 'VBZ'):
            isVerb = True
    
    return isVerb
    

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.

