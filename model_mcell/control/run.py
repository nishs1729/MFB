import os, sys
import numpy as np
import pickle as pk
from random import randint
from itertools import *
import scipy.interpolate as itp
from multiprocessing import Pool, Process

sys.path.append('/home/nishant/lab/MFB/scripts')
sys.path.append('/home/nishant/lab/MFB/steps')
sys.path.append('/home/nishant/lab/scripts')
from analysis import *
from peaks import *

dataPath = "/media/nishant/4tb/output/MFB/control/"
resultPath = "/home/nishant/lab/MFB/results/control/"

#dirs = [a for a in getDirs(resultPath, sstr='nVDCC') if "ISI_50" in a]
dirs = [a for a in getDirs(dataPath, sstr='nVDCC') if "ISI_20" in a]

tempdirs = np.array(dirs)[[0,25,26]]


from MFB_model import *
mdl, sim, r = get_MFB_model()

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

def getVesRel(d, RRP, resultPath, fname='CaConc.dat', trials=2000, pools=False):
    nAZ = int(getSimInfo(d, 'nAZ'))
    
    CaFile = os.path.join(resultPath, d, fname)
    CaData = np.genfromtxt(CaFile, unpack=True) # in uM
    
    if pools:
        p = Pool(pools)
    else:
        p = Pool()
        
    vesData = {}
    desc = str([int(a) for a in re.findall(r'\d+', d)[:-1]])
    for iCa in tq(range(1,nAZ+1), desc=desc):
        info = product([CaData[(0,iCa),:]], [RRP]*trials)
        data = np.array(p.starmap(runAZTrials, info))
        
        vesSync  = [a['sync'] for a in data[:,0]]
        vesAsync = [a['async'] for a in data[:,0]]
        vesSpont = [a['spont'] for a in data[:,0]]
        vesData.update({f'AZ{iCa}': {'sync': vesSync, 'async':vesAsync, 'spont':vesSpont}})
        
        resAZ = data[:,1]
        AZstates = np.mean(resAZ, axis=0)
        fAZ = os.path.join(resultPath, d, f'AZ_{iCa}.dat')
        AZdata = np.hstack((np.array([CaData[0]]).T, AZstates))
        np.savetxt(fAZ, AZdata, fmt=['%0.5f']+['%0.4f']*18, delimiter="\t")
        
    #print(vesData)
    p.close()
    return vesData


for d in tq(tempdirs[:]):
    try:
        nVDCC, dVDCC, nAZ, RRP = [int(getSimInfo(d, key)) for key in ['nVDCC', 'dVDCC', 'nAZ', 'RRP']]
        #print(nVDCC, dVDCC, nAZ, RRP)
        
        vesData = getVesRel(d, RRP=RRP, resultPath=resultPath, 
                            trials=2000, pools=False)
        with open(os.path.join(resultPath, d, 'vesData.dat'),"wb") as outfile:
            pk.dump(vesData, outfile)
            
        relStat(d, resultPath, resample=1000)
    except:
        print(f'Error in {d}')
