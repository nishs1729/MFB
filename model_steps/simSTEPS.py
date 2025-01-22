import os, sys
import numpy as np
import pickle as pk
from random import randint
# from itertools import product, chain
# import scipy.interpolate as itp
from multiprocessing import Pool

sys.path.append('../scripts')
sys.path.append('../steps')
from analysis import *
from peaks import *
from misc import *

simType = 'control'
resultPath = os.path.join("../results/", simType)

siminfo = []
with open('newsims', 'r') as nf:
	for line in nf:
		siminfo.append([int(a) for a in line.split(' ')])
# print(siminfo, len(siminfo))


dirs = []
# for nVDCC, dVDCC, nAZ in product(nvdcc, dvdcc, naz):
for nVDCC, dVDCC, nAZ, RRP in siminfo:
    f = "nVDCC_" + str(nVDCC) + "_dVDCC_" + str(dVDCC) + "_nAZ_" + str(nAZ) + "_RRP_" + str(RRP) + "_ISI_20_nAP_10"
    dirs.append(f)

# for i,d in enumerate(dirs):
#     print(i, d)

# dd = []
# for i in [15,14,13,12,11,9,8,7,6,5,4,3,2,1]:
#     dd = dd + [d for d in dirs if f'nVDCC_{i}_' in d]


# dd = [d for d in dd if 'nAZ_31' not in d]
# dd = [d for d in dd if 'nAZ_33' not in d]
# dd = [d for d in dd if 'nAZ_35' not in d]

dd = [d for d in dirs if 'nAZ_35' in d][-22:]
tempdirs = dd 

for i,d in enumerate(tempdirs):
    print(i, d)

from MFB_model import *
mdl, sim, r = get_MFB_model()

def runAZTrials(CaData, RRPs):
    vesData = []
    resAZs = []
    # print(CaData[0], CaData[1], RRPs)
    for RRP in RRPs:
        # resCa, resAZ, vesRel = simAZ(CaData[0], CaData[1], sim, r, RRP=RRP)
        resAZ, vesRel = simAZ(CaData[0], CaData[1], sim, r, RRP=RRP)
        vesRelTot = np.sum(vesRel, axis=1)
        pks = detect_peaks(vesRelTot, edge='rising', show=False)
        vesData.append(list(CaData[0,pks]))
        resAZs.append(resAZ)
    
    return [vesData, resAZs]

def getVesRel(dir, RRPs, resultPath, fname='CaConc.dat', trials=2000):
    nAZ = int(getSimInfo(dir, 'nAZ'))
    rrps = len(RRPs)
    
    CaFile = os.path.join(resultPath, dir, fname)
    CaData = np.genfromtxt(CaFile, unpack=True) # in uM
    
    p = Pool(38)
    vesRelTimes = []
    for iCa in tq(range(1,nAZ+1), desc=dir):
    # for iCa in range(1,nAZ+1):
        
        info = product([CaData[(0,iCa),:]], [RRPs]*trials)
        # print(list(info)[0])
        vesRelTime = np.array(p.starmap(runAZTrials, info), dtype=object)
        # vesRelTime = runAZTrials(CaData[(0,iCa),:], RRPs)

        # print(vesRelTime[:,0])
        AZstates = vesRelTime[:,1]
        vesRelTime = vesRelTime[:,0]
        vesRelTime = [[vesRelTime[i][j] for i in range(trials)] for j in range(rrps)]
        vesRelTimes.append(vesRelTime)
        #print(vesRelTime[:,1])

        AZstates = np.mean(AZstates, axis=0)

        #print(AZstates[0])
        #print(np.vstack((CaData[0,],AZstates[0])))
    
        for i,rrp in enumerate(RRPs):
            fAZ = os.path.join(resultPath, dir, f'AZ_{iCa}_RRP_{rrp}.dat')
            AZdata = np.hstack((np.array([CaData[0]]).T, AZstates[i]))
            np.savetxt(fAZ, AZdata, fmt=['%0.5f']+['%0.3f']*18, delimiter="\t")

    p.close()
    p.join()
    
    vesRelTimes = [[list(chain(*[vesRelTimes[i][j][k] for i in range(nAZ)])) for k in range(trials)] for j in range(rrps)]
    vesData = {}
    for RRP,v in zip(RRPs, vesRelTimes):
        vesData.update({str(RRP): v})
    
    return vesData

# dir = tempdirs[1] 
# rrp = int(getSimInfo(dir, 'RRP'))
# vesData = getVesRel(dir, RRPs=[rrp], resultPath=resultPath, trials=35)

for dir in tq(tempdirs):
    try:
        rrp = int(getSimInfo(dir, 'RRP'))
        vesData = getVesRel(dir, RRPs=[rrp], resultPath=resultPath, trials=2000)
        with open(os.path.join(resultPath, dir, 'vesData.dat'),"wb") as outfile:
            pk.dump(vesData, outfile)
    except:
        print(f'Error in {dir}')
