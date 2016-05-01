#####
# Do all tasks
#

from Helper import *
from FST import *
from task0 import *
from task1 import *
from task2 import *
from task3 import *


if __name__ == "__main__":
	
	# The tasks to perform
	tasks = [0, 1, 2, 3]

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
		H.generate_mono_translation_fsts()
		print "\tGenerating the best derivations in those monotone translations..."
		H.generate_best_derivations_fsts()
		print "\tDone with task 3.\n"

	print "All tasks are done!"