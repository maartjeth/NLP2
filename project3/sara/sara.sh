#PBS -lnodes=1
#PBS -lwalltime=24:00:00

name="part1"

# Parameters
scratch="$TMPDIR"
home="$HOME"
#home="/home/basc"
#scratch="$home/nlp/project3/test"

project_root="$home/nlp/project3"
input_archive_fn="$project_root/sara/test-$name.gz"

# Prepare scratch
echo Copying files...
mkdir -p "$scratch/output"
cp "$input_archive_fn" "$scratch/archive.gz"
input_fn="$(tar ztf $scratch/archive.gz)"
cp -r "$project_root/mate" "$scratch/mate"
echo Unpacking...
tar zxvf "$scratch/archive.gz"

# Filenames
mate="$scratch/mate/anna-3.61.jar"
model_lemma="$scratch/mate/lemma-ger-3.6.model"
model_tag="$scratch/mate/tag-ger-3.6.model"
model_morph="$scratch/mate/morphology-ger-3.6.model"
model_parse="$scratch/mate/parser-ger-3.6.model"
output_base="$scratch/output-$name/translations"
output_lemma_fn="${output_base}.lem"
output_postag_fn="${output_base}.postag"
output_morph_fn="${output_base}.morph"
output_parse_fn="${output_base}.parse"

# Go, go, go!
java -cp $mate is2.lemmatizer.Lemmatizer -model $model_lemma -test $input_fn -out $output_lemma_fn
java -cp $mate is2.tag.Tagger -model $model_tag -test $output_lemma_fn -out $output_postag_fn
java -cp $mate is2.mtag.Tagger -model $model_morph -test $output_postag_fn -out $output_morph_fn
java -cp $mate is2.parser.Parser -model  $model_parse -test $output_morph_fn -out $output_parse_fn

echo Zipping...
cd "$scratch/output"
tar zcvf "$scratch/output-$name/lem.gz" translations.lem
tar zcvf "$scratch/output-$name/postag.gz" translations.postag
tar zcvf "$scratch/output-$name/morph.gz" translations.morph
tar zcvf "$scratch/output-$name/parse.gz" translations.parse

echo Cleaning up and storing
rm "$output_lemma_fn"
rm "$output_postag_fn"
rm "$output_morph_fn"
rm "$output_parse_fn"

cp -r "$scratch/output" "$project_root"
echo "Done."
