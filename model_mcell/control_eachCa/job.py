#!/usr/bin/python
#PBS -j oe
#PBS -t 1-100
#PBS -q neurobio
#PBS -l walltime=10:00:00

import os

## get array index
array_id = int(os.getenv('PBS_ARRAYID'))

i = int(os.getenv('I'))

## subjob to run
query = f'echo {i+array_id}'
print(query)

## submit job
# os.system(query)
