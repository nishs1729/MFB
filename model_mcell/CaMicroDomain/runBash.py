#!/usr/bin/python3

from itertools import product
from subprocess import check_output
from multiprocessing import Pool
from tqdm import tqdm
import os, sys
from time import sleep

nPool = 14
seeds = 300

nVDCC = [9]
dVDCC = [60, 120]
nAZ   = [19]
ISI   = [20]
nAP   = [10]

def simulation(query):
    #print(query)
    os.system(query)
    #check_output(query, shell=True)

p=Pool(nPool)
for nvdcc, dvdcc, naz, isi, nap in product(nVDCC, dVDCC, nAZ, ISI, nAP):
	mdlFile = f"xmain_nVDCC_{nvdcc}_dVDCC_{dvdcc}_nAZ_{naz}_ISI_{isi}_nAP_{nap}.mdl"
	query = f"mcell32 {mdlFile} -seed "
	queries = [query+str(seed)+" -logfreq 10000" for seed in range(1,1+seeds)]

	#print(f"File: {mdlFile}")
	res=p.map(simulation, queries)
