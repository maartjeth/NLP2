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
# from task6 import *

def do_tasks(H, tasks=[0,1,2,3,4], draw=False, bleu=False):
	print "\nStarting with Helper " + H.type
	
	# Task 0
	if 0 in tasks:
		print "\tTask 0..."
		H.preprocess_oov()
		print "\tDone with task 0.\n"
	
	# Task 1
	if 1 in tasks:
		print "\tTask 1..."
		H.generate_input_fsts(draw=draw)
		print "\tDone with task 1.\n"

	# Task 1
	if 5 in tasks:
		print "\tTask 5..."
		H.generate_input_lattices(draw=draw)
		print "\tDone with task 5.\n"

	# Task 2
	if 2 in tasks:
		print "\tTask 2..."
		H.generate_phrase_table_fsts(draw=draw)
		print "\tDone with task 2.\n"

	# Task 3
	if 3 in tasks:
		print "\tTask 3..."
		print "\tGenerating monotone translation FSTs..."
		H.generate_translation_fsts(draw=draw)
		print "\tGenerating the best derivations in those monotone translations..."
		H.generate_best_derivations_fsts(draw=draw)
		print "\tDone with task 3.\n"

	# Task 4
	if 4 in tasks:
		print "\tTask 4..."
		H.dump_translations()
		if bleu:
			print H.dump_bleu_scores()

if __name__ == "__main__":
	
	# H = Helper("blackdog-monotone")
	# do_tasks(H, draw=True)

	# H = Helper("blackdog-lattice")
	# do_tasks(H, tasks=[0,5,2,3,4], draw=True)

	# H = Helper("freundin-monotone")
	# do_tasks(H, draw=True)

	# # TO DO: make some permuation filie (cf blackdog.perm)
	# # H = Helper("freundin-lattice")
	# # do_tasks(H, tasks=[0,5,2,3,4], draw=True)

	H = Helper("all-monotone")
	do_tasks(H, draw=False, bleu=True)

	H = Helper("all-lattice")
	do_tasks(H, tasks=[0,5,2,3,4], draw=False, bleu=True)
