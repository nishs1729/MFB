# NOTICE

`mfb/cell/` and the 15 channel mechanisms in `mfb/mechanisms/` are a trimmed copy of the
Python/NEURON port in `../poirazi_model`. That port reproduces the CA1 pyramidal neuron
model of Poirazi, Brannon & Mel (2003), originally written in HOC/NMODL for NEURON 5.x:

- Original model: https://github.com/Poirazi-Lab/Poirazi_CA1_detailed
- Source commit: `d2013e754a7e1a5801392f8bc363446f75f28123`

The model, its morphology, mechanisms and parameters are the work of Panayiota (Yiota)
Poirazi, Terrence Brannon and Bartlett W. Mel. Several `.mod` files credit further authors
in their headers, which are kept unchanged. Please cite:

1. Poirazi P, Brannon T, Mel BW (2003a). Arithmetic of subthreshold synaptic summation in a
   model CA1 pyramidal cell. *Neuron* 37:977–987.
2. Poirazi P, Brannon T, Mel BW (2003b). Pyramidal neuron as two-layer neural network.
   *Neuron* 37:989–999.

## What was copied, and what changed

- **Copied unchanged:** `morphology.json`, `section_lists.json`, `biophys.py` (port of
  `cell_setup`), `balance.py`, `distance.py` and `hoc_compat.py`, apart from import paths.
  Also the `.mod` files `cad cagk calH cal car cat h hha2 hha_old kadist kaprox kca km nap
  somacar`.
- **Trimmed:** `params.py` keeps only `CellParams`. `build.py` merges `morphology.py` and
  `cell.py` and drops the block procedures.
- **Left out:** tuning and `tunings.dat`, the original experiments, the GLU/NMDA/GABAa/GABAb
  synapses, and `d3.mod`.
- **New:** `mfbsyn.mod` (quantal AMPA+NMDA synapse) and everything outside `mfb/cell/`.
- **Behavioural difference from the original:** [Ca]ᵢ is reset before every run (see
  `../poirazi_model/ISSUES.md`, I6). The cell itself is unchanged: the soma input resistance
  is 59.6821 MΩ, as in the original.
