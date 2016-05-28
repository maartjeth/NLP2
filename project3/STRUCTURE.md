# Directory structure

# `data` directory
Contains the raw data. This folder shouldn't be changed.

# `data-dev` and `data-test` directories
They contain all files for development and testing respectively. They should contain roughly similar subdirectories (I explain `dev` only)

* `dev-sentences.json`: a JSON file with information about every sentence. It contains a list of dictionaries, containing the sentence number, the first line (in the 1000best file), the last line (in the 1000best file) and the target and source sentences.
* `dev-translations.txt`: a file with all candidate translations from the 1000best file.
* `dev-targets.txt`: a file with the corresponding target translations
* `eval/`: a folder with all METEOR evaluations of the candidate translations. It contains target translations per part, the raw meteor output `dev-meteor-output-part?.txt` and the post-processed meteor scores `dev-meteor-part?.txt`
* `parse/`: directory with parsed translation candidates
* `parse-pre`: contains preporatory files for parsing. I compressed the files, since they are massively repetative (the unpacked file is ~2GB, and ~40MB packed)
* `translations/`: contains the translations, split into six parts, of 500 000 sentences each (except for the last, which contains the remaining sentences)

# `src` directory
Contains all scripts

# `docs` directory
Contains all PDFs etc.

# `libraries` directory
Contains all external libraries such as Mate and METEOR