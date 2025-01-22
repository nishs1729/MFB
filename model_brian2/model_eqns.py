from brian2 import *


#################################
## Mossy fiber bouton (MFB)
Ca0 = 0.1
tau_bCa = 200*ms
tau_syncRel = 1*ms
tau_asyncRel = 100*ms
tau_rrp = 1000*ms
tau_V = 1*ms

## MFB model equations
eqnMFB = '''
dV/dt = -V/tau_V : 1
dbCa/dt = V/tau_V/10 + (Ca0 - bCa)/tau_bCa : 1
drrp/dt = -V/tau_V/30 + (1 - rrp)/tau_rrp : 1

dsyncRel/dt = rrp*bCa*720*V/tau_V - syncRel/tau_syncRel : 1
dasyncRel/dt = rrp*bCa*34*V/tau_V - asyncRel/tau_asyncRel : 1
'''


#################################
## CA3 neuron (Leaky-Integrate)
V_L = -60.0*mV
V_thr = -42.0*mV
V_reset = -65.0*mV

Cm = 0.025*nF # membrane capacitance
gm = 0.5*nS  # membrane leak
tau_rp = 1.0*ms # refractory period 

gmax_ampa = 1*nsiemens # max AMPA conductance
tau_g_ampa = 10*ms
tau_d = 50*ms # desensitisation
tau_x = 1*ms # on_pre effector

tau_nt = 1*ms

A1, A2 = 5/(mM*ms), 0.18/ms
g_gabaA = 1*nsiemens
V_gabaA = -85*mV

B1, B2 = 0.09/(mM*ms), 0.0012/ms
K1, K2 = 0.18/ms, 0.034/ms
g_gabaB = 3*nsiemens
V_gabaB = -95*mV

## v: mambrane potential
## x: on_pre effector. Upon stimulation changes g_ampa and ampa desensitisation (d)
## d: implements ampa desensitisation
eqnCA3 = '''
dv/dt = (- gm*(v - V_L) - I_ampa - I_gabaA - I_gabaB) / 
        Cm + sigma/sqrt(1*ms)*xi*mV: volt (unless refractory)

dx/dt = -x/tau_x : 1
I_ampa = gmax_ampa*g_ampa*d*v : amp
dg_ampa/dt = x/tau_x + -g_ampa/tau_g_ampa : 1
dd/dt = -x/tau_x/5 + (1-d)/tau_d : 1

I_gabaA = g_gabaA*f_gabaA*(v - V_gabaA) : amp
df_gabaA/dt = A1*nt*(1 - f_gabaA) - A2*f_gabaA : 1

I_gabaB = g_gabaB * G**4/(G**4+100)*(v - V_gabaB) : amp
df_gabaB/dt = B1*nt*(1 - f_gabaB) - B2*f_gabaB : 1
dG/dt = K1*f_gabaB - K2*G: 1

nt : mM
'''

#################################
### Pinsky-Rinzel CA3 Model
Gna, Gkdr, Gkca, Gkahp, Gca, Gl, Gc = 30.0*mS, 15.0*mS, 15.0*mS, 0.8*mS, 2.1*mS, 0.1*mS, 0.18*mS
Vna, Vk, Vca, Vl, Vnmda, Vdmpa = 60.0*mV, -75.0*mV, 80.0*mV, -60.0*mV, 3.5*mV, 0.0*mV
p, Cm_PR, Isapp, Idapp = 0.5, 3.0*uF, 0.0, 0.0
Gmax_ampa = 1*msiemens
G_gabaA = 1*msiemens
G_gabaB = 3*msiemens

z0, z1, z2, z3, z4, z5, z6, z7, z8 = 1,1,1,1,1,1,0,0,0
eqnCA3_PR = '''
alphaM = 0.32*4/(exprel((13.1 - Vs/mV)/4))/ms : Hz
betaM  = 0.28*5/(exprel((Vs/mV + 40.1)/5))/ms : Hz
alphaN = 0.016*5/(exprel((35.1 - Vs/mV)/5))/ms : Hz
betaN  = 0.25*exp((0.5 - 0.025*Vs/mV))/ms : Hz
alphaH = 0.128*exp((17 - Vs/mV)/18)/ms : Hz
betaH  = 4/(1 + exp((40 - Vs/mV)/5))/ms : Hz
alphaS = 1.6/(1 + exp(-0.072*(Vd/mV - 65)))/ms : Hz
betaS  = 0.02*5/exprel((Vd/mV - 51.1)/5)/ms : Hz
qinf   = 0.7894*exp(0.0002726*Ca) - 0.7292*exp(-0.01672*Ca) : 1
tauq   = (657.9*exp(-0.02023*Ca) + 301.8*exp(-0.002381*Ca))*ms : second
cinf   = 1.0/(1.0 + exp((-10.1 - Vd/mV)/0.1016))**0.00925 : 1
tauc   = 3.627*exp(0.03704*Vd/mV)*ms : second
chi    = 1.073*sin(0.003453*Ca + 0.08095) +
         0.08408*sin(0.01634*Ca - 2.34) + 
         0.01811*sin(0.0348*Ca - 0.9918) : 1

         
## Currents
Ina    = Gna*m**2*h*(Vs - Vna) : amp
Ikdr   = Gkdr*n*(Vs - Vk) : amp
Ica    = Gca*s**2*(Vd - Vca) : amp
Ikca   = Gkca*c*chi*(Vd - Vk) : amp
Ikahp  = Gkahp*q*(Vd - Vk) : amp
Isd    = Gc*(Vd - Vs) : amp
Ids    = -Isd : amp
Ileakd = Gl*(Vd - Vl) : amp
Ileaks = Gl*(Vs - Vl) : amp


## ODEs
dVs/dt  = z0*(- Ileaks - Ina - Ikdr - Ids/p)/Cm_PR : volt
dVd/dt  = z1*(- Ileakd - Ica - Ikca - I_ampa - I_gabaA - I_gabaB - Ikahp - Isd/(1-p))/Cm_PR : volt
dm/dt   = z2*(alphaM - m*(alphaM + betaM)) : 1
dn/dt   = z3*(alphaN - n*(alphaN + betaN)) : 1
dh/dt   = z4*(alphaH - h*(alphaH + betaH)) : 1
ds/dt   = z5*(alphaS - s*(alphaS + betaS)) : 1
dq/dt   = z6*(qinf - q)/tauq : 1
dc/dt   = z7*(cinf - c)/tauc : 1
dCa/dt  = z8*(-0.13*Ica/uA - 0.075*Ca)/ms : 1


dx/dt = -x/tau_x : 1
## AMPA model
I_ampa = Gmax_ampa*g_ampa*d*Vd : amp
dg_ampa/dt = x/tau_x + -g_ampa/tau_g_ampa : 1
dd/dt = -x/tau_x/5 + (1-d)/tau_d : 1

nt : mM
## GABA_A model
I_gabaA = G_gabaA*f_gabaA*(Vd - V_gabaA) : amp
df_gabaA/dt = A1*nt*(1 - f_gabaA) - A2*f_gabaA : 1

## GABA_B model
I_gabaB = G_gabaB * G**4/(G**4+100)*(Vd - V_gabaB) : amp
df_gabaB/dt = B1*nt*(1 - f_gabaB) - B2*f_gabaB : 1
dG/dt = K1*f_gabaB - K2*G: 1
'''


#################################
## Inhibitory Interneuron
Cm_in = 0.1*nF # membrane capacitance
gm_in = 4.0*nS # membrane leak
tau_rp_in = 1*ms # refractory period
Vin_rest = -57.0*mV
Vin_thr, Vin_reset = -50.0*mV, -60.0*mV
gInmax_ampa = 3*nS
tau_gIn_ampa = 5*ms

eqnIn = '''
dv/dt = (- gm_in*(v - Vin_rest) - I_ampa)/Cm_in + sigma*sqrt(1/(1*ms))*xi*mV: volt (unless refractory)
I_ampa = gInmax_ampa*gIn_ampa*v : amp
dgIn_ampa/dt = -gIn_ampa/tau_gIn_ampa : 1
'''

#################################
# Synapse
eqnSIn = '''
dnT/dt = -nT/tau_nt: mM (clock-driven)
nt_post = nT : mM (summed) '''

