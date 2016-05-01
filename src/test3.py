from FST import *
import subprocess

fst = FST("../dummydata/short-path-fsts/example")
fst = FST("../data/inputs/input-35")
fst.compile()
fst.draw()

shortest = fst.find_n_best(5, "../data/inputs/input-35-shortest")
shortest.draw()
shortest.decompile()

# call = "fstdeterminize %s | fstminimize > ../dummydata/short-path-fsts/test.fst" % shortest.fst_fn
# subprocess.call([call], shell=True)

# call = "fstminimize %s ../dummydata/short-path-fsts/test.fst" % shortest.fst_fn
# subprocess.call([call], shell=True)


# f = FST("../dummydata/short-path-fsts/test")
# # f.decompile()
# f.draw()

# .draw()
