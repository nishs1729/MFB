# Plan: MFB vesicle release → Poirazi CA1 cell → EPSCs

Goal: use the vesicle release times simulated for N mossy-fibre boutons (MFBs) as the
input to N synapses on the Poirazi et al. (2003) cell (Python/NEURON port in
`../poirazi_model`), then record the EPSC at every synapse compartment and at the soma.

**Status (2026-11-13): implemented.** See README.md. The decisions are recorded in section 4,
in square brackets. Differences from this plan are listed in section 6.

---

## 1. Input data (checked on the example file)

`data/control_buffer/nVDCC_9_dVDCC_220_nAZ_31_RRP_15_ISI_20_nAP_10_cb_45uM/vesData.dat`
is a pickle with this structure (written by `model_mcell/control_buffer/run.py`):

```
{ 'AZ1': {'sync': [trial_0, ..., trial_1999], 'async': [...], 'spont': [...]},
  ...
  'AZ31': {...} }
trial_k = list of release times in **seconds**
```

- 31 AZs × 2000 trials. In total there are 13,653 sync, 40,370 async and 64 spont releases.
- Per trial, summed over all AZs and all three types: mean 27 releases, range 10–47.
- Release times run from 2.45 to 209.85 ms. The 10 APs are at 1.5 + 20·k ms, so ISI = 20 ms.
- One AZ can release up to 6 vesicles of one type in one trial. The synapse model therefore
  has to handle several vesicles arriving close together.

Other folders use a different layout. In `data/control/*/vesData.dat` it is
`{'<RRP>': [trial_0, ...]}`, a single key with the 31 AZs already merged. `data/findPr/*` has
12 keys. The loader will detect the layout, and the path will be a command-line argument.

**Meaning of one MFB:** I assume one trial is one bouton. That bouton's release times are all
releases from all of its AZs in that trial. This matches how `scripts_analysis/analysis.py`
(`relStat`) merges the data. N MFBs is then N trials drawn from the file.

---

## 2. Proposed layout (minimal)

```
MFB_poirazi_model/
  PLAN.md, README.md, NOTICE.md     (NOTICE: attribution to Poirazi et al. + source commit)
  run.py                            CLI: python run.py --ves PATH --n-mfb N [--mode vclamp] ...
  plot.py                           EPSC figures from a results file
  mfb/
    vesicles.py                     load_mfb_trains(path, n, ...) -> list of arrays (ms)
    synapses.py                     synapse placement and event delivery
    experiment.py                   build cell, add synapses and recordings, run, save .npz
    cell/                           trimmed copy of the cell from ../poirazi_model
      data/morphology.json, section_lists.json
      build.py, biophys.py, balance.py, hoc_compat.py
    mechanisms/                     15 channel .mod files (unchanged) + 1 new synapse .mod
  results/
```

What is left out of the port: tuning, `tunings.dat`, the 5 original experiments, the
GLU/NMDA/GABA/d3 mechanisms, plotting of the old figures, and tests other than one sanity
check.

---

## 3. Implementation steps

1. **Trimmed cell copy.** Copy only what builds the cell: morphology, section lists,
   distance metric, `cell_setup` biophysics and `current_balance`. Compile the 15 channel
   mechanisms.
   *Check:* soma input resistance is 59.68 MΩ, the same as the full port and the original
   `Rins.dat`. This shows that nothing was lost in the copy.
2. **Vesicle loader** (`vesicles.py`).
   - Read the pickle and detect which layout it uses.
   - Choose N trials, either the first N or N at random with a seed.
   - Choose which release types to include (sync / async / spont).
   - Convert seconds to ms and sort the times.
   - Optionally keep each release's AZ id and type, for later analysis.
   - *Check:* the number of events delivered to the model equals the number of releases in
     the file.
3. **Synapse mechanism.** Write one new small `.mod` file with an event-driven AMPA + NMDA
   synapse.
   - AMPA: two-exponential conductance.
   - NMDA: two-exponential conductance with voltage-dependent Mg²⁺ block.
   - Each vesicle is one event that adds one quantal conductance, so vesicles sum linearly.
     Multiple vesicles arriving together are handled correctly.
   - The AMPA and NMDA currents are recorded separately.
   - Events are queued directly with `NetCon.event(t)`. This NEURON build has no `VecStim`,
     and this way no extra mechanism is needed.
4. **Placement** (`synapses.py`).
   - Each MFB becomes one AMPA+NMDA pair at one location. The whole bouton (all of its AZs)
     sits on one compartment.
   - Because the conductances sum linearly, this is exactly equivalent to 31 separate
     synapses at the same spot.
   - The placement rule is set by decision 4.1.
   - Several MFBs that land in the same compartment are allowed. Each keeps its own recorded
     current.
5. **Recording and run** (`experiment.py`).
   - For each synapse: AMPA and NMDA currents and conductances, plus the voltage of its
     compartment.
   - At the soma: membrane voltage, and the clamp current when in voltage-clamp mode.
   - Settings: dt = 0.025 ms, tstop = 300 ms, celsius = 34, rest balanced to −70 mV as in the
     original.
   - Save one `.npz` file per run, containing the traces, synapse locations (section, x,
     distance) and the full run configuration.
6. **Repetitions.** Run M independent realisations, each with a different set of N trials.
   Reset the cell's state between runs.
7. **Plots.** Somatic EPSC, the local EPSC at each synapse, the AMPA vs NMDA split, and the
   mean ± sd over repetitions, all aligned to the 10 APs.
8. **Sanity checks**, written as a small script:
   - A single vesicle gives the intended quantal EPSC amplitude and kinetics.
   - Two vesicles at the same time give twice the current (linearity).
   - The event count matches the file (from step 2).

---

## 4. Decisions I need from you

**4.1 Where should the synapses go?**
- **The caveat:** mossy fibres contact CA3 pyramidal cells, on thorny excrescences in
  stratum lucidum, close to the soma. This model is a CA1 cell, and it has no spines (see the
  earlier explanation). [ignore it]
- My proposal is to treat the proximal apical trunk (≤ ~100 µm from the soma, about 10
  sections from ~41 µm) as the "stratum lucidum". [use this]
- Alternatives:
  - (b) Soma + proximal trunk + proximal basal.
  - (c) An explicit list of (section, x) positions that you provide.
  - (d) Random positions over the whole dendrite.

**4.2 N and which trials.** How many MFBs: one value, or a sweep? For context, a CA3
pyramidal cell receives roughly tens of MF inputs. Should the trials be the first N, or N
random trials with a seed? [N random trials with a seed. To begin, keep N = 1]

**4.3 Which release types?** My default is sync + async + spont, i.e. everything the bouton
releases. Other options are sync only, or a choice per type. [use default]

**4.4 Timing across boutons.** In the file every bouton is driven by the same AP train. As-is,
the N granule cells therefore fire in perfect synchrony. Is that what you want, or should
each MFB get a random offset or jitter? [this is what I want]

**4.5 Synapse model and parameters.**
- I recommend the new event-driven quantal synapse from step 3. [implement this]
- The original Poirazi GLU/NMDA does not fit vesicle input:
  - Every trigger opens the same saturating 1.1 ms transmitter pulse, so 2, 5 or 10 vesicles
    give the same response.
  - Triggers that arrive within the dead time are dropped.
  - The original tuning to a 5 mV EPSP at each location has no meaning for single quanta.
- Parameters I need (I would use MF→CA3-like placeholders until you give values):
  - Quantal AMPA conductance (order of 0.5–1 nS).
  - AMPA rise/decay (about 0.5 / 5 ms).
  - NMDA/AMPA ratio and NMDA rise/decay (about 3 / 50–100 ms).
  - Mg²⁺ = 1 mM.
- Optional: a slow kainate component, which is characteristic of the MF synapse.
- [Decided: use the MF-like placeholders: gq_AMPA 0.5 nS, 0.5/5 ms; NMDA 0.3×, 3/70 ms;
  Mg 1 mM; no kainate. All of them are CLI flags.]

**4.6 What "EPSC" means here.** The model normally runs in current clamp, so this needs a
definition:
- **(a) Voltage clamp at the soma (recommended default).** An SEClamp holds −70 mV. [use this]
  - Somatic EPSC = the clamp current. This is what a patch experiment measures, including
    space-clamp error for dendritic inputs.
  - Local EPSC = the synaptic current at each synapse, under the same clamp.
- **(b) Current clamp.** Local EPSC = the synaptic current, and you also get EPSPs at the
  synapse and at the soma. There is no "somatic EPSC" as such. The nearest equivalent is the
  axial current flowing from the dendrite into the soma, which I can record if wanted.
- I can make the mode a flag and support both. [Decided: both, `--mode vclamp` by default.]
- **Related:** with many synchronous MFBs, the cell (or, under the clamp, the dendrites) may
  fire Na⁺/Ca²⁺ spikes. Should there be an option to block Na⁺ (TTX/QX-314-like) or all active
  conductances (passive cell)? [Decided: no blocker flags.]

**4.7 Repetitions.** How many independent realisations M per data file? Is it acceptable to
reset all state between runs? Resetting removes the original's `cai` carry-over (ISSUES I6 in
the port), so runs become independent. [Decided: `--reps M`, default 1, full reset.]

**4.8 Code reuse.** I recommend a **trimmed copy** of the cell code, so the directory is fully
self-contained. The alternative is to import `ca1` from `../poirazi_model`: less duplicated
code, but the two directories stay coupled. [use trimmed copy as recommended]

**4.9 Time step.** dt = 0.025 ms (recommended: AMPA rises in about 0.5 ms, and release times
have 0.05 ms resolution) versus the original's 0.1 ms. Event times are rounded to the dt grid
either way. [Decided: 0.025 ms, the recommendation.]

---

## 5. Known difficulties and limitations

- **Cell type mismatch** (4.1). The results describe MF-like input onto a CA1 morphology and
  channel set, not a CA3 cell. The CA1 channel gradients (I_h, A-type K⁺) at proximal sites are
  close to their somatic values, so this matters less for proximal placement. It is still not
  a CA3 model. [ignore]
- **No spines.** Without thorny excrescences, synapses sit directly on the dendritic shaft. No
  spine-neck filtering is modelled; this is probably minor for the large MF spine complexes. [ignore]
- **Space clamp.** In mode (a), dendritic voltage is not held. The somatic EPSC is filtered,
  and NMDA and active channels in the dendrites see real depolarisation. This is realistic, but
  it should be kept in mind when comparing local and somatic currents.
- **Quantal parameters drive the result.** The model's original synaptic tuning cannot be
  reused, so the absolute EPSC sizes depend entirely on the values chosen in 4.5.
- **Data formats differ between folders** (section 1). This is handled in the loader. Older
  layouts lose the AZ identity of each release, which only matters for per-AZ analysis.
- **Runtime.** It should be small: 331 compartments, 300 ms, dt = 0.025 ms gives 12,000 steps,
  which I expect to take seconds per run. I have not measured it yet.
---

## 6. Differences between the implementation and this plan

- **Placement window.** "≤ 100 µm" includes apical_dendrite[0](0.25) at 13 µm. That gives 12
  segments in 10 sections, not "from ~41 µm". Segments are drawn weighted by length, and the
  sites stay fixed across the repetitions of one run. `--dmin`, `--dmax` and `--site` change
  this.
- **Clamp.** Rs = 0.01 MΩ (near-ideal), at soma[0](0.5), the section the original treats as
  "soma".
- **Extra recording.** The axial current from the trunk into the soma (`soma_i_axial`) is
  recorded in both modes.
- **Runtime.** Measured: about 4.5 s per repetition (the estimate above said "seconds").
