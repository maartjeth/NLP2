# 1)	Make new phrase table transducers that correspond to the permuted sentences
#		We need to add the new weights
# 2) 	Combine these transducers with the input transducers of task 5
# 3) 	Score the best 100 again, just like in task 4

from Helper import *
import task2

if __name__ == '__main__':
	H = Helper(task6=True)
	H.generate_phrase_table_fsts()