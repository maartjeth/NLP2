# task 5

# Task: pack permutations into weighted lattices: these are the transducers as shown in figure 6 of the assignment (or determinstic versions of those)

# 1) Read file --> [] ||| probs ||| permutation in numbers --> isyms ||| permutations in words --> osyms
# 2) Make the files for the fst
# 3) Produce fsts --> input for question 6
# 4) Want to make a determinstic version of the non-deterministic version?

# + add new weights!

from Helper import *
from FST import *
from collections import defaultdict
import math

def generate_perm_input(self, permutations):
	""" Turns the text into a dict that can be used to generate the permutation lattice
		Permutation lattice: look at fig 6 of assignment 
	"""

	perm_dict = defaultdict(list)

	with open(permutations, 'r') as f:
		permutations = f.read().split("\n")

		for perm in permutations[0:5]: # [0:something] for testing purposes
			permutation = perm.split(' ||| ')

			perm_num = permutation[0]
			prob = permutation[1].split(" ")[2].split('=')[1]
			perm_input = permutation[2]
			perm_output = permutation[3]

			perm_dict[perm_num].append((prob, perm_input, perm_output)) # we're adding triples of strings

	return perm_dict

def generate_perm_input_fsts(self, perm_dict, out_base, draw=False):
	""" Generate input fst (input as it's used as input for task 6 later on)
	"""

	for perm_num, perm_vals in perm_dict.iteritems():

		# build fst per permuted sentence
		fst = FST("%s-%s" % (out_base, perm_num))

		fst_txt = ""
		isyms = set()
		osyms = set()
		isymbols_txt = "<eps> 0\n"
		osymbols_txt = "<eps> 0\n"
		state = 0

		# loop over all permutations per sentence
		for p in perm_vals: 

			prob = -math.log(float(p[0]))
			input_pos = p[1].split(" ")
			output_words = p[2].split(" ")

			for i, inp in enumerate(input_pos):
				if i == 0:
					fst_txt += "%s %s %s %s \n" % (0, state+1, inp, output_words[i])
				elif i == len(input_pos)-1: # add the weights only to the last arc
					fst_txt += "%s %s %s %s %s \n" % (state, state+1, inp, output_words[i], prob)
				else:
					fst_txt += "%s %s %s %s \n" % (state, state+1, inp, output_words[i])

				isyms.add(inp)
				osyms.add(output_words[i])
				state += 1

			fst_txt += "%s \n" % (state)


		for i, word in enumerate(osyms):
			osymbols_txt += "%s %s\n" % (word, i+1)

		for i, word in enumerate(isyms):
			isymbols_txt += "%s %s\n" % (word, i+1)

		# Update fst and compile
		fst.update_fst(fst_txt)
		fst.update_osymbols(osymbols_txt)
		fst.update_isymbols(isymbols_txt)
		fst.compile()

		if draw: fst.draw()


# Turn this method into a class method
Helper.generate_perm_input = generate_perm_input
Helper.generate_perm_input_fsts = generate_perm_input_fsts

if __name__ == '__main__':
	H = Helper()
	permutation_file = "../data/dev.enpp.nbest"
	out_base = "../data/5-permutation-lattices/perm-lat"
	perm_dict = H.generate_perm_input(permutation_file)
	H.generate_perm_input_fsts(perm_dict, out_base, draw=True)