#################################
## Task 2
#
# Transform the phrase tables into transducers. 
#
## To do
# * Weigh all arcs using the linear model. Now they all have weight .5 or 1
# *
#

english_text_file = "../data/dev.en"
grammar_file = "../data/rules.monotone.dev/grammar." # Without extension
out_dir = "../data/phrase-tables/"

# Read in all lines
with open(english_text_file, "r") as f: 
    lines = f.read().split("\n")

# A simple grammar for testing purposes
test_grammar = """
    ||| the ||| le
    ||| the ||| un
    ||| dog ||| chien
    ||| black ||| noir
    ||| black ||| noirs
    ||| black dog ||| chien noir
    ||| black dog barks ||| chien noir aboie
"""[1:-1]

# Line 35 is the shortest one, line 2 the longest 
for line_num in [35]: # or: range(len(lines)):
    with open(grammar_file + str(line_num)) as f:
        grammar = f.read().split("\n")
        
    # For testing:
    # grammar = test_grammar.split("\n")

    node = 0 # The last node number
    fst, isymbols, osymbols = "", [], []
    for rule in grammar:
        if rule == "": continue
        parts = rule.split(" ||| ")
        english = parts[1].split(" ")
        japanese = parts[2].split(" ")
        isymbols += english
        osymbols += japanese

        ###################################
        # TO DO: calculate actual weights #
        ###################################
        weight = 0.5

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