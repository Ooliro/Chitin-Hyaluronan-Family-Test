#!/usr/bin/env sh

"Crea una base de datos de las primeras 100 secuencias resultado de Omnia para que puedan ser anxadas a cualquiera de las dos sub-bases de datos de metazoa"

# Nuevos archivos
echo "
Tabla completa tipo hmmsearch de Omnia: $1
DB de Omnia: $2
"
echo "[OK]  Tablas cargadas"

# -----------------[OMNIA] Rangos de hmmsearch para hmm, ali & env [OMNIA]------------------

# --------------Primero creamos una subbase de datos para solo OMNIA------------------

cut -f1 $1 | head -100 > 100om_accsnm.temp 
seqtk subseq $2 100om_accsnm.temp > omn_subdb.fasta

# Y corta solo las columnas de número de acceso, inicio y fin de dominio
cut -f1,5,6 $1 | head -100 > omn_hmm.bed
cut -f1,7,8 $1 | head -100 > omn_ali.bed
cut -f1,9,10 $1 | head -100 > omn_env.bed

echo "[OK]  Archivos BED creados para OMNIA"
# ---------------------------------Esto para sacar las deltas de qué tamaño de dominio encontramos---------------------------------------
awk '{print $0 "\t" $3-$2}' omn_hmm.bed > omn_hmm_diff.bed
awk '{print $0 "\t" $3-$2}' omn_ali.bed > omn_ali_diff.bed
awk '{print $0 "\t" $3-$2}' omn_env.bed > omn_env_diff.bed
echo "Deltas de dominios BED creados [OK] "
# --------------------------------Elige el rango a tomar en cuenta----------------------------------------
echo "Escribe un formato de rangos para Metazoa:"
echo "hmm"
echo "ali"
echo "env"
read selection

if [[ $selection == "hmm" ]]; then
    temp_file="omn_hmm.bed"
elif [[ $selection == "ali" ]]; then
    temp_file="omn_ali.bed"
elif [[ $selection == "env" ]]; then
    temp_file="omn_env.bed"
else
    echo "Opcion no valida"
    exit 1
fi

bedtools getfasta -fi omn_subdb.fasta -bed $temp_file -fo omn_domdb.fasta
# ------------------------------ACOMODA TUS ARCHIVOS------------------------------------------
#[CARPETAS PRINCIPALES]
mkdir omn_bedrooms
mkdir omn_bedrooms/diff

#[ARCHIVOS BED]
mv omn_hmm.bed omn_bedrooms/
mv omn_ali.bed omn_bedrooms/
mv omn_env.bed omn_bedrooms/

#[DELTAS DE LOS RANGOS BED]
mv omn_hmm_diff.bed omn_bedrooms/diff
mv omn_ali_diff.bed omn_bedrooms/diff
mv omn_env_diff.bed omn_bedrooms/diff

#[ARCHIVOS CONTROL]

#---------------------------Cambio de etiquetas---------------------------------------

python taggin_omn.py omn_subdb.fasta omn_domdb.fasta
echo "Cambio de etiquetas exitoso! Archivo final para pasar al alineamiento con etiquetas cambiadas será temporalmente denominada omn_modified.fasta y su traducción está en el archivo tag.BED"

rm tags.txt
#rm tag.BED
echo "ahrre"
