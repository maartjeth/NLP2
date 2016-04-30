import subprocess
from collections import defaultdict
from Helper import *
from FST import *

def task3(src_fst, trnsl_fst, out_dir_comp, out_dir_short, out_dir_decomp, n=3):

	# Composition using the FST class
	composite = input_fst.compose(phrase_table_fst, out_dir_comp)

	# Finding n-best paths
	n_best_fst = composite.find_n_best(str(n), out_dir_short)
	n_best_fst.draw()

	# "Decompile" into readable format
	n_best_fst.decompile(out_dir_decomp)

	# Write the n-best translations in text format
	trans = n_best_to_text(out_dir_decomp)

	return trans



	#def find_n_best(self, n, short_fst_base):
	#short_fst = "../data/short-path-fsts/short-test.fst"
	#find_n_best(str(n), short_fst)

def n_best_to_text(txtfst):
	""" Write the n-best file to text format

		First preprocess the file: put all lines in path_dict
		Key = state
		Value = all other info

		Later on we use this info to proceed over the graph, as one path follows
		an ascending paths of states

	"""
	
	# preprocess file
	path_dict = defaultdict(list)	
	with open(txtfst, 'r') as f:
		lines = f.read().split("\n")
		complete_trans = ""
		starting_points = []
		for line in lines:
			parts = line.split("\t")
			

			if len(parts) == 5:
				path_dict[parts[0]].append((parts[1], parts[2], parts[3], parts[4]))
			elif len(parts) == 4: # case with no weights --> epsilon
				path_dict[parts[0]].append((parts[1], parts[2], parts[3]))
			else:
				print "n_best_to_text: needs either 4 or 5 columns"

	# make trans
	starting_points = path_dict['0']
	all_transitions = ''
	for start in starting_points:
		eps_seen_before = False
		pos1 = ''
		state = start[0]

		# loop over all paths, they have ascending states
		if start[2] == '<eps>':
			eps_seen_before = True
			pos1 = start[1]
			transition = ""
		else:
			transition = "%s |%s:%s| " % (start[2], start[1], start[1])

		print "start transition: ", transition

		state_int = int(state)
		while state_int >= 1:
			print "state int: ", state_int
			print "eps seen before: ", eps_seen_before
			
			state_info = path_dict[str(state_int)]
			if len(state_info) > 0:
				word = state_info[0][2]
				print "word: ", word
				pos = state_info[0][1] 
				print "pos: ", pos

				if word == '<eps>':
					# if it's the first epsilon in the row you encounter
					if eps_seen_before == False:
						eps_seen_before = True
						pos1 = pos
						print "pos1: ", pos1

				elif word != '<eps>' and eps_seen_before == True:
					eps_seen_before = False
					new_transition = "%s |%s:%s| " % (word, pos1, pos)
					transition += new_transition
					print "transition: ", transition
				elif word != '<eps>' and eps_seen_before == False:
					new_transition = "%s |%s:%s| " % (word, pos, pos)
					#print "New transition: ", new_transition
					transition += new_transition
			state_int -= 1

		all_transitions += transition+'\n'
		print "Transition: ", transition

	return all_transitions








if __name__ == '__main__':

	#input_fst = FST("../dummydata/blackdog-input-0")
	#phrase_table_fst = FST("../dummydata/blackdog-phrase-table-0")
	#out_dir = "../dummydata/blackdog-composite-0"

	input_fst = FST("../data/inputs/input-35")
	phrase_table_fst = FST("../data/phrase-tables/phrase-table-35")
	out_dir_comp = "../data/composition-fsts/comp-35"
	out_dir_short = "../data/short-path-fsts/short-35"
	out_dir_decomp = "../data/short-path-fsts/short-35.txtfst"


	trans_file = "../data/output/output_task3.txt"
	with open(trans_file, 'w') as f:
		trans = task3(input_fst, phrase_table_fst, out_dir_comp, out_dir_short, out_dir_decomp)
		f.write(trans)




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

