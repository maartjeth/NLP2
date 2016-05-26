#PBS -lnodes=1
#PBS -lwalltime=24:00:00

# Parameters
scratch="$TMPDIR"
home_root="$HOME/nlp/project3"
input_fn="$home_root/sara/test.txt"


# Prepare scratch 
mkdir "$scratch/output"
cp "$input_fn" "$scratch/$input_fn"
cp "$home_root/mate" "$scratch/mate"

# Filenames
mate="$scratch/mate/anna-3.61.jar"
model_lemma="$scratch/mate/lemma-ger-3.6.model"
model_tag="$scratch/mate/tag-ger-3.6.model"
model_morph="$scratch/mate/morphology-ger-3.6.model"
model_parse="$scratch/mate/parser-ger-3.6.model"
output_base="$scratch/output/translations"
output_lemma_fn="${output_base}.lem"
output_postag_fn="${output_base}.postag"
output_morph_fn="${output_base}.morph"
output_parse_fn="${output_base}.parse"

# Go, go, go!
java -cp $mate is2.lemmatizer.Lemmatizer -model $model_lemma -test $input_fn -out $output_lemma_fn
java -cp $mate is2.tag.Tagger -model $model_tag -test $output_lemma_fn -out $output_postag_fn
java -cp $mate is2.mtag.Tagger -model $model_morph -test $output_postag_fn -out $output_morph_fn
java -cp $mate is2.parser.Parser -model  $model_parse -test $output_morph_fn -out $output_parse_fn

mv "$scratch/output" "$home_root/output"