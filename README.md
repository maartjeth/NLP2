"Repo for NLP2 projects" 

# Tasks
## Task 0: preprocessing
In this task we preprocess all sentences and replace all words that are not in the grammar with `OOV`. Then we forget about the original sentences in `data/dev.en` and only use `data/dev-ooved.en` afterwards. Technically, there is no need to think about this; the helper can fetch all sentences: `Helper.get_sentences()`.

## Task 1: input transducers
In this task the English source sentences are converted into transducers. These transducers are stored as `data/input/input-i.*` where `i` is the line-number and the extension follows the naming conventions (see below).

## Task 2: phrase table transducers.
Here the phrase tables as given in `grammar.i` are turned into transducers. We follow the suggestion in the instructions for the representation of multi-word phrases: first all source words are detected, then all target words returned. The weights of the connections are determined using a log-linear model, whose feature weights have already been trained (see `weights.monotone`).

## Task 3: composition.
...

# Architecture

## FST Class
The FST class is our custom wrapper around the command line interface for OpenFST. It should make dealing with all those different files much easier and more streamlined, as the class will always respect the naming conventions (see below). The FST class is initialized using its (file) base. An example...

```python
from FST import *

my_fst = FST("../data/input/input-0")
my_fst.compile()
my_fst.sort()
my_fsts.draw() # Look at ../data/input/input-0.pdf!
# Or my_fst.compile().sort().draw()
```

## Helper Class
This class has a simple goal: to help. It contains some useful function (non FST-specific), that are used in all tasks. Also, it contains global options such as the number of sentences, some directories, filenames etc. Within a given task, we typically extend the class, so that we can easily access those niceties. 

The syntax for that is pretty straight-forward:
```python
from Helper import *

# In my_file.py, *outside* the Helper class definition
def my_function(self, argument):
    N = self.num_sentences # this is a property of your Helper object
    return N 

# Save `my_function` as a method of the Helper class
Helper.a_great_function = my_function

my_helper = Helper()
print my_helper.my_function() # Prints the number of sentences
```

## Naming conventions

FSTs are described by several files. We assume that files belonging to the same FST have the same name, but different extensions. The extensions used are the following:

* `.txtfst` A text file describing the fst
* `.fst` A compiled fst
* `.isyms` A text file with in-labels
* `.osyms` A text file with out-labels

The `FST` class also crucially relies on these naming conventions. 

## Glossary
Some (weird) terminology:

* **base** refers to the path of a file, without (optional suffix) and extension. So the base of `/data/inputs/input-0.fst` is `/data/inputs/input`. So an FST has one base, but multiple files associated to it.
* ...

# Notes
## OpenFST composition
When you compose two FSTs that have mismatching in-out labels, weird things happen. More precisely, suppose you compose `FST1` (input) and `FST2` (phrase table):
```
    FST1: (0) ---[0:the]--- (1) ---[2:cat]--- (2)
    FST2: (0) ---[the:le; foo:bar]--- (1)
```
Since `cat` is not an input label of `FST2`, it seems to ignore the label values, and only use the indices (as specified in the in- and out-symbols). That gives unexpected results.

**Bottom line:** In any case, weird things happens if there is an input label in `FST2` that is *not* in `FST1`. In particular, when there is an `OOV:OOV` in the phrase table, but there is no `OOV` in the input sentence (and hence no `OOV` output label in `FST1`). This will in fact often happen in our setup, as we add the `OOV:OOV` rule to *every* grammar, even if there is no `OOV` in the input sentence.

However, there is an easy fix: we only have to make sure that the output labels of the input FST are a *super set* of the input labels of the phrase table FST.  After preprocessing, we can assume that the phrase table is sufficient (i.e. actually covers the input sentence). So then we can just use the input symbols of the phrase table FST as the output symbols of the input FST. This might result in superfluous output labels for the input FST (e.g. a superflous `OOV` output symbol), but who cares?



