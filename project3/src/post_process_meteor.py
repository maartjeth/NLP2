"""
Post-process METEOR output.
The output of METEOR is a bit fluffly: we only need the scores
for every segment (candidate translation). This script extracts
the segment scores and writes them to a new file.
"""
import re

# The raw meteor output for a certain part
meteor_fn = '../data-test/eval/test-meteor-output-part%s.txt'

# The output file with scores only
scores_fn = '../data-test/eval/test-meteor-part%s.txt'

# number of parts
num_parts = 5

###############################################################

for part in range(1, num_parts+1):
	num_matches = 0
	with open(meteor_fn % part, 'r') as meteor_file:
		with open(scores_fn % part, 'w') as scores_file:
			for i, line in enumerate(meteor_file):
				# if i > 20: break
				matches = re.findall('Segment \d+ score:\s(\d.\d+)\n', line)
				if len(matches) > 0:
					scores_file.write(matches[0]+"\n")
					num_matches += 1

	print "Part %s: %s scores found" % (part, num_matches)