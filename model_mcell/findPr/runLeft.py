#!/usr/bin/python3

from itertools import product
from multiprocessing import Pool
from tqdm import tqdm
import os, sys
from time import sleep
import numpy as np



dataPath = "/media/nishant/4tb/output/MFB/findPr/"
resultPath = "/home/nishant/lab/results/MFB/findPr/"

dirs = os.listdir(dataPath)
#print(dirs)


def missingSeeds(dirs, dataPath):
	jobInfo = []
	totSet = set(range(1,41))
	for d in dirs:
	    seedDirs = os.listdir(os.path.join(dataPath, d))
	    if len(seedDirs) < 40: 
	        seeds = set([int(a.split('_')[1]) for a in seedDirs])
	        tbd = totSet - seeds
	        
	        fname = 'xmain_'+d+'.mdl'
	        #print(tbd)
	        
	        for seed in tbd:
	            jobInfo.append([fname, seed])

	return jobInfo


def emptyFiles(dirs, dataPath):
	jobInfo = []
	totSet = set(range(1,41))
	for d in dirs:
	    seedDirs = os.listdir(os.path.join(dataPath, d))
	    for seeddir in seedDirs:
	        fsize = os.path.getsize(os.path.join(dataPath,d,f'{seeddir}/dat/ca.dat'))
	        if fsize < 100:
	            #print(fsize, seeddir, d)
	            fname = 'xmain_'+d+'.mdl'
	            seed = int(seeddir.split('_')[1])
	            jobInfo.append([fname, seed])

	return jobInfo


def runmdl(fname, seed):
	loc = '/home/nishant/lab/MFB/mcell/findPr'
	query = f"mcell32 {os.path.join(loc,fname)} -seed {seed} -logfreq 5000"
	print(query)
	os.system(query)



#jobInfo = missingSeeds(dirs, dataPath)
jobInfo = emptyFiles(dirs, dataPath)
for ji in jobInfo:
	print(ji)

print(len(jobInfo))

p = Pool(30)
res = p.starmap(runmdl, jobInfo)
print(res)


