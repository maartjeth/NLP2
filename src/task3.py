import subprocess
from collections import defaultdict
from Helper import *
from FST import *

def get_next_states(state, states, rec=0, max_rec_depth=1000):
	"""
	Recursively get all future states from the current one.

	Args:
		state: a tuple (next_state_id, isymbol, osymbol, weight)
				describing this state
		states: a dictionary with all states, indexed by state indices
		returns: a list of future states.
	"""
	if rec > max_rec_depth:
		print "ERROR: Max recursion depth exceeded!"
		return [state] 

	next_state_id = state[0]
	if next_state_id == 1:
		return [state]
	else:
		next_state = states[next_state_id][0]
		return [state] + get_next_states(next_state, states, 
			rec=rec+1, max_rec_depth=max_rec_depth)

def path2translation(path):
	"""
	Turn a path (list of states) into a string formatted as in the instructions
	For more details about the path format, see `get_next_states()`
	"""

	# Go through the path store phrases and start/ending positions
	phrases = []
	begin_new_phrase = True
	for _, isymb, osymb, _ in path:
		
		# If inside the initial segment of empty states
		if osymb == "<eps>" and isymb == "<eps>":
			continue

		# Else, if inside a multiword phrase
		elif osymb == "<eps>" or isymb == "<eps>":
			if begin_new_phrase:
				phrases += [{"phrase": "", "start": int(isymb), "end": int(isymb)-1}]
				begin_new_phrase = False
			
			if osymb == "<eps>":
				# Update the length/ending position of the phrase
				phrases[-1]["end"] += 1
			else:
				phrases[-1]["phrase"] += osymb + " "

		# Else, if in a single-word phrase
		else: 
			phrases += [{"phrase": osymb, "start": int(isymb), "end": int(isymb)}]
			begin_new_phrase = True


	# Finally, get the derivation and translation strings
	derivation = ""
	translation = ""
	for phrase in phrases:
		if phrase["phrase"] != "":
			if phrase["phrase"][-1] == " ": phrase["phrase"] = phrase["phrase"][:-1]
			derivation += "%s |%s-%s| " % (phrase['phrase'], phrase['start'], phrase['end'])
			translation += phrase["phrase"] + " "
	translation = translation[:-1]
	derivation = derivation[:-1]
	weight =  sum([float(w) for _, _, _, w in path])

	return translation, derivation, weight

def get_path_translations(txtfst_fn):
	"""
	Get the translations of to all paths in the FST. If the FST has loops,
	this will fail miserably. Typically, you use this function on a FST
	that contains the top-n paths.

	Arguments:
		txtfst_fn: filename of a .txtfst file describing the FST.
	"""
	states = defaultdict(list)	
	with open(txtfst_fn, 'r') as f:
		lines = f.read().split("\n")
		for line in lines:
			if line == "": continue
			parts = line.split("\t")
			state = int(parts[0])

			if len(parts) == 1: continue
			elif len(parts) == 5:
				states[state].append((int(parts[1]), parts[2], parts[3], parts[4]))
			elif len(parts) == 4: # case with no weights --> epsilon
				states[state].append((int(parts[1]), parts[2], parts[3], 0))
			else:
				print "n_best_to_text: needs either 4 or 5 columns"

	# Get all path, transform to path strings and return.
	translations = []
	for init_state in states[0]:
		path = get_next_states(init_state, states)
		translations.append(path2translation(path))

	return translations

def generate_best_derivations_fsts(self, n=100):
	"""
	Get the best n derivations from a given FST
	"""
	for i in range(self.num_sentences):
		best_derivations_fn = self.best_derivation_fst_base + ("-%s.100best" % i)
		fst = FST("%s-%s" % (self.translation_fst_base, i))
		best_derivations_fst = fst.find_n_best(n, best_derivations_fn)
		best_derivations_fst.decompile()
		best_derivations_fst.copy_symbols()

		# Save to file
		out_fn 		 = "%s.100best.%s" % (self.best_derivations_base, i)
		full_out_fn  = "%s.100best.%s.full" % (self.best_derivations_base, i)
		translations = get_path_translations(best_derivations_fst.txtfst_fn)
		with open(out_fn, "w") as out_f:
			with open(full_out_fn, "w") as full_out_f:
				for i, (trans, deriv, w) in enumerate(translations):
					out_f.write(deriv +"\n")
					full_out_f.write("%s ||| %s ||| %s ||| %s\n" % (i, trans, deriv, w))

def generate_translation_fsts(self, translation_fst_base=None, draw=False):
	"""
	Generates translation FSTs from input and phrase table FSTs. 
	The translation is then simply the composition of the two.
	"""
	if translation_fst_base == None: translation_fst_base = self.translation_fst_base

	for i in range(self.num_sentences):

		# The phrase table
		phrase_table_fst = FST("%s-%s" % (self.phrase_table_fst_base, i))

		# Updating osymbols and recompiling is pretty essential: all isymbols
		# of the phrase-table FST should be osymbols of the input FST. This is 
		# easily fixed by  updating the input_fst.osymbols accordingly
		# More info in the Notes section of the README
		input_fst = FST("%s-%s" % (self.input_fst_base, i))
		input_fst.osymbols_fn = phrase_table_fst.isymbols_fn
		input_fst.compile()

		# Generate translation SFT and copy in- and out-symbol files
		translation = input_fst.compose(phrase_table_fst, "%s-%s" % (translation_fst_base, i))
		# translation.osymbols_fn = phrase_table_fst.osymbols_fn
		translation.decompile()
		translation.copy_symbols()

		if draw: translation.draw()

# Add Helper methods
Helper.generate_translation_fsts = generate_translation_fsts
Helper.generate_best_derivations_fsts = generate_best_derivations_fsts

if __name__ == '__main__':
	# Do do the whole thing
	H = Helper()
	H.generate_translation_fsts()
	H.generate_best_derivations_fsts()
	
	# # Generate composition: translation
	# input_fst = FST("../dummydata/blackdog-input-0")
	# phrase_table_fst = FST("../dummydata/blackdog-phrase-table-0")
	# input_fst.osymbols_fn = phrase_table_fst.isymbols_fn
	# input_fst.compile()

	# translation = input_fst.compose(phrase_table_fst, "../dummydata/blackdog-translation-0")
	# # translation = FST("../dummydata/blackdog-translation-0")
	# translation.isymbols_fn = "../dummydata/blackdog-input-0.isyms"
	# translation.osymbols_fn = "../dummydata/blackdog-phrase-table-0.osyms"
	# translation.compile().draw()

	# # Get best derivations
	# best_derivation_fst = translation.find_n_best(5, "../dummydata/blackdog-translation-best")
	# best_derivation_fst.decompile()
	# best_derivation_fst.copy_symbols()
	# best_derivation_fst.draw()

	# # Print best translations
	# translations = get_path_translations(best_derivation_fst.txtfst_fn)
	# for i, (trans, deriv, weight) in enumerate(translations):
	# 	# print trans, "\t\t", deriv, "\t\t", weight
	# 	print "%s ||| %s ||| %s ||| %s" % (i, trans, deriv, weight)
