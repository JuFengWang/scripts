#!/usr/bin/env python3
import sys
import tempfile
# usage: python agp2assembly.py assembly.cleaned.fasta.fai scaffolds_FINAL.agp salsa.assembly

a_file_name = sys.argv[1]
b_file_name = sys.argv[2]
c_file_name = sys.argv[3]

with open(a_file_name, 'r') as a_file, open(b_file_name, 'r') as b_file:
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
        for a, line in enumerate(a_file, start=1):
            col1, col2 = line.split('\t')[0], line.split('\t')[1]
            tmp_file.write(f'>{col1} {a} {col2}\n')
        
        for b, line in enumerate(b_file, start=1):
            b1, b6, b9 = line.split('\t')[0], line.split('\t')[5], line.split('\t')[8]
            a_file.seek(0)
            for a, line in enumerate(a_file, start=1):
                col1, col2 = line.split('\t')[0], line.split('\t')[1]
                if b6 == col1:
                    a = -a if b9.strip() == '-' else a
                    tmp_file.write(f'{b1} {a}\n')
                    
        tmp_file.seek(0)
        with open(c_file_name, 'w') as c_file:
            b1_dict = {}
            for line in tmp_file:
                if line.startswith('>'):
                    c_file.write(line)
                else:
                    b1, a = line.split()
                    if b1 in b1_dict:
                        b1_dict[b1].append(a)
                    else:
                        b1_dict[b1] = [a]
            for b1 in sorted(b1_dict.keys(), key=lambda x: int(x.split("_")[1])):
                alist = b1_dict[b1] 
                c_file.write(f'{" ".join(alist)}\n')

a_file.close()
b_file.close()
c_file.close()
tmp_file.close()
