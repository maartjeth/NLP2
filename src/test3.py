from FST import *
from 
import subprocess

fst = FST("../dummydata/short-path-fsts/example")
fst.compile()
# fst.sort(how="ilabel")
fst.draw()

shortest = fst.find_n_best(5, "../dummydata/short-path-fsts/example-shortest")
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