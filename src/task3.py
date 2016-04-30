import subprocess
from Helper import *
from FST import *

def task3(src_fst, trnsl_fst, out_dir, line_num, n=100):

	outfst = "../data/composition-fsts/combined-test.fst" # this is for testing purposes now, need to change in final version
	compose_fst(src_fst, trnsl_fst, outfst)


	short_fst = "../data/short-path-fsts/short-test.fst"
	find_n_best(str(n), outfst, short_fst)


def find_n_best(n, fst, short_fst):
	#call = "fstshortestpath " + " " + n + " " + fst + " " + short_fst
	call = "fstshortestpath " + fst + " " + short_fst
	subprocess.call([call], shell=True)
	# TODO: still include n
	#fstshortestpath [--opts] a.fst out.fst

if __name__ == '__main__':

	# Composition using the FST class
	input_fst = FST("../dummydata/blackdog-input-0")
	phrase_table_fst = FST("../dummydata/blackdog-phrase-table-0")
	composite = input_fst.compose(phrase_table_fst, "../dummydata/blackdog-composite-0")
	composite.draw()

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

