import subprocess
from Helper import *
from FST import *

def task3(src_fst, trnsl_fst, out_dir, n=100):

	# Composition using the FST class
	composite = input_fst.compose(phrase_table_fst, out_dir)

	# Finding n-best paths
	short_fst = "../dummydata/short-path-fsts/short-test"
	n_best_fst = composite.find_n_best(str(n), short_fst)
	n_best_fst.draw()

	# "Decompile" into readable format
	n_best_fst.decompile("../dummydata/short-path-fsts/short-test.txtfst")



	#def find_n_best(self, n, short_fst_base):
	#short_fst = "../data/short-path-fsts/short-test.fst"
	#find_n_best(str(n), short_fst)






if __name__ == '__main__':

	input_fst = FST("../dummydata/blackdog-input-0")
	phrase_table_fst = FST("../dummydata/blackdog-phrase-table-0")
	out_dir = "../dummydata/blackdog-composite-0"

	task3(input_fst, phrase_table_fst, out_dir)



	#composite.draw()

	##
	# This is weird; the composite does not look like figure 4,
	# as a result of the OOV. If you drop the extra OOV rule from the
	# grammar (comment out line 125 from Helper.py) and re-run task 1, 
	# task 3 and task 3 (they now onlyuse dummydata) then you get the right figure:
	# have a look at `blackdog-composite-0-without-OOV.pdf`
	#
	# So maybe look again at how we implemented OOV's and if they work as expected.



	# src_fst = "../data/sorted-fsts/fst-sort-35.fst"
	# trnsl_fst = "../data/sorted-fsts/fst-sort-36.fst"
	# out_dir = "../data/composition-fsts"

	# for line_num in range(1):
	# 	task3(src_fst, trnsl_fst, out_dir, line_num)

