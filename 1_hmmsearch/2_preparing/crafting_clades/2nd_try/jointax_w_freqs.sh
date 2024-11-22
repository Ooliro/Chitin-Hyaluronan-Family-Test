#!/usr/bin/env sh

# En este script primero va el archivo tax_clades donde la segunda columna tiene el nombre del organismo
# y después va el archivo h_frequencies donde la primera columna tiene el nombre del organismo.
# Este script crea una tabla comprehensiva donde incluyes las frecuencias de las especies y su clado
# asignado.

awk -F'\t' '
FNR==NR { # Process the first file
    map[$2] = $1; # Store column B as key and column A as value
    next;
}
$1 in map { # Process the second file and look for matches in column B
    print map[$1] "\t" $1 "\t" $3; # Print A (from file1), B, and D (from file2)
}' $1 $2 > tax_and_freqs.csv

# Y por último haz un resumen de los valores por clado aqui obtenido

awk -F '\t' '{totals[$1] += $3} END {for (name in totals) print name "\t" totals[name]}' tax_and_freqs.csv > tax_and_freqs_SUMMARY.csv
