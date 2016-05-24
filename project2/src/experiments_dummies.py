####
# This will perform translation (monotone & lattice) on two
# dummy sentences. Also, all FSTs will be drawn, so you can easily
# inspect the FSTs. The dummies are called 'blackdog' and 'freundin'
# and all files are stored in results-blackdog-[monotone/lattice]
# (Note: we did not make permutation data for the freundin dummysentence,
# hence there's no lattice translation for that.)

from Helper import *
from all_tasks import *

if __name__ == "__main__":
	for exp_type in ['blackdog-monotone', 'blackdog-lattice', 'freundin-monotone']:
		root = "../results-%s/" % exp_type

		print "\n" + "-"*80 + "\nSTARTING %s" % exp_type
		print "All files will be written to the folder "+root
		
		# Initialize helper	
		H = Helper(exp_type, root=root)
		H.blue_scores_fn = root+"%s-bleu-scores.txt" % exp_type

		# Go!
		do_tasks(H, exp_type=exp_type.split("-")[1], bleu=True, draw=True)
