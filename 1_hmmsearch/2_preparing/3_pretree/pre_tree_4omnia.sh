#!/usr/bin/env sh

# Nuevos archivos
echo "
Tabla tipo GTF de Metazoa con filtros EDOG: $1
Tabla completa tipo hmmsearch de Omnia: $2
Resultados hmmsearch para Metazoa nivel F: $3
DB de Metazoa: $4
DB de Omnia: $5
"
echo "[OK]  Tablas cargadas"

#------------------------------------------------------------------------
# Toma los números de acceso de no_dups y anexa los 100-Omnia para crear una lista de búsqueda
cut -f4 $1 > met_accsnm.temp # ProtID
cut -f1 $2 | head -100 > 100om_accsnm.temp 
cat met_accsnm.temp 100om_accsnm.temp > accs_prompts.txt

# ------------------------------------------------------------------------
# PRIMERO creamos una base de datos base, sólo con las secuencias que utilizaremos y sin ningun filtro o edición

seqtk subseq $5 met_accsnm.temp > met_subdb.fasta # Metazoa
seqtk subseq $6 100om_accsnm.temp > omn_subdb.fasta # Omnia

# SEGUNDO editamos estas DB para conservar solo los rangos ubicados, solo uno y el primero que aparezca si hay mas de uno
# Ahora con los numeros de acceso que usamos antes hacemos una búsqueda en las tablas de resultados crudos para sacar los diferentes rangos disponibles

# ------[METAZOA] Obtenemos rangos de hmmsearch [METAZOA]-------
for S in met_accsnm.temp;
do
        echo $S
        grep $S $3 >> catched.temp && echo $S >> found.temp || echo $S >> lost.temp
done
# Con las coincidencias, usa solo el primer campo de números de acceso para eliminar duplicados
sort -u -k1,1 catched.temp > catch_sort.temp
# Y corta solo las columnas de número de acceso, inicio y fin de dominio
cut -f1,5,6 catch_sort.temp > met_hmm.bed
cut -f1,7,8 catch_sort.temp > met_ali.bed
cut -f1,9,10 catch_sort.temp > met_env.bed
#awk -F'\t' 'FNR==NR{a[$1];next} $1 in a{count++} END{print "De un total de " FNR " secuencias en la lista A, " count " están contenidas en la lista B"}' catch_sort.temp acc.txt
#Limpia archivos temporales
rm catched.temp
rm found.temp
rm lost.temp
rm catch_sort.temp
echo "Archivos BED creados [OK] "
# ------------------------------------------------------------------------
awk '{print $0 "\t" $3-$2}' met_hmm.bed > met_hmm_diff.bed
awk '{print $0 "\t" $3-$2}' met_ali.bed > met_ali_diff.bed
awk '{print $0 "\t" $3-$2}' met_env.bed > met_env_diff.bed
echo "Deltas de dominios BED creados [OK] "
# ------------------------------------------------------------------------
echo "Escribe un formato de rangos para Metazoa:"
echo "hmm"
echo "ali"
echo "env"
read selection

if [[ $selection == "hmm" ]]; then
    temp_file="met_hmm.bed"
elif [[ $selection == "ali" ]]; then
    temp_file="met_ali.bed"
elif [[ $selection == "env" ]]; then
    temp_file="met_env.bed"
else
    echo "Opcion no valida"
    exit 1
fi

bedtools getfasta -fi met_subdb.fasta -bed $temp_file -fo met_domdb.fasta
echo "[OK]  Sub-base de datos para Metazoa cortada"
# -----------------------------------------------------------------------
# Acomoda tus archivos
mkdir met_bedrooms
mkdir met_bedrooms/diff

mv met_hmm.bed met_bedrooms/
mv met_ali.bed met_bedrooms/
mv met_env.bed met_bedrooms/

mv met_hmm_diff.bed met_bedrooms/diff
mv met_ali_diff.bed met_bedrooms/diff
mv met_env_diff.bed met_bedrooms/diff

echo "[OK] La tabla domdb.fasta será la que utilices para tu alineamiento"
echo "[EXTRA] La tabla subdb.fasta serán las secuencias FASTA de tus claves contenidas en tu archivo no_duplicates!"

# Cambio de etiquetas
python taggin.py met_subdb.fasta met_domdb.fasta
echo "Cambio de etiquetas exitoso! Archivo final para pasar al alineamiento con etiquetas cambiadas será temporalmente denominada modified.fasta y su traducción está en el archivo tag.BED"
rm tags.txt



# -----------------[OMNIA] Obtenemos rangos de hmmsearch [OMNIA]------------------

# Y corta solo las columnas de número de acceso, inicio y fin de dominio
cut -f1,5,6 $2 | head -100 > omn_hmm.bed
cut -f1,7,8 $2 | head -100 > omn_ali.bed
cut -f1,9,10 $2 | head -100 > omn_env.bed
#awk -F'\t' 'FNR==NR{a[$1];next} $1 in a{count++} END{print "De un total de " FNR " secuencias en la lista A, " count " están contenidas en la lista B"}' catch_sort.temp acc.txt

echo "[OK]  Archivos BED creados para OMNIA"
# ------------------------------------------------------------------------
awk '{print $0 "\t" $3-$2}' omn_hmm.bed > omn_hmm_diff.bed
awk '{print $0 "\t" $3-$2}' omn_ali.bed > omn_ali_diff.bed
awk '{print $0 "\t" $3-$2}' omn_env.bed > omn_env_diff.bed
echo "Deltas de dominios BED creados [OK] "
# ------------------------------------------------------------------------
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
echo "[OK]  Sub-base de datos para Omnia cortada"
# ------------------------------------------------------------------------
# Acomoda tus archivos
mkdir omn_bedrooms
mkdir omn_bedrooms/diff

mv omn_hmm.bed omn_bedrooms/
mv omn_ali.bed omn_bedrooms/
mv omn_env.bed omn_bedrooms/

mv omn_hmm_diff.bed omn_bedrooms/diff
mv omn_ali_diff.bed omn_bedrooms/diff
mv omn_env_diff.bed omn_bedrooms/diff

echo "[OK] La tabla domdb.fasta será la que utilices para tu alineamiento"
echo "[EXTRA] La tabla subdb.fasta serán las secuencias FASTA de tus claves contenidas en tu archivo no_duplicates!"

#---------------------------Cambio de etiquetas---------------------------------------

python taggin.py omn_subdb.fasta omn_domdb.fasta
echo "Cambio de etiquetas exitoso! Archivo final para pasar al alineamiento con etiquetas cambiadas será temporalmente denominada modified.fasta y su traducción está en el archivo tag.BED"

rm tags.txt

# -------- Combina tus bases de datos -------------------
cat met_domdb.fasta omn_domdb.fasta > metomn_added.fasta