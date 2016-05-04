# task 5

# Task: pack permutations into weighted lattices: these are the transducers as shown in figure 6 of the assignment (or determinstic versions of those)

# 1) Read file --> [] ||| probs ||| permutation in numbers --> isyms ||| permutations in words --> osyms
# 2) Make the files for the fst
# 3) Produce fsts --> input for question 6
# 4) Want to make a determinstic version of the non-deterministic version?

# + add new weights!

from Helper import *
from FST import *
import task2
from collections import defaultdict
import math

def parse_permutation_file(self, permutation_fn):
	"""
	Turns the text into a dict that can be used to generate the permutation lattice
	Permutation lattice: look at fig 6 of assignment 
	"""

	perm_dict = defaultdict(list)
	with open(permutation_fn, 'r') as f:
		permutations = f.read().split("\n")
		for perm in permutations[:3]: # [0:something] for testing purposes
			if perm == "": continue; 
			sentence, stats, perm_positions, perm_words = perm.split(' ||| ') 
			stats = dict([s.split("=") for s in stats.split(" ")])
			perm_dict[sentence].append((float(stats['prob']), perm_positions, perm_words)) # we're adding triples of strings
			
	return perm_dict

def generate_input_lattices(self, perm_dict, out_base, draw=False):
	"""
	Generate input fst (input as it's used as input for task 6 later on)
	"""
	lattice_cost = self.get_feature_weights()['LatticeCost']

	for sentence, perm_vals in perm_dict.iteritems():

		# build fst per permuted sentence
		fst = FST("%s-%s" % (out_base, sentence))

		fst_txt = ""
		isyms, osyms = set(), set()
		isymbols_txt = "<eps> 0\n"
		osymbols_txt = "<eps> 0\n"
		state = 0

		# loop over all permutations per sentence
		for prob, perm_positions, perm_words in perm_vals: 

			prob = (- math.log(prob)) * lattice_cost
			perm_positions = perm_positions.split(" ")
			perm_words = perm_words.split(" ")

			for i, (pos, word) in enumerate(zip(perm_positions, perm_words)):
				if i == 0:
					fst_txt += "%s %s %s %s\n" % (0, state+1, pos, word)
				elif i == len(perm_positions) - 1: # add the weights only to the last arc  # TODO: multiply by the " weight " of this feature
					fst_txt += "%s %s %s %s %s \n" % (state, state+1, pos, word, prob)
				else:
					fst_txt += "%s %s %s %s\n" % (state, state+1, pos, word)

				isyms.add(pos)
				osyms.add(word)
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

		# Make deterministic version
		det_base = "../data/5-permutation-lattices/5-determinized/determinized"
		det_base = "../dummydata/determinized"
		fst.determinize()
		fst.push()
		fst.draw()

		# Make minimised version
		# min_base = "../data/5-permutation-lattices/5-det-minimized/minimized"
		min_base = "../dummydata/minimized"
		minimized_fst = fst.minimize(min_base)
		minimized_fst.draw()
		# minimized_fst.decompile()

		# fst2 = FST(min_base+'-2')
		# # fst2.isymbols_fn = fst.isymbols_fn
		# # fst2.osymbols_fn = fst.osymbols_fn
		# fst2.draw()

		# if draw: fst.draw(), determinized_fst.draw(), minimized_fst.draw()

		

# Turn this method into a class method
Helper.parse_permutation_file = parse_permutation_file
Helper.generate_input_lattices = generate_input_lattices

if __name__ == '__main__':
	H = Helper(pre_ordered=True)
	# permutation_file = "../data/dev.enpp.nbest"
	# out_base = "../data/5-permutation-lattices/perm-lat"
	# perm_dict = H.generate_perm_input(permutation_file)
	# H.generate_perm_input_fsts(perm_dict, out_base, draw=True)

	permutations = H.parse_permutation_file("../dummydata/blackdog.perm")
	print permutations
	H.generate_input_lattices(permutations, "../dummydata/input-lattice", draw=True)

