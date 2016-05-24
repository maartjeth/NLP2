# Task 6

from Helper import *
import task2
import task3
import task4

if __name__ == '__main__':

	# We only need to update the helper and can then reuse most of the code
	H = Helper(type="all-lattice")

	# First, generate new phrase tables
	H.generate_phrase_table_fsts()

	# And combine those with the inputs lattices.
	H.generate_translation_fsts() 

	# Then get the best derivations
	H.generate_best_derivations_fsts()

	# Dump the final translations
	# To get the bleus score, simply run 
	# ./multi-bleu.perl dev.ja < monotone-translations.map
	# ./multi-bleu.perl dev.ja < monotone-translations.viterbi
	# ./multi-bleu.perl dev.ja < lattice-translations.map
	# ./multi-bleu.perl dev.ja < lattice-translations.viterbi
	H.dump_translations()
	H.dump_bleu_scores()