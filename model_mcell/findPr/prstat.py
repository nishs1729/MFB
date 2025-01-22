import os, sys
import numpy as np
import pickle as pk
from itertools import product, chain
from multiprocessing import Pool, Process

sys.path.append('/home/nishant/lab/MFB/scripts')
sys.path.append('/home/nishant/lab/MFB/steps')
sys.path.append('/home/nishant/lab/scripts')
from analysis import *
from peaks import *
from misc import *

resultPath = "/home/nishant/lab/MFB/results/findPr/"

nVDCC = [2]
dVDCC = range(60, 220, 20)
nAZ = range(7,8,2)
tempdirs = []
for vdcc, dvdcc, naz in product(nVDCC, dVDCC, nAZ):
    tempdirs.append(f'nVDCC_{vdcc}_dVDCC_{dvdcc}_nAZ_{naz}')
#print(tempdirs)

d, resultPath = sys.argv[1], sys.argv[2]
#print(d, resultPath)

vesData = PrStat(d, resultPath=resultPath)