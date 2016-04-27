def task3(src_fst, trnsl_fst):
	src = open(src_fst, "r")
	trsl = open(trnsl_fst, "r")
	
	# put the src input in a dict, to reduce complexity (looping over the source file once now
	# instead of n-times, while going through the translation phrase table)
	trsl_dict = {}
	for line in src.read().split("\n"):
		if line == "":
			continue
		line_list = line.split(" ")			 # pos 1         pos 2        weight
		trsl_dict[line_list[3].lower()] = (line_list[0], line_list[1], line_list[4])

	for line in trsl.read().split("\n"):
		if line == "":
			continue		
		line_list = line.split(" ")
		src_wrd = line_list[2]
		trsl_wrd = line_list[3]
		weight = line[4]

		# get the input (i.e. input:output:weight) for the derivation fst
		if src_wrd != '<eps>':
			in_der_fst = trsl_dict[src_wrd][0]

			# TODO here: put in new fst
			# TODO here: how to deal with epsilon



		print "src word: ", src_wrd
		print "input: ", in_der_fst


	src.close()
	trsl.close()

if __name__ == '__main__':
	src_fst = "../data/inputs/input-test.fst"
	trnsl_fst = "../data/phrase-tables/phrase-table-35.fst"
	task3(src_fst, trnsl_fst)

