###
## Task 1: 
# encode source sentences as transducers. The file loops over all
# Sentences (of the first 100) and saves OpenFST files describing the
# transducer corresponding to the sentence.
#

from Helper import *
from FST import *

def generate_input_fsts(self, sentences=None, out_base="../data/inputs/input"):
    """
    Turns a list of sentences into intput transducers. These are
    all stored as .txtfst, .osyms, .isyms, .fst files.
    """
    if sentences == None: sentences = self.get_sentences()

    for line_num, sentence in enumerate(sentences):

        # FST object
        fst = FST("%s-%s" % (out_base, line_num))

        # Create the FST
        words = sentence.split(" ")
        voc = set()
        fst_txt = ""
        isymbols_txt = ""
        for i, word in enumerate(words):
            voc.add(word)
            fst_txt += "%s %s %s %s 0\n" % (i, i+1, i, word)
            isymbols_txt += "%s %s\n" % (i, i)
        fst_txt += str(i+1)

        # Create the out-symbols
        osymbols_txt = "<eps> 0\n"
        for i, word in enumerate(voc):
            osymbols_txt += "%s %s\n" % (word, i+1)
        
        # Update fst and compile
        fst.update_fst(fst_txt)
        fst.update_osymbols(osymbols_txt)
        fst.update_isymbols(isymbols_txt)
        fst.compile().draw()

# Turn this into a class method
Helper.generate_input_fsts = generate_input_fsts

if __name__ == "__main__" or True:
    H = Helper()
    # H.generate_input_fsts()
    H.generate_input_fsts(sentences=['the black dog'], out_base="../dummydata/blackdog-input")
