###
# In task 0, we preprocess all sentences and replace all words
# that are not in the grammar by OOV. Also, we keep only 100 words.
from Helper import *
from FST import *

def preprocess_oov(self, raw_sentences_fn=None, 
    grammar_base_fn=None, num_sentences=None, sentences_fn=None):
    """Replace all words not in the grammar by OOV and write to new file

    Args:
        sentences: text file with the sentences (e.g. `dev.en`)
        grammar_file: the file with a sentence grammar (Without extension; e.g. `grammar.`)
        num_sentences: Number of sentences, defaults to the value of Helper
    """
    if num_sentences == None: num_sentences = self.num_sentences
    if sentences_fn == None: sentences_fn = self.sentences_fn
    if raw_sentences_fn == None: raw_sentences_fn = self.raw_sentences_fn

    with open(raw_sentences_fn, 'r') as  f:
        sentences = f.read().split("\n")
    
    ooved_sentences = '';
    for line_num in range(num_sentences):
        
        en_words = set()
        grammar = self.get_grammar(line_num, grammar_base_fn)
        for rule in grammar:
            if rule == "": continue
            parts = rule.split(" ||| ")
            english = parts[1].split(" ")
            for word in english:
                en_words.add(word)

        # Replace all the unknown words with OOV and add the OOV'ed line to ooved_lines
        replace_oov = lambda word: word if word in en_words else self.OOV
        ooved_words = map(replace_oov, sentences[line_num].split(" "))
        ooved_sentences += " ".join(ooved_words) + "\n"

    with open(self.sentences_fn, 'w') as f:
        f.write(ooved_sentences)

# Add to helper class
Helper.preprocess_oov = preprocess_oov

if __name__ == '__main__':
    H = Helper(type="all-monotone")
    H.preprocess_oov('../data/dev.en')