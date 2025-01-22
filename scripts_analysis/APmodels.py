import numpy as np
from scipy.integrate import *
import matplotlib.pyplot as plt
from collections import OrderedDict as od

colors = ['#EE442F',
          '#0F2080',
          '#601A4A',
          '#F5793A',
          '#63ACBE',
          '#A95AA1',
          '#85C0F9',
          '#382119',
          '#F9F4EC']

def showAllColors(colors):
    x = np.arange(0,1,0.1)
    y = np.zeros(len(x))
    for i,c in enumerate(colors):
        plt.plot(x, y+i, color=c, lw=15)
        
    plt.box(on=None)
    plt.tick_params(axis=u'both', which=u'both',length=0, labelbottom=False)
    plt.show()
    
######################################################
### Hodgekin-Huxley Model Class
class HH:
    ## Must be in same order as dXdt return
    label = ['V', 'm', 'h', 'n']
    nVar = len(label)

    ## Parameters
    p = {
    'C_m' : 1.0,
    'g_Na': 120.0,
    'g_K' : 36.0,
    'g_L' : 0.3,
    'E_Na': 50.0,
    'E_K' : -77.0,
    'E_L' : -54.387
    }

    ## Get initial values for the system
    def __init__(self, X0=[-65, 0.05, 0.6, 0.32], T=np.arange(0, 50e-3, 1e-5), I_amp=2.245):
        self.X0 = X0
        self.T = T
        self.sol = od()
        self.I_amp = I_amp

    ## External current (step function)
    def I_ext(self, t): return self.I_amp*(t>0.001 and t<0.0015)
         
    # Channel gating variables (ms)
    def alpha_m(self, V):  return 0.1*(V+40.0)/(1.0 - np.exp(-(V+40.0) / 10.0))
    def beta_m(self, V):   return 4.0*np.exp(-(V+65.0) / 18.0)
    def alpha_h(self, V):  return 0.07*np.exp(-(V+65.0) / 20.0)
    def beta_h(self, V):   return 1.0/(1.0 + np.exp(-(V+35.0) / 10.0))
    def alpha_n(self, V):  return 0.01*(V+55.0)/(1.0 - np.exp(-(V+55.0) / 10.0))
    def beta_n(self, V):   return 0.125*np.exp(-(V+65) / 80.0)

    # Membrane current (in uA/cm^2)
    def I_Na(self, V, m, h):  return self.p['g_Na'] * m**3 * h * (V - self.p['E_Na'])
    def I_K(self, V, n):      return self.p['g_K']  * n**4 * (V - self.p['E_K'])
    def I_L(self, V):         return self.p['g_L'] * (V - self.p['E_L'])

    
    ## Define the dX/dt for the system
    def dXdt(self, X, t):
        V, m, h, n = X

        dV = 1000*(self.I_ext(t) - self.I_Na(V, m, h) - self.I_K(V, n) - self.I_L(V)/self.p['C_m'])
        dm = 1000*(self.alpha_m(V)*(1.0-m) - self.beta_m(V)*m)
        dh = 1000*(self.alpha_h(V)*(1.0-h) - self.beta_h(V)*h)
        dn = 1000*(self.alpha_n(V)*(1.0-n) - self.beta_n(V)*n)

        return dV, dm, dh, dn
    
    def solve(self):
        sol = odeint(self.dXdt, self.X0, self.T, hmax=5e-4)
        #self.sol.update({'_T': T})
        for i,s in enumerate(sol.T):
            self.sol.update({self.label[i]: s})
            

######################################################
### Hodgekin-Huxley based model for action potential in hippocampal mossy fiber bouton 
### Engel and Jonas, Presynaptic Action Potential Amplification by Voltage-Gated Na+ Channels in Hippocampal Mossy Fiber Boutons
class hhMFB:
    ## Must be in same order as dXdt return
    label = ['V', 'm', 'h', 'n']
    nVar = len(label)

    ## Parameters
    p = {
        'C_m' : 1.0,
        'g_Na': 49.0,
        'g_K' : 36.0,
        'g_L' : 0.3,
        'E_Na': 50.0,
        'E_K' : -85.0,
        'E_L' : -81
    }

    ## Get initial values for the system
    def __init__(self, X0=[-80.789, 0.028, 0.68, 0.12], T=np.arange(0, 50e-3, 1e-5), I_amp=2.245):
        self.X0 = X0
        self.T = T
        self.sol = od()
        self.I_amp = I_amp
        self.Vshift = -12

    ## External current (step function)
    def I_ext(self, t): return self.I_amp*(t>0.001 and t<0.0015)
         
    # Channel gating variables (ms)
    def alpha_m(self, V):  return 93.83*((V-12) - 105.02)/(1 - np.exp(-((V-12) - 105.02)/17.71))       
    def beta_m(self, V):   return 0.168*np.exp(-(V-12)/23.27)
    def alpha_h(self, V):  return 3.54e-4*np.exp(-(V-12)/18.71)
    def beta_h(self, V):   return 6.627/(np.exp(-((V-12) + 17.68)/13.31) + 1)

    def alpha_n(self, V):  return 0.01*(V + 55.0)/(1.0 - np.exp(-(V + 55.0) / 10.0))
    def beta_n(self, V):   return 0.125*np.exp(-(V + 65) / 80.0)

    # Membrane current (in uA/cm^2)
    def I_Na(self, V, m, h):  return self.p['g_Na'] * m**3 * h * (V - self.p['E_Na'])
    def I_K(self, V, n):      return self.p['g_K']  * n**4 * (V - self.p['E_K'])
    def I_L(self, V):         return self.p['g_L'] * (V - self.p['E_L'])

    ## Define the dX/dt for the system
    def dXdt(self, X, t):
        V, m, h, n = X

        dV = 1000*(self.I_ext(t) - self.I_Na(V, m, h) - self.I_K(V, n) - self.I_L(V)/self.p['C_m'])
        dm = 1000*(self.alpha_m(V)*(1.0-m) - self.beta_m(V)*m)
        dh = 1000*(self.alpha_h(V)*(1.0-h) - self.beta_h(V)*h)
        dn = 1000*(self.alpha_n(V)*(1.0-n) - self.beta_n(V)*n)

        return dV, dm, dh, dn
    
    def solve(self):
        sol = odeint(self.dXdt, self.X0, self.T, hmax=5e-4)
        #self.sol.update({'_T': T})
        for i,s in enumerate(sol.T):
            self.sol.update({self.label[i]: s})
            

######################################################
### VDCC parameters
# from Bischofberger et al. 2002 J. Neuro
a10, a20, a30, a40 = np.array([4040, 6700, 4390, 17330])*1 # /sec
b10, b20, b30, b40 = np.array([2880, 6300, 8160, 1840])*1 # /sec
V1,  V2,  V3,  V4  = 49.14, 42.08, 55.31, 26.55 # mV

### VDCC gating variables
def a1(V):    return a10*np.exp( V/V1)
def b1(V):    return b10*np.exp(-V/V1)
def a2(V):    return a20*np.exp( V/V2)
def b2(V):    return b20*np.exp(-V/V2)
def a3(V):    return a30*np.exp( V/V3)
def b3(V):    return b30*np.exp(-V/V3)
def a4(V):    return a40*np.exp( V/V4)
def b4(V):    return b40*np.exp(-V/V4)


# Calcium flux through VDCC
def CaFlux(P, V):
    #P = 3.003 # from Bartol et al. 2015, Q10 = 1.55; 3.003 in Bischoffberger et al. 2003 # pA/mV
    C = 80.36 # mV
    D = 0.3933
    r = P*V*(D - np.exp(-V/C))/(1 - np.exp(V/C))*1e3 # Ms^{-1} assuming 1um^3 of cytosol
    return r


######################################################
### Generate voltage trace for a protocol with 
### number of AP: nap
### intra-burst spike interval: isi
### inter-burst interval: bg (burst gap)
### number pf bursts: nb
def getProtocolV(sol, isi, nap, bg=0, nb=1):
    #print(isi, bg, nb, nap)
    assert(isi >= 20), "ISI must be >= 20"

    tstep = 1e-5
    ti, tf = 0, ((nb-1)*((nap-1)*isi + bg) + nap*isi + 10.0 + tstep)*1e-3
    T = np.arange(ti, tf, tstep)

    Vtemp = sol[0][:2000] # 100 points = 1 ms

    V = np.array([])
    for nbb in range(nb):
        for i in range(nap):
            temp = np.full((isi-20)*100, -8.07890166e+01)
            V = np.concatenate((V, Vtemp, temp))

        if nbb != nb-1:
            bgap = np.full((bg-isi)*100, -8.07890166e+01)
            V = np.concatenate((V, bgap))
        
    temp = np.full((10)*100+1, -8.07890166e+01)
    V = np.concatenate((V, temp))
    #print(tf, T.shape, V.shape)
    
    return T, V

#############################################################333
def getProtocolV_spike_times(AP_trace, spike_times, total_dur):
    spike_times = np.array(spike_times)
    """
    AP_trace: AP trace
    spike_time: list of spike times (ms)
    total_dur: total duration of the protocol (ms)
    """

    assert(min(spike_times[1:] - spike_times[:-1]) >= 20), "ISI must be >= 20"
    # print(AP_trace, spike_times, total_dur)

    tstep = 1e-5 # 0.01 ms
    ti, tf = 0, total_dur*1e-3

    T = np.arange(ti, tf, tstep)
    V = np.full(total_dur*100, -8.07890166e+01)

    print(T.shape, V.shape, AP_trace.shape)

    for spike_time in spike_times:
        V[spike_time*100:(spike_time+20)*100] = AP_trace

    # print(tf, T.shape, V.shape)
    
    return T, V

def getProtocolV_old(sol, isi=20, n=2):
    assert(isi >= 20), "ISI must be >= 20"

    tstep = 1e-5
    ti, tf = 0, ((n-1)*isi+30.0 + tstep)*1e-3
    T = np.arange(ti, tf, tstep)

    Vtemp = sol[0][:2000] # 100 points = 1 ms

    V = np.array([])
    for i in range(n-1):
        temp = np.full((isi-20)*100, -8.07890166e+01)
        V = np.concatenate((V, Vtemp, temp)) 

    temp = np.full((10)*100+1, -8.07890166e+01)
    V = np.concatenate((V, Vtemp, temp)) 
    
    return T, V


