#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Argumentos
# Primero: El archivo uniques que sale de referenceXuniques.py o el archivo temporal de llamado itol_annotation.txt que salio de pos_tree.py

# Important imports
import sys
import pandas as pd

# Input file name
input_file = sys.argv[1]
#input_file = "/home/raulrosas/Documentos/IFC/repo/operaciones/one4all/caramel/for_rax_nocdhit/evolview/color_tree/cgchm_pretree/itool_annotation.txt"
print("Archivo utilizado:", input_file)

# Output file name
output_file = "ITOL_color_reference.txt"

# Create a dictionary to map values in the second column to the corresponding third column values
# Here we also add the color code for ITOL as needed, in this case for dataser_colorstrip
column_mapping = {
    "Mammalia": "#FF5733",
    "Actinopteri": "#47D147",
    "Amphibia": "#FFC300",
    "Anthozoa": "#33C7FF",
    "Arachnida": "#B266FF",
    "Ascidiacea": "#FF3366",
    "Aves": "#33FF8D",
    "Bivalvia": "#FF8533",
    "Branchiopoda":"#CC33FF",
    "Cephalopoda": "#33FFD6",
    "Ceratodontiformes": "#FF33A6",
    "Chondrichthyes": "#FFD733",
    "Chromadorea": "#33FF4D",
    "Cladistia": "#FF3366",
    "Gastropoda": "#33FFC0",
    "Hexanauplia": "#FF33A6",
    "Hydrozoa": "#FF5733",
    "Hyperoartia": "#33FF4D",
    "Insecta": "#FF8533",
    "Lepidosauria": "#33C7FF",
    "Leptocardii": "#47D147",
    "Malacostraca": "#FFC300",
    "Testudines": "#33FFD6",
    "Cestoda": "#fafa6e",
    "Clitellata": "#c4ec74",
    "Cnidaria": "#92dc7e",
    "Coelacanthiformes": "#64c987",
    "Collembola": "#39b48e",
    "Crinoidea": "#089f8f",
    "Crocodylia": "#00898a",
    "Demospongiae": "#08737f",
    "Echinoidea": "#215d6e",
    "Enteropneusta": "#2a4858",
    "Lingulata": "#fa7070",
    "Merostomata": "#b67032",
    "Priapulimorpha": "#9d6f26",
    "Thecostraca": "#856c1f",
    "Trichoplacidae": "#576320"
    # Add morre if needed
}

#Open the input and output files
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        # Split the line into columns based on whitespace (adjust as needed)
        columns = line.strip().split()

        # Check if there are at least two columns
        if len(columns) >= 2:
            value_in_second_column = columns[1]

            # Lookup the corresponding third column value in the dictionary
            third_column_value = column_mapping.get(value_in_second_column, "")

            # Append the third column value to the line and write it to the output file
            outfile.write(f"{line.strip()}\t{third_column_value}\n")
        else:
            # If there are less than two columns, just write the line as is
            outfile.write(line)

print("Primer procesado completo. Salida escrita a:", output_file)

extended_clade_file = "extended_clades.txt" # New file
extended_in_file = "ITOL_color_reference.txt" # Reference file from first mapping

# This is so you can simplify the clades to... simpler clades!
second_column_mapping = {
    "Mammalia": "Chordata",
    "Actinopteri": "Chordata",
    "Amphibia": "Chordata",
    "Anthozoa": "Cnidaria",
    "Arachnida": "Arthropoda",
    "Ascidiacea": "Chordata",
    "Aves": "Chordata",
    "Bivalvia": "Mollusca",
    "Branchiopoda":"Arthropoda",
    "Cephalopoda": "Mollusca",
    "Ceratodontiformes": "Chordata",
    "Chondrichthyes": "Chordata",
    "Chromadorea": "Nematoda",
    "Cladistia": "Chordata",
    "Gastropoda": "Mollusca",
    "Hexanauplia": "Arthropoda",
    "Hydrozoa": "Cnidaria",
    "Hyperoartia": "Chordata",
    "Insecta": "Arthropoda",
    "Lepidosauria": "Chordata",
    "Leptocardii": "Chordata",
    "Malacostraca": "Arthropoda",
    "Testudines": "Chordata",
    "Cestoda": "Otro",
    "Clitellata": "Otro",
    "Cnidaria": "Cnidaria",
    "Coelacanthiformes": "Chordata",
    "Collembola": "Arthropoda",
    "Crinoidea": "Otro",
    "Crocodylia": "Chordata",
    "Demospongiae": "Otro",
    "Echinoidea": "Otro",
    "Enteropneusta": "Otro",
    "Lingulata": "Otro",
    "Merostomata": "Arthropoda",
    "Priapulimorpha": "Otro",
    "Thecostraca": "Arthropoda",
    "Trichoplacidae": "Otro"
    # Add more if needed    
}

with open(extended_in_file, "r") as infile, open(extended_clade_file, "w") as outfile:
    for line in infile:
        reference_columns = line.strip().split()
        
        # Check if there are at least three columns
        if len(reference_columns) >= 3:
            clade_in_second_column = reference_columns[1]
            
            # Search for the corresponding extended column value in the dictionary
            extended_column_value = second_column_mapping.get(clade_in_second_column, "")
            
            # Append the extended column value to the line and write it to the output file
            outfile.write(f"{line.strip()}\t{extended_column_value}\n")
        else:
            # If there are less than 3 columns, write the line as is
            outfile.write(line)


simple_output_file = "extended_simple_clades.txt" # New file
long_extended_clades = "extended_clades.txt" # Reference file with 4 columns, from the second mapping

# This is so you can color the simpler clades!
third_column_mapping = {
    "Arthropoda":"#F7C1BB",
    "Chordata":"#885A5A",
    "Cnidaria":"#353A47",
    "Mollusca":"#84B082",
    "Nematoda":"#DC136C",
    "Otro": "#b5b5b5"
}

with open(long_extended_clades,"r") as infile, open(simple_output_file,"w") as outfile:
    for line in infile:
        simplified_columns = line.strip().split()

        # Check if there are at least 4 columns
        if len(simplified_columns) >= 4:
            clade_in_fourth_column = simplified_columns[3]

            # Search for the corresponding simplified column value in the dictionary
            simplified_column_value = third_column_mapping.get(clade_in_fourth_column,"")

            # Append the extended column value to the line and wirte it to the output file
            outfile.write(f"{line.strip()}\t{simplified_column_value}\n")
        else:
            # If there are less than 4 columns, write the line as is
            outfile.write(line)

print("Segundo procesado completo. Salida escrita a:", simple_output_file)

# Content for the ds_legend_label variable
source_file = "extended_simple_clades.txt"
pd_file = pd.read_csv(source_file, sep = "\t", header = None)
interest_column = pd_file.iloc[:,3]
unique_labels = sorted(interest_column.unique())
result_labels = '\t'.join(unique_labels) # Usable VAR

# Content count for colors, shapes and scales
elements_count = len(unique_labels)

# Content for the ds_legend_colors, assuming the main clades are the one in the third_column_mapping
# Arthtopoda, Chordata, Cnidaria, Mollusca, Nematoda and Other (6 total)
color_mapping = {
    1:["#F7C1BB"],
    2:["#F7C1BB","#885A5A"],
    3:["#F7C1BB","#885A5A","#353A47"],
    4:["#F7C1BB","#885A5A","#353A47","#84B082"],
    5:["#F7C1BB","#885A5A","#353A47","#84B082","#DC136C"],
    6:["#F7C1BB","#885A5A","#353A47","#84B082","#DC136C", "#b5b5b5"],
    7:["#F7C1BB","#885A5A","#353A47","#84B082","#DC136C", "#b5b5b5","#d60cfa"],
}

label_hex_col = color_mapping.get(elements_count,['#000000']*elements_count)
hex_line = '\t'.join(label_hex_col) # USABLE VAR

# Content for ds_legend_shapes
shape_line = '\t'.join(['1']*elements_count) # USABLE VAR

#Content for ds_legend_shape_scales
scale_line = '\t'.join(['1']*elements_count) # USABLE VAR

# File headers for DATASET_COLORSTRIP format, outside the branches

# First: Obligatory stuff, you HAVE to change the separator according to your data. Then LABEL, COLOR can be whatever you want.
ds_colors_header = "DATASET_COLORSTRIP\nSEPARATOR TAB\nDATASET_LABEL\tSimplified_Clades\nCOLOR\t#ffff00\n"

#Second: This will affect the legend atop your tree, particulary it's position and name/title
ds_legend_header = "LEGEND_TITLE\tCOLORED_CLADES\nLEGEND_POSITION_X\t180\nLEGEND_POSITION_Y\t100\nLEGEND_HORIZONTAL\t0\n"

# Third: Shapes for your legend's figures. You can use either one from 1-5, or use just one type, up to you.
ds_legend_shapes = "LEGEND_SHAPES\t"+ shape_line + "\n"

# Fourth: Colors for your legend's figures. This HAVE to match the ones you use in your actual data so it is useful of something
ds_legend_colors = "LEGEND_COLORS\t" + hex_line + "\n"

#Fifth: Labels for your legend's figure. This HAVE to match your actual data so you can tell them apart
ds_legend_lables = "LEGEND_LABELS\t" + result_labels + '\n'

# Sixth: Scale/size of the shapes, keeping it in one is good enough.
ds_legend_shape_scales = "LEGEND_SHAPE_SCALES\t" + scale_line + "\n"

# Final: Delimiter for actual data
ds_data_delimiter_head = "DATA\n"

# Actual DATA writing
simplified_output_file = "ITOL_simplified_color_dataset.txt" # New file

with open(simple_output_file, "r") as infile, open(simplified_output_file,"w") as outfile:
    outfile.write(ds_colors_header)
    outfile.write(ds_legend_header)
    outfile.write(ds_legend_shapes)
    outfile.write(ds_legend_colors)
    outfile.write(ds_legend_lables)
    outfile.write(ds_legend_shape_scales)
    outfile.write(ds_data_delimiter_head)
    for line in infile:
        columns = line.strip().split()
        if len(columns) >= 4:
            cod = columns[0]
            color = columns[4]
            sim_clade = columns[3]
            outfile.write(f"{cod}\t{color}\t{sim_clade}\n")
print("Tercer procesado completo. Salida escrita a:", simplified_output_file)

# Creating CHN colored datasets

second_input = "ITOL_simplified_color_dataset.txt"
chn_dataframe = pd.read_csv(second_input, sep = "\t", header= None, skiprows=13,names = ["COD","HEX","Clade"])
chn_dataframe["CEP"] = [""]*len(chn_dataframe)
chn_dataframe.loc[chn_dataframe['COD'].str.contains('C'), 'CEP'] = "#B5D5C5" #light green
chn_dataframe.loc[chn_dataframe['COD'].str.contains('H'), 'CEP'] = "#B08BBB" #pastel purple
chn_dataframe.loc[chn_dataframe['COD'].str.contains('N'), 'CEP'] = "#ECA869" #pastel orange
chn_dataframe.to_csv('CHN_noheader.txt', sep = '\t', header = None, index = None)

# ITOL colored dataset header
chn_header_info = "DATASET_COLORSTRIP\nSEPARATOR TAB\nDATASET_LABEL\tC|H|N DISTRIBUTION\nCOLOR\t#F5F5DC\n"
chn_header_legend = "LEGEND_TITLE\tCOLORED_PROTEINS\nLEGEND_POSITION_X\t180\nLEGEND_POSITION_Y\t170\nLEGEND_HORIZONTAL\t0\n"
chn_header_shapes = "LEGEND_SHAPES\t2\t2\t2\n"
chn_header_colors = "LEGEND_COLORS\t#B5D5C5\t#B08BBB\t#ECA869\n"
chn_header_labels = "LEGEND_LABELS\tQuitina\tHialuronano\tS/N\n"
chn_header_scales = "LEGEND_SHAPE_SCALES\t1\t1\t1\n"
chn_header_data_delimiter = "DATA\n"

# Actual data writing
chn_in = "CHN_noheader.txt"
chn_out = "CHN_with_header.txt"
with open(chn_in,"r") as input, open(chn_out,"w") as output:
    output.write(chn_header_info)
    output.write(chn_header_legend)
    output.write(chn_header_shapes)
    output.write(chn_header_colors)
    output.write(chn_header_labels)
    output.write(chn_header_scales)
    output.write(chn_header_data_delimiter)
    for line in input:
        columns = line.strip().split()
        if len(columns)>= 4:
            cod = columns[0]
            color = columns[3]
            output.write(f"{cod}\t{color}\n")

print("Fin del procesado")
print("Archivo para colorear por datasets de clados simplificados:", simplified_output_file)
print("Archivo para colorear por datasets de proteínas C|H|NA:",chn_out)