
# The root directory
root=~/Github\ Projects/NLP2/project3
name="val-sample-size-160"
kind="val"
# sample_size="-10"
output_fn="models/$name/$name-best-translations-results.txt"
target_fn="data-dev/val-targets.txt"
results_fn="models/$name/$name-evaluation.txt"

# cd "$root/libraries/multeval"
# ./multeval.sh eval \
# 	--refs $target_fn \
# 	--hyps-baseline $output_fn \
# 	--meteor.language de
# 	
meteor="libraries/meteor/meteor-1.5.jar"
paraphrase_de="libraries/meteor/data/paraphrase-de.gz"
cd "$root"
java -Xmx2G -jar $meteor $output_fn $target_fn -l de -norm -a $paraphrase_de > $results_fn