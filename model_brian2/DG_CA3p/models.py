from brian2 import *

#####################################################################
### Pinsky-Rinzel CA3 Model
CA3p_PR_params = {
    'Gna': 30.0*mS,
    'Gkdr': 15.0*mS, 
    'Gkca': 15.0*mS,
    'Gkahp': 0.8*mS,
    'Gca': 2.1*mS,
    'Gl': 0.1*mS,
    'Gc': 1*mS,
    'Vna': 60.0*mV,
    'Vk': -75.0*mV,
    'Vca': 80.0*mV,
    'Vl': -60.0*mV,
    'Vnmda': 3.5*mV,
    'Vdmpa': 0.0*mV,
    'p': 0.5,
    'Cm_PR': 3.0*uF,
    'Isapp': 0.0,
    'Idapp': 0.0,
    'Gmax_ampa':  1*msiemens,
    'G_gabaA':  1*msiemens,
    'G_gabaB':  3*msiemens
}

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
Isyn : amp

## ODEs
dVs/dt  = (- Ileaks - Ina - Ikdr - Ids/p)/Cm_PR : volt
dVd/dt  = (- Ileakd - Ica - Ikca - Ikahp - Isyn - Isd/(1-p))/Cm_PR : volt
dm/dt   = alphaM - m*(alphaM + betaM) : 1
dn/dt   = alphaN - n*(alphaN + betaN) : 1
dh/dt   = alphaH - h*(alphaH + betaH) : 1
ds/dt   = alphaS - s*(alphaS + betaS) : 1
dq/dt   = (qinf - q)/tauq : 1
dc/dt   = (cinf - c)/tauc : 1
dCa/dt  = (-0.13*Ica/uA - 0.075*Ca)/ms : 1
'''

#####################################################################
## MFB-CA3p synapse model
MFB_CA3p_syn_params = {
   'tau_AMPA': 2.0 * ms,  # AMPA receptor time constant
   'g_AMPA': 1 * mS,   # Maximum AMPA conductance
   'V_E': 0.0 * mV       # AMPA reversal potential
}

# Synapse model equations
eqs_MFB_CA3p_syn = '''
ds_AMPA/dt = -s_AMPA / tau_AMPA : siemens (clock-driven)
I_AMPA = s_AMPA * (Vd_post- V_E) : amp
Isyn_post = I_AMPA : amp (summed)
'''

# Presynaptic updates
MFB_CA3p_onpre = '''
s_AMPA += g_AMPA  # Increment conductance on vesicle release
'''