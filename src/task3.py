import subprocess

def task3(src_fst, trnsl_fst, out_dir, line_num, n=100):

	outfst = "../data/composition-fsts/combined-test.fst" # this is for testing purposes now, need to change in final version
	compose_fst(src_fst, trnsl_fst, outfst)


	short_fst = "../data/short-path-fsts/short-test.fst"
	find_n_best(str(n), outfst, short_fst)



def compose_fst(src_fst, trnsl_fst, outfile):
	# composition of the two fsts
	call = "fstcompose " + src_fst + " " + trnsl_fst + " " + outfile
	subprocess.call([call], shell=True)

def find_n_best(n, fst, short_fst):
	#call = "fstshortestpath " + " " + n + " " + fst + " " + short_fst
	call = "fstshortestpath " + fst + " " + short_fst
	subprocess.call([call], shell=True)
	# TODO: still include n
	#fstshortestpath [--opts] a.fst out.fst

if __name__ == '__main__':
	src_fst = "../data/sorted-fsts/fst-sort-35.fst"
	trnsl_fst = "../data/sorted-fsts/fst-sort-36.fst"
	out_dir = "../data/composition-fsts"

	for line_num in range(1):
		task3(src_fst, trnsl_fst, out_dir, line_num)

