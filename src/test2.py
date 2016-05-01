from FST import *
input_fst = FST("../dummydata/blackdog-input-0")
phrase_table_fst = FST("../dummydata/blackdog-phrase-table-0")

## THIS IS CRUCIAL!
input_fst.osymbols_fn = phrase_table_fst.isymbols_fn
input_fst.compile()
##

input_fst.draw()


composite = input_fst.compose(phrase_table_fst, "../dummydata/blackdog-composite-0")
print composite.is_empty()
composite.draw()

 # ||| the ||| le ||| EgivenFCoherent=0 SampleCountF=0 CountEF=0 MaxLexFgivenE=0 MaxLexEgivenF=0 IsSingletonF=0
 # ||| the ||| un ||| EgivenFCoherent=0 SampleCountF=0 CountEF=0 MaxLexFgivenE=0 MaxLexEgivenF=0 IsSingletonF=0
 # ||| dog ||| chien ||| EgivenFCoherent=0 SampleCountF=0 CountEF=0 MaxLexFgivenE=0 MaxLexEgivenF=0 IsSingletonF=0
 # ||| black ||| noir ||| EgivenFCoherent=0 SampleCountF=0 CountEF=0 MaxLexFgivenE=0 MaxLexEgivenF=0 IsSingletonF=0
 # ||| black ||| noirs ||| EgivenFCoherent=0 SampleCountF=0 CountEF=0 MaxLexFgivenE=0 MaxLexEgivenF=0 IsSingletonF=0
 # ||| black dog ||| chien noir ||| EgivenFCoherent=0 SampleCountF=0 CountEF=0 MaxLexFgivenE=0 MaxLexEgivenF=0 IsSingletonF=0