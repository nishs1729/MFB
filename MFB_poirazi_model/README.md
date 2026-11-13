# MFB vesicle release → Poirazi CA1 cell → EPSCs

This takes vesicle release times from the MCell mossy-fibre bouton (MFB) simulations
(`../data/*/*/vesData.dat`) and plays them into N synapses on the Poirazi et al. (2003) CA1
pyramidal cell. It is a trimmed, self-contained copy of the port in `../poirazi_model`. It
records the EPSC at every synapse and at the soma. The design and the decisions behind it
are in [PLAN.md](PLAN.md).

## Setup

You need NEURON 9.0.2, numpy and matplotlib (see `requirements.txt`). The venv in
`../poirazi_model/.venv` already has them:

```bash
PY=../poirazi_model/.venv/bin/python        # or your own env: pip install -r requirements.txt
```

The mechanisms in `mfb/mechanisms/` are compiled with `nrnivmodl` automatically on first
use, and again whenever a `.mod` file changes.

## Run

```bash
$PY run.py --ves ../data/control_buffer/nVDCC_9_dVDCC_220_nAZ_31_RRP_15_ISI_20_nAP_10_cb_45uM --plot
$PY run.py --ves <dir> --n-mfb 10 --reps 20 --seed 3            # 10 MFBs, 20 realisations
$PY run.py --ves <dir> --mode iclamp                            # EPSPs instead of a somatic clamp
$PY run.py --ves ../data/findPr/nVDCC_10_dVAZ_100_nAZ_11 --key 30   # flat file with several keys
$PY run.py --ves <dir> --site 'apical_dendrite[14](0.5)'        # fixed site instead of random
$PY plot.py results/<run>.npz [--rep 2]                          # figures from a saved run
$PY checks/sanity.py                                             # 7 checks, about 25 s
```

`$PY run.py -h` lists every option. Each run writes
`results/<data-dir>_N<n>_M<reps>_seed<s>_<mode>.npz`, plus a `.png` with `--plot`.
One repetition takes about 4.5 s (300 ms of simulated time at dt = 0.025 ms).

## What the model does

| | |
|---|---|
| **One MFB** | One MCell trial: every release from every AZ of that bouton, in that trial. |
| **N MFBs** | N different trials drawn at random (`--seed`). All boutons are driven by the same AP train, so they fire in synchrony, as intended. |
| **Release types** | sync + async + spont by default (`--types`). Flat-layout files (`control`, `findPr`) do not store the type, so they always use all releases. |
| **Placement** | Proximal apical trunk, 0–100 µm from the soma (`--dmin/--dmax`; the model's own distance metric). That is 12 segments, apical_dendrite[0]–[26]. Each MFB gets one segment, drawn at random with weights by segment length. Several MFBs may share a segment. The sites stay fixed for all repetitions of a run. |
| **Synapse** | `MFBSyn` (`mfb/mechanisms/mfbsyn.mod`). Each vesicle adds one quantum of AMPA and NMDA conductance, and the quanta sum linearly (no saturation, no dead time). Each component is a two-exponential conductance normalised so one vesicle peaks at exactly `gq`. NMDA has the Jahr–Stevens Mg²⁺ block. |
| **Defaults** (placeholders) | gq_AMPA 0.5 nS, τ 0.5 / 5 ms; NMDA peak 0.3 × AMPA, τ 3 / 70 ms; Mg 1 mM; E_rev 0 mV. |
| **vclamp** (default) | An SEClamp at the soma (soma[0]) holds −70 mV with Rs = 0.01 MΩ (`--v-hold`, `--rs`). Somatic EPSC = clamp current. |
| **iclamp** | No clamp. You get the local synaptic currents and the EPSPs at each synapse and at the soma. |
| **Repetitions** | `--reps M`. Each repetition uses new trials: without replacement across the whole run when N·M ≤ number of trials. All state is reset between repetitions, including [Ca]ᵢ, which the original carried over between runs. |
| **Run control** | dt 0.025 ms, tstop 300 ms, 34 °C, rest balanced to −70 mV (`current_balance`), fixed step. |

## Output (`.npz`)

Currents are in pA, with **inward = negative** (as a measured EPSC). Conductances are in nS,
voltages in mV and time in ms. `M` = repetitions, `N` = MFBs, `T` = samples.

| key | shape | |
|---|---|---|
| `t` | T | time |
| `soma_i_clamp` | M×T | somatic EPSC (vclamp only) |
| `soma_v` | M×T | somatic voltage |
| `soma_i_axial` | M×T | axial current from the trunk into the soma (both modes) |
| `syn_i_ampa`, `syn_i_nmda` | M×N×T | local EPSC components at each synapse |
| `syn_g_ampa`, `syn_g_nmda` | M×N×T | conductances (g_NMDA without the Mg block) |
| `syn_v` | M×N×T | voltage at each synapse's compartment |
| `syn_section`, `syn_x`, `syn_distance` | N | where each synapse sits |
| `trials` | M×N | trial index of each MFB in each repetition |
| `ev_rep, ev_syn, ev_trial, ev_t, ev_az, ev_type` | events | every delivered vesicle: AZ number (−1 if unknown) and type (0 sync, 1 async, 2 spont, −1 unknown) |
| `ap_times` | | AP times, 1.5 + k·ISI ms, parsed from `ISI_x_nAP_y` in the path (or `--isi/--n-ap`) |
| `config`, `meta` | | JSON strings: the full run configuration, units, data layout |

Large runs: the per-synapse traces take up most of the space. `--save-every k` keeps every
k-th sample.

Recorded `g_*`/`i_*` lag the synaptic state by one time step. This is the usual NEURON
behaviour for values computed in BREAKPOINT. Events themselves are delivered at their exact
release times.

## Sanity checks (`checks/sanity.py`)

| check | result |
|---|---|
| Soma input resistance of the trimmed cell | 59.6821 MΩ, same as the original `Rins.dat` |
| Rest without input | soma stays within 0.012 mV of −70 (the original model has this small transient) |
| One vesicle | peak g_AMPA = 0.500 nS, g_NMDA = 0.150 nS, delivered at the exact event time, rise times as designed; about −35 pA local and −25 pA somatic EPSC at 52 µm |
| Two simultaneous vesicles | conductance exactly 2×, somatic EPSC 1.9995× |
| Reset between repetitions | repeated runs are bit-identical, even after a spiking run in between |
| Event count | the loader finds every release in the file (54,087), and every loaded vesicle is delivered |

## Layout

```
run.py              CLI
plot.py             figures
checks/sanity.py    sanity checks
mfb/vesicles.py     vesData.dat loader (per-AZ and flat layouts), trial drawing
mfb/synapses.py     SynParams, placement, MFBSynapse (NetCon.event delivery)
mfb/experiment.py   MFBModel (cell + clamp + synapses + recordings), run_experiment
mfb/cell/           trimmed copy of ../poirazi_model/ca1: morphology, distance metric,
                    cell_setup biophysics, current_balance
mfb/mechanisms/     15 original channel .mod files (unchanged) + mfbsyn.mod
```

## Using it from Python

```python
import numpy as np
from mfb.experiment import MFBModel
m = MFBModel(mode="vclamp")
m.add_synapses(["apical_dendrite[14](0.5)", "apical_dendrite[25](0.5)"])
r = m.run([np.array([10.0, 10.0, 12.5]), np.array([30.0])], tstop=100)   # release times in ms
r["soma_i_clamp"], r["syn_i_ampa"]
```

## Limitations

- This is a CA1 morphology and channel set receiving MF-like input, not a CA3 cell. The
  model has no spines.
- The absolute EPSC sizes depend entirely on the quantal parameters, which are placeholders.
- In vclamp the dendrites are not space-clamped. NMDA and the active dendritic channels see
  real depolarisation, and with enough synchronous input the dendrite (or, in iclamp, the
  cell) fires.
- In flat-layout files the AZ identity and the release type are lost.
