#!/usr/bin/env python
# coding: utf-8

import sys

def process_fasta(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if line.startswith('>'):  # Check if the line is a header line
                # Split the header line by whitespace and keep the first part (accession number)
                accession_number = line.split('.')[0][1:]
                # Write the modified header to the output file
                f_out.write(f'>{accession_number}\n')
            else:
                # Write sequence lines as they are to the output file
                f_out.write(line)

#input_file = sys.argv[1]
input_file = 'domdb.fasta'
output_file = 'modified_acc_taggd.fasta'
