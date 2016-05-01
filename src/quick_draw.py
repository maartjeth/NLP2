from FST import *

i = 36
input_fst = FST("../data/1-inputs/input-%s" % i)
phrase_table_fst = FST("../data/2-phrase-tables/phrase-table-%s" % i)
translation = FST("../data/3-mono-translations/mono-translation-%s" % i)
best_derivation = FST("../data/4-best-mono-derivations/mono-translation-%s.100best" % i)

# input_fst.draw()
# phrase_table_fst.draw()
# translation.draw()
best_derivation.draw()