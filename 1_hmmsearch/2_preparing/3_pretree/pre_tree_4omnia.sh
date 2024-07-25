#!/usr/bin/env sh

echo "
Tabla con valores de e-value y dominios filtrados: $1
Tabla de referencia de campos a cortar: $2
Base de datos refseq: $3
"
# Primero sería el archivo "f" de 1stdomeval
# Segundo sería el archivo "c" de allfields
# Tercero sería la base de datos sobre la que se hizo esto. En este caso: Omnia

echo "Tablas cargadas [OK] "

#------------------------------------------------------------------------
# Quitar secuencias cuyo valor de e-value es menor a 0.0001

awk '$7 <0.0001' $2 > good_values.temp
awk -F'\t' '($19 - $18 > 200)' good_values.temp > good_fields.tab
# ------------------------------------------------------------------------

# Recortar la base de datos refseq a solo secuencias halladas con hmmsearch
cut -f1 $1 > acc.txt
seqtk subseq $3 acc.txt > subdb.fasta
echo "Sub-base de datos cortada [OK] "

# Busqueda y rescate. Dada la lista 1, busca coincidencias en la lista 2 e imprime las mismas.
# Primero ids y luego los campos
for S in $(cat acc.txt | awk '{print $1}');
do
        echo $S
        grep $S good_fields.tab >> catched.temp && echo $S >> found.temp || echo $S >> lost.temp
done

# Con las coincidencias, usa solo el primer campo de números de acceso para eliminar duplicados
sort -u -k1,1 catched.temp > catch_sort.temp


# Y corta solo las columnas de número de acceso, inicio y fin de dominio
cut -f1,3,6,10,11,16-21 $2 > which_domain.temp

cut -f1,16,17 catch_sort.temp > hmm.bed
cut -f1,18,19 catch_sort.temp > ali.bed
cut -f1,20,21 catch_sort.temp > env.bed

awk -F'\t' 'FNR==NR{a[$1];next} $1 in a{count++} END{print "De un total de " FNR " secuencias en la lista A, " count " están contenidas en la lista B"}' catch_sort.temp acc.txt


#Limpia archivos temporales
rm catched.temp
rm found.temp
rm lost.temp
rm catch_sort.temp

echo "Archivos BED creados [OK] "
# ------------------------------------------------------------------------

awk '{print $0 "\t" $3-$2}' hmm.bed > hmm_diff.bed
awk '{print $0 "\t" $3-$2}' ali.bed > ali_diff.bed
awk '{print $0 "\t" $3-$2}' env.bed > env_diff.bed

echo "Sumas de dominios BED creados [OK] "
# ------------------------------------------------------------------------

echo "Escribe un formato de rangos:"
echo "hmm"
echo "ali"
echo "env"
read selection

if [[ $selection == "hmm" ]]; then
    temp_file="hmm.bed"
elif [[ $selection == "ali" ]]; then
    temp_file="ali.bed"
elif [[ $selection == "env" ]]; then
    temp_file="env.bed"
else
    echo "Invalid selection"
    exit 1
fi

bedtools getfasta -fi subdb.fasta -bed $temp_file -fo domdb.fasta
echo "Sub-base de datos cortada [OK] "
# ------------------------------------------------------------------------
# Limpia otros archivos
rm acc.txt
rm subdb.fasta.fai
rm good_values.temp

# Acomoda tus archivos
mkdir bedrooms
mkdir bedrooms/diff

mv which_domain.temp bedrooms/
mv hmm.bed bedrooms/
mv ali.bed bedrooms/
mv env.bed bedrooms/

mv hmm_diff.bed bedrooms/diff
mv ali_diff.bed bedrooms/diff
mv env_diff.bed bedrooms/diff

echo "[OK] La tabla domdb.fasta será la que utilices para tu alineamiento"
echo "[EXTRA] La tabla subdb.fasta serán las secuencias FASTA de tus claves contenidas en tu archivo no_duplicates!"

#---------------------------Cambio de etiquetas---------------------------------------

python taggin.py subdb.fasta domdb.fasta
echo "Cambio de etiquetas exitoso! Archivo final para pasar al alineamiento con etiquetas cambiadas será temporalmente denominada modified.fasta y su traducción está en el archivo tag.BED"

rm tags.txt
