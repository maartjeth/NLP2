# task 5

# Task: pack permutations into weighted lattices: these are the transducers as shown in figure 6 of the assignment (or determinstic versions of those)

# 1) Read file --> [] ||| probs ||| permutation in numbers --> isyms ||| permutations in words --> osyms
# 2) Make the files for the fst
# 3) Produce fsts --> input for question 6
# 4) Want to make a determinstic version of the non-deterministic version?

# + add new weights!

from Helper import *
from collections import defaultdict

def generate_perm_input(self, permutations, draw=False):
	""" Turns the text into a dict that can be used to generate the permutation lattice
		Permutation lattice: look at fig 6 of assignment 
	"""

	perm_dict = defaultdict(list)

	with open(permutations, 'r') as f:
		permutations = f.read().split("\n")

		for perm in permutations[0:2]: # [0:2] for testing purposes
			permutation = perm.split(' ||| ')

			perm_num = permutation[0]
			prob = permutation[1].split(" ")[2].split('=')[1]
			perm_input = permutation[2]
			perm_output = permutation[3]

			perm_dict[perm_num].append((prob, perm_input, perm_output)) # we're adding triples of strings

			# print perm_num
			# print prob
			# print perm_input
			# print perm_output
			# print perm_dict

	return perm_dict

def generate_perm_input_fsts(self, perm_dict):
	""" Generate input fst (input as it's used as input for task 6 later on)
	"""

	for perm_nums, perm_vals in perm_dict.iteritems():
		# use perm (= number of the permuted sentence) to store the file later on

		# build fst per permuted sentence
		fst_txt = ""
		isymbols_txt = "<eps> 0\n"
		osymbols_txt = "<eps> 0\n"
		state = 0
		for p in perm_vals: # loop over all permutations per sentence

			prob = p[0]
			input_pos = p[1].split(" ")
			output_words = p[2].split(" ")

			# TODO: check whether this works with the count the states get etc
			weight = 1
			for i, inp in enumerate(input_pos):
				state += 1
				if i == 0:
					fst_txt += "%s %s %s %s %s\n" % (1, state, inp, output_words[i], weight)
				else:
					fst_txt += "%s %s %s %s %s\n" % (state, state+1, inp, output_words[i], weight)


			# print prob
			# print input_pos
			# print output_words
			print fst_txt



# Turn this method into a class method
Helper.generate_perm_input = generate_perm_input
Helper.generate_perm_input_fsts = generate_perm_input_fsts

if __name__ == '__main__':
	H = Helper()
	permutation_file = "../data/dev.enpp.nbest"
	perm_dict = H.generate_perm_input(permutation_file)
	H.generate_perm_input_fsts(perm_dict)