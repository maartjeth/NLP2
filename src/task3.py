import subprocess

def task3(src_fst, trnsl_fst, out_dir, line_num):

	outfile = "../data/derivations-fsts/combined-test.fst"
	# composition of the two fsts
	call = "fstcompose [--opts] " + src_fst + " " + trnsl_fst + " " + outfile
	print "CALL: ", call
	subprocess.call([call], shell=True)
	


if __name__ == '__main__':
	src_fst = "../data/inputs/input-test.fst"
	trnsl_fst = "../data/phrase-tables/phrase-table-35.fst"
	out_dir = "../data/derivations-fsts"

	for line_num in range(1):
		task3(src_fst, trnsl_fst, out_dir, line_num)

