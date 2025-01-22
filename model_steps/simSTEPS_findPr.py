import os, sys
import numpy as np
import pickle as pk
from random import randint
from itertools import product, chain
import scipy.interpolate as itp
from multiprocessing import Pool, Process

sys.path.append('/home/nishant/lab/MFB/scripts')
sys.path.append('/home/nishant/lab/MFB/steps')
# sys.path.append('/home/nishant/lab/scripts')
from analysis import *
from peaks import *
from misc import *


resultPath = "/media/nishant/data/results/findPr/"
# dirs = np.array(getDirs(resultPath, sstr='nVDCC'))
# print(dirs.shape[0])

# nvdcc = [15]
# dvdcc = range(60, 230, 20)
# naz   = range(7, 30, 2)

# nvdcc = range(2,15)
# dvdcc = range(60, 230, 20)
# naz   = [31, 33, 35]

# tempdirs = []
# for nVDCC, dVDCC, nAZ in product(nvdcc, dvdcc, naz):
#     tempdirs.append(f"nVDCC_{nVDCC}_dVDCC_{dVDCC}_nAZ_{nAZ}")

# tempdirs = [a for a in tempdirs if 'nVDCC_' in a][191:200]
# for i,d in enumerate(tempdirs):
#     print(i, d)

###################################################################
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
        # resAZs.append(resAZ)
    
    return [vesData, resAZs]

def getVesRel(dir, RRPs, resultPath, fname='CaConc.dat', trials=2000):
    nAZ = int(getSimInfo(dir, 'nAZ'))
    rrps = len(RRPs)
    
    CaFile = os.path.join(resultPath, dir, fname)
    CaData = np.genfromtxt(CaFile, unpack=True) # in uM
    
    p = Pool()
    vesRelTimes = []
    for iCa in tq(range(1,nAZ+1), desc=dir):
    # for iCa in range(1,nAZ+1):
        
        info = product([CaData[(0,iCa),:]], [RRPs]*trials)
        # print(list(info)[0])
        vesRelTime = np.array(p.starmap(runAZTrials, info), dtype=object)
        # vesRelTime = runAZTrials(CaData[(0,iCa),:], RRPs)

        # print(vesRelTime[:,0])
        # AZstates = vesRelTime[:,1]
        vesRelTime = vesRelTime[:,0]
        vesRelTime = [[vesRelTime[i][j] for i in range(trials)] for j in range(rrps)]
        vesRelTimes.append(vesRelTime)
        #print(vesRelTime[:,1])

        # AZstates = np.mean(AZstates, axis=0)

        #print(AZstates[0])
        #print(np.vstack((CaData[0,],AZstates[0])))
    
        # for i,rrp in enumerate(RRPs):
        #     fAZ = os.path.join(resultPath, dir, f'AZ_{iCa}_RRP_{rrp}.dat')
        #     AZdata = np.hstack((np.array([CaData[0]]).T, AZstates[i]))
        #     np.savetxt(fAZ, AZdata, fmt=['%0.5f']+['%0.3f']*18, delimiter="\t")

    p.close()
    p.join()
    
    vesRelTimes = [[list(chain(*[vesRelTimes[i][j][k] for i in range(nAZ)])) for k in range(trials)] for j in range(rrps)]
    vesData = {}
    for RRP,v in zip(RRPs, vesRelTimes):
        vesData.update({str(RRP): v})
    
    return vesData
############################################################33

with open(os.path.join(resultPath, 'correctionSim'), "rb") as infile:
    correctionSim = pk.load(infile)

sims = correctionSim[300:]
for i, s in enumerate(sims):
    print(i, s)

for dir, RRP in tq(sims):
    # print(dir, RRP)
    try:
        with open(os.path.join(resultPath, dir, 'vesData.dat'), 'rb') as file:
            vesData = pk.load(file)
            newVesData = getVesRel(dir, RRPs=RRP, resultPath=resultPath, trials=1000)
            vesData.update(newVesData)
        with open(os.path.join(resultPath, dir, 'vesData.dat'), "wb") as outfile:
            pk.dump(vesData, outfile)

    except FileNotFoundError:
        try:
            vesData = getVesRel(dir, RRPs=range(5,61,5), resultPath=resultPath, trials=1000)
            with open(os.path.join(resultPath, dir, 'vesData.dat'), "wb") as outfile:
                pk.dump(vesData, outfile)
        except:
            print(f'Error in {dir}')
    
    except:
        print(f'Error in {dir}')