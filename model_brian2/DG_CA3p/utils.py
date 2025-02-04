from models import *
from brian2 import *

def run_sim(nMFB, spid, sptimes, tstep=0.1):
    defaultclock.dt = tstep*ms
    start_scope()

    MFBvrel = SpikeGeneratorGroup(nMFB, spid, sptimes*ms)


    MFB_CA3p_syn_params['g_AMPA'] = 0.1 * mS
    nCA3p = nMFB
    CA3p = NeuronGroup(nCA3p, eqnCA3_PR, 
                    method='exponential_euler', 
                    threshold='Vs>0*mV', 
                    refractory='Vs>0*mV', 
                    namespace=CA3p_PR_params)
    CA3p.Vd = -61.3 * mV
    CA3p.Vs = -61.2 * mV

    # Synapse: MFB to CA3 pyramidal neuron
    MFB_CA3p_syn = Synapses(MFBvrel, CA3p,
                            model=eqs_MFB_CA3p_syn,
                            on_pre=MFB_CA3p_onpre,
                            method='exponential_euler',
                            namespace=MFB_CA3p_syn_params)
    MFB_CA3p_syn.connect(j='i')

    # Monitors
    stMCA3p = StateMonitor(CA3p, ['Vd', 'Vs', 'Isyn'], record=True)
    spMCA3p = SpikeMonitor(CA3p)

    # Run the simulation
    run(1210 * ms)

    return stMCA3p, spMCA3p

def test_plot(stMCA3p, spMCA3p, vrel_times):
    fig, axes = plt.subplots(2, 2, figsize=(10, 5))
    fig.subplots_adjust(wspace=0.2, hspace=0.15)
    # fig.suptitle("Simulation Results")

    ## Plot the CA3 spikes
    axes[0,0].plot(stMCA3p.t/ms, stMCA3p.Vd[0]/mV, 'b-', label='Vd')
    axes[0,0].plot(stMCA3p.t/ms, stMCA3p.Vs[0]/mV, 'r-', label='Vs')
    axes[0,0].set_xlabel("Time (ms)")
    axes[0,0].set_ylabel("Membrane Potential (mV)")
    axes[0,0].legend(frameon=False)

    ## Plot the synaptic current
    axes[0,1].plot(stMCA3p.t/ms, -stMCA3p.Isyn[0]/uA, 'b-', label='Isyn')
    axes[0,1].set_xlabel("Time (ms)")
    axes[0,1].set_ylabel(r"AMPA current ($\mu$A)")
    axes[0,1].legend(frameon=False)

    ## Raster plot of the CA3 spikes
    CA3p_sptimes = [a/ms for a in spMCA3p.spike_trains().values()]
    # axes[1,0].plot(spMCA3p.t/ms, spMCA3p.i, 'k.', markersize=2)
    axes[1,0].eventplot(CA3p_sptimes)

    ## Raster plot of the MFB vesicle releases
    axes[1,1].eventplot(vrel_times)

    for ax in axes.ravel():
        # ax.set_xlim(0, runt)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.tick_params(axis=u'both', which=u'both', length=2, labelsize=8)
        ax.set_xlim(1000, 1210)

    plt.tight_layout()
    plt.show()

def check_multiple_rel(spike, tstep=0.1):
    diff = spike[1:] - spike[:-1]
    if any(diff <= tstep):
        idx = np.where(diff <= tstep)
        # print(idx, diff)
        # print(spike)
        for i in idx:
            spike[i+1] = spike[i+1] + tstep*1.1
        return False
    else:
        return True

def get_spike_generator_info(spikes):
    spid, sptimes = [], []
    for n, spike in enumerate(spikes):
        spike = np.sort(spike)
        check_multiple_rel(spike)
        # if not check_multiple_rel(spike):
            # print(spike,'\n')

        spid += np.full((len(spike)), n).tolist()
        sptimes += spike.tolist()

    return len(spikes), spid, [float(a) for a in sptimes]
