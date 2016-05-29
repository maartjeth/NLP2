"""
Unsplits a set of pars. That is, it concatenates the 
parts into one new file.
"""
# Kind of file
kind = 'test'

# Number of parts
num_parts = 5

#############################################

input_fn = "../data-%s/eval/%s-meteor-part%s.txt"
output_fn = "../data-%s/eval/%s-meteor.txt"

with open(output_fn % (kind,kind), 'w') as output_file:
	for part in range(1,num_parts+1):
		with open(input_fn % (kind,kind,part), 'r') as input_file:
			for line in input_file:
				output_file.write(line)
