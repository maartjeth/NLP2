###
## Task 1: 
# encode source sentences as transducers. The file loops over all
# Sentences (of the first 100) and saves OpenFST files describing the
# transducer corresponding to the sentence.
#

outdir = "../data/inputs/"
lines = open('../data/dev.en').read().split("\n")

N = 100
for line_num, sentence in enumerate(lines[:N]):
    fstfile = open(outdir + "input-%s.fst" % line_num, "w")
    osymfile = open(outdir + "input-%s.osyms" % line_num, "w")
    osymfile.write("<eps> 0\n")

    words = sentence.split(" ")
    voc = set()
    for i, word in enumerate(words):
        voc.add(word)
        fstfile.write("%s %s %s %s 1\n" %(i, i+1, i, word))
        
    for i, word in enumerate(voc):
        osymfile.write(word + " " + str(i+1) + "\n")
    
    fstfile.close()
    osymfile.close()


# fstcompile --osymbols=osyms-0.txt fst-0.fst binary-0.fst