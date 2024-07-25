#!/usr/bin/env sh

# -----|Butterscotch|-----

echo $1;
echo "
Tabla de hmmsearch a procesar: $1
";
echo "
¡NOTA IMPORTANTE!

Este script esta diseñado para trabajar con tablas de hits (--domtblout) por dominio de HMMER y para la base de datos OMNIA (Todo registro disponible en el NCBI)!
";

# Quita encabezados y colas de archivo que empiecen con el caracter "#"
egrep -v "^#" $1 > a_noheadtail.temp;

# Reemplaza espacios múltiples por un solo tabulador
sed 's/[[:space:]]\{1,\}/\t/g' a_noheadtail.temp > b_rawfields.tab

# Formatea de modo que tengas todos los campos de la tabla bien delimitados.
cut -f1-22 b_rawfields.tab > data.temp;
cut -f23- b_rawfields.tab |  sed 's/\t/ /g' | sed 's/,/ /g' > description.temp;
paste data.temp description.temp > c_allfields.tab;

# Extraemos campos de interés. Consulta `Control Lists/col_index.md` para más información
cut -f1,3,4,7,16-21,23 c_allfields.tab > d_dom_fields.tab;

# Borramos intermedios
rm data.temp;
rm description.temp;

# Filtro de E-values: Solo los resultados con un e-value menor o igual a 0.0001 se conservan
awk '$4 <= 0.0001' d_dom_fields.tab > e_good_evalues.tab

# De los dominios, toma solo al primero. Esto solo se hace tomando el primer resultado.
awk '!a[$1]++' e_good_evalues.tab > f_1stdomeval.tab

echo "
---------------------------
||| Búsqueda finalizada |||
---------------------------

Encontraras tus listas en la carpeta de resultados


"
# Resultados importantes que pasan a la siguiente parte del proceso
mkdir resultados;

mv f_1stdomeval.tab resultados/;

#mv g_gtf_ordered.csv resultados/;
#mv h_no_duplicates.csv resultados/;
#mv h_frequencies.csv resultados/;
# Acomodamos listas de referencia y control

mkdir resultados/refctl_lsts;
mv a_noheadtail.temp resultados/refctl_lsts;
mv b_rawfields.tab resultados/refctl_lsts;
mv c_allfields.tab resultados/refctl_lsts;
mv d_dom_fields.tab resultados/refctl_lsts;
mv e_good_evalues.tab resultados/refctl_lsts;
