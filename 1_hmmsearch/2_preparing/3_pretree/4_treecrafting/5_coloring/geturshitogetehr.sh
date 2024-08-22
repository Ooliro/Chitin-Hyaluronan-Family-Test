#!/usr/bin/env sh

# Script para crear una tabla con información de completa que contenga números de
# acceso, IDs del árbol, spp y clados en OMNIA

echo "
Tercera parte: Tabla tag.BED con IDs del árbol: $1
Quitna/Segunda parte: Tabla resultado con spp+clado de crafting clades: $2
Tercera parte: Subbase de datos FASTA con etiquetas originales: $3"

# Primera parte para sacar tabla de accession number y spp

first_output_file="access&spp.txt"

egrep "^>" $3 | while read -r line; do
    accession=$(echo "$line" | awk '{print $1}' | sed 's/^>//')
    species=$(echo "$line" | grep -o "\[.*\]" | sed 's/\[//;s/\]//')
    echo -e "$accession\t$species">>"$first_output_file"
    done
echo "Extracción uno lista, tabla escrita a $first_output_file"

# Segunda parte para incluir el ID a cada número de acceso

second_output_file="acc&spp&ID.txt"

declare -A species_id_map

while IFS=$'\t' read -r $1; do
    species_id_map["$acc"]="$id"
done < "$acc_id_table"

while IFS=$'\t' read -r $first_output_file; do
    id="${acc_id_map[$acc]}"
    echo -e "$accession\t$species\t$id" >> "$second_output_file"
done < "$first_output_file"

echo "Process complete. Output saved to $output_file"
