# Task 2

import math
from Helper import *
from FST import *

def get_feature_weights(self, refresh=False):
    """
    Gets a dictionary with feature weights
    """
    if refresh:
        del self.feature_weights
        return self.get_feature_weights()
        
    try: 
        return self.feature_weights
    except AttributeError:
        with open(self.weight_file, "r") as f:
            w_lines = f.read().split("\n")
            feature_weights = []
            for line in w_lines:
                if line == "":
                    continue
                else:
                    key, val = line.split(" ")
                    if key in self.features:
                        feature_weights.append((key, float(val)))
        self.feature_weights = dict(feature_weights)
    return self.feature_weights

def generate_phrase_table_fsts(self, sentence_ids=None, grammar_base_fn=None, out_base=None, draw=False):
    """
    Generates all phrase table FSTS 

    Args:
        sentence_ids: a list of ids (numbers) of the sentences (to find the right grammars)
        grammar_base_fn: the base of the grammr files; defaults to Helper value.
        out_base: base of the resulting fsts; defaults to Helper value for phrase tables.
        draw: draw the fsts?
    """
    if out_base == None: out_base = self.phrase_table_fst_base
    if sentence_ids == None: sentence_ids = range(self.num_sentences)

    for line_num in sentence_ids:
        fst = FST(out_base + "-" + str(line_num))
        grammar = self.get_grammar(line_num, grammar_base_fn=grammar_base_fn)
        
        node, fst_txt, isymbols, osymbols = 0, "", [], []
        for rule in grammar:

            parts = rule.split(" ||| ")
            english = parts[1].split(" ")
            japanese = parts[2].split(" ")              
            isymbols += english
            osymbols += japanese

            # Calculate additional features
            OOV_count = english.count(self.OOV)
            glue = 1 
            word_penalty = float(len(english)) * (-1.0 / math.log(10))

            # Determine the weight (this is the log-linear model)
            weight = 0
            feature_weights = self.get_feature_weights()
            for feature_value in parts[3].split(" "):
                feature, value = feature_value.split("=")
                if feature in feature_weights.keys():
                    weight += feature_weights[feature] * float(value)
            weight += feature_weights['Glue'] * glue
            weight += feature_weights['WordPenalty'] * word_penalty
            weight += feature_weights['PassThrough'] * OOV_count
                
            # Build the FST 
            if len(english) == 1 and len(japanese) == 1:

                # Arc 0 --> 0 labeled english[i]:japanese[0] with weight of the rule
                fst_txt += "0 0 %s %s %s\n" % (english[0], japanese[0], weight)

            else:
                # Arc 0 --> [new node] labeled english[0]:<eps> with weight 1
                node += 1
                fst_txt += "0 %s %s <eps> 0\n" % (node, english[0])

                for en in english[1:]:
                    # Arc [node] --> [new node] labeled english[i]:<eps> with weight 1
                    node += 1
                    fst_txt += "%s %s %s <eps> 0\n" % (node-1, node, en)

                for ja in japanese[:-1]:
                    node += 1
                    # Arc [node] --> [new node] labeled <eps>:japanese[i] with weight 1
                    fst_txt += "%s %s <eps> %s 0\n" % (node-1, node, ja)

                # Arc [node] --> 0 labeled <eps>:japanese[-1] with the weight of the rule
                fst_txt += "%s 0 <eps> %s %s\n" % (node, japanese[-1], weight)
        
        # Add final node
        fst_txt += "0"

        # The in and out symbol dictionaries
        isymbols_txt = "<eps> 0\n"
        for i, en in enumerate(set(isymbols)):
            isymbols_txt += "%s %s\n" % (en, i+1)
        
        osymbols_txt = "<eps> 0\n"
        for i, ja in enumerate(set(osymbols)):
            osymbols_txt += "%s %s\n" % (ja, i+1)
        
        # Update & compile the FST
        fst.update_fst(fst_txt)
        fst.update_isymbols(isymbols_txt)
        fst.update_osymbols(osymbols_txt)
        fst.compile()

        # Drawing large FST's can take a very long time!
        if draw: fst.draw()
  
# Add methods to Helper class
Helper.generate_phrase_table_fsts = generate_phrase_table_fsts
Helper.get_feature_weights = get_feature_weights

if __name__ == '__main__':
    # H = Helper(type="all-monotone")
    # H.generate_phrase_table_fsts()
    
    H = Helper(type="blackdog-monotone")
    H.generate_phrase_table_fsts(draw=True)
    