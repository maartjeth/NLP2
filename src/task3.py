import subprocess

def task3(src_fst, trnsl_fst, out_dir, line_num):

	outfile = "../data/composition-fsts/combined-test.fst"
	# composition of the two fsts
	call = "fstcompose " + src_fst + " " + trnsl_fst + " " + outfile
	print "CALL: ", call
	subprocess.call([call], shell=True)
	


if __name__ == '__main__':
	src_fst = "../data/fsts/fst-35.fst"
	trnsl_fst = "../data/fsts/fst-35.fst"
	out_dir = "../data/composition-fsts"

	for line_num in range(1):
		task3(src_fst, trnsl_fst, out_dir, line_num)

