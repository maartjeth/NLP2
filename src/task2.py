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

def task2():
    debug = True # false
    english_text_file = "../data/dev.en"
    grammar_file = "../data/rules.monotone.dev/grammar." # Without extension
    weight_file = "../data/weights.monotone"
    out_dir = "../data/phrase-tables/"

    # Read in all lines
    with open(english_text_file, "r") as f: 
        lines = f.read().split("\n")

    weights = []
    with open(weight_file, "r") as f:
        w_lines = f.read().split("\n")
        for w in w_lines:
            weights.append(float(w.split(" ")[1]))

    weight_vector = np.asarray(weights[0:-2]) # TODO: for now I deleted the last two features

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

            glue = float(len(grammar)) # TODO: do i interpret glue correctly from the assignment?
        
        # Now I hope this occurs only really really sporadically
        preprocessed_line, included_OOV = preprocess(lines[line_num], grammar)
        if included_OOV == True:
            with open(english_text_file, "w") as f:
                sentences = f.readlines()
                sentences[line_num] = preprocessed_line
                f.write(sentences)
           

        # For testing:
        if debug == True:
            grammar = test_grammar.split("\n")

        #TODO: we still need to word penalty feature, but need to think of a more efficient way to do this
        #TODO: pass through feature

        node = 0 # The last node number
        fst, isymbols, osymbols = "", [], []
        for rule in grammar:
            if rule == "": continue
            parts = rule.split(" ||| ")
            english = parts[1].split(" ")
            japanese = parts[2].split(" ")  
            isymbols += english
            osymbols += japanese

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
        with open("%sphrase-table-%s.fst" % (out_dir, line_num), "w") as f: 
            f.write(fst)
        with open("%sphrase-table-%s.isyms" % (out_dir, line_num), "w") as f: 
            f.write(isyms)
        with open("%sphrase-table-%s.osyms" % (out_dir, line_num), "w") as f: 
            f.write(osyms)

def preprocess(line, grammar):
    en_words = set()
    included_OOV = False

    for rule in grammar:
        if rule == "": continue
        parts = rule.split(" ||| ")
        english = parts[1].split(" ")
        for word in english:
            en_words.add(word)

    line_list = line.split(" ")
    for i, word in enumerate(line_list):
        if word not in en_words:
            line_list[i] = 'OOV'
            included_OOV = True

    if included_OOV == True:
        new_line = ''.join(line_list)
    else:
        new_line = line

    return new_line, included_OOV

if __name__ == '__main__':
    task2()