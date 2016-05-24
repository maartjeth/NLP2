# Phrase Based Machine Translation Using Finite State Transducers
## Maartje ter Hoeve & Bas Cornelissen

Scroll down for instructions on how to run the experiments. Note that you will have to unzip `data.zip`.

### Requirements
The code of course crucially depends on OpenFST. Furthermore, we use *Python 2.7* and standard packages.

### Directory structure
This directory is structured as follows:

* `data` contains the actual data provided for the project. **IMPORTANT:** you still have to unzip `data.zip`!
* `dummydata` contains data for some dummy sentences that can be used for testing and also nicely illustrate how everything works
* `src` contains the source code

All FSTs are stored in three files. The `.txtfst` file is a plain text file describing the fst. The `.isyms` and `.osyms` contain the in and out labels. Finally, the `.fst` file is the compiled version and the `.pdf` a, well, PDF. One FST has one _base name_: the filename without extension.

### Code structure
Fist, we wrote an `FST` class that acts as an interface between Python and the OpenFST command line interface. Using it is pretty straightforward: 
```python
fst = new FST('/path/to/the/base/name') 
fst.compile().draw()
fst.sort().determinize()

other_fst = new FST('some/other/base/name')
composite = fst.compose(other_fst)
```
Note that you only pass it the _base name_ (i.e. without extension). It looks for all other files (`.isyms`, `.osyms` etc.)

Second, there is a `Helper` class that holds all information mainly that we use throughout the experiments (filenames, general settings etc). All tasks are stored as methods of this class to be able to access that information.

(Tasks are further divided into Python files, following the instructions. However, the structure is closer to the steps we mention in our report.)

### Running the experiments
In the `src` directory, there are three experiments: the main experiments (`experiments_main.py`), some auxiliary experiments (`experiments_auxiliary`) and dummy experiments (`experiments_dummies.py`). We assume all code is run from that directory! Running these scripts (using e.g. `python experiments_dummies.py`) will create a bunch of new directories and write all FSTs needed for the whole task and BLEU scores. 

* Main experiment: does monotone and lattice translation on the first 100 sentences in `data/dev.en`. 
* Dummy experiment: runs all the translation experiments  on dummy sentences. This allows you to inspect what our code does precisely, because the produced PDFs are relatively small. Highly recommended to run this first.
* Auxiliary experiments: we did some further experiments (investigating effects of features etc), those are in the auxiliary experiments.
