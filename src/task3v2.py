import subprocess
from collections import defaultdict
from Helper import *
from FST import *

def get_next_states(state, states, rec=0, max_rec_depth=1000):
	"""
	Recursively get all future states from the current one.
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
		

def path_to_string(path):
	# Go through the path store phrases and start/ending positions
	phrases = []
	begin_new_phrase = True
	for _, isymb, osymb, _ in path:
		if osymb == "<eps>" and isymb == "<eps>":
			continue

		elif osymb == "<eps>" or isymb == "<eps>":
			# Inside a multiword phrase!
			if begin_new_phrase:
				phrases += [{"phrase": "", "start": int(isymb), "end": int(isymb)-1}]
			begin_new_phrase = False
			if osymb == "<eps>":
				phrases[-1]["end"] += 1
			else:
				phrases[-1]["phrase"] += osymb + " "

		else: 
			phrases += [{"phrase": osymb, "start": int(isymb), "end": int(isymb)}]
			begin_new_phrase = True

	# Finally, output a string
	path_string = ""
	for phrase in phrases:
		path_string += "%s |%s-%s| " % (phrase['phrase'], phrase['start'], phrase['end'])
	
	return path_string

def get_shortest_path_strings(txtfst_fn):
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

	path_strings = []
	for init_state in states[0]:

		# Path from this initial state
		path = get_next_states(init_state, states)
		# Store path string
		path_strings.append(path_to_string(path))

	return path_strings

if __name__ == '__main__':

	# fst = FST("../dummydata/short-path-fsts/example")
	fst = FST("../dummydata/blackdog-composite-0")
	fst.isymbols_fn = "../dummydata/blackdog-input-0.isyms"
	fst.osymbols_fn = "../dummydata/blackdog-phrase-table-0.osyms"
	fst.compile()
	fst.draw()

	# shortest_paths_fst = fst.find_n_best(3, "../dummydata/short-path-fsts/example-shortest")
	shortest_paths_fst = fst.find_n_best(10, "../dummydata/blackdog-composite-shortest")
	shortest_paths_fst.draw()
	shortest_paths_fst.decompile()

	path_strings = get_shortest_path_strings(shortest_paths_fst.txtfst_fn)
	for s in path_strings:
		print s