from FST import *

i = 1
root = "../results/"
input_fst = FST(root + "lat-inputs/input-%s" % i)
phrase_table_fst = FST(root + "lat-phrase-tables/phrase-table-%s" % i)
translation = FST(root + "lat-translations/lat-translation-%s" % i)
best_derivation = FST(root + "lat-derivations/lat-derivation-%s.100best" % i)

# input_fst.draw()
# phrase_table_fst.draw()
# translation.draw()
best_derivation.draw()