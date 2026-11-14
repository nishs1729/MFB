import os, sys
import numpy as np
import pickle as pk
from random import randint
from itertools import product, chain
import scipy.interpolate as itp
from multiprocessing import Pool, Process

from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
sys.path.append(str(REPO / 'scripts_analysis'))
sys.path.append(str(REPO / 'model_steps'))
from analysis import *
from peaks import *
from misc import *


dataPath = "/media/nishant/4tb/output/MFB/findPr/"
resultPath = str(REPO / 'data/findPr') + '/'
fname = "ca.dat" 

dir = sys.argv[1]

try:
    vesData = PrStat(dir, resultPath=resultPath, resample=1000)
except:
    print(f'Error in {dir}')
