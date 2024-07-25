#!/usr/bin/env python
# coding: utf-8

# Archivos a usar 
#-----------------------------------------------------------------------------
#tags = "scfs_pretree/tag.BED"
#subdb = "scfs_pretree/subdb.fasta"
#clades = "../../lolipop/freqs/the_clades/scfs_cc.csv"
#-----------------------------------------------------------------------------
import sys
tags = sys.argv[1]
subdb = sys.argv[2]
clades = sys.argv[3]
#-----------------------------------------------------------------------------

tags_dict = {}

with open(tags, "r") as file_:
    for line in file_:
        cod, acc = line.strip().split()
        tags_dict[cod] = acc

subdb_dict = {}

with open(subdb, "r") as file_:
    db_acc = ""
    db_spp = ""

    for line in file_:
        if line.startswith(">"):
            # Extract accession number from header
            db_acc = line.split(".")[0][1:]

            # Extract species information from header (within square brackets)
            db_spp = line.split("[")[1].split("]")[0]

            # Store the accession number-species pair in the dictionary
            subdb_dict[db_acc] = db_spp

## Este diccionario es de 27 cuando debería ser de 340
clades_dict = {}

with open(clades, "r") as file_:
    for line in file_:
        columns = line.strip().split("\t")
        clade = columns[0]
        spp = columns[1]
        clades_dict[spp] = clade

complete_table = open('complete_table.txt', 'w')

notinclades = []
tag_clade_dict = {}
for acc, tag in tags_dict.items():
    sp = subdb_dict[acc]
    if sp in clades_dict:
        tag_clade_dict[tag] = clades_dict[sp]
        # fill complete table
        line = f"{tag}\t{acc}\t{sp}\t{clades_dict[sp]}\n"
        complete_table.write(line)
    else:
        notinclades.append(sp)

complete_table.close()

with open('itool_annotation.txt', 'w') as outfile:
    for k, v in tag_clade_dict.items():
        line = k + '\t' + v + '\n'
        outfile.write(line)

print(set(notinclades))
