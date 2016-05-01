from FST import *
input_fst = FST("../dummydata/blackdog-input-0")
phrase_table_fst = FST("../dummydata/blackdog-phrase-table-0")
composite = input_fst.compose(phrase_table_fst, "../dummydata/blackdog-composite-0")
composite.draw()