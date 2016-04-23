#!/bin/bash

###
# Draws an FST by its name. We assume the fst has extension .fst,
# the isymbols are in the .isyms file and osymbols in .osyms. Exapmle:
# ./draw-fst phrase-table-35
# writes a postscript file phrase-table-35.ps to the current directory

# Get name argument
name="$1"

# Files
fst_binary="${name}.bin.tmp"
fst_dot="${name}.dot.tmp"
fst_ps="${name}.ps"

# Go!
fstcompile --isymbols="${name}.isyms" --osymbols="${name}.osyms" "${name}.fst" "$fst_binary"
fstdraw --isymbols="${name}.isyms" --osymbols="${name}.osyms" "$fst_binary" "$fst_dot"
dot -Tps "$fst_dot" > "$fst_ps"
# For PDF (doesn't work for Bas)
# dot -Tpdf "$fst_dot" > "${root}/fst-$i.pdf"

# Done
echo "Finished drawing FST: ${name}.ps"
rm "$fst_binary"
rm "$fst_dot"
