import numpy as np
import pickle as pk
import os, sys, shutil
from random import randint
import scipy.interpolate as itp
from itertools import product, chain
from multiprocessing import Pool, Process

sys.path.append('/home/nishant/lab/MFB/scripts')
sys.path.append('/home/nishant/lab/MFB/steps')
from peaks import *
from analysis import *

dataPath = "/media/nishant/4tb/output/MFB/control/"
resultPath = "/home/nishant/lab/MFB/results/syt7KO/"

syt7KO = 'syt7KO'

#dirs = [a for a in getDirs(dataPath, sstr='nVDCC') if "ISI_20" in a]
#tempdirs = np.array(dirs)

setupLoc = '/home/nishant/lab/MFB/mcell'
setup = np.genfromtxt(os.path.join(setupLoc, 'controls.dat'), usecols=(1,2,3,4,6), dtype='int')

tempdirs = []
for s in setup:
    naz   = s[2]
    dvdcc = s[1]
    rrp   = s[3]
    nvdcc = s[0]
    done  = s[4]

    nap = 10
    ISI = [20]
    
    if not done:
        for isi in ISI:
            f = f"nVDCC_{nvdcc}_dVDCC_{dvdcc}_nAZ_{naz}_RRP_{rrp}_ISI_{isi}_nAP_{nap}"
            tempdirs.append(f)
            
tempdirs = np.array(tempdirs)
print(tempdirs)

from MFB_model import *
mdl, sim, r = get_MFB_model(syt7KO=syt7KO)

def runAZTrials(CaData, RRP):
    vesData = {}

    resAZ, vesRel = simAZ(CaData[0], CaData[1], sim, r, RRP=RRP)
    vesRelSync  = np.sum(vesRel[:,:3], axis=1)
    vesRelAsync = np.sum(vesRel[:,3:-2], axis=1)
    vesRelSpont  = vesRel[:,-1]

    vesRelTot = np.sum(vesRel, axis=1)
    #print(vesRelSync, vesRelAsync, vesRelSpont)

    pksSync = detect_peaks(vesRelSync, edge='rising', show=False)
    pksAsync = detect_peaks(vesRelAsync, edge='rising', show=False)
    pksSpont = detect_peaks(vesRelSpont, edge='rising', show=False)

    vesData.update({'sync' : list(CaData[0,pksSync])})
    vesData.update({'async': list(CaData[0,pksAsync])})
    vesData.update({'spont': list(CaData[0,pksSpont])})

    return vesData, resAZ


def getVesRel(d, resultPath, trials=2000, pools=False):
    nAZ = int(getSimInfo(d, 'nAZ'))
    RRP = int(getSimInfo(d, 'RRP'))
    
    for naz in range(1,nAZ+1):
        CaFile = os.path.join(resultPath, d, f'CaConc_AZ_{naz}.dat')
        temp = np.genfromtxt(CaFile, usecols=(0,2), unpack=True) # in uM
        #print(temp.shape)
        if naz == 1:
            CaData = temp
        else:
            CaData = np.append(CaData, [temp[1]], axis=0)

    if pools: p = Pool(pools)
    else: p = Pool()
        
    vesData = {}
    desc = '_'.join([a for a in re.findall(r'\d+', d)[:-1]])
    for iCa in tq(range(1,nAZ+1), desc=desc):
        info = product([CaData[(0,iCa),:]], [RRP]*trials)
        data = np.array(p.starmap(runAZTrials, info))
        
        vesSync  = [a['sync'] for a in data[:,0]]
        vesAsync = [a['async'] for a in data[:,0]]
        vesSpont = [a['spont'] for a in data[:,0]]
        vesData.update({f'AZ{iCa}': {'sync': vesSync, 'async':vesAsync, 'spont':vesSpont}})
        
        resAZ = data[:,1]
        AZstates = np.mean(resAZ, axis=0)
        fAZ = os.path.join(resultPath, d, f'aAZ_{iCa}.dat')
        AZdata = np.hstack((np.array([CaData[0]]).T, AZstates))
        np.savetxt(fAZ, AZdata, fmt=['%0.5f']+['%0.4f']*18, delimiter="\t")
    
    
    #print(vesData)
    p.close()
    return vesData
    
#'''
for d in tq(tempdirs[:]):
    #try:
    vesData = getVesRel(d, resultPath=resultPath, trials=2000, pools=False)
    with open(os.path.join(resultPath, d, 'vesData.dat'), "wb") as outfile:
        pk.dump(vesData, outfile)

    relStat(d, resultPath)
    #except: print(f'Error in {d}')
#'''