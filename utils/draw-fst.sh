#!/bin/bash

###
# Draws the FST by its id and directory. For example:
# ./draw-fst 4 ../data/fsts
# writes a postscript file fst-4.ps to the ../data/fsts directory.
# Directory is optional and default is the current one.

# Get & set arguments
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
i="$1"
root="$2"
if [ "$root" = "" ]; then
	root="$DIR"
	echo "No directory given, assuming $root"
fi

# Files
osyms="${root}/osyms-$i.txt"
fst="${root}/fst-$i.fst"
fst_binary="${root}/fst-$i.bin"
fst_dot="${root}/fst-$i.dot"
fst_ps="${root}/fst-$i.ps"
fst_pdf="${root}/fst-$i.pdf"

# Go!
fstcompile --osymbols="$osyms" "$fst" "$fst_binary" #>/dev/null
fstdraw --osymbols="$osyms" "$fst_binary" "$fst_dot" >/dev/null
dot -Tps "$fst_dot" >"$fst_ps"
# For PDF (doesn't work for Bas)
# dot -Tpdf "$fst_dot" > "${root}/fst-$i.pdf"
echo "Finished drawing FST: $fst_ps"

# Clean up
rm "$fst_binary"
rm "$fst_dot"
