#!/usr/bin/python3

from itertools import product
from subprocess import check_output
from multiprocessing import Pool
from time import sleep
from tqdm import tqdm
import os, sys

nPool = 34 
seeds = 100

nVDCC = range(7,8)
dVDCC = [130]
nAZ = list(range(26,30))

def simulation(query):
    #print(query)
    os.system(query)
    #check_output(query, shell=True)


p=Pool(nPool)
for nv, dv, naz in tqdm(list(product(nVDCC, dVDCC, nAZ))):
	mdlFile = f"xmain_nVDCC_{nv}_dVDCC_{dv}_nAZ_{naz}.mdl"
	query = f"mcell32 {mdlFile} -seed "
	queries = [query+str(seed)+" -logfreq 5000" for seed in range(1,1+seeds)]

	#print(f"File: {mdlFile}")
	res=p.map(simulation, queries)

#print(len(list(product(nVDCC, dVDCC, nAZ))))
