#!/usr/bin/python
#PBS -j oe
#PBS -t 1-100

import os

# get seed value from array index
seed = os.getenv('PBS_ARRAYID')

mcellFile = os.getenv('I')

# define bash command
query = '/home/nishant/mcell32 '+ mcellFile +' -seed '+ seed
print(query)

# run bash command
os.system(query)