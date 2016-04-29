#################################
## Task 2
#
# Transform the phrase tables into transducers. 
#
## To do
# * Weigh all arcs using the linear model. Now they all have weight .5 or 1
# *
#

import numpy as np
import math
import subprocess

def task2():
    debug = False
    english_text_file = "../data/dev.en"
    grammar_file = "../data/rules.monotone.dev/grammar." # Without extension
    weight_file = "../data/weights.monotone"
    out_dir = "../data/phrase-tables/"
    out_dir_fst = "../data/fsts/"
    out_dir_sort = "../data/sorted_fsts/"

    # Read in all lines
    with open(english_text_file, "r") as f: 
        lines = f.read().split("\n")

    weights = []
    with open(weight_file, "r") as f:
        w_lines = f.read().split("\n")
        for w in w_lines:
            weights.append(float(w.split(" ")[1]))

    weight_vector = np.asarray(weights)
    # A simple grammar for testing purposes
    test_grammar = """
        ||| the ||| le
        ||| the ||| un
        ||| dog ||| chien
        ||| black ||| noir
        ||| black ||| noirs
        ||| black dog ||| chien noir"""#[1:-1]
        #||| black dog barks ||| chien noir aboie"""[1:-1]

    # Line 35 is the shortest one, line 2 the longest 
    for line_num in [35]: # or: range(len(lines)):
        with open(grammar_file + str(line_num)) as f:
            grammar = f.read().split("\n") # set dummy features to 0
            grammar.append('[X] ||| OOV ||| OOV ||| EgivenFCoherent=0 SampleCountF=0 CountEF=0 MaxLexFgivenE=0 MaxLexEgivenF=0 IsSingletonF=0 oov=1')
                
        # For testing:
        if debug == True:
            grammar = test_grammar.split("\n")

        node = 0 # The last node number
        fst, isymbols, osymbols = "", [], []
        for rule in grammar:
            pass_through_count = 0
            if rule == "": continue
            parts = rule.split(" ||| ")
            english = parts[1].split(" ")
            japanese = parts[2].split(" ")              
            isymbols += english
            osymbols += japanese

            # new features
            OOV_count = english.count('OOV')    
            glue = 1
            word_penalty = len(english) * (-1/math.log(10))
   

            # getting all the features from the file (TODO: for loop.. one regex??)
            if debug == True:
                weight = 0.5
            else:
                feature_list = []
                features = parts[3]
                features = features.split(" ")

                for f in features:
                    feature_list.append(float(f.split("=")[1]))
                feature_list.append(glue)
                feature_list.append(OOV_count)
                feature_list.append(word_penalty)
                feature_vector = np.asarray(feature_list)

                weight = np.dot(weight_vector.T, feature_vector)

            if len(english) == 1 and len(japanese) == 1:

                # Arc 0 --> 0 labeled english[i]:japanese[0] with weight of the rule
                fst += "0 0 %s %s %s\n" % (english[0], japanese[0], weight)

            else:
                # Arc 0 --> [new node] labeled english[0]:<eps> with weight 1
                node += 1
                fst += "0 %s %s <eps> 1\n" % (node, english[0])

                for en in english[1:]:
                    # Arc [node] --> [new node] labeled english[i]:<eps> with weight 1
                    node += 1
                    fst += "%s %s %s <eps> 1\n" % (node-1, node, en)

                for ja in japanese[:-1]:
                    node += 1
                    # Arc [node] --> [new node] labeled <eps>:japanese[i] with weight 1
                    fst += "%s %s <eps> %s 1\n" % (node-1, node, ja)

                # Arc [node] --> 0 labeled <eps>:japanese[-1] with the weight of the rule
                fst += "%s 0 <eps> %s %s\n" % (node, japanese[-1], weight)


        # The in and out symbol dictionaries
        isyms = "<eps> 0\n"
        for i, en in enumerate(set(isymbols)):
            isyms += "%s %s\n" % (en, i+1)
        
        osyms = "<eps> 0\n"
        for i, ja in enumerate(set(osymbols)):
            osyms += "%s %s\n" % (ja, i+1)
        
        # Write everything to a file
        fst_f = "%sphrase-table-%s.fst" % (out_dir, line_num)
        isymbols_f = "%sphrase-table-%s.isyms" % (out_dir, line_num)
        osymbols_f = "%sphrase-table-%s.osyms" % (out_dir, line_num)
        output_f = "%sfst-%s.fst" % (out_dir_fst, line_num)

        with open(fst_f, "w") as f: 
            f.write(fst)
        with open(isymbols_f, "w") as f: 
            f.write(isyms)
        with open(osymbols_f, "w") as f: 
            f.write(osyms)

        # make real fsts
        call = "fstcompile --isymbols=" + isymbols_f + " --osymbols=" + osymbols_f + " " + fst_f + " " + output_f
        subprocess.call([call], shell=True)

        # sort the fst (that's needed for the composition later on)
        output_fst = "%sfst-%s.fst" % (out_dir_fst, line_num)
        sort_f = "%sfst_sort-%s.fst" % (out_dir_sort, line_num)
        call_sort = "fstarcsort " + output_fst + " " + sort_f
        subprocess.call([call_sort], shell=True)
  

if __name__ == '__main__':
    task2()