import os
import re

class Helper:

	settings = {
		# Directories
		"data_dir": "../data",
		"results_dir": "../results/",
		"parse_dir": "../parse/",

		# Weights
		"baseline_weights_fn": "{data_dir}/baseline.weights",
		# Input lattices
		"dev_input_lattice_fn": "{data_dir}/nlp2-dev.en.pw.plf-100",
		"test_input_lattice_fn": "{data_dir}/nlp2-test.en.pw.plf-100",
		# 1000 best translations candidates (German)
		"dev_1000best_fn": "{data_dir}/nlp2-dev.1000best",
		"test_1000best_fn": "{data_dir}/nlp2-test.1000best",
		# Reference translations (German)
		"dev_reference_trans_fn": "{data_dir}/nlp2-dev.de",
		"test_reference_trans_fn": "{data_dir}/nlp2-test.de", 
		# Input (source) sentences (English)
		"dev_inputs_fn": "{data_dir}/nlp2-dev.en.s",
		"test_inputs_fn": "{data_dir}/nlp2-test.en.s",		
	}

	def __init__(self, settings={}):
		"""
		Initializes the Helper. The settings are all passed through
		a settings dictionary. Every key ending in `_fn` is treated
		as a filename and it will be checked if they actually exist.
		Similarly, every directory should end in `_dir`. You can use
		placeholders `{mydirectory_dir}` in the filenames, as long as
		`settings[mydirectory_dir]` is defined.

		All settings are then stored as class properties. So if you 
		have defined `settings[root_dir]` then the initializer will 
		define `myhelper.root_dir = settings[root_dir]`.
		"""

		# Update, check and store all setings as class properties
		self.settings.update(settings)
		for key, value in self.settings.items():

			# Check if files exist
			if key[-3:] == "_fn":
				# Try and replace {dirname_dir} by directory path
				try:
					matches = re.findall('{(\w+)\}(.*)', value)
					root = self.settings[matches[0][0]]
					value = root + matches[0][1]
				except IndexError: pass

				# Raise exception for nonexistent files
				if not os.path.isfile(value):
					raise Exception("File %s does not exist." % value)

			# Create missing directories
			elif key[-4:] == "_dir":
				if not os.path.isdir(value):
					os.mkdir(value)

			# Store as class property 
			setattr(self, key, value)

	def read_1000best(self, kind="dev", first=0, last=0):
		"""
		Loads the 1000 best translation candidates for sentences (not lines!) 
		`first` up to and including `last`. For every sentence, it yields
		the sentence number and a list of 1000 candidates. A candidate is a dict:
		```
			candidate = {
				'rank': 		integer in 0..1000 
				'translation': 	[(phrase, a, b), (phrase, a, b), ...] where a 
								and b are states in the input lattice
				'features': 	{'TargetLM': -36.3119, 'PermutationDistortion0': 
								[0,0,0,0], 'SourceLM': -56.2117, ...},
				'alignment': 	[(i,j), (i,j), ...] where i is a state in the input
								lattice and j is a target word position
				'system_score': float, dot product of features and baseline weights?
				'source': 		string, the source sentence
			}
		``` 
		Typically you would use this as follows:
		```
		for i, candidates in helper.read_1000best(first=10, last=15):
			for candidate in candidates:
				// Do something...
		```

		Arguments
			kind (string, default="dev") Either "dev" or "test"
			first (int, default=0) First sentence
			last (int, default=0) Last sentence

		Yields
			(sentence_nr, candidate)
		"""
		# Get start/end line numbers
		if last == None: last = first;
		start = first * 1000
		end = (last + 1 )* 1000 - 1
		
		# Open the file
		fn = getattr(self, "%s_1000best_fn" % kind)
		with open(fn, 'r') as file:

			# Go through all lines, but only parse those between start and end
			for i, line in enumerate(file):
				if i < start: continue
				if i > end: break
				if i % 1000 == 0: candidates = []

				# Split!
				line = line.replace("\n","")
				sentence, r_translation, r_features, \
					system_score, r_alignment, source = line.split(" ||| ")

				## Features
				# Turn TargetLM= -36.3119 PermutationDistortion0= 0 0 0 0 SourceLM= -56.2177 ...
				# into {'TargetLM': -36.3119, 'PermutationDistortion0': [0,0,0,0], 'SourceLM': -56.2117, ...}
				features = {}
				parts = re.split("\s?([A-Za-z0-9]+)=\s?", r_features)[1:]
				for j in range(0, len(parts) - 1, 2):
					name = parts[j]
					feat = map(float, parts[j+1].split())
					features[name] = feat[0] if len(feat) == 1 else feat
				
				## Alignment
				# Turn 0-0 10-5 ... into [(0,0), (10,5), ...]
				split_by_dash = lambda string: tuple(map(int, string.split('-')))
				alignment = [a for a in r_alignment.split(" ") if a != '']
				alignment = map( split_by_dash, alignment)
				
				## Translation
				# turn phrase1 |1-3| phase2 |3-4| ... 
				# into [(phrase1, 1, 3), (phras2, 3, 4), ...]
				translation = []
				translation_sent = ""
				parts = re.split(" \|(\d+)-(\d+)\| ", r_translation)
				for j in range(0, len(parts)-1, 3):
					translation.append((parts[j], parts[j+1], parts[j+2])) 
					translation_sent += parts[j] + ' '

				# Put all that in a dictionary and store
				candidates.append({
					'rank': i % 1000,
					'translation': translation,
					'translation_sent': translation_sent,
					'features': features,
					'alignment': alignment,
					'system_score': float(system_score),
					'source': source
				})

				if i % 1000 == 999:
					yield sentence, candidates

if __name__ == "__main__":
	H = Helper()
	for s, candidates in H.read_1000best(first=1, last=2):
		print candidates[0]['translation_sent']
		#print s, [candidate['source']+"\n" for candidate in candidates]
		#print candidate['translation']