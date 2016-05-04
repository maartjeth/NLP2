# task 4
from collections import defaultdict
from Helper import *
from scipy.misc import logsumexp
import math

def viterbi_best_translation(self):
	out = ""
	for i in range(self.num_sentences):
		with open("%s.100best.%s.full" % (self.best_mono_derivations_base , i), "r") as f:
			for i, l in enumerate(f):
				if i < 1:
					out += l.replace("\n","").split(" ||| ")[1] + "\n"
		
	with open("../data/4-best-trans-der/viterbi_best.txt", "w") as f:
		f.write(out)

def MAP_best_translation(self):
	out_trans = ""
	out_der = ""
	
	for i in range(self.num_sentences):
		# store all translations to dict
		trans_dict = defaultdict(list)
		with open("%s.100best.%s.full" % (self.best_mono_derivations_base , i), "r") as f:
			for i, l in enumerate(f):
				parts = l.split(" ||| ")
				trans = parts[1]
				der = parts[2]
				weight = parts[3]
	
				trans_dict[trans].append((weight, der))

		# Compute largest weights 	return logsumexp([float(weight) for weight, _ in derivations])
		weight = 0.0
		max_weight = -float('inf')
		best_trans = ""
		best_der = ""
		for trans, weight_der in trans_dict.iteritems():
			for i in weight_der:
				weight += math.exp(float(i[0]))
			log_weight = math.log(weight)
			if log_weight > max_weight:
				max_weight = log_weight
				best_trans = trans
				best_der = i[1]

		out_trans += best_trans + "\n"
		out_der += best_der + "\n"

	with open("../data/4-best-trans-der/MAP_best_trans.txt", "w") as f:
		f.write(out_trans)

	with open("../data/4-best-trans-der/MAP_best_der.txt", "w") as f:
		f.write(out_der)




Helper.viterbi_best_translation = viterbi_best_translation
Helper.MAP_best_translation = MAP_best_translation



if __name__ == '__main__':
	#best_der = '../dummydata/blackdog-trans-der-weight'
	#max_weight, best_trans, best_der = find_best_translations(best_der)
	H = Helper()
	H.MAP_best_translation()

