###
# All auxiliary experiments we did are in this file. 
#
# Simply uncomment the experiment and run. The bleu scores in the 
# ../results/bleu-scores file will be put in a unique file,
# but all other files (fsts) are overwritten. Results are written to th
# folder `results`. Running all experiments takes quite a while...

from Helper import *
from all_tasks import *
from copy import copy

if __name__ == "__main__":

	# EXPERIMENT 1
	# Monotone translation on 100 sentences
	print "\n" + "-"*80 + "\nEXPERIMENT 1"
	H = Helper("all-monotone")
	H.blue_scores_fn = "../results/blue-scores/E01-mono-bleu-scores.txt"
	do_tasks(H, draw=False, bleu=True)

	# EXPERIMENT 2
	# Lattice translation on 100 sentences
	# print "\n" + "-"*80 + "\nEXPERIMENT 2"
	# H = Helper("all-lattice")
	# H.blue_scores_fn = "../results/blue-scores/E02-lat-bleu-scores.txt"
	# do_tasks(H, tasks=[0,5,2,3,4], draw=False, bleu=True)

	# # EXPERIMENT 3
	# # Monotone translation on full corpus
	# print "\n" + "-"*80 + "\nEXPERIMENT 3"
	# H = Helper("all-monotone")
	# H.num_sentences = 1416
	# H.blue_scores_fn = "../results/blue-scores/E03-mono-bleu-scores.txt"
	# do_tasks(H, draw=False, bleu=True)

	# # EXPERIMENT 4
	# # Lattice translation of full corpus
	# print "\n" + "-"*80 + "\nEXPERIMENT 4"
	# H = Helper("all-lattice")
	# H.num_sentences = 1416
	# H.blue_scores_fn = "../results/blue-scores/E04-lat-bleu-scores.txt"
	# do_tasks(H, tasks=[0,5,2,3,4], draw=False, bleu=True)

	# EXPERIMENT 9 - 14
	# Lattice translation, ignoring one feature at a time.
	# H = Helper("all-lattice")
	# features = H.get_feature_weights()
	# for i, (feature, val) in enumerate(features.iteritems()):
	# 	print "\n" + "-"*80 + "\nEXPERIMENT %s" % i
	# 	H.get_feature_weights(refresh=True)
	# 	H.feature_weights[feature] = 0
	# 	H.blue_scores_fn = "../results/blue-scores/E%s-lat-%s-bleu-scores.txt" \
	# 						% (str(i+5).zfill(2), feature)
	# 	do_tasks(H, tasks=[0,5,2,3,4], draw=False, bleu=True)
	# 	print H.blue_scores_fn

	# EXPERIMENT 15 - 24
	# Lattice translation, using only one feature at a time
	# H = Helper("all-lattice")
	# features = H.get_feature_weights()
	# for i, (feature, val) in enumerate(features.iteritems()):
	# 	print "\n" + "-"*80 + "\nEXPERIMENT %s" % i
	# 	H.get_feature_weights(refresh=True)
	# 	for feat, v in H.feature_weights.iteritems():
	# 		if feat != feature:
	# 			H.feature_weights[feat] = 0
	# 	H.blue_scores_fn = "../results/blue-scores/E%s-lat-%s-bleu-scores.txt" \
	# 						% (str(i+15).zfill(2), feature)
	# 	do_tasks(H, tasks=[0,5,2,3,4], draw=False, bleu=True)
	# 	print H.blue_scores_fn	

	# # EXPERIMENT 25
	# # Check if the magical 25 BLEU extends to the whole set...
	# H = Helper("all-lattice")
	# H.num_sentences = 1416
	# features = H.get_feature_weights()
	# for feat, v in H.feature_weights.iteritems():
	# 	if feat != 'EgivenFCoherent':
	# 		H.feature_weights[feat] = 0
	# H.blue_scores_fn = "../results/blue-scores/E25-lat-only-EgivenFCoheren.txt"
	# do_tasks(H, tasks=[0,5,2,3,4], draw=False, bleu=True)
	# print H.blue_scores_fn
