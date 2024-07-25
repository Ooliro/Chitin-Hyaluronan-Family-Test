#!/usr/bin/env python3

#!/usr/bin/env python
# coding: utf-8

"""This scritp extracts the paths from the leaves to the root in a ncbi taxonomy tree, narrow it to spp and clade, and finally append the clade column to an existing table"""

# Argumentos de terminal:
#arg1 = Arbol en formato phylip

# Primera parte: Corta hojas y raices
from Bio import Phylo
import sys

# Read files from bash
arbol = open(sys.argv[1])

# read tree
tree = Phylo.read(arbol, 'newick')
tree.ladderize()

# get leaves
leaves = tree.get_terminals()

# get paths
paths = []
for leaf in leaves:
    path = tree.get_path(leaf)
    paths.append(path)

# write to a file
outfile_name = 'branch_leaf.txt'
with open(outfile_name, 'w') as outf:
    for path in paths:
        names = [clade.name for clade in path]
        line = '\t'.join(names) + '\n'
        outf.write(line)

# Segunda parte: Limpia ramas para quedarte con clados y spp
import pandas
archivo=open('branch_leaf.txt')
myclades = []
for line in archivo:
    line = line.split("\t")
    if len(line) == 2:
        myclades.append((line[0], line[1]))
    else:
        myclades.append((line[1], line[-1]))

save_file = open('tax_clades.tab', 'w+')

for elemento in myclades:
    linea = elemento[0] + "\t" + elemento[1]
    save_file.write(linea)
save_file.close()

print("Si no hay problemas hasta aqui, procede a la parte dos y agrega AL FINAL las especies que no encuentre de inicio")
