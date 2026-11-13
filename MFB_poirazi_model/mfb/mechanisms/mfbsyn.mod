COMMENT
MFBSyn: event-driven quantal AMPA + NMDA synapse for vesicle-release input.

Written for MFB_poirazi_model (not part of the original Poirazi et al. 2003 model).

Every NET_RECEIVE event is one released vesicle. It adds one quantum of AMPA and
NMDA conductance (weight = number of vesicles, normally 1). The quanta sum
linearly, so k vesicles arriving together give k times the conductance. There is
no saturation and no dead time.

Each component is a two-exponential (rise/decay) conductance, normalised so that
one vesicle gives a peak of exactly gq_ampa (AMPA) and nmda_ratio*gq_ampa (NMDA,
before the Mg block):

  g_ampa = A2 - A1,   g_nmda = B2 - B1
  i_ampa = g_ampa * (v - e)
  i_nmda = g_nmda * mgblock(v) * (v - e)
  mgblock(v) = 1 / (1 + exp(-0.062 v) * mg / 3.57)      (Jahr & Stevens 1990)

Conductances are in uS (NEURON convention for point processes); currents in nA,
negative = inward. The Python side sets and reports them in nS / pA.
nev counts the vesicles received (for checking event delivery).
ENDCOMMENT

NEURON {
	POINT_PROCESS MFBSyn
	RANGE gq_ampa, tau_r_ampa, tau_d_ampa
	RANGE nmda_ratio, tau_r_nmda, tau_d_nmda, mg, e
	RANGE g_ampa, g_nmda, i_ampa, i_nmda, mgblock, nev
	NONSPECIFIC_CURRENT i
	THREADSAFE
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
	(mM) = (milli/liter)
}

PARAMETER {
	gq_ampa = 0.0005 (uS)    : peak AMPA conductance of one vesicle (0.5 nS)
	tau_r_ampa = 0.5 (ms)
	tau_d_ampa = 5 (ms)
	nmda_ratio = 0.3 (1)     : peak g_NMDA / peak g_AMPA of one vesicle (no Mg block)
	tau_r_nmda = 3 (ms)
	tau_d_nmda = 70 (ms)
	mg = 1 (mM)
	e = 0 (mV)
}

ASSIGNED {
	v (mV)
	i (nA)
	i_ampa (nA)
	i_nmda (nA)
	g_ampa (uS)
	g_nmda (uS)
	mgblock (1)
	f_ampa (1)
	f_nmda (1)
	nev (1)
}

STATE {
	A1 (uS)
	A2 (uS)
	B1 (uS)
	B2 (uS)
}

INITIAL {
	if (tau_r_ampa / tau_d_ampa > 0.9999) { tau_r_ampa = 0.9999 * tau_d_ampa }
	if (tau_r_nmda / tau_d_nmda > 0.9999) { tau_r_nmda = 0.9999 * tau_d_nmda }
	f_ampa = peaknorm(tau_r_ampa, tau_d_ampa)
	f_nmda = peaknorm(tau_r_nmda, tau_d_nmda)
	A1 = 0
	A2 = 0
	B1 = 0
	B2 = 0
	nev = 0
}

BREAKPOINT {
	SOLVE state METHOD cnexp
	g_ampa = A2 - A1
	g_nmda = B2 - B1
	mgblock = 1 / (1 + exp(0.062 (/mV) * -v) * (mg / 3.57 (mM)))
	i_ampa = g_ampa * (v - e)
	i_nmda = g_nmda * mgblock * (v - e)
	i = i_ampa + i_nmda
}

DERIVATIVE state {
	A1' = -A1 / tau_r_ampa
	A2' = -A2 / tau_d_ampa
	B1' = -B1 / tau_r_nmda
	B2' = -B2 / tau_d_nmda
}

FUNCTION peaknorm(tr (ms), td (ms)) (1) {
	LOCAL tp
	tp = (tr * td) / (td - tr) * log(td / tr)
	peaknorm = 1 / (-exp(-tp / tr) + exp(-tp / td))
}

NET_RECEIVE(weight (1)) {
	A1 = A1 + weight * gq_ampa * f_ampa
	A2 = A2 + weight * gq_ampa * f_ampa
	B1 = B1 + weight * nmda_ratio * gq_ampa * f_nmda
	B2 = B2 + weight * nmda_ratio * gq_ampa * f_nmda
	nev = nev + weight
}
