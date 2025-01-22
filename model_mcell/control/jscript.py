#!/usr/bin/python
#PBS -p 1 
#PBS -j oe
#PBS -J 1-300

import os

# get seed value from array index
seed = os.getenv('PBS_ARRAY_INDEX')

mcellFile = os.getenv('I')

# define bash command
query = '/apps/bin/mcell '+ mcellFile +' -seed '+ seed
#print query

# run bash command
os.system(query)