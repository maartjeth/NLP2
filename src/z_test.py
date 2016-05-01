sentence = "The black dog"
line_num = "test"
outdir = "../data/inputs/"

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