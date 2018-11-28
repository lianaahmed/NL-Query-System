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
    def queryUnary(self, pred, e1):

        found = False

        for fact in self.facts:
            if(fact == (pred, e1)):
                found = True

        return found

    # Checks if a binary fact already exists in the facts list
    # in form of a tuple
    # Returns true if found
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
    # add code here

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

