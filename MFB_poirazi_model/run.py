"""MFB vesicle release -> Poirazi CA1 cell -> EPSCs.

Example:
    python run.py --ves ../data/control_buffer/nVDCC_9_dVDCC_220_nAZ_31_RRP_15_ISI_20_nAP_10_cb_45uM \\
                  --n-mfb 1 --reps 1 --seed 0
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from mfb.experiment import RunConfig, run_experiment  # noqa: E402
from mfb.synapses import SynParams  # noqa: E402
from mfb.vesicles import TYPES  # noqa: E402


def build_parser(description: str = __doc__, ves_required: bool = True) -> argparse.ArgumentParser:
    """The run options (shared with diagnose.py)."""
    p = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_argument_group("input")
    g.add_argument("--ves", required=ves_required, help="vesData.dat, or the directory that contains it")
    g.add_argument("--key", default=None, help="key to use for a flat file with several keys (findPr)")
    g.add_argument("--types", default=",".join(TYPES),
                   help="release types to include, comma-separated (default: %(default)s)")
    g.add_argument("--n-mfb", type=int, default=1, help="N boutons (= N random trials) (default: 1)")
    g.add_argument("--reps", type=int, default=1, help="M repetitions, each with new trials (default: 1)")
    g.add_argument("--seed", type=int, default=0, help="RNG seed for trials and placement (default: 0)")
    g.add_argument("--isi", type=float, default=None, help="AP interval (ms); default: from the path")
    g.add_argument("--n-ap", type=int, default=None, help="number of APs; default: from the path")

    g = p.add_argument_group("placement (apical trunk)")
    g.add_argument("--dmin", type=float, default=0.0, help="min distance from soma, um (default: 0)")
    g.add_argument("--dmax", type=float, default=100.0, help="max distance from soma, um (default: 100)")
    g.add_argument("--site", action="append", default=[],
                   help="explicit site, e.g. 'apical_dendrite[14](0.5)'; give once per MFB")

    g = p.add_argument_group("recording")
    g.add_argument("--mode", choices=("vclamp", "iclamp"), default="vclamp")
    g.add_argument("--v-hold", type=float, default=-70.0, help="clamp holding potential, mV")
    g.add_argument("--rs", type=float, default=0.01, help="clamp series resistance, MOhm")
    g.add_argument("--tstop", type=float, default=300.0)
    g.add_argument("--dt", type=float, default=0.025)
    g.add_argument("--save-every", type=int, default=1, help="save every k-th sample (default: 1)")
    g.add_argument("--out", default=None, help="output .npz (default: results/<data>_N.._M.._seed.._mode.npz)")

    d = SynParams()
    g = p.add_argument_group("quantal synapse (one vesicle)")
    g.add_argument("--gq-ampa", type=float, default=d.gq_ampa, help="peak AMPA conductance, nS")
    g.add_argument("--tau-r-ampa", type=float, default=d.tau_r_ampa)
    g.add_argument("--tau-d-ampa", type=float, default=d.tau_d_ampa)
    g.add_argument("--nmda-ratio", type=float, default=d.nmda_ratio, help="peak gNMDA/gAMPA")
    g.add_argument("--tau-r-nmda", type=float, default=d.tau_r_nmda)
    g.add_argument("--tau-d-nmda", type=float, default=d.tau_d_nmda)
    g.add_argument("--mg", type=float, default=d.mg, help="[Mg2+]o, mM")
    g.add_argument("--e-rev", type=float, default=d.e_rev, help="reversal potential, mV")
    return p


def config_from_args(p: argparse.ArgumentParser, a: argparse.Namespace) -> RunConfig:
    types = tuple(t.strip() for t in a.types.split(",") if t.strip())
    if a.site and len(a.site) != a.n_mfb:
        p.error(f"{len(a.site)} --site given but --n-mfb is {a.n_mfb}")
    cfg = RunConfig(
        ves=a.ves, n_mfb=a.n_mfb, reps=a.reps, seed=a.seed, types=types, key=a.key, mode=a.mode,
        dmin=a.dmin, dmax=a.dmax, sites=tuple(a.site), tstop=a.tstop, dt=a.dt, v_hold=a.v_hold,
        rs=a.rs, isi=a.isi, n_ap=a.n_ap, save_every=a.save_every,
        syn=SynParams(gq_ampa=a.gq_ampa, tau_r_ampa=a.tau_r_ampa, tau_d_ampa=a.tau_d_ampa,
                      nmda_ratio=a.nmda_ratio, tau_r_nmda=a.tau_r_nmda, tau_d_nmda=a.tau_d_nmda,
                      mg=a.mg, e_rev=a.e_rev),
    )
    return cfg


def main(argv=None) -> None:
    p = build_parser()
    p.add_argument("--plot", action="store_true", help="also write the figures (plot.py)")
    a = p.parse_args(argv)
    cfg = config_from_args(p, a)
    try:
        out = run_experiment(cfg, out=a.out)
    except ValueError as e:
        p.error(str(e))
    if a.plot:
        from plot import plot_results
        plot_results(out)


if __name__ == "__main__":
    main()
