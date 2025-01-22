import os, sys
import numpy as np
import pickle as pk
from random import randint
from itertools import product, chain
import scipy.interpolate as itp
from multiprocessing import Pool, Process

sys.path.append('/home/nishant/lab/MFB/scripts')
sys.path.append('/home/nishant/lab/MFB/steps')
sys.path.append('/home/nishant/lab/scripts')
from analysis import *
from peaks import *
from misc import *

resultPath = "/home/nishant/lab/MFB/results/findPr/"
fname = "ca.dat" 

from MFB_model import *
mdl, sim, r = get_MFB_model()

def runAZTrials(CaData, RRPs):
    vesData = []
    for RRP in RRPs:
        resAZ, vesRel = simAZ(CaData[0], CaData[1], sim, r, RRP=RRP)
        vesRelTot = np.sum(vesRel, axis=1)
        pks = detect_peaks(vesRelTot, edge='rising', show=False)
        vesData.append(list(CaData[0,pks]))
    
    return vesData
    
    
def getVesRel(d, RRPs, resultPath, fname='CaConc.dat', trials=2000):
    nAZ = int(d.split('_')[-1])
    rrps = len(RRPs)
    
    CaFile = os.path.join(resultPath, d, fname)
    CaData = np.genfromtxt(CaFile, unpack=True) # in uM

    p = Pool(38)
    vesRelTimes = []
    for iCa in tq(range(1,nAZ+1), desc=d):
        
        info = product([CaData[(0,iCa),:]], [RRPs]*trials)
        #print(list(info))
        vesRelTime = p.starmap(runAZTrials, info)
        vesRelTime = [[vesRelTime[i][j] for i in range(trials)] for j in range(rrps)]
        vesRelTimes.append(vesRelTime)

    p.close()
    p.join()
    
    vesRelTimes = [[list(chain(*[vesRelTimes[i][j][k] for i in range(nAZ)])) for k in range(trials)] for j in range(rrps)]
    vesData = {}
    for RRP,v in zip(RRPs, vesRelTimes):
        vesData.update({str(RRP): list(v)})
    
    return vesData

nVDCC = [5,9]
dVDCC = range(220, 221, 20)
nAZ = range(17,30,2)
tempdirs = []
for vdcc, dvdcc, naz in product(nVDCC, dVDCC, nAZ):
    tempdirs.append(f'nVDCC_{vdcc}_dVDCC_{dvdcc}_nAZ_{naz}')
#print(tempdirs)

for d in tq(tempdirs):
    try:
        #print(d)
    	vesData = getVesRel(d, RRPs=range(5,41,5), resultPath=resultPath, trials=500)
    	with open(os.path.join(resultPath, d, 'vesData.dat'),"wb") as outfile:
    	    pk.dump(vesData, outfile)
    
    except: print(f'Error in {d}')
