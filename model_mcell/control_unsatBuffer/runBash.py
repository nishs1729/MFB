#!/usr/bin/python3

from itertools import product
from subprocess import check_output
from multiprocessing import Pool
from tqdm import tqdm
import os, sys
from time import sleep

nPool = 35
seeds = 700
sseed = 301

'''nVDCC = [7,9]
dVDCC = [100]
nAZ   = [7]
ISI   = range(20, 101, 10)
nAP   = [6]'''

mdlPath = os.getcwd()
files = [[a, os.path.join(mdlPath, a)] for a in os.listdir(mdlPath) \
				if os.path.isfile(os.path.join(mdlPath, a)) and '9_dVDCC_100_nAZ_9_RRP_10_ISI_20_nAP_10' in a]

print(len(files))

def simulation(query):
    #print(query)
    os.system(query)

p=Pool(nPool)
for file in files[:]:
	query = f"mcell32 {file[0]} -seed "
	queries = [f"{query} {seed} -logfreq 50000" for seed in range(sseed,sseed+seeds)]

	#print(f"File: {mdlFile}")
	#for q in queries: print(q)

	res=p.map(simulation, queries)

'''
for nvdcc, dvdcc, naz, isi, nap in product(nVDCC, dVDCC, nAZ, ISI, nAP):
	mdlFile = f"xmain_nVDCC_{nvdcc}_dVDCC_{dvdcc}_nAZ_{naz}_ISI_{isi}_nAP_{nap}.mdl"
	query = f"mcell32 {mdlFile} -seed "
	queries = [query+str(seed)+" -logfreq 10000" for seed in range(1,1+seeds)]

	#print(f"File: {mdlFile}")
	res=p.map(simulation, queries)'''

p.close()
