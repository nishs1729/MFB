import os, sys
import numpy as np
import pickle as pk
from random import randint
from itertools import product, chain
import scipy.interpolate as itp
from multiprocessing import Pool, Process

sys.path.append('/home/nishant/MFB/scripts')
sys.path.append('/home/nishant/MFB/steps')
sys.path.append('/home/nishant/scripts')
from analysis import *
from peaks import *
from misc import *

resultPath = "/home/nishant/results/MFB/findPr/"
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
    
    
def getVesRel(dir, RRPs, resultPath, fname='CaConc.dat', trials=2000):
    nAZ = int(dir.split('_')[-1])
    rrps = len(RRPs)
    
    CaFile = os.path.join(resultPath, dir, fname)
    CaData = np.genfromtxt(CaFile, unpack=True) # in uM

    p = Pool(35)
    vesRelTimes = []
    for iCa in tqdm(range(1,nAZ+1), desc=dir):
        
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

vdccs = [1,2,3,4,5,6,7,8,9]
dvdccs = [90]
nazs = list(range(7,30)) # 7 has been mising... gotta do those 7s !!!
tempdirs = []
for vdcc, dvdcc, naz in product(vdccs, dvdccs, nazs):
    tempdirs.append(f'nVDCC_{vdcc}_dVDCC_{dvdcc}_nAZ_{naz}')
#print(tempdirs)

for dir in tqdm(tempdirs):
    try:
        #print(dir)
        vesData = getVesRel(dir, RRPs=range(5,41,5), resultPath=resultPath, trials=2000)
        with open(os.path.join(resultPath, dir, 'vesData.dat'),"wb") as outfile:
            pk.dump(vesData, outfile)
    except:
        print(f'Error in {dir}')

