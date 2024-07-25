#!/usr/bin/env python
# coding: utf-8

# arg1 = Archivo fasta con todos los nombres completos
# arg2 = Archivo fasta al que le vamos a cambiar los nombres


import sys

filename = sys.argv[1]
#filename = '/home/raulrosas/Documentos/IFC/lab/one4all/caramel/subdb/sub_cgchm.fasta'

infile = open(filename, 'r')

# son los identificadores ya utilizados
idcounts = {}
species = {}
my_list = []

for line in infile:
    line = line.strip()
    if line == '' or line[0] != '>':
        continue

    # protid

    protid = line.split('.')[0][1:]

    # Chitin or Hyaluronan
    if 'hitin' in line:
        tipo = 'C'
    elif 'yaluronan' in line:
        tipo = 'H'
    else:
        tipo = 'N'

    # species id
    spname = line.split('[')[1].split(']')[0]
    genre, sp, *_ = spname.split(' ')

    spidentifier = genre[0].lower() + sp[:2]

    if spidentifier in species:
        if species[spidentifier] != spname:
                spidentifier = genre[0].lower() + sp[:3]
    else:
         species[spidentifier] = spname

    # numero

    if spidentifier in idcounts:
        number = idcounts[spidentifier] + 1
        idcounts[spidentifier] += 1
    else:
        number = 1
        idcounts[spidentifier] = 1

    final_id = f"{spidentifier}{tipo}{number}"

    print(f"{protid}\t{final_id}")
    
    my_list.append((protid, final_id))

# Close file
                   
infile.close()

list_str = '\n'.join(str(item) for item in my_list)

with open ("tags.txt", "w") as output:
    output.write(list_str)


# Guardalo de forma segura

file = open("tags.txt")

data = file.read()
replace_one = data.replace(',' , '\t')
replace_two = replace_one.replace("'", "")
replace_three = replace_two.replace("(" , "")
replace_four = replace_three.replace(")" , "")

file.close()

print(replace_four)

save_tab = open('tag.BED', 'w+')
save_tab.writelines(replace_four)
save_tab.close()


fasta_file = sys.argv[2]
mapping_file = open("tag.BED", "r")

#fasta_file = "scfm-hit.fasta"
#mapping_file = "tag.BED"

output_file = "modified.fasta"

# Read the mapping file and create a dictionary of partial names to new names
mapping = {}
with mapping_file as f:
    for line in f:
        partial_name, new_name = line.strip().split("\t")
        mapping[partial_name] = new_name

# Open the input FASTA file and the output file
with open(fasta_file, "r") as f_in, open(output_file, "w") as f_out:
    for line in f_in:
        if line.startswith(">"):
            header = line.strip()[1:]  # Remove the ">" character
#            header = line.strip()
            new_header = header
            for partial_name, new_name in mapping.items():
                if partial_name in header:
                    new_header = header.replace(partial_name, new_name)
                    break
            new_header = new_header.split(":")[0]  # Remove second part delimited by ":"
            new_header = new_header.split(".")[0]  # Remove second part delimited by "."
            f_out.write(f">{new_header}\n")
        else:
            f_out.write(line)

mapping_file.close()
