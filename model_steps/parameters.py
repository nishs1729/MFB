from time import time
import numpy as np
from functools import reduce
from scipy.integrate import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import OrderedDict as od
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


######################################################
### Misclenious parameters
vrange = [-100.0e-3, 50e-3, 1e-4]
NA = 6.023e23
######################################################
### Steady state initial values
initV = {
    'Ca':       [100e-9],
    'HH':       [-64.0, 0.05, 0.6, 0.32],
    'PMCA':     [180*i for i in [0.80, 0.1953, 0.0047]], # Fraction; surface density = 180 num/um^2; Total conc. = 2.98e-6 uM
    'VDCC':     [80, 0.0, 0.0, 0.0, 0.0, 0.0],
    'cb':       [1.48e-05, 7.00e-06, 8.27e-07, 1.21e-05, 5.74e-06, 6.79e-07,
                 2.49e-06, 1.18e-06, 1.39e-07], # Total conc. = 45e-6 uM
    'AZ':       [1.65e-6] + [0.0 for _ in range(17)],
}

######################################################
cytVolVal = 9.61e-19 # cyt vol = 1 - ER vol = 0.961 um^3
cytArea = 8.5e-12 # cyt surf area = 8.5 um^2

erVolVal = 3.9e-20 # ER vol = 0.039 um^3
erArea = 1.58e-12 # ER surf area = 1.58 um^2
######################################################
### Parameters
## Calcium diffusion constant
diffCa = 2.2e-10 # m^2/s


######################################################
pmcaMolName = ['PMCA0', 'PMCA1', 'PMCA2']


## PMCA reaction rates
kPMCA01    = 1.5e8
kPMCA10    = 20
kPMCA12    = 100
kPMCA20    = 1e5
kPMCA0leak = 12.5


######################################################
cbMolName = ['H0M0', 'H0M1', 'H0M2', 
             'H1M0', 'H1M1', 'H1M2', 
             'H2M0', 'H2M1', 'H2M2']


## Calbindin reaction rates
cbHon  = 1.1e7
cbHoff = 2.6
cbMon  = 8.7e7
cbMoff = 35.8


######################################################
azMolName = ['AZ00',  'AZ10',  'AZ20',  'AZ30',  'AZ40',  'AZ50',
             'AZ01',  'AZ11',  'AZ21',  'AZ31',  'AZ41',  'AZ51',
             'AZ02',  'AZ12',  'AZ22',  'AZ32',  'AZ42',  'AZ52',
             'dAZ00', 'dAZ10', 'dAZ20', 'dAZ30', 'dAZ40', 'dAZ50',
             'dAZ01', 'dAZ11', 'dAZ21', 'dAZ31', 'dAZ41', 'dAZ51',
             'dAZ02', 'dAZ12', 'dAZ22', 'dAZ32', 'dAZ42', 'dAZ52']

## Calcium Sensor
sf = 0.612e8    # /M s
sb = 2.32e3     # /s
af = 3.82e6     # /s
ab = 13         # /s
b  = 0.25       # /s
krefrac = 0.36  # /s 
ksync = 2e3     # /s
kasync = 0.025*ksync    # /s
kspont = 0.417e-3       # /s


######################################################
vdccMolName = ['VDCC_C0', 'VDCC_C1', 'VDCC_C2', 'VDCC_C3', 'VDCC_O']

### pqVDCC
pq_a10, pq_a20, pq_a30, pq_a40, pq_a = 5890, 9210, 5200, 1823180, 247710 # /sec
pq_b10, pq_b20, pq_b30, pq_b40, pq_b = 14990, 6630, 132800, 248580, 8280 # /sec
pq_V1,  pq_V2,  pq_V3,  pq_V4        = 62.61, 33.92, 135.08, 20.86 # mV

### pqVDCC gating variables
def pq_a1(V):    return pq_a10*np.exp( V/pq_V1)
def pq_b1(V):    return pq_b10*np.exp(-V/pq_V1)
def pq_a2(V):    return pq_a20*np.exp( V/pq_V2)
def pq_b2(V):    return pq_b20*np.exp(-V/pq_V2)
def pq_a3(V):    return pq_a30*np.exp( V/pq_V3)
def pq_b3(V):    return pq_b30*np.exp(-V/pq_V3)
def pq_a4(V):    return pq_a40*np.exp( V/pq_V4)
def pq_b4(V):    return pq_b40*np.exp(-V/pq_V4)

# Calcium flux through VDCC
def CaFlux(V):
    P = 3.72 # from Bartol et al. 2015, Q10 = 1.55; 3.003 in Bischoffberger et al. 2003 # pA/mV
    C = 80.36 # mV
    D = 0.3933
    r = P*V*(D - np.exp(-V/C))/(1 - np.exp(V/C)) # s^{-1}
    return r


######################################################
### HH model
C_m  = 1.0
g_Na = 120.0
g_K  = 36.0
g_L  = 0.3
E_Na = 50.0
E_K  = -77.0
E_L  = -54.387

### External Current for HH model
def I_inj(t):  return 7#*(t>0.005) - 10*(t>0.015) + 35*(t>0.3) - 35*(t>0.4)

### Channel gating variables (ms)
def alpha_m(V):   return 0.1*(V+40.0)/(1.0 - np.exp(-(V+40.0) / 10.0))
def beta_m(V):    return 4.0*np.exp(-(V+65.0) / 18.0)
def alpha_h(V):   return 0.07*np.exp(-(V+65.0) / 20.0)
def beta_h(V):    return 1.0/(1.0 + np.exp(-(V+35.0) / 10.0))
def alpha_n(V):   return 0.01*(V+55.0)/(1.0 - np.exp(-(V+55.0) / 10.0))
def beta_n(V):    return 0.125*np.exp(-(V+65.0) / 80.0)

### Membrane current (in uA/cm^2)
def I_Na(V, m, h):  return g_Na*m**3*h*(V - E_Na)
def I_K(V, n):      return g_K*n**4*(V - E_K)
def I_L(V):         return g_L*(V - E_L)
#np.set_printoptions(precision=4)


######################################################
## RyR model

ryrMolName = ['RyRLC1', 'RyRLC2', 'RyRLC3', 'RyRLC4', 'RyRLC5',
              'RyRLO1', 'RyRLO2', 'RyRLO3',
              'RyRH1C1', 'RyRH1C2', 'RyRH1C3', 'RyRH1C4',
              'RyRH1O1', 'RyRH1O2']


## L mode rates:
kRyRC1C2_L = 1.24e6
kRyRC2C1_L = 13.6
kRyRC2C3_L = 29.8e6
kRyRC3C2_L = 3867
kRyRC2C5_L = 1.81
kRyRC5C2_L = 3.63
kRyRC3O1_L = 731.2
kRyRO1C3_L = 4185
kRyRC3O2_L = 24.5
kRyRO2C3_L = 156.5
kRyRC3O3_L = 8.5
kRyRO3C3_L = 111.7
kRyRO2C4_L = 1995
kRyRC4O2_L = 415.3
kRyRO3C4_L = 253.3
kRyRC4O3_L = 43.3

## H1 mode rates:
kRyRC1C2_H1 = 3.26e6
kRyRC2C1_H1 = 116
kRyRC2C3_H1 = 0.66e6
kRyRC3C2_H1 = 163
kRyRC2O1_H1 = 7.86e6
kRyRO1C2_H1 = 1480
kRyRC3O2_H1 = 7.77e6
kRyRO2C3_H1 = 330
kRyRC4O2_H1 = 2390
kRyRO2C4_H1 = 298

## L <-> H1 transition rates: */
kRyRC1C2_LH1 = 2e3/3
kRyRC2C1_H1L = 0.25/3
kRyRC2C3_LH1 = 2e3/3
kRyRC3C2_H1L = 0.25/3
kRyRC3C4_LH1 = 2e3/3
kRyRC4C3_H1L = 0.25/3

kRyRflux = 1.09e9