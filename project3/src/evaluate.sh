
# The root directory
root=~/Github\ Projects/NLP2/project3
name="val-meteor"
kind="val"
sample_size="-100"
output_fn="data-$kind/results/$name-best-translations$sample_size.txt"
target_fn="data-$kind/results/$name-best-translations-targets$sample_size.txt"
results_fn="data-$kind/$name-evaluation.txt"

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