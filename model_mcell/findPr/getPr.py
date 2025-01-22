import os, sys
import numpy as np
import pickle as pk
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


dataPath = "/media/nishant/4tb/output/MFB/findPr/"
resultPath = "/home/nishant/lab/results/MFB/findPr/"
fname = "ca.dat" 

dir = sys.argv[1]

try:
    vesData = PrStat(dir, resultPath=resultPath, resample=1000)
except:
    print(f'Error in {dir}')
