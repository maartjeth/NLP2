from Helper import *
from FST import *
H = Helper()

out = ""
for i in range(H.num_sentences):
	with open("%s.100best.%s.full" % (H.best_mono_derivations_base , i), "r") as f:
		for i, l in enumerate(f):
			if i < 1:
				out += l.replace("\n","").split(" ||| ")[1] + "\n"
#print out

with open("../data/test.txt", "w") as f:
	f.write(out)