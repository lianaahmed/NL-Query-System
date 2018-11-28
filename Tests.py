
#%%
from statements import *

lex = Lexicon()
lex.add("John","P")
lex.add("Mary","P")
lex.add("like", "T")
if lex.getAll("P") == ['John', 'Mary']:
    print "Passed"


#%%
from statements import *

fb = FactBase()
fb.addUnary("duck","John")
fb.addBinary("love","John","Mary")
a = fb.queryUnary("duck","John")
b = not fb.queryBinary("love","Mary","John")
if a:
    print "Passed a"
if b:
    print "Passed b"


#%%
from statements import *

verbStems = ["like", "eat", "tell", "show", "pay", "buy", "fly", "try", "unify", "die", "lie", "tie", "go", "box", "attach", "wash", "dress", "fizz", "lose", "daze", "lapse", "analyse", "have", "like", "hate", "bathe"]
threesForm = ["likes", "eats", "tells", "shows", "pays", "buys", "flies", "tries", "unifies", "dies", "lies", "ties", "goes", "boxes", "attaches", "washes", "dresses", "fizzes", "loses", "dazes", "lapses", "analyses", "has", "likes", "hates", "bathes"]
passed = True

for stem, threes in zip(verbStems, threesForm):
    passed &= verb_stem(threes) == stem
    if verb_stem(threes) != stem:
        print "Failed: should've been {} but was actually {}".format(stem, verb_stem(threes))
if passed:
    print "Passed all"


#%%
from statements import *
from pos_tagging import *

words = ["like", "John", "orange", "fish", "a", "zxghqw", "fishes", "duck", "ducks"]
outputs = [['Ts'], ["P"], ["Ns", "A"], ["Ns","Np","Ip","Tp"], ["AR"], [], [], ["Ns"], ["Np"]]
passed = True

lx = Lexicon()
lx.add("John","P")
lx.add("orange", "N")
lx.add("orange", "A")
lx.add("fish", "N")
lx.add("fish", "N")
lx.add("fish", "I")
lx.add("fish", "T")
lx.add("like", "T")

for word, output in zip(words, outputs):
    passed &= sorted(tag_word(lx, word)) == sorted(output)
    if sorted(tag_word(lx, word)) != sorted(output):
        print "Failed: should've been {} but was actually {}".format(sorted(output), sorted(tag_word(lx, word)))
if passed:
    print "Passed all"


#%%
from statements import *
from pos_tagging import *
from agreement import *

lx = Lexicon()
lx.add("duck", "N")

#tr0 = all_valid_parses(lx, ['Who', 'is', 'duck', '?'])[0]
#tr = restore_words(tr0, ['Who', 'is', 'duck', '?'])
#tr.draw()


