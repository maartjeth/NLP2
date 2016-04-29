from collections import defaultdict

def task3(src_fst, trnsl_fst, out_dir, line_num):
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

	# loop over the phrase-table file and get the source words, the target words and the weights
	der_fst, isymbols, osymbols = "", [], []  # initialize fst for the derivation
	der_list = []
	phrase_len = 0
	for line in trsl.read().split("\n"):
		if line == "":
			continue		
		line_list = line.split(" ")
		src_wrd = line_list[2]
		trsl_wrd = line_list[3]
		weight = line[4]

		# get the input (i.e. input:output:weight) for the derivation fst from the transl dict
		node = 0
		weight = 0.5 # TODO: change to real weights
		if src_wrd != '<eps>' and trsl_wrd != '<eps>': # if it's not epsilon we have a 1:1 mapping
			phrase_len = 0
			der_list = []
			in_der_fst = trsl_dict[src_wrd][0]
			print "src word: ", src_wrd
			print "input: ", in_der_fst			
											 # 1st node	   2nd node       input  		    output
 			der_fst += "%s %s %s %s %d\n" % (in_der_fst, int(in_der_fst)+1, in_der_fst, trsl_wrd, weight)
 			
 			isymbols.append(in_der_fst)
 			osymbols.append(trsl_wrd)

 		if trsl_wrd == '<eps>':
 			in_der_fst = trsl_dict[src_wrd][0] # TODO: outside if?
 			der_fst += "%s %s %s %s %d\n" % ('SOMETHING', 'SOMETHING+1', in_der_fst, '<eps>', weight)
 			

 			der_list.append((in_der_fst, trsl_wrd)) # getting a list of tuples in the correct order
 			phrase_len += 1

 		if src_wrd == '<eps>':
 			der_fst += "%s %s %s %s %d\n" % ('SOMETHING', 'SOMETHING+1', '<eps>', trsl_wrd, weight)
 			

 			


	# Making fst
	isyms = "<eps> 0\n"
 	for i, src in enumerate(set(isymbols)):
        isyms += "%s %s\n" % (src, i+1)

    osyms = "<eps> 0\n"
  	for i, tar in enumerate(set(osymbols)):
      	osyms += "%s %s\n" % (tar, i+1)

	with open("%sderivation-fst-%s.fst" % (out_dir, line_num), "w") as f: 
            f.write(der_fst)
        with open("%sderivation-fst-%s.isyms" % (out_dir, line_num), "w") as f: 
            f.write(isyms)
        with open("%sderivation-fst-%s.osyms" % (out_dir, line_num), "w") as f: 
            f.write(osyms)

			# TODO here: how to deal with epsilon


	src.close()
	trsl.close()

if __name__ == '__main__':
	src_fst = "../data/inputs/input-test.fst"
	trnsl_fst = "../data/phrase-tables/phrase-table-35.fst"
	out_dir = "../data/derivations-fsts"

	for line_num in range(1)
	task3(src_fst, trnsl_fst, out_dir, line_num)

