import matplotlib.pyplot as plt
from brian2 import *
import numpy as np


def visualise_connectivity(S):
    """
    Visualize the connectivity of a Synapses object (brian2) as a graph and a connectivity matrix.

    Parameters
    ----------
    S : Synapses
        The Synapses object to be visualized.

    Returns
    -------
    None
    """
    Ns = len(S.source)
    Nt = len(S.target)
    shift = (Nt - Ns)/2.0

    f, axs = plt.subplots(1, 2, figsize=(8, 4))
    f.subplots_adjust(wspace=0.1, hspace=0)

    ## Connectivity graph
    for i, j in zip(S.i, S.j):
        axs[0].plot([0, 1], [i+shift, j], '-', c='gray', lw=1)
    axs[0].plot(np.zeros(Ns), np.arange(Ns)+shift, 'om', ms=7)
    axs[0].plot(np.ones(Nt), range(Nt), 'og', ms=7)
    
    for i in S.i: # Source neuron index
        axs[0].text(-0.1, i-0.2+shift, i)

    for j in S.j: # Target neuron index
        axs[0].text(1.07, j-0.2, j)

    axs[0].spines[["right","top","left","bottom"]].set_visible(False)
    axs[0].tick_params(axis=u'both', which=u'both', length=0, labelsize=10)
    axs[0].set_xticks([0, 1], ['Source', 'Target'])
    axs[0].set_yticks([], [])
    axs[0].set_xlim(-0.1, 1.1)

    ## Connectivity matrix
    c = np.zeros((Nt, Ns))
    for s,t in zip(S.i, S.j):
        c[t,s] = 1
    axs[1].imshow(c, cmap="Greys", origin='lower')
    axs[1].set_xlabel('Source')
    axs[1].set_ylabel('Target')
    axs[1].set_title("Connectivity matrix", fontsize=10)
    axs[1].set_xticks(np.arange(c.shape[1]+1)-0.5, minor=True)
    axs[1].set_yticks(np.arange(c.shape[0]+1)-0.5, minor=True)
    axs[1].grid(which="minor", color="black", linestyle='-', linewidth=1, alpha=0.2)
    axs[1].tick_params(which="both", bottom=False, left=False)
    
    f.tight_layout()
    plt.show()


if __name__ == '__main__':
    pass