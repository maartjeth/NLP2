"""
Splits a file into chunks.
"""

# Well, the size of the chunk.
chunk_size = 500000

# The file that has to be chunked
input_fn = "../data-dev/dev-targets.txt"

# The chunk filenames. The wildcard %s will be replace
# by the chunk number
chunk_fn = "../data-dev/eval/dev-targets-part%s.txt"

##############################################################

with open(input_fn,'r') as file:
	lines = ""
	chunk = 1
	for k, line in enumerate(file):
		lines += line
		if k % chunk_size == chunk_size-1 :
			# chunk = (k/(chunk_size-1))
			with open(chunk_fn % chunk, "w") as chunk_file:
				chunk_file.write(lines)
			lines = ""
			chunk += 1

	with open(chunk_fn % chunk, "w") as chunk_file:
		chunk_file.write(lines)

		