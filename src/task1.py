
outdir = "../data/fsts/"
lines = open('../data/dev.en').read().split("\n")

N = 100
for line_num, sentence in enumerate(lines[:N]):
    fstfile = open(outdir + "fst-%s.fst" % line_num, "w")
    osymfile = open(outdir + "osyms-%s.txt" % line_num, "w")
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