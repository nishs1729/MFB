from brian2 import *

#####################################################################
### Pinsky-Rinzel CA3 Model
### taken from: https://doi.org/10.1007/s10827-016-0606-8

CA3p_PR_params = {
    'Gna': 30.0*mS,
    'Gkdr': 15.0*mS, 
    'Gkca': 15.0*mS,
    'Gkahp': 0.8*mS,
    'Gca': 10*mS,
    'Gl': 0.1*mS,
    'Gc': 10*mS,
    'Vna': 60.0*mV,
    'Vk': -75.0*mV,
    'Vca': 80.0*mV,
    'Vl': -60.0*mV,
    'p': 0.75,
    'Cm': 3.0*uF,
    'Isapp': -0.5*uA, # background inhibition
    'Idapp': 0.0,
    'noise': 0.5*uA
}

eqnCA3_PR = '''
alphaM = 0.32*4/(exprel((-46.9 - Vs/mV)/4))/ms : Hz
betaM  = 0.28*5/(exprel((Vs/mV + 19.9)/5))/ms : Hz
alphaN = 0.016*5/(exprel((-24.9 - Vs/mV)/5))/ms : Hz
betaN  = 0.25*exp((-1 - 0.025*Vs/mV))/ms : Hz
alphaH = 0.128*exp((-43 - Vs/mV)/18)/ms : Hz
betaH  = 4/(1 + exp((-20 - Vs/mV)/5))/ms : Hz
alphaS = 1.6/(1 + exp(-0.072*(Vd/mV - 5)))/ms : Hz
betaS  = 0.02*5/exprel((Vd/mV + 8.9)/5)/ms : Hz
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
Iampa : amp
Inmda : amp

## ODEs
# dVs/dt  = (- Ileaks - Ina - Ikdr - Ids/p)/Cm : volt
# dVd/dt  = (- Ileakd - Ica - Ikca - Ikahp - Iampa - Inmda - Isd/(1-p))/Cm : volt
dVs/dt  = (- Ileaks - Ina - Ikdr - Ids/p - noise*sqrt(1/1*ms)*xi + Isapp)/Cm : volt
dVd/dt  = (- Ileakd - Ica - Ikca - Ikahp - Iampa - Inmda - Isd/(1-p) - noise*sqrt(1/1*ms)*xi_1)/Cm : volt
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
    'tau_AMPA': 5.0 * ms,      # AMPA receptor time constant
    'g_AMPA': 0.2 * mS,        # Maximum AMPA conductance
    'V_AMPA': 0.0 * mV,        # AMPA reversal potential
    'g_NMDA': 0.1 * mS,        # Maximum NMDA conductance
    'V_NMDA': 0.0 * mV,        # NMDA reversal potential
    'tau_NMDA_rise': 2.0 * ms,
    'tau_NMDA_decay': 100.0 * ms,
    'alpha': 0.5 / ms,
    'Mg2': 1.0
}

# Synapse model equations
eqs_MFB_CA3p_syn = '''
## AMPA model
ds_AMPA/dt = -s_AMPA / tau_AMPA : siemens (clock-driven)
I_AMPA = s_AMPA * (Vd_post - V_AMPA) : amp
Iampa_post = I_AMPA : amp (summed)

## NMDA model
I_NMDA = g_NMDA*(Vd_post - V_NMDA)/(1 + Mg2*exp(-0.062*Vd_post/mV)/3.57)*s_NMDA : amp
ds_NMDA / dt = - s_NMDA / tau_NMDA_decay + alpha * x * (1 - s_NMDA) : 1 (clock-driven)
dx / dt = - x / tau_NMDA_rise : 1 (clock-driven)
Inmda_post = I_NMDA : amp (summed)
'''

# Presynaptic updates
MFB_CA3p_onpre = '''
s_AMPA += g_AMPA  # Increment conductance on vesicle release
x += 1
'''