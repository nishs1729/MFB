"""EPSC figures from a results file written by run.py.

    python plot.py results/<run>.npz [--rep 0] [--out fig.png]

Panels (shared time axis, APs marked as dashed lines):
  1. vesicle releases of each MFB in one repetition, coloured by release type
  2. somatic EPSC (vclamp: clamp current) or somatic EPSP (iclamp), every repetition
     plus the mean +/- sd when M > 1
  3. local EPSC at each synapse (AMPA + NMDA), one repetition
  4. AMPA vs NMDA current summed over all synapses, mean over repetitions
  5. (iclamp only) membrane potential at each synapse, one repetition
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

# Reference palette (dataviz skill), validated light-mode: slots 1-3 + neutrals
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#a3a29c", "#e6e5e0", "#fcfcfb"
TYPE_COLOR = {0: BLUE, 1: ORANGE, 2: AQUA, -1: INK2}
TYPE_NAME = {0: "sync", 1: "async", 2: "spont", -1: "release"}
SERIES = (BLUE, ORANGE, AQUA)   # validated all-pairs for <= 3 series; more -> one ink colour


def _syn_color(i: int, n: int) -> str:
    return INK if n == 1 else (SERIES[i] if n <= 3 else INK2)


def _style(ax) -> None:
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(MUTED)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.yaxis.label.set_color(INK2)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def _aps(ax, aps) -> None:
    for t in aps:
        ax.axvline(t, color=MUTED, lw=0.6, ls=(0, (3, 3)), zorder=0)


def plot_results(path: str | Path, rep: int = 0, out: str | Path | None = None) -> Path:
    d = np.load(path, allow_pickle=False)
    cfg = json.loads(str(d["config"]))
    t, aps = d["t"], d["ap_times"]
    M, N = d["trials"].shape
    vclamp = cfg["mode"] == "vclamp"
    rep = min(rep, M - 1)

    n_pan = 4 if vclamp else 5
    fig, axes = plt.subplots(n_pan, 1, figsize=(9, 2.0 * n_pan + 0.6), sharex=True,
                             gridspec_kw={"height_ratios": [max(1.0, 0.25 * N)] + [1.6] * (n_pan - 1)})
    fig.patch.set_facecolor(SURFACE)
    for ax in axes:
        _style(ax)
        _aps(ax, aps)

    # 1. releases
    ax = axes[0]
    sel = d["ev_rep"] == rep
    present = sorted(set(d["ev_type"][sel].tolist()))
    for code in present:
        m = sel & (d["ev_type"] == code)
        ax.scatter(d["ev_t"][m], d["ev_syn"][m], marker="|", s=90, lw=1.5,
                   color=TYPE_COLOR[code], label=TYPE_NAME[code])
    ax.set_ylim(-0.6, N - 0.4)
    ax.set_yticks(range(N))
    ax.set_yticklabels([f"MFB {i}" for i in range(N)] if N <= 12 else [])
    ax.grid(False)
    n_rel = int(sel.sum())
    ax.set_title(f"Vesicle releases, rep {rep} ({n_rel} vesicles, trials {list(map(int, d['trials'][rep]))})",
                 loc="left", fontsize=9, color=INK)
    if len(present) > 1:
        ax.legend(loc="upper right", fontsize=7, frameon=False, ncol=len(present), markerscale=0.6)

    # 2. somatic EPSC / EPSP
    ax = axes[1]
    y = d["soma_i_clamp"] if vclamp else d["soma_v"]
    for r in range(M):
        ax.plot(t, y[r], color=MUTED if M > 1 else INK, lw=0.6 if M > 1 else 1.0)
    if M > 1:
        mu, sd = y.mean(0), y.std(0)
        ax.fill_between(t, mu - sd, mu + sd, color=BLUE, alpha=0.18, lw=0, label="mean ± sd")
        ax.plot(t, mu, color=BLUE, lw=1.4, label=f"mean of {M} reps")
        ax.legend(loc="lower right" if vclamp else "upper right", fontsize=7, frameon=False)
    ax.set_ylabel("pA" if vclamp else "mV")
    ax.set_title("Somatic EPSC (voltage clamp at %g mV)" % cfg["v_hold"] if vclamp else "Somatic EPSP",
                 loc="left", fontsize=9, color=INK)

    # 3. local EPSC per synapse
    ax = axes[2]
    loc = d["syn_i_ampa"][rep] + d["syn_i_nmda"][rep]
    for i in range(N):
        lab = f"MFB {i}: {d['syn_section'][i]}({d['syn_x'][i]:g}), {d['syn_distance'][i]:.0f} µm"
        ax.plot(t, loc[i], lw=0.9, color=_syn_color(i, N), alpha=1.0 if N <= 3 else 0.5,
                label=lab if N <= 3 else None)
    if N <= 3:
        ax.legend(loc="lower right", fontsize=7, frameon=False)
    ax.set_ylabel("pA")
    ax.set_title(f"Local EPSC at each synapse (AMPA + NMDA), rep {rep}", loc="left", fontsize=9, color=INK)

    # 4. AMPA vs NMDA
    ax = axes[3]
    ia = d["syn_i_ampa"].sum(1).mean(0)
    inm = d["syn_i_nmda"].sum(1).mean(0)
    ax.plot(t, ia, color=BLUE, lw=1.0, label="AMPA")
    ax.plot(t, inm, color=ORANGE, lw=1.4, label="NMDA")
    ax.legend(loc="lower right", fontsize=7, frameon=False)
    ax.set_ylabel("pA")
    ax.set_title("Synaptic current by receptor, summed over synapses"
                 + (f", mean of {M} reps" if M > 1 else ""), loc="left", fontsize=9, color=INK)

    # 5. local voltage (iclamp)
    if not vclamp:
        ax = axes[4]
        for i in range(N):
            ax.plot(t, d["syn_v"][rep][i], lw=0.9, color=_syn_color(i, N), alpha=1.0 if N <= 3 else 0.5,
                    label=f"MFB {i}" if N <= 3 else None)
        ax.plot(t, d["soma_v"][rep], lw=1.0, color=INK2, ls=(0, (4, 2)), label="soma")
        ax.legend(loc="upper right", fontsize=7, frameon=False)
        ax.set_ylabel("mV")
        ax.set_title(f"Membrane potential at each synapse, rep {rep}", loc="left", fontsize=9, color=INK)

    axes[-1].set_xlabel("time (ms)", color=INK2)
    axes[-1].set_xlim(t[0], t[-1])
    fig.suptitle(f"{Path(cfg['ves']).name}  ·  N = {N} MFB, M = {M} reps, seed {cfg['seed']}, "
                 f"gq_AMPA {cfg['syn']['gq_ampa']} nS", x=0.01, ha="left", fontsize=9, color=INK2)
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    out = Path(out) if out else Path(path).with_suffix(".png")
    fig.savefig(out, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    print(f"[mfb] figure {out}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results")
    ap.add_argument("--rep", type=int, default=0, help="repetition shown in the per-rep panels")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    plot_results(a.results, a.rep, a.out)


if __name__ == "__main__":
    main()
