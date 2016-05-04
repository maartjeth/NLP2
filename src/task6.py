# 1)	Make new phrase table transducers that correspond to the permuted sentences
#		We need to add the new weights
# 2) 	Combine these transducers with the input transducers of task 5
# 3) 	Score the best 100 again, just like in task 4

from Helper import *
import task2
import task3

if __name__ == '__main__':
	# Run the whole thing --> need to have run task5 before this will work
	H = Helper(pre_ordered=True)
	H.generate_phrase_table_fsts()
	H.generate_mono_translation_fsts() 
	H.generate_best_derivations_fsts()

	# TODO: still need the BLUE scores=