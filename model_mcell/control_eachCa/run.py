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

dataPath = "/media/nishant/4tb/output/MFB/control_eachCa/"
resultPath = "/home/nishant/lab/MFB/results/control_eachCa/"

dirs = [a for a in getDirs(resultPath, sstr='nVDCC') if "ISI_20" in a]
#dirs = [a for a in getDirs(dataPath, sstr='nVDCC') if "ISI_20" in a]

tempdirs = np.array(dirs)[8:9]

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

def getVesRel(d, resultPath, trials=2000, pools=False):
    nAZ = int(getSimInfo(d, 'nAZ'))
    RRP = int(getSimInfo(d, 'RRP'))
    
    #sCaData, aCaData = [], []
    for naz in range(1,nAZ+1):
        CaFile = os.path.join(resultPath, d, f'CaConc_AZ_{naz}.dat')
        temp = np.genfromtxt(CaFile, unpack=True) # in uM
        if naz == 1:
            sCaData = temp[[0,1]]
            aCaData = temp[[0,2]]
        else:
            sCaData = np.append(sCaData, [temp[1]], axis=0)
            aCaData = np.append(aCaData, [temp[2]], axis=0)
            
    #print(sCaData.shape, aCaData.shape)

    if pools: p = Pool(pools)
    else: p = Pool()
        
    svesData, avesData = {}, {}
    desc = 's_'+'_'.join([a for a in re.findall(r'\d+', d)[:-1]])
    for iCa in tq(range(1,nAZ+1), desc=desc):
        info = product([sCaData[(0,iCa),:]], [RRP]*trials)
        data = np.array(p.starmap(runAZTrials, info))
        
        vesSync  = [a['sync'] for a in data[:,0]]
        vesAsync = [a['async'] for a in data[:,0]]
        vesSpont = [a['spont'] for a in data[:,0]]
        svesData.update({f'AZ{iCa}': {'sync': vesSync, 'async':vesAsync, 'spont':vesSpont}})
        
        resAZ = data[:,1]
        AZstates = np.mean(resAZ, axis=0)
        fAZ = os.path.join(resultPath, d, f'sAZ_{iCa}.dat')
        AZdata = np.hstack((np.array([sCaData[0]]).T, AZstates))
        np.savetxt(fAZ, AZdata, fmt=['%0.5f']+['%0.4f']*18, delimiter="\t")
    
    desc = 'a_'+'_'.join([a for a in re.findall(r'\d+', d)[:-1]])
    for iCa in tq(range(1,nAZ+1), desc=desc):
        info = product([aCaData[(0,iCa),:]], [RRP]*trials)
        data = np.array(p.starmap(runAZTrials, info))
        
        vesSync  = [a['sync'] for a in data[:,0]]
        vesAsync = [a['async'] for a in data[:,0]]
        vesSpont = [a['spont'] for a in data[:,0]]
        avesData.update({f'AZ{iCa}': {'sync': vesSync, 'async':vesAsync, 'spont':vesSpont}})
        
        resAZ = data[:,1]
        AZstates = np.mean(resAZ, axis=0)
        fAZ = os.path.join(resultPath, d, f'aAZ_{iCa}.dat')
        AZdata = np.hstack((np.array([aCaData[0]]).T, AZstates))
        np.savetxt(fAZ, AZdata, fmt=['%0.5f']+['%0.4f']*18, delimiter="\t")
    
    
    #print(vesData)
    p.close()
    return svesData, avesData
   

#'''
for d in tq(tempdirs[:]):
    #try:
    svesData, avesData = getVesRel(d, resultPath=resultPath, trials=2000, pools=38)
    with open(os.path.join(resultPath, d, 'svesData.dat'), "wb") as outfile:
        pk.dump(svesData, outfile)

    relStat(d, resultPath, inf='svesData.dat', resultf='sresult.dat')

    with open(os.path.join(resultPath, d, 'avesData.dat'), "wb") as outfile:
        pk.dump(avesData, outfile)

    relStat(d, resultPath, inf='avesData.dat', resultf='aresult.dat')
#'''

