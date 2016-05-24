# task 4
from collections import defaultdict
from Helper import *
from scipy.misc import logsumexp
import math

def dump_translations(self):
	"""
	Write all translations for the two decision rules (Viterbi and MAP)
	to two different files.
	"""

	viterbi_translations = ""
	map_translations = ""
	for i in range(self.num_sentences):
		
		# File with the 100 best derivations
		derivations_fn = "%s.100best.%s.full" % (self.best_derivations_base , i)
		
		# Get the Viterbi translation; the best (highest) score
		with open(derivations_fn, "r") as f:
			for i, line in enumerate(f):
				if i == 0:
					_, trans, der, weight = line.split(" ||| ")
					print der
					viterbi_translations += trans + "\n"

		# The MAP translation
		map_trans, _ = get_MAP_translation(derivations_fn)
		map_translations += map_trans + "\n"

	# Save
	with open(self.translation_base + ".map", "w") as f:
		f.write(map_translations)

	with open(self.translation_base + ".viterbi", "w") as f:
		f.write(viterbi_translations)

Helper.dump_translations = dump_translations

def get_MAP_translation(derivations_fn):
	"""
	Approximate the MAP translation from a file containing several derivations 
	of a single sentence. The input file is supposed to be of the form
	```
	line number ||| translation ||| derivation ||| weight
	```
	Even though in fact, only `translation` and `weight` are needed. The weights
	are treated as if they are joint probabilities `log(translation, derivation)`.
	""" 

	# store all translations to dict
	deriv_dict = defaultdict(list)
	with open(derivations_fn) as f:
		for line in f:
			if line == "": continue;
			_, trans, der, weight = line.split(" ||| ")
			deriv_dict[trans].append((weight, der))

	max_prob = -float('inf')
	best_trans = ""
	for trans, derivations in deriv_dict.iteritems():
		trans_prob = get_translation_prob(derivations);
		if trans_prob > max_prob:
			max_prob = trans_prob
			best_trans = trans

	return best_trans, max_prob

def get_translation_prob(derivations):
	"""
	Get the translation probability (posterior) given a set of weighted derivations.
	Interpreting weighs as log-probability, it calculates log( sum_w exp(w) )
	"""
	return sum([math.exp(-float(weight)) for weight, _ in derivations])


if __name__ == '__main__':
	root = "../results-monotone/"
	H = Helper(type="all-monotone", root=root)
	H.num_sentences = 2;
	H.dump_translations()

	# H = Helper(type="blackdog-monotone")
	# H.dump_translations()

