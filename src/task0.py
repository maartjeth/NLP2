###
# In task 0, we preprocess all sentences and replace all words
# that are not in the grammar by OOV. Also, we keep only 100 words.

def preprocess_oov(sentences, grammar_file, N=100):
    """Replace all words not in the grammar by OOV and write to new file

    Args:
        sentences: text file with the sentences (e.g. `dev.en`)
        grammar_file: the file with a sentence grammar (Without extension; e.g. `grammar.`)
        N: Number of sentences, default 100
    """

    with open(sentences, 'r') as  f:
        lines = f.read().split("\n")
    
    ooved_lines = '';
    for line_num in range(N):

        with open(grammar_file + str(line_num), 'r') as f:
            grammar = f.read()
        
        en_words = set()
        for rule in grammar.split("\n"):
            if rule == "": continue
            parts = rule.split(" ||| ")
            english = parts[1].split(" ")
            for word in english:
                en_words.add(word)

        # Replace all the unknown words with OOV and add the OOV'ed line to ooved_lines
        replace_oov = lambda word: word if word in en_words else "OOV"
        ooved_words = map(replace_oov, lines[line_num].split(" "))
        ooved_lines += " ".join(ooved_words) + "\n"

    with open('../data/dev-ooved.en', 'w') as f:
        f.write(ooved_lines)
       

if __name__ == '__main__':
    # Preprocess our sentences
    preprocess_oov('../data/dev.en', '../data/rules.monotone.dev/grammar.')