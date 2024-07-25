# Contando clados

Quiero juntar todas las frecuencias de clados para poder hacer un gráfico de frecuencias con clados. Para esto podemos usar:

## Script inicial

`awk '{freq[$1]+=$3} END {for (clade in freq) print clade, freq[clade]}' input.txt > output.txt`

Donde:

- {freq[$1]+=$3}: This tells awk to create an associative array freq with keys equal to the values in the first column ($1), and to add the value in the third column ($3) to the corresponding value in freq.

- END: This tells awk to execute the following commands after all input lines have been processed.

- {for (clade in freq) print clade, freq[clade]}: This tells awk to loop through the freq array, assigning each key to the variable clade, and to print the clade and its corresponding value in freq to output.txt.


## Script final

`awk '{freq[$1]+=$NF} END {for (clade in freq) print clade, freq[clade]}' input.txt > output.txt`
 
Donde:

- awk '{freq[$1]+=$NF}': Hace referencia a tomar el primer campo como llave; y $NF para tomar la última columna


NOTA IMPORTANTE: Este script cuenta como separadores a los espacios en blanco! Antes de usarlo haz un sed:

`sed 's/\t/ /g'`
