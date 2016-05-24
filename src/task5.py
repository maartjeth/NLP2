# task 5

from Helper import *
from FST import *
import task2
from collections import defaultdict
import math
import task0

def parse_permutation_file(self, permutations_fn=None, num_sentences=None, sentences_fn=None):
	"""
	Turns the text into a dict that can be used to generate the permutation lattice
	Permutation lattice: look at fig 6 of assignment 
	"""
	if num_sentences == None: num_sentences = self.num_sentences
	if sentences_fn == None: sentences_fn = self.sentences_fn
	if permutations_fn == None: permutations_fn = self.permutations_fn

	vocabularies = []
	with open(sentences_fn, 'r') as f:
		for sentence in f:
			sentence = sentence.replace("\n", "")
			vocabularies.append( set(sentence.split(" ")) )

	perm_dict = defaultdict(list)
	with open(permutations_fn, 'r') as f:
		permutations = f.read().split("\n")
		for perm in permutations:
			if perm == "": continue; 
			sentence, stats, perm_positions, perm_words = perm.split(' ||| ')
			if int(sentence) >= num_sentences: continue
			
			# Replace OOV words in the permutation
			voc = vocabularies[int(sentence)]
			replace_oov = lambda word: word if word in voc else self.OOV
			perm_words = map(replace_oov, perm_words.split(" "))

			perm_positions = perm_positions.split(" ")
			stats = dict([s.split("=") for s in stats.split(" ")])
			perm_dict[sentence].append((float(stats['prob']), perm_positions, perm_words))
			
	return perm_dict

def generate_input_lattices(self, fst_base=None, draw=False, num_sentences=None):
	""" Generate input fst (input as it's used as input for task 6 later on)
	"""
	if num_sentences == None: num_sentences = self.num_sentences;
	if fst_base == None: fst_base = self.input_fst_base

	# Get permutations
	perm_dict = self.parse_permutation_file();

	lattice_cost = self.get_feature_weights()['LatticeCost']
	for sentence, perm_vals in perm_dict.iteritems():
		if int(sentence) > num_sentences: continue;

		# build fst per permuted sentence
		fst = FST("%s-%s" % (fst_base, sentence))

		fst_txt = ""
		isyms, osyms = set(), set()
		isymbols_txt = "<eps> 0\n"
		osymbols_txt = "<eps> 0\n"
		state = 0
		# loop over all permutations per sentence
		for prob, perm_positions, perm_words in perm_vals: 

			prob =  -math.log(prob) * lattice_cost

			for i, (pos, word) in enumerate(zip(perm_positions, perm_words)):
				if i == 0:
					fst_txt += "%s %s %s %s\n" % (0, state+1, pos, word)
				elif i == len(perm_positions) - 1: # add the weights only to the last arc
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

		# Update FST
		fst.update_fst(fst_txt)
		fst.update_osymbols(osymbols_txt)
		fst.update_isymbols(isymbols_txt)

		# GO, GO, GO!
		fst.compile().determinize().push().minimize().decompile()

		if draw: fst.draw()


# Turn this method into a class method
Helper.parse_permutation_file = parse_permutation_file
Helper.generate_input_lattices = generate_input_lattices

if __name__ == '__main__':
	
	H = Helper(type="all-lattice")
	H.preprocess_oov()
	H.generate_input_lattices()

	# H = Helper(type="blackdog-lattice")
	# H.generate_input_lattices(draw=True)
