"""
This script extracts the translations from the 1000 best lists
and writes them to a single file. Also, it creates a file with 
all target translations on the corresponding lines.

Moreover, it creates a JSON
file with some information about every sentence. More precisely,
it contains a list of dictionaries of the form
```
	sentences[i] = {
		'sentence': sentence number,
		'num_candidates': number of candidate translations,
		'first_line': the line-number of the first candidate in the 1000best file,
		'last_line': the line-number of the last candidate in the 1000best file,
		'source': the source sentence,
		'target': the target translation
	}
```
"""

from Helper import *
import json

# Some settings
kind = "test"
translations_fn = "../data-%s/%s-translations.txt" % (kind,kind)
targets_fn = "../data-%s/%s-targets.txt" % (kind,kind)
sentences_fn = '../data-%s/%s-sentences.json' % (kind,kind)

# Read out the target translations
with open('../data/nlp2-%s.de' % kind, 'r') as file:
	targets = file.read().split("\n")

with open(translations_fn, 'w') as trans_file:
	with open(targets_fn, 'w') as targets_file:
		# Read out all candidates
		sentences = []
		start = 0;
		H = Helper()
		for s, candidates in H.read_1000best(kind=kind,first=0, last=3000, translation_only=True):
			
			# Extract information about the line numbers and sentences
			info = {
				'sentence': s,
				'num_candidates': len(candidates),
				'first_line': start,
				'last_line': start + len(candidates) - 1,
				'source': candidates[0]['source'],
				'target': targets[s]
			}
			sentences.append(info)
			start += len(candidates)

			# # Write out translation
			translations = [candidate['translation_sent'] for candidate in candidates ]
			for trans in translations:
				trans_file.write(trans+"\n")
				targets_file.write(targets[s]+"\n")
				
	# Store sentence information
	json.dump(sentences, open(sentences_fn,'w'), indent=True)


### Some tests
# sentences = json.load(open(sentences_fn))
# s = 4
# sentence = sentences[s]
# with open(targets_fn) as file:
# 	for i, line in enumerate(file):
# 		if i < sentence['first_line'] - 2: continue
# 		if i > sentence['first_line'] + 2: break
# 		if i == sentence['first_line']: print "---\n"
# 		print i
# 		print sentence['target']
# 		print line

