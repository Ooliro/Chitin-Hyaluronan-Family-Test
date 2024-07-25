#!/usr/bin/env python3

# Tercera parte: agrega la columa de clados al final de tu archivo objetivo

#arg1 = Archivo de frecuencias al que se le va a anexar la columna de clados

import sys

# Carga archivos desde la linea de comandos
countfile = sys.argv[1]  # Tabla de frecuencias con Spp

## Inicia el diccionario y acomoda las columnas
taxdict1 = {}

with open('tax_clades.tab') as infile:
    for line in infile:
        line = line.strip()
        if line == "":
            continue
        clade, spp = line.split("\t")
        taxdict1[spp] = clade

## Prepara los archivos de salida

outfilename = "clades_n_freqs.tab"
outfile = open(outfilename, "w")

## Con el diccionario, busca coincidencias dentro del archivo de frecuencias y agrega el clado al final
with open(countfile) as infile:
    for line in infile:
        line = line.strip()
        if line == "":
            continue
        data = line.split("\t")
        if len(data) != 3:
            continue
        spp, taxid, freq = line.split("\t")
        newline = "\t".join([taxdict1[spp], spp, taxid, freq]) + "\n"
        outfile.write(newline)

outfile.close()

print("Listo!")
