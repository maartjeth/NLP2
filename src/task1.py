###
## Task 1: 
# encode source sentences as transducers. The file loops over all
# Sentences (of the first 100) and saves OpenFST files describing the
# transducer corresponding to the sentence.
#

from helpers import *

def generate_input_fsts(sentences, outdir="../data/inputs/"):
    """
    Turns a list of sentences into intput transducers. These are
    all stored as .fst, .osyms and .isyms files.
    """

    for line_num, sentence in enumerate(sentences):

        # FST object
        fst = FST("%sinput-%s.fst" % (outdir,line_num))

        # Create the FST
        words = sentence.split(" ")
        voc = set()
        fst_txt = ""
        isymbols_txt = ""
        for i, word in enumerate(words):
            voc.add(word)
            fst_txt += "%s %s %s %s 0\n" % (i, i+1, i, word)
            isymbols_txt += "%s %s\n" % (i, i)
        fst_txt += str(i)

        # Create the out-symbols
        osymbols_txt = "<eps> 0\n"
        for i, word in enumerate(voc):
            osymbols_txt += "%s %s\n" % (word, i+1)
        
        # Update fst and compile
        fst.update_fst(fst_txt)
        fst.update_osymbols(osymbols_txt)
        fst.update_isymbols(isymbols_txt)
        fst.compile()


if __name__ == "__main__":
    
    # Get our (preprocessed) English sentences
    # sentences = load_sentences();
    # generate_input_fsts(sentences, "../data/inputs/")
    generate_input_fsts(['the black dog'], "../dummydata/")