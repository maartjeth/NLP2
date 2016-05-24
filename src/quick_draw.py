from FST import *

i = 1
root = "../results-monotone/"
kind = "mono"
input_fst = FST("%s%s-inputs/%s-input-%s" % (root, kind, kind, i))
phrase_table_fst = FST("%s%s-phrase-tables/%s-phrase-table-%s"  % (root, kind, kind, i))
translation = FST("%s%s-translations/%s-translation-%s"  % (root, kind, kind, i))
best_derivation = FST("%s%s-derivations/%s-derivation-%s.100best"  % (root, kind, kind, i))

input_fst.draw()
phrase_table_fst.draw()
translation.draw()
best_derivation.draw()