import os, sys, re
import numpy as np
import scipy as sp
from peaks import *
import pickle as pk
import pandas as pd
from time import time, sleep
from random import randint
from itertools import product
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from multiprocessing import Pool, Process

if 'jupyter' in os.environ['_']:
    from tqdm import tqdm_notebook as tq
    # print("you're in jupyter")
else:
    from tqdm import tqdm as tq
    # print("you're not in jupyter")

sys.path.append('./')
from misc import *

##################################################
### Get list of directories in the path starting with 's_'
def getDirs(path, sstr='s_'):
    dirs = [d for d in os.listdir(path) if os.path.isdir(path + '/' + d) and sstr in d]
    dirs.sort()
    return(dirs)

##################################################
### Get data from dataFile in array
def _getData(file):
    return np.genfromtxt(file, unpack=True)

def getData(dataPath, d, fname, cores=None):
    path = os.path.join(dataPath, d)
    allDirs = getDirs(path)
    files = [os.path.join(path, d, 'dat',fname) for d in allDirs]
    
    if cores:
        p = Pool(cores)
        #data = p.map(np.genfromtxt, files, )
        data = p.map(_getData, files)
        p.close()
        #p.join()

    else:
        data = []
        for d in tq(allDirs, desc=d):
            file = os.path.join(path,d,'dat',fname)
            try: 
                temp = np.genfromtxt(file, unpack=True)
                #print(temp.shape, d)
            except: print(d)
            #print(temp.shape, d)
            data.append(temp)
    
    return np.array(data)

##################################################
### Average Over all Seeds
def avg_dat(dataPath, resultPath, d, fname, header='', std=False, 
            fmt=['%.05f'], ret=False, write=True, cores=None):
    data = getData(dataPath, d, fname, cores=cores)

    seeds = len(data)
    avg = np.mean(data, axis=0)
    ncols = len(avg)

    if not os.path.exists(os.path.join(resultPath,d)):
        os.makedirs(os.path.join(resultPath,d))

    if std:
        std = np.std(data, axis=0)

        temp = np.zeros((avg.shape[0]*2-1, avg.shape[1]))
        temp[0,:] = avg[0]
        temp[1::2,:] = avg[1:]
        temp[2::2,:] = std[1:]

        if write:
            np.savetxt(os.path.join(resultPath,d,fname), temp.T,
                       fmt=['%.5f']+fmt*(ncols-1)*2, header=header, delimiter='\t')

    else:
        temp = avg
        if write:
            np.savetxt(os.path.join(resultPath,d,fname), temp.T,
                       fmt=['%.5f']+fmt*(ncols-1), header=header, delimiter='\t')
    #print("Writing averaged data to:\t" + fname)

    if ret:
        return temp
    
##################################################
### Ca Concentration Calculation
def getConc(data, step):
    #sdata = savgol_filter(data[1], 51, 3)
    sdata = data[1]
    
    #plt.plot(data[0],sdata)
    #plt.ylim(0,0.2)
    
    c_tc = np.multiply(data[0],sdata)
    dt = step*(data[0][1]-data[0][0])

    c_out = []
    for i in range(0,len(data[0])-step-1,step):
        c_out.append((c_tc[i+step]-c_tc[i])/dt)

    return np.array(c_out)

def CaConc(resultPath, d, fname='ca.dat', header='', step=5, skip=[1]):
    try:
        data = np.genfromtxt(os.path.join(resultPath,d,fname), unpack=True)

        # 0th index containing timepoints
        CaData = [data[0,range(0,len(data[0])-step-1,step)]]
        #print(CaData)
        for i in range(1,data.shape[0]):
            if i not in skip:
                CaData.append(getConc([data[0],data[i]], step=step))

        CaData = np.array(CaData)

        tmp = fname.split('ca')[::-1][0].split('.')[0]
        np.savetxt(os.path.join(resultPath,d,f'CaConc{tmp}.dat'), CaData.T, delimiter='\t',
                   fmt=['%.5f']+['%.03f']*(CaData.shape[0]-1), header=header)
        # print(f'{d} : Done!')
    except:
        print(f"Error in {d}")
        
##################################################
### Smoothen a curve    
def smoothen(resultPath, d, fname='ca.dat', header='', window=51):
    try: 
        path = os.path.join(resultPath,d,fname)
        data = np.genfromtxt(path, unpack=True)

        for i in range(2, data.shape[0]):
            data[i] = sp.signal.savgol_filter(data[i], 71, 3)

        np.savetxt(path, data.T, delimiter='\t', header=header, 
                   fmt=['%.5f']+['%.06f']*(data.shape[0]-1))
    except:
        print(f"Error in {d}")
   
##################################################
### Get Pr 
## isi in ms
def PrStat(dir, resultPath, resample=1000, tsi=1.5e-3, tc=0.02):
    nVDCC, dVDCC, nAZ = [int(getSimInfo(dir, key, skip=0)) for key in ['nVDCC', 'dVDCC', 'nAZ']]
    #print(nVDCC, dVDCC, nAZ)
    
    with open(os.path.join(resultPath, dir, 'vesData.dat'), "rb") as infile:
        vesData = pk.load(infile)
    
    # print(f'Vesicle release stats:')
    result = []
    for rrp, timedata in tq(vesData.items(), desc=dir):
        seeds = len(timedata)
        #print(seeds)

        prs = []
        for _ in range(resample):
            x = [randint(0,seeds-1) for p in range(seeds)]
            #print(x)

            nRel, nAllRel = 0, 0
            for times in [timedata[i] for i in x]: 
                
                ifRel = int(len(list(filter(lambda a: a>tsi and a<tsi+tc, times)))>0)
                allRel = sum(map(lambda a: a>tsi and a<tsi+tc, times))
                
                if ifRel == 1: nRel += 1
                nAllRel += allRel

            #print(nRel, nAllRel)
            prs.append(np.array([nRel, nAllRel])/seeds)

        m = np.mean(prs, axis=0)
        s = np.std(prs, axis=0)

        result.append(np.concatenate((np.array(list(zip(m,s))).flatten(),[nAZ, nVDCC, dVDCC, int(rrp)]), axis=0).tolist())
        
    # for res in result:
    #     print([f'{i:.4f}' for i in res[:4]] + [f'{i:.2f}' for i in res[4:]])
        
    header = 'p1\tep1\t\ttRel\tetRel\tnAZ\tnV\tdV\tRRP'
    np.savetxt(os.path.join(resultPath, dir, 'result.dat'), result, header=header, 
              fmt=['%0.4f']*4+['%d']*4, delimiter="\t")

    return(result)

### Get release stats
def getTimesData(args):
    times, ts, tc = args
    nRelTrial = [int(len(list(filter(lambda a: a>tsi and a<tsi+tc, times)))>0) for tsi in ts]
    allRelTrial = [sum(map(lambda a: a>tsi and a<tsi+tc, times)) for tsi in ts]

    return np.array([nRelTrial, allRelTrial])

def relStat(dir, resultPath, resample=1000, ts=1.5e-3, tc=0.02,
            inf='vesData.dat', resultf='result.dat'):
    inf = os.path.join(resultPath, dir, inf)
        
    with open(inf, "rb") as infile:
        data = pk.load(infile)

        # print(data.values())
        aa = [[a for a in aa.values()] for aa in list(data.values())]
        # print(len(aa), len(aa[1]), len(aa[1][1]))
        bb = list(zip(*[[np.concatenate(x).tolist() for x in list(zip(*_))] for _ in aa]))
        vesData = list([np.concatenate(x).tolist() for x in bb])
        # print('sdfgsdfg',len(vesData))
        # print([len(a) for a in vesData])

        # vesData = list(data.values())[0]
        # print(vesData)

    try:
        n = int(getSimInfo(dir, 'nAP')) # number of AP
    except ValueError:
        n = 1
        
    try:
        isi = int(getSimInfo(dir, 'ISI')) # isi in ms
    except ValueError:
        isi = 0
    
    ts = [(i*isi+1.5)/1000.0 for i in range(n)]

    seeds = len(vesData)
    #print(seeds, vesData)

    result = []
    prs, rels, prratios = [], [], []
    desc = str([int(a) for a in re.findall(r'\d+', dir)[:-1]])
    for _ in tq(range(resample), desc=f'Resampling {desc}'):
        trials = [randint(0,seeds-1) for p in range(seeds)]

        timesInfo = list(product([vesData[i] for i in trials[:]], [ts], [tc]))
        # print(timesInfo[0])

        relData = np.array(list(map(getTimesData, timesInfo)))
        relData = np.sum(relData, axis=0)

        nRel = relData[0]
        allRel = relData[1]
        prratio = nRel/nRel[0]

        prs.append(np.array(nRel))
        rels.append(np.array(allRel))
        prratios.append(np.array(prratio))

    prs = np.array(prs)/seeds
    rels = np.array(rels)/seeds

    mpr = np.mean(prs, axis=0)
    spr = np.std(prs, axis=0)

    mrel = np.mean(rels, axis=0)
    srel = np.std(rels, axis=0)

    mprratios = np.mean(prratios, axis=0)
    sprratios = np.std(prratios, axis=0)

    result = np.array([mpr, spr, mrel, srel, mprratios, sprratios]).T

    header = 'Pr\tePr\tRel\teRel\tFac\teFac'
    # print(result)
    
    np.savetxt(os.path.join(resultPath, dir, resultf), 
               result, header=header, fmt=['%0.4f']*6, delimiter='\t')
    
    return(result)

#######################################################################
###### EPSC calculation

# qEPSC kernel
def dexp(x, a=146, b=407, c=1154):
    """fit values:
    a, b, c = 146, 407, 1154"""
    #a,b,c = 70, 107, 2154
    return a*np.exp(-b*x)-a*np.exp(-c*x)

def getEPSC(resultDir, vr, tpoints):
    EPSCk = dexp(tpoints[:301]) # EPSC kernel of 15 ms
    EPSC = np.zeros(tpoints.shape)
    for vt in vr:
        tid = int(vt/5e-5+1e-6)
        EPSC[tid:tid+301] += EPSCk
    return(EPSC)

## Get vrel for all seeds
def getAllEPSC(resultDir, ttt=''):
    inf = os.path.join(resultDir, ttt+'vesData.dat')
    with open(inf, "rb") as infile:
        vesData = pk.load(infile)

    df = pd.io.json.json_normalize(vesData, sep='_')    
    df = df.to_dict(orient='records')[0]
    seeds = len(df['AZ1_sync'])
    emptyKeys = []
    for k,v in df.items():
        if all([not a for a in v]):
            emptyKeys.append(k)
    for e in emptyKeys:
        df.pop(e)

    try:
        caFile = os.path.join(resultDir, 'CaConc.dat')
        tpoints = np.genfromtxt(caFile, unpack=True, usecols=(0)).tolist()
    except OSError:
        caFile = os.path.join(resultDir, 'CaConc_AZ_1.dat')
        tpoints = np.genfromtxt(caFile, unpack=True, usecols=(0)).tolist()

    tstep = tpoints[1] - tpoints[0]
    tpoints += np.arange(tpoints[-1],tpoints[-1]+0.015, tstep).tolist()
    tpoints = np.array(tpoints)
    EPSCk = dexp(tpoints[:301]) # EPSC kernel of 15 ms

    vrel = [[] for _ in range(seeds)]
    for vs in df.values():
        for i,v in enumerate(vs):
            vrel[i] += v
    for i,vr in enumerate(vrel):
        vrel[i] = np.sort(vr)
    #vrel[0].shape, vrel[0]

    EPSC = np.array([getEPSC(resultDir, vrel[i], tpoints) for i in range(seeds)])
    return EPSC, tstep

### Get the average EPSC
def getAvgEPSC(resultDir, vesFile, tstep=5e-5):
    inf = os.path.join(resultDir, vesFile)
    with open(inf, "rb") as infile:
        vesData = pk.load(infile)
        
    df = pd.io.json.json_normalize(vesData, sep='_')    
    df = df.to_dict(orient='records')[0]
    seeds = len(df['AZ1_sync'])
    emptyKeys = []
    for k,v in df.items():
        if all([not a for a in v]):
            emptyKeys.append(k)
    for e in emptyKeys:
        df.pop(e)
    
    try:
        caFile = os.path.join(resultDir, 'CaConc.dat')
        tpoints = np.genfromtxt(caFile, unpack=True, usecols=(0)).tolist()
    except OSError:
        caFile = os.path.join(resultDir, 'CaConc_AZ_1.dat')
        tpoints = np.genfromtxt(caFile, unpack=True, usecols=(0)).tolist()
        
    tpoints += np.arange(tpoints[-1],tpoints[-1]+0.015, tstep).tolist()
    tpoints = np.array(tpoints)
    EPSCk = dexp(tpoints[:301]) # EPSC kernel of 15 ms
    
    # times of all the releases
    vTimes = np.sort(np.concatenate(np.concatenate(list(df.values()))))
    avgEPSC = np.zeros(tpoints.shape)
    
    for vt in vTimes:
        tid = int(vt/5e-5+1e-6)
        #print(vt, tid, tpoints[tid])
        avgEPSC[tid:tid+301] += EPSCk

    avgEPSC = avgEPSC/seeds
    tpoints, avgEPSC = tpoints[:-301], avgEPSC[:-301]

    return tpoints, avgEPSC

### Get AP times for each trial
def getAPTimes(resultDir, vesFile, APth=100, tstep=5e-5):
    inf = os.path.join(resultDir, vesFile)
    with open(inf, "rb") as infile:
        vesData = pk.load(infile)
        
    df = pd.io.json.json_normalize(vesData, sep='_')    
    df = df.to_dict(orient='records')[0]
    seeds = len(df['AZ1_sync'])
    emptyKeys = []
    for k,v in df.items():
        if all([not a for a in v]):
            emptyKeys.append(k)
    for e in emptyKeys:
        df.pop(e)
    
    try:
        caFile = os.path.join(resultDir, 'CaConc.dat')
        tpoints = np.genfromtxt(caFile, unpack=True, usecols=(0)).tolist()
    except OSError:
        caFile = os.path.join(resultDir, 'CaConc_AZ_1.dat')
        tpoints = np.genfromtxt(caFile, unpack=True, usecols=(0)).tolist()
        
    tpoints += np.arange(tpoints[-1],tpoints[-1]+0.015, tstep).tolist()
    tpoints = np.array(tpoints)
    EPSCk = dexp(tpoints[:301]) # EPSC kernel of 15 ms
    
    vrel = [[] for _ in range(seeds)]
    for vs in df.values():
        for i,v in enumerate(vs):
            vrel[i] += v
    for i,vr in enumerate(vrel):
        vrel[i] = np.sort(vr).tolist()        
    #print(vTimes.shape, np.concatenate(vrel).shape)

    # calculating individual EPSC and AP probability
    apTimes = []
    for vr in vrel:
        EPSC = np.zeros(tpoints.shape)
        for vt in vr:
            tid = int(vt/5e-5+1e-6)
            #print(vt, tid, tpoints[tid])
            EPSC[tid:tid+301] += EPSCk

        pkids = detect_peaks(EPSC, mph=APth, mpd=100)
        pkts = tpoints[pkids]

        #plt.plot(tpoints, EPSC)
        apTimes.append(pkts.tolist())
    
    return apTimes

### Get indices and vesicle release times for 
### input to CA3 neuron
def getVesInput(resultDir, ttt='', delta=1e-4):
    inf = os.path.join(resultDir, ttt+'vesData.dat')
    with open(inf, "rb") as infile:
        vesData = pk.load(infile)

    df = pd.io.json.json_normalize(vesData, sep='_')    
    df = df.to_dict(orient='records')[0]
    seeds = len(df['AZ1_sync'])
    emptyKeys = []
    for k,v in df.items():
        if all([not a for a in v]):
            emptyKeys.append(k)
    for e in emptyKeys:
        df.pop(e)

    vrel = [[] for _ in range(seeds)]
    for vs in df.values():
        for i,v in enumerate(vs):
            vrel[i] += v
    for i,vr in enumerate(vrel):
        vrel[i] = np.sort(vr)
        
    mins = [delta]
    while min(mins)<=delta:
        mins=[]
        for aa in vrel:
            if len(aa)>1:
                temp = aa[1:]-aa[:-1]
                mins.append(min(temp))
                sm = [i+1 for i,x in enumerate(temp) if x < delta]
                aa[sm] += delta*1.1
        #print(min(mins), delta, min(mins)<=delta)
        #print('aa')
        
    indices = []
    for i,e in enumerate(vrel):
        indices += np.full(len(e), i).tolist()
        
    return indices, np.concatenate(vrel), len(vrel)




