#!/usr/bin/python3

from itertools import product
from subprocess import check_output
from multiprocessing import Pool
from tqdm import tqdm
import os, sys
from time import sleep

nPool = 10
seeds = 50

nVDCC = [7]
dVDCC = [100]
nAZ   = [7]
ISI   = range(70, 81, 10)
nAP   = [6]

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
