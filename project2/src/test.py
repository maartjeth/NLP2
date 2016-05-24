####
# The main experiments
#
# Here we do monotone and lattice translation of the first 100 sentences
# in ../data/dev.en. The results (all FSTs created in the process and the 
# BLEU scores) are stored the folders `results-monotone` and `results-lattice`.
# 
# All further experiments can be found in `experiments-auxiliary.py`. It is also
# recommended to run `experiments_dummies.py`.

from Helper import *
from all_tasks import *

if __name__ == "__main__":

	# Monotone translation on 100 sentences
	root = "../results-monotone/"
	print "\n" + "-"*80 + "\nMONOTONE TRANSLATION"
	print "This can take a while. All files will be written to"\
		+ " the folder "+root+"\nThere you can also find the BLEU scores."

	H = Helper("all-monotone", root=root)
	H.num_sentences = 100
	H.blue_scores_fn = root+"monotone-bleu-scores.txt"
	do_tasks(H, tasks=[0,1,2,3,4], exp_type="monotone", bleu=True, draw=False)

