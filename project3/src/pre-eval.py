from Helper import *

if __name__ == "__main__":
	H = Helper()

	for s, candidates in H.read_1000best(kind="dev",first=0, last=2):
		# a = 'boe'
		for i, candidate in enumerate(candidates):
			# print candidate['rank']
			print " ".join([t[0] for t in candidate['translation']])
		# 	i