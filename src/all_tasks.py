#####
# Do all tasks
#

from Helper import *
from FST import *
from task0 import *
from task1 import *
from task2 import *
from task3 import *
from task4 import *
from task5 import *
from task6 import *


if __name__ == "__main__":
	
	# The tasks to perform
	#tasks = [0, 1, 2, 3, 4, 5, 6]
	tasks = [4]

	# The helper with all parameters (these are the defaults, but repeated for clarity)
	H = Helper()

	# Task 0
	if 0 in tasks:
		print "Task 0..."
		H.preprocess_oov()
		print "\tDone with task 0.\n"
	
	# Task 1
	if 1 in tasks:
		print "Task 1..."
		H.generate_input_fsts()
		print "\tDone with task 1.\n"

	# Task 2
	if 2 in tasks:
		print "Task 2..."
		H.generate_phrase_table_fsts()
		print "\tDone with task 2.\n"

	# Task 3
	if 3 in tasks:
		print "Task 3..."
		print "\tGenerating monotone translation FSTs..."
		H.generate_translation_fsts()
		print "\tGenerating the best derivations in those monotone translations..."
		H.generate_best_derivations_fsts()
		print "\tDone with task 3.\n"

	# Task 4
	if 4 in tasks:
		print "Task 4..."
		print "Getting the Viterbi best translation..."
		H.viterbi_best_translation()
		print "Getting the MAP best translations..."
		H.MAP_best_translation()

	# From here on we switch to pre-ordered translation, so we need a new Helper object
	H1 = Helper(pre_ordered=True)

	# Task 5
	if 5 in tasks:
		print "Task 5..."
		print "\tGenerating permutation lattices..."			
		permutation_file = "../data/dev.enpp.nbest"
		out_base = "../data/5-permutation-lattices/perm-lat"
		perm_dict = H1.generate_perm_input(permutation_file)
		H1.generate_perm_input_fsts(perm_dict, out_base)
		print "\tDone with task 5."

	if 6 in tasks:
		print "Task 6..."
		print "\tGenerating new fsts from pre-ordered phrase tables..."
		H1.generate_phrase_table_fsts()
		print "\tGenerate translation FSTs..."
		H1.generate_mono_translation_fsts() 
		print "\tGenerating the best derivations in those translations..."
		H1.generate_best_derivations_fsts()
		print "\tDone with task 6." 

	print "All tasks are done!"