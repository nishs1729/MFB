import random
import os, sys, time
import numpy as np
import pandas as pd
from itertools import *
import itertools as it
import matplotlib.pyplot as plt

# qEPSC kernel
def dexp(x, a=146, b=0.407, c=1.154):
    """fit values: 
    a, b, c = 146, 407,   1154 # sec
    a, b, c = 146, 0.407, 1.154 # msec"""
    return a*(np.exp(-b*x)-np.exp(-c*x))

def getEPSC(vr, runt, dt):
    tpoints = np.arange(0, runt+15+dt, dt)
    EPSCk = dexp(tpoints[:int(15/dt)]) # EPSC kernel of 15 ms+
    EPSC = np.zeros(tpoints.shape)
    for vt in vr:
        tid = int(vt/dt)
        EPSC[tid:tid+int(15/dt)] += EPSCk
    return(EPSC)

## Get EPSC for all trials
def getAllEPSC(vrel):
    EPSCs = np.array([getEPSC(vr) for vr in vrel])
    return EPSCs

def getSpikeRate(spM, trials, runt, bindt=5):
    try:
        apTimes = np.sort(np.concatenate(list(spM.spike_trains().values())))*1e3
    except:
        apTimes = np.sort(np.concatenate(spM))
    bins = np.arange(0, runt, bindt)
    n, bins = np.histogram(apTimes, bins)
    aprate = n/(trials*bindt)*1e3 # rate: s^{-1}
    apratet = [a-bindt for a in bins[1:]]
    return apratet, aprate

def vesInput(vrel, delta=1e-4):
    vrel = [np.array(vr) for vr in vrel]
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


############################################
### Poisson Spike Trains
def genPoissonTrain(rate, tspan=1e3, dt=0.1, refrac=0):
    """
    rate: Hz; tspan: ms
    Assumption: no multiple event within t=refrac ms
    """
    tt = rate*refrac/(1000-rate*refrac)
    arefrac = refrac*(1+tt)
    train = []
    rp = np.random.uniform(size=int(tspan*(1+tt)/dt))
    temp = -np.inf
    for i,r in enumerate(rp):
        if r<rate*dt*1e-3 and i*dt-temp > arefrac:
            #print(i, f'{i*dt:0.2f}, {temp:0.2f} {r:0.4f}')
            temp = i*dt
            train += [temp]
    return np.array(train)/(1+tt)

def getSubTrains(train, p, n=1):
    """
    Generate n random subsets of original train 
    with probability p
    """
    rr = np.random.uniform(size=(n,train.shape[0]))
    subTrains = []
    for r in rr:
        temp = np.array(np.where(np.less(r, p) == True))[0]
        subTrains.append(train[temp].tolist())
    return subTrains

def genCorrSpikeTrains(corr, rate=1, n=1, tspan=1e3, dt=0.1, refrac=5):
    """
    corr: expected coefficient of correlation
    rate: Hz
    n: number of trains
    tspan: ms
    """
    corrTrains = []
    if hasattr(corr, '__iter__'):
        if hasattr(n, '__iter__'):
            for c, nn in zip(corr, n):
                poisTrain = genPoissonTrain(rate/c, tspan=tspan, dt=dt, refrac=refrac)
                cTrains = getSubTrains(poisTrain, c, n=nn)
                corrTrains += cTrains
        else:
            for c in corr:
                poisTrain = genPoissonTrain(rate/c, tspan=tspan, dt=dt, refrac=refrac)
                cTrains = getSubTrains(poisTrain, c, n=n)
                corrTrains += cTrains
    else:
        poisTrain = genPoissonTrain(rate/corr, tspan=tspan, dt=dt, refrac=refrac)
        corrTrains = getSubTrains(poisTrain, corr, n=n)
    return corrTrains

def genCorrPoisBursts(c, rate, tspan=500, ibi=1e3, nB=1, st=0, nn=1, dt=0.1, refrac=0):
    '''
    c: correlation between trains
    rate: Hz
    tspan: span of individual poisson train, ms
    ibi: inter-burst interval, ms
    nB: number of bursts
    st: start time, ms
    nn: number of neurons
    refrac: minimum gap between two spikes, ms'''
    
    cTrains = [[] for _ in range(nn)]
    for n in range(nB):
        poisTrain = genPoissonTrain(rate/c, tspan=tspan, dt=dt, refrac=refrac)
        tr = [[a+st+n*(tspan+ibi) for a in t] for t in getSubTrains(poisTrain, c, n=nn)]
        cTrains = [ct+t for ct,t in zip(cTrains, tr)]
    
    return cTrains

##############################################################
### Visualise connectivity in brian2
def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    shift = (Nt - Ns)/2.0
    f, ax = plt.subplots(1, 2, figsize=(8, 4))
    f.subplots_adjust(wspace=0.1, hspace=0)

    ax[0].plot(np.zeros(Ns), np.arange(Ns)+shift, 'om', ms=10)
    ax[0].plot(np.ones(Nt), range(Nt), 'og', ms=10)
    for i, j in zip(S.i, S.j):
        ax[0].plot([0, 1], [i+shift, j], '-c')

    for i in S.i: # Source neuron index
        ax[0].text(-0.1, i-0.2+shift, i)

    for j in S.j: # Target neuron index
        ax[0].text(1.07, j-0.2, j)

    ax[0].set_xticks([0, 1], ['Source', 'Target'])
    ax[0].set_yticks([], [])
    ax[0].set_xlim(-0.1, 1.1)
    # ax[0].set_ylim(-1, max(Ns, Nt))

    c = np.zeros((Nt, Ns))
    for s,t in zip(S.i, S.j):
        c[t,s] = 1
    ax[1].imshow(c, cmap="ocean")
    ax[1].set_xlabel('Source')
    ax[1].set_ylabel('Target')
    ax[1].set_title("Connectivity matrix", fontsize=10)

    ax[1].set_xticks(np.arange(c.shape[1]+1)-.5, minor=True)
    ax[1].set_yticks(np.arange(c.shape[0]+1)-.5, minor=True)
    ax[1].grid(which="minor", color="black", linestyle='-', linewidth=1)
    ax[1].tick_params(which="both", bottom=False, left=False)

    for axis in ax.ravel():
        axis.spines["right"].set_visible(False)
        axis.spines["top"].set_visible(False)
        axis.spines["left"].set_visible(False)
        axis.spines["bottom"].set_visible(False)
        axis.tick_params(axis=u'both', which=u'both', length=0, labelsize=10)
    
    f.tight_layout()
    plt.show()

##############################################################
### Select spikes with pr probability from a list of spikes
def get_In_train_from_MFB_input(trains, pr=0.4, n=1):
    InTrain = []
    for tr in trains:
        for _ in range(n):
            mask = np.random.uniform(size=len(tr)) < 0.4
            InTrain.append(np.array(tr)[mask].tolist())
    random.shuffle(InTrain)

    ind = []
    for i,e in enumerate(InTrain):
        ind += np.full(len(e), i).tolist()

    return InTrain, ind

##############################################################
### Select spikes with pr probability from a list of spikes
def get_rate(events, runt, bindt=5):
    trials = len(events)
    bins = np.arange(0, runt, bindt)
    n, _ = np.histogram(np.concatenate(events), bins)
    return (bins - bindt/2)[1:], 1000*n/(trials*bindt) 


##############################################################
def getSpikeRate(spM, seeds, runt, bindt=5):
    apTimes = np.sort(np.concatenate(list(spM.spike_trains().values())))*1e3
    bins = np.arange(0, runt, bindt)
    n, bins = np.histogram(apTimes, bins)
    aprate = n/(seeds*bindt)*1e3 # rate: s^{-1}
    apratet = [a-bindt for a in bins[1:]]
    return apratet, aprate