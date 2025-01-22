import os, sys
import numpy as np
import pickle as pk
import seaborn as sns
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


dirType = "CaMicroDomain"
dataPath = "/media/nishant/4tb/output/MFB/" + dirType 
resultPath = "/home/nishant/lab/results/MFB/" + dirType

dirs = np.array(getDirs(dataPath, sstr=''))

def getCaCount(simdir, resultPath=resultPath, timepoint=2500, step=0.05):
    """
    step: individual cell size in um
    timepoint in nano second
    """
    xlim, ylim, zlim = [-2.05, 2.05], [-1.25, 1.25], [-0.4, 0.4]

    ### Generate grid to store calcium ion count
    caGrid = np.zeros((int(np.ceil((ylim[1] - ylim[0])/step)), int(np.ceil((xlim[1] - xlim[0])/step))))
    #print(caGrid.shape)

    nseeds = len([a for a in os.listdir(os.path.join(dataPath, simdir))
                  if os.path.isdir(os.path.join(dataPath, simdir, a))])
    #print(nseeds)
    for seed in range(nseeds):#, desc=f'{timepoint} {simdir}'):
        data = np.genfromtxt(os.path.join(dataPath, simdir, f's_{seed+1:05}', f'viz.ascii.{timepoint:05}.dat'), 
                             usecols=(2,3,4))
        boxidx = np.array(np.floor((data - np.array([xlim[0], ylim[0], zlim[0]]))/step), dtype='int')

        for xid, yid, zid in boxidx:
            if zid == 0:
                caGrid[yid][xid] += 1

    caGrid = caGrid/nseeds
    
    if not os.path.exists(resultPath):
        os.makedirs(resultPath)

    if not os.path.exists(os.path.join(resultPath,simdir)):
        os.makedirs(os.path.join(resultPath,simdir))

    with open(os.path.join(resultPath, simdir, f'caGrid_{timepoint:05}.dat'),"wb") as outfile:
        pk.dump(caGrid, outfile)
        
    print(f'{simdir} at {timepoint} is done!')

dirId = int(sys.argv[1])
t = int(sys.argv[2])
getCaCount(dirs[dirId], timepoint=t)