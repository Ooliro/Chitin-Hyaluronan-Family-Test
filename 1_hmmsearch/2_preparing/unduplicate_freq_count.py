#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import sys 

archivo = sys.argv[1]
data = pd.read_table(archivo, names=['GenName', 'TransID', 'GenID', 'ProtID', 'TaxID', 'Spp'],
                    na_values=True,
                    dtype={'TaxID':object, 'GenID':object})

#data = pd.read_table("/home/raulrosas/Documentos/IFC/lab/eden/cgch_ops/maze/resultados/gtf_ordered.csv",
#                    names=['GenName', 'TransID', 'GenID', 'ProtID', 'TaxID', 'Spp'],
#                    na_values=True,
#                    dtype={'TaxID':object, 'GenID':object})
#print(data.head(n=10))



#Inicio
data_inicial=len(data)
print("Tus resultados iniciales totales son:", data_inicial)

#Objetivo A: Filtrar por GenID
pure_data = data.drop_duplicates(subset='GenID',keep='first')
data_final = len(pure_data)
print("Tus resultados finales son:", data_final)

#Objetivo B: Cuenta frecuencias de especies unicas
count_uniqs=pure_data.groupby(['Spp', 'TaxID']).size().sort_values(ascending=False)
uniq_len=len(count_uniqs)
print("Numero de especies unicas:", uniq_len)

#Final y escritura
pure_data.to_csv('h_no_duplicates.csv', index=False, header=False, sep='\t')
count_uniqs.to_csv('h_frequencies.csv',header=None, sep='\t')
