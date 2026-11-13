"""Sanity checks for the trimmed cell, the synapse and the vesicle loader.

    python checks/sanity.py [--ves PATH]

Each check runs in its own Python process (NEURON state is global).
"""
from __future__ import annotations

import argparse
import json
import pickle
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DEFAULT_VES = ROOT.parent / "data/control_buffer/nVDCC_9_dVDCC_220_nAZ_31_RRP_15_ISI_20_nAP_10_cb_45uM"
SITE = "apical_dendrite[14](0.5)"


# ----------------------------------------------------------------------------- checks
def check_rin(_):
    """Soma input resistance = 59.6821 MOhm (original Rins.dat; H_current.hoc protocol)."""
    from neuron import h
    from mfb.cell import Cell
    c = Cell()
    ic = h.IClamp(c.soma(0.5))
    ic.delay, ic.dur, ic.amp = 10.0, 300.0, -0.2
    v = h.Vector().record(c.soma(0.5)._ref_v)
    h.cvode_active(0)
    h.celsius, h.dt, h.steps_per_ms, h.tstop = 34.0, 0.1, 10.0, 310.0
    h.setdt()
    h.finitialize(-70.0)
    h.fcurrent()
    h.continuerun(310.0)
    rin = (v[v.size() - 1] - v[int(10.0 / 0.1)]) / ic.amp
    return abs(rin - 59.6821) < 5e-5, f"R_in soma = {rin:.4f} MOhm (original 59.6821)"


def _model(mode="vclamp", sites=(SITE,)):
    from mfb.experiment import MFBModel
    m = MFBModel(mode=mode)
    m.add_synapses(list(sites))
    return m


def check_rest(_):
    """No vesicles: the cell stays at -70 mV.

    The original model itself has a small transient (soma dips 0.012 mV near 50 ms and
    recovers; the same at dt = 0.1), hence the 0.02 mV tolerance.
    """
    import numpy as np
    r1 = _model("iclamp").run([np.empty(0)], tstop=200.0)
    vmin, vmax = r1["soma_v"].min(), r1["soma_v"].max()
    ok = -70.02 < vmin <= vmax < -69.98
    return ok, f"iclamp: soma V in [{vmin:.4f}, {vmax:.4f}] mV"


def check_rest_vclamp(_):
    import numpy as np
    r = _model("vclamp").run([np.empty(0)], tstop=200.0)
    imax = np.abs(r["soma_i_clamp"]).max()
    return imax < 0.5, f"vclamp: |clamp current| <= {imax:.3f} pA"


def check_quantal(_):
    """One vesicle at t=10 ms: peak g_AMPA = gq, peak g_NMDA = ratio*gq, correct timing."""
    import numpy as np
    from mfb.synapses import SynParams
    from neuron import h
    p = SynParams()
    m = _model()
    a2 = h.Vector().record(m.synapses[0].syn._ref_A2)   # AMPA decay state
    r = m.run([np.array([10.0])], tstop=100.0)
    t, ga, gn = r["t"], r["syn_g_ampa"][0], r["syn_g_nmda"][0]
    # The event is delivered at t = 10: the state jumps in the step 10 -> 10+dt. The
    # recorded g (computed in BREAKPOINT) lags the state by one step, as usual in NEURON.

    def tpk(tr, td):
        return tr * td / (td - tr) * np.log(td / tr)

    onset = t[np.argmax(np.array(a2) > 0)] - 0.025
    tpa, tpn = t[np.argmax(ga)] - 10.0, t[np.argmax(gn)] - 10.0
    ok = (abs(ga.max() - p.gq_ampa) / p.gq_ampa < 2e-3
          and abs(gn.max() - p.nmda_ratio * p.gq_ampa) / (p.nmda_ratio * p.gq_ampa) < 2e-3
          and abs(onset - 10.0) < 1e-6
          and abs(tpa - tpk(p.tau_r_ampa, p.tau_d_ampa)) <= 0.05
          and abs(tpn - tpk(p.tau_r_nmda, p.tau_d_nmda)) <= 0.05)
    k = np.argmin(r["soma_i_clamp"])
    msg = (f"peak gAMPA {ga.max():.4f} nS (gq {p.gq_ampa}), peak gNMDA {gn.max():.4f} nS "
           f"(expect {p.nmda_ratio * p.gq_ampa}); event delivered at {onset:.3f} ms; "
           f"t_peak AMPA {tpa:.3f} (expect {tpk(p.tau_r_ampa, p.tau_d_ampa):.3f}) ms, "
           f"NMDA {tpn:.3f} (expect {tpk(p.tau_r_nmda, p.tau_d_nmda):.3f}) ms; "
           f"local EPSC {r['syn_i_ampa'][0].min() + r['syn_i_nmda'][0][np.argmin(r['syn_i_ampa'][0])]:.2f} pA, "
           f"somatic EPSC {r['soma_i_clamp'][k]:.2f} pA at {t[k] - 10:.3f} ms")
    return ok, msg


def check_linearity(_):
    """Two vesicles together give exactly 2x the conductance and ~2x the somatic EPSC."""
    import numpy as np
    m = _model()
    r1 = m.run([np.array([10.0])], tstop=100.0)
    r2 = m.run([np.array([10.0, 10.0])], tstop=100.0)
    g_ratio = r2["syn_g_ampa"].max() / r1["syn_g_ampa"].max()
    gn_ratio = r2["syn_g_nmda"].max() / r1["syn_g_nmda"].max()
    i_ratio = r2["soma_i_clamp"].min() / r1["soma_i_clamp"].min()
    ok = abs(g_ratio - 2) < 1e-9 and abs(gn_ratio - 2) < 1e-9 and abs(i_ratio - 2) < 0.02
    return ok, (f"g_AMPA ratio {g_ratio:.10f}, g_NMDA ratio {gn_ratio:.10f}, "
                f"somatic EPSC ratio {i_ratio:.4f} (space clamp + Mg block -> ~2)")


def check_reset(_):
    """Same input twice in a row (with a spiking run in between) -> identical traces."""
    import numpy as np
    m = _model("iclamp")
    tr = [np.array([5.0, 5.0, 7.0, 20.0])]
    a = m.run(tr, tstop=60.0)
    m.run([np.full(400, 5.0)], tstop=60.0)        # big input: spikes, raises [Ca]i
    b = m.run(tr, tstop=60.0)
    d = max(np.abs(a[k] - b[k]).max() for k in ("soma_v", "syn_i_ampa", "syn_i_nmda"))
    return d == 0.0, f"max difference between repeated runs: {d:g}"


def check_events(ves):
    """Loader count = file count, and every loaded vesicle is delivered to the model."""
    import numpy as np
    from mfb.vesicles import TYPES, VesicleData
    raw = pickle.load(open(Path(ves) / "vesData.dat" if Path(ves).is_dir() else ves, "rb"))
    if isinstance(next(iter(raw.values())), dict):
        n_file = sum(len(tr) for a in raw.values() for t in TYPES for tr in a[t])
    else:
        n_file = sum(len(tr) for v in raw.values() for tr in v) if len(raw) == 1 else None
    vd = VesicleData(ves)
    n_load = vd.n_releases()
    rng = np.random.default_rng(1)
    trials = vd.draw_trials(5, 1, rng)[0]
    trains = [vd.train(int(k)).times for k in trials]
    m = _model(sites=[SITE] * 5)
    r = m.run(trains, tstop=300.0)
    expected = [len(x) for x in trains]
    delivered = [int(x) for x in r["syn_nev"]]
    ok = (n_file is None or n_file == n_load) and delivered == expected
    return ok, (f"file {n_file} releases, loaded {n_load}; 5 trials {list(map(int, trials))}: "
                f"delivered {delivered}, expected {expected}")


CHECKS = {
    "rin": check_rin, "rest": check_rest, "rest_vclamp": check_rest_vclamp,
    "quantal": check_quantal, "linearity": check_linearity, "reset": check_reset,
    "events": check_events,
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ves", default=str(DEFAULT_VES))
    ap.add_argument("--one", help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a.one:
        ok, msg = CHECKS[a.one](a.ves)
        print("RESULT " + json.dumps({"ok": bool(ok), "msg": msg}))
        return 0
    failed = 0
    for name in CHECKS:
        p = subprocess.run([sys.executable, __file__, "--one", name, "--ves", a.ves],
                           capture_output=True, text=True, cwd=ROOT)
        line = next((ln for ln in p.stdout.splitlines() if ln.startswith("RESULT ")), None)
        if line is None:
            failed += 1
            print(f"[FAIL] {name}: crashed\n{p.stdout}\n{p.stderr}")
            continue
        res = json.loads(line[7:])
        failed += not res["ok"]
        print(f"[{'PASS' if res['ok'] else 'FAIL'}] {name}: {res['msg']}")
    print(f"{len(CHECKS) - failed}/{len(CHECKS)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
