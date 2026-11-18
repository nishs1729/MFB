"""Diagnostic figures: what every component of the model is doing in one repetition.

Reruns one repetition with extra recordings, then writes four figures:

  1_input.png     where the synapses are (morphology), the vesicle releases, releases per
                  AP interval, and release latency after each AP
  2_synapse.png   inside one MFBSyn: g_AMPA, g_NMDA with and without the Mg block,
                  local voltage, the Mg block itself, i_AMPA / i_NMDA, B(v) and charge
                  (full time course on the left, a zoom on the right)
  3_channels.png  the cell's own ionic currents (Na, K split by channel, Ca, Ih, leak) and
                  [Ca]i, at the synapse compartment and at the soma
  4_spread.png    synaptic vs axial vs clamp current, their charge, the voltage along the
                  apical trunk (heatmap) and the peak depolarisation vs distance

Usage (from MFB_poirazi_model/):

    # reproduce repetition 0 of a saved run exactly (same trials, same sites, same settings)
    python diagnose.py --from results/<run>.npz [--rep 0] [--syn 0]

    # or give the run options directly (same flags as run.py; nothing is saved but the figures)
    python diagnose.py --ves <dir> [--seed 3 --n-mfb 2 --mode iclamp ...]

The figures go to <run>_diag/ next to the .npz (or to results/<data>_..._diag/), or to
--out-dir. Currents are in pA (inward negative). Channel currents are the total over the
compartment (density x area), so they can be compared directly with the synaptic current.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402
from neuron import h  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402  (Agg backend is set by plot.py)
from mfb.experiment import MFBModel, RunConfig, _rec, default_out  # noqa: E402
from mfb.synapses import SynParams, random_sites  # noqa: E402
from mfb.vesicles import VesicleData, ap_times, protocol_from_path  # noqa: E402
from plot import (AQUA, BLUE, INK, INK2, MUTED, ORANGE, SURFACE, TYPE_COLOR,  # noqa: E402
                  TYPE_NAME, _aps, _style, _syn_color)
from run import build_parser, config_from_args  # noqa: E402

YELLOW = "#eda100"     # categorical slot 4 (adjacent pairs validated for lines)
SEQ = LinearSegmentedColormap.from_list(  # sequential blue ramp, 100 -> 700
    "seq_blue", ["#cde2fb", "#86b6ef", "#3987e5", "#256abf", "#184f95", "#0d366b"])
PA = 10.0              # mA/cm2 * um2 -> pA


# ============================================================================ recordings
class SegProbe:
    """Records the membrane currents of one segment. Currents in pA for the whole segment."""

    def __init__(self, seg) -> None:
        self.seg = seg
        self.area = seg.area()                       # um2
        mech = {m.name() for m in seg}
        self.mech = mech
        r = {"v": _rec(seg._ref_v)}
        if "na_ion" in mech:
            r["ina"] = _rec(seg._ref_ina)
        if "k_ion" in mech:
            r["ik"] = _rec(seg._ref_ik)
        if "ca_ion" in mech:
            r["ica"] = _rec(seg._ref_ica)
            r["cai"] = _rec(seg._ref_cai)
        if "Ca_ion" in mech:
            r["iCa"] = _rec(seg._ref_iCa)            # T-type current (separate ion in the model)
        if "h" in mech:
            r["h_g"] = _rec(seg.h._ref_g)
        for m in ("kap", "kad"):
            if m in mech:
                r[f"{m}_g"] = _rec(getattr(seg, m)._ref_gka)
        if "km" in mech:
            r["km_g"] = _rec(seg.km._ref_gk)
        if "kca" in mech:
            r["kca_g"] = _rec(seg.kca._ref_gk)
        if "mykca" in mech:
            r["mykca_i"] = _rec(seg.mykca._ref_ik)
        if "pas" in mech:
            r["pas_i"] = _rec(seg.pas._ref_i)
        self.hha = next((m for m in ("hha2", "hha_old") if m in mech), None)
        if self.hha:
            hh = getattr(seg, self.hha)
            r["il"] = _rec(hh._ref_il)
            r["hh_n"] = _rec(hh._ref_n)
        self.rec = r

    def currents(self) -> dict[str, np.ndarray]:
        """Per-channel currents (pA, inward negative) and [Ca]i (uM)."""
        a = {k: np.array(v) for k, v in self.rec.items()}
        seg, v, z = self.seg, a["v"], np.zeros(len(a["v"]))
        ek = seg.ek if "k_ion" in self.mech else 0.0
        ih = a["h_g"] * (v - h.eh_h) if "h_g" in a else z
        k_a = (a.get("kap_g", z) + a.get("kad_g", z)) * (v - ek)
        k_m = 1e-4 * a.get("km_g", z) * (v - ek)
        k_ca = a.get("kca_g", z) * (v - ek) + a.get("mykca_i", z)
        k_dr = getattr(seg, self.hha).gkbar * a["hh_n"] ** 2 * (v - ek) if self.hha else z
        out = {
            "v": v,
            "Na": (a.get("ina", z) - ih),                    # h.mod writes its current as ina
            "K_A": k_a, "K_DR": k_dr, "K_M": k_m, "K_Ca": k_ca,
            "K_rest": a.get("ik", z) - (k_a + k_dr + k_m + k_ca),   # closure check, should be ~0
            "Ca_LR": a.get("ica", z),                        # L-type, R-type, somatic R
            "Ca_T": a.get("iCa", z),
            "Ih": ih,
            "leak": a.get("pas_i", z) + a.get("il", z),
        }
        for k in list(out):
            if k != "v":
                out[k] = PA * self.area * out[k]
        out["cai"] = 1e3 * a["cai"] if "cai" in a else z       # mM -> uM
        return out


def region_currents(probes: list[SegProbe]) -> dict[str, np.ndarray]:
    """Sum the currents over several segments; area-weighted mean of v and [Ca]i."""
    cs = [p.currents() for p in probes]
    w = np.array([p.area for p in probes]) / sum(p.area for p in probes)
    out = {k: sum(c[k] for c in cs) for k in cs[0] if k not in ("v", "cai")}
    out["v"] = sum(wi * c["v"] for wi, c in zip(w, cs))
    out["cai"] = sum(wi * c["cai"] for wi, c in zip(w, cs))
    return out


def trunk_segments(cell) -> list[tuple[float, object]]:
    """soma(0.5) plus every apical trunk segment, sorted by distance from the soma."""
    segs = [(0.0, cell.soma(0.5))]
    for sec in cell.lists["apical_trunk_list"]:
        for seg in sec:
            segs.append((cell.distance(sec, seg.x), seg))
    return sorted(segs, key=lambda s: s[0])


# ============================================================================ the run
def setup(a, p):
    """Return cfg, the trains of one repetition, the trials and (if any) the saved trace."""
    saved = None
    if a.from_npz:
        d = np.load(a.from_npz, allow_pickle=False)
        c = json.loads(str(d["config"]))
        c["types"], c["sites"] = tuple(c["types"]), tuple(c["sites"])
        c["syn"] = SynParams(**c["syn"])
        cfg = RunConfig(**c)
        rep = min(a.rep, d["trials"].shape[0] - 1)
        trials = d["trials"][rep]
        sites = [f"{s}({x:g})" for s, x in zip(d["syn_section"], d["syn_x"])]
        key = "soma_i_clamp" if cfg.mode == "vclamp" else "soma_v"
        saved = (key, d[key][rep], d["t"])
        out_dir = Path(a.out_dir) if a.out_dir else Path(a.from_npz).with_suffix("").parent / (
            Path(a.from_npz).stem + (f"_rep{rep}" if rep else "") + "_diag")
        ves = VesicleData(_find(cfg.ves), types=cfg.types, key=cfg.key)
        return cfg, ves, trials, sites, rep, saved, out_dir
    if not a.ves:
        p.error("give --from <run.npz> or --ves <dir>")
    cfg = config_from_args(p, a)
    rng = np.random.default_rng(cfg.seed)        # same order of draws as run_experiment
    ves = VesicleData(cfg.ves, types=cfg.types, key=cfg.key)
    reps = max(cfg.reps, a.rep + 1)
    trials = ves.draw_trials(cfg.n_mfb, reps, rng)[a.rep]
    sites = list(cfg.sites) or rng                # random sites are drawn after the cell is built
    out_dir = Path(a.out_dir) if a.out_dir else default_out(cfg).with_suffix("").parent / (
        default_out(cfg).stem + (f"_rep{a.rep}" if a.rep else "") + "_diag")
    return cfg, ves, trials, sites, a.rep, saved, out_dir


def _find(path: str) -> str:
    for cand in (Path(path), ROOT / path):
        if cand.exists():
            return str(cand)
    raise FileNotFoundError(path)


def run_diagnostics(cfg: RunConfig, ves: VesicleData, trials, sites) -> dict:
    model = MFBModel(syn=cfg.syn, mode=cfg.mode, v_init=cfg.v_init, v_hold=cfg.v_hold, rs=cfg.rs)
    if isinstance(sites, np.random.Generator):
        sites = random_sites(model.cell, cfg.n_mfb, sites, cfg.dmin, cfg.dmax)
    model.add_synapses(sites)
    cell = model.cell

    mg = [_rec(s.syn._ref_mgblock) for s in model.synapses]
    syn_probe = {}
    for s in model.synapses:
        seg = s.sec(s.site.x)
        syn_probe.setdefault((cell.name(s.sec), seg.x), SegProbe(seg))
    soma_probes = [SegProbe(seg) for sec in cell.lists["soma_list"] for seg in sec]
    trunk = trunk_segments(cell)
    trunk_v = [_rec(seg._ref_v) for _, seg in trunk]

    trains = [ves.train(int(tr)) for tr in trials]
    res = model.run([tr.times for tr in trains], cfg.tstop, cfg.dt, cfg.celsius)

    proto = protocol_from_path(ves.path)
    isi = cfg.isi if cfg.isi is not None else proto["isi"]
    n_ap = cfg.n_ap if cfg.n_ap is not None else proto["n_ap"]
    res.update({
        "cfg": cfg, "model": model, "trains": trains, "trials": trials,
        "aps": ap_times(isi, n_ap), "isi": isi,
        "syn_mg": np.stack([np.array(r) for r in mg]),
        "syn_chan": [syn_probe[(cell.name(s.sec), s.sec(s.site.x).x)].currents() for s in model.synapses],
        "syn_area": [syn_probe[(cell.name(s.sec), s.sec(s.site.x).x)].area for s in model.synapses],
        "soma_chan": region_currents(soma_probes),
        "soma_area": sum(p.area for p in soma_probes),
        "trunk_d": np.array([d for d, _ in trunk]),
        "trunk_v": np.stack([np.array(r) for r in trunk_v]),
    })
    return res


# ============================================================================ figures
def _st(ax) -> None:
    _style(ax)
    try:
        ax.ticklabel_format(axis="y", useOffset=False)
    except AttributeError:          # axes with fixed tick labels
        pass


def _fig(rows, cols=1, **kw):
    fig, axes = plt.subplots(rows, cols, squeeze=False, **kw)
    fig.patch.set_facecolor(SURFACE)
    for ax in axes.flat:
        _st(ax)
    return fig, axes


def _title(ax, s):
    ax.set_title(s, loc="left", fontsize=9, color=INK)


def _legend(ax, loc="best", **kw):
    ax.legend(loc=loc, fontsize=7, frameon=False, **kw)


def _legend_above(ax, ncol):
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 1.0), fontsize=7, frameon=False, ncol=ncol,
              borderaxespad=0.2)


def _save(fig, path, suptitle):
    fig.suptitle(suptitle, x=0.01, ha="left", fontsize=9, color=INK2)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(path, dpi=140, facecolor=SURFACE)
    plt.close(fig)
    print(f"[diag] {path}")


def _events(r, i=None):
    """(times, type codes) of all releases, or of synapse i."""
    trs = r["trains"] if i is None else [r["trains"][i]]
    t = np.concatenate([tr.times for tr in trs]) if trs else np.empty(0)
    k = np.concatenate([tr.kind for tr in trs]) if trs else np.empty(0, int)
    return t, k


def fig_input(r, path, sup):
    cell, model, aps, isi = r["model"].cell, r["model"], r["aps"], r["isi"]
    N = len(model.synapses)
    fig = plt.figure(figsize=(12, 7.5))
    fig.patch.set_facecolor(SURFACE)
    gs = fig.add_gridspec(3, 2, width_ratios=[1, 2.2], height_ratios=[max(1.0, 0.3 * N), 1.2, 1.2])
    axm = fig.add_subplot(gs[:, 0])
    axr, axc, axl = (fig.add_subplot(gs[i, 1]) for i in range(3))
    for ax in (axm, axr, axc, axl):
        _st(ax)

    # morphology (x-y projection); the placement window in blue
    trunk = set(cell.lists["apical_trunk_list"])
    soma = set(cell.lists["soma_list"])
    cfg = r["cfg"]
    for sec in cell.all:
        n = int(sec.n3d())
        if n < 2:
            continue
        x = np.array([sec.x3d(j) for j in range(n)])
        y = np.array([sec.y3d(j) for j in range(n)])
        col, lw = (INK, 2.5) if sec in soma else ((INK2, 1.2) if sec in trunk else (MUTED, 0.6))
        axm.plot(x, y, color=col, lw=lw, solid_capstyle="round")
        if sec in trunk:      # highlight the segments inside the placement window
            arc = np.array([sec.arc3d(j) for j in range(n)]) / sec.L
            for seg in sec:
                d = cell.distance(sec, seg.x)
                if cfg.dmin <= d <= cfg.dmax:
                    lo, hi = seg.x - 0.5 / sec.nseg, seg.x + 0.5 / sec.nseg
                    m = (arc >= lo - 1e-9) & (arc <= hi + 1e-9)
                    axm.plot(x[m], y[m], color=BLUE, lw=3, alpha=0.5, solid_capstyle="round")
    for i, s in enumerate(model.synapses):
        px, py = _xyz(s.sec, s.site.x)
        axm.plot(px, py, "o", ms=9, mfc=_syn_color(i, N), mec=SURFACE, mew=2, zorder=5)
        if N <= 6:
            axm.annotate(f"MFB {i}", (px, py), xytext=(8, 0), textcoords="offset points",
                         fontsize=7, color=INK2, va="center")
    sx, sy = _xyz(cell.soma, 0.5)
    axm.plot(sx, sy, "s", ms=7, mfc=SURFACE, mec=INK, mew=1.5, zorder=6)
    axm.annotate("soma" + (" (clamp)" if cfg.mode == "vclamp" else ""), (sx, sy), xytext=(-8, 6),
                 textcoords="offset points", fontsize=7, color=INK2, ha="right")
    axm.set_aspect("equal")
    axm.grid(False)
    axm.set_xlabel("x (µm)", color=INK2)
    axm.set_ylabel("y (µm)", color=INK2)
    _title(axm, f"Morphology; blue: placement window\n{cfg.dmin:g}–{cfg.dmax:g} µm on the apical trunk")

    # raster
    _aps(axr, aps)
    for i, tr in enumerate(r["trains"]):
        for code in sorted(set(tr.kind.tolist())):
            m = tr.kind == code
            axr.scatter(tr.times[m], np.full(m.sum(), i), marker="|", s=110, lw=1.5,
                        color=TYPE_COLOR[code], label=TYPE_NAME[code] if i == 0 or N == 1 else None)
    axr.set_ylim(-0.6, N - 0.4)
    axr.set_yticks(range(N))
    axr.set_yticklabels([f"MFB {i}\ntrial {int(t)}" for i, t in enumerate(r["trials"])] if N <= 8 else [])
    axr.grid(False)
    axr.set_xlim(0, cfg.tstop)
    axr.set_xlabel("time (ms)", color=INK2)
    t_all, k_all = _events(r)
    handles, labels = axr.get_legend_handles_labels()
    uniq = dict(zip(labels, handles))
    axr.legend(uniq.values(), uniq.keys(), loc="lower right", bbox_to_anchor=(1.0, 1.0), fontsize=7,
               frameon=False, ncol=3, markerscale=0.6, borderaxespad=0.2)
    _title(axr, f"Vesicle releases ({t_all.size} vesicles); dashed: APs")

    # releases per AP interval, stacked by type
    edges = np.concatenate([[0.0], aps, [cfg.tstop]]) if aps.size else np.array([0.0, cfg.tstop])
    labels_x = ["pre"] + [f"AP{k + 1}" for k in range(aps.size)]
    bottom = np.zeros(edges.size - 1)
    codes = sorted(set(k_all.tolist()))
    for code in codes:
        cnt, _ = np.histogram(t_all[k_all == code], edges)
        axc.bar(np.arange(cnt.size), cnt, 0.7, bottom=bottom, color=TYPE_COLOR[code],
                edgecolor=SURFACE, lw=1, label=TYPE_NAME[code])
        bottom += cnt
    axc.set_xticks(np.arange(bottom.size))
    axc.set_xticklabels(labels_x, fontsize=7)
    axc.set_ylabel("vesicles", color=INK2)
    _legend_above(axc, len(codes))
    _title(axc, "Releases in each AP interval (from one AP to the next), all MFBs")

    # latency after the preceding AP
    if aps.size:
        idx = np.searchsorted(aps, t_all, side="right") - 1
        ok = idx >= 0
        lat = t_all[ok] - aps[idx[ok]]
        kk = k_all[ok]
        bins = np.arange(0, (isi or lat.max() + 1) + 0.5, 0.5)
        data = [lat[kk == c] for c in codes]
        axl.hist(data, bins, stacked=True, color=[TYPE_COLOR[c] for c in codes],
                 label=[TYPE_NAME[c] for c in codes], edgecolor=SURFACE, lw=0.5)
        _legend_above(axl, len(codes))
        med = np.median(lat) if lat.size else np.nan
        _title(axl, f"Release latency after the preceding AP (median {med:.1f} ms)")
    axl.set_xlabel("ms after AP", color=INK2)
    axl.set_ylabel("vesicles", color=INK2)
    axl.yaxis.set_major_locator(MaxNLocator(integer=True))
    axc.yaxis.set_major_locator(MaxNLocator(integer=True))
    _save(fig, path, sup)


def _xyz(sec, x):
    n = int(sec.n3d())
    arc = np.array([sec.arc3d(j) for j in range(n)])
    xs = np.array([sec.x3d(j) for j in range(n)])
    ys = np.array([sec.y3d(j) for j in range(n)])
    return np.interp(x * sec.L, arc, xs), np.interp(x * sec.L, arc, ys)


def fig_synapse(r, i, zoom, path, sup):
    t, aps, cfg = r["t"], r["aps"], r["cfg"]
    s = r["model"].synapses[i]
    ga, gn, B = r["syn_g_ampa"][i], r["syn_g_nmda"][i], r["syn_mg"][i]
    ia, inm, v = r["syn_i_ampa"][i], r["syn_i_nmda"][i], r["syn_v"][i]
    tr = r["trains"][i]
    fig = plt.figure(figsize=(13, 11))
    fig.patch.set_facecolor(SURFACE)
    gs = fig.add_gridspec(6, 2, width_ratios=[2.2, 1], height_ratios=[0.45, 1.2, 1, 0.8, 1.2, 1.3])
    rows = []
    for k in range(5):
        a0 = fig.add_subplot(gs[k, 0])
        a1 = fig.add_subplot(gs[k, 1])
        rows.append((a0, a1))
    for a0, a1 in rows:
        for ax, lim in ((a0, (t[0], t[-1])), (a1, zoom)):
            _st(ax)
            _aps(ax, aps)
            ax.set_xlim(*lim)
    n_ves = tr.times.size

    for ax in rows[0]:
        for code in sorted(set(tr.kind.tolist())):
            m = tr.kind == code
            ax.scatter(tr.times[m], np.zeros(m.sum()), marker="|", s=150, lw=1.5, color=TYPE_COLOR[code],
                       label=TYPE_NAME[code])
        ax.set_yticks([])
        ax.grid(False)
    rows[0][1].legend(loc="lower right", bbox_to_anchor=(1.0, 1.0), fontsize=7, frameon=False, ncol=3,
                      markerscale=0.6, borderaxespad=0.2)
    _title(rows[0][0], f"MFB {i} at {s.site}: {n_ves} vesicles (trial {int(r['trials'][i])}); "
                       "each one adds a quantum of g")
    _title(rows[0][1], f"zoom {zoom[0]:g}–{zoom[1]:g} ms")

    for ax in rows[1]:
        ax.plot(t, ga, color=BLUE, lw=1.0, label="g_AMPA")
        ax.plot(t, gn, color=ORANGE, lw=1.0, ls=(0, (4, 2)), label="g_NMDA (no Mg block)")
        ax.plot(t, gn * B, color=ORANGE, lw=1.6, label="g_NMDA × B(v) (effective)")
        ax.set_ylabel("nS")
    _legend(rows[1][0])
    _title(rows[1][0], f"Conductance; one vesicle peaks at {cfg.syn.gq_ampa:g} nS (AMPA), "
                       f"{cfg.syn.gq_ampa * cfg.syn.nmda_ratio:g} nS (NMDA)")

    for ax in rows[2]:
        ax.plot(t, v, color=INK, lw=1.0, label="synapse")
        ax.plot(t, r["soma_v"], color=INK2, lw=1.0, ls=(0, (4, 2)), label="soma")
        ax.set_ylabel("mV")
    _legend(rows[2][0])
    _title(rows[2][0], f"Membrane potential (driving force = v − {cfg.syn.e_rev:g} mV)")

    for ax in rows[3]:
        ax.plot(t, B, color=ORANGE, lw=1.2)
        ax.set_ylabel("B")
    _title(rows[3][0], f"NMDA Mg²⁺ block B(v) = 1 / (1 + e^(−0.062 v) · {cfg.syn.mg:g}/3.57): "
                       "fraction of g_NMDA unblocked")

    for ax in rows[4]:
        ax.plot(t, ia, color=BLUE, lw=1.0, label="i_AMPA")
        ax.plot(t, inm, color=ORANGE, lw=1.4, label="i_NMDA")
        ax.plot(t, ia + inm, color=INK, lw=0.8, alpha=0.8, label="total")
        ax.set_ylabel("pA")
    _legend(rows[4][0])
    _title(rows[4][0], "Synaptic current = g · B · (v − E)  (inward negative)")
    for ax in rows[4]:
        ax.set_xlabel("time (ms)", color=INK2)

    # B(v) curve with the range visited, and cumulative charge
    axb = fig.add_subplot(gs[5, 1])
    axq = fig.add_subplot(gs[5, 0])
    _st(axb)
    _st(axq)
    vv = np.linspace(-90, 20, 300)
    axb.plot(vv, 1 / (1 + np.exp(-0.062 * vv) * cfg.syn.mg / 3.57), color=MUTED, lw=1.2, label="B(v)")
    on = gn > 0.01 * max(gn.max(), 1e-12)
    axb.plot(v[on], B[on], ".", ms=2, color=ORANGE, label="visited while g_NMDA > 0")
    axb.set_xlabel("v (mV)", color=INK2)
    axb.set_ylabel("B", color=INK2)
    _legend(axb)
    _title(axb, "Mg block vs voltage")
    dt = t[1] - t[0]
    qa, qn = np.cumsum(ia) * dt * 1e-3, np.cumsum(inm) * dt * 1e-3   # pA*ms = fC -> pC
    _aps(axq, aps)
    axq.plot(t, qa, color=BLUE, lw=1.2, label=f"AMPA {qa[-1]:.2f} pC")
    axq.plot(t, qn, color=ORANGE, lw=1.4, label=f"NMDA {qn[-1]:.2f} pC")
    axq.plot(t, qa + qn, color=INK, lw=0.9, label=f"total {qa[-1] + qn[-1]:.2f} pC")
    axq.set_xlim(t[0], t[-1])
    axq.set_xlabel("time (ms)", color=INK2)
    axq.set_ylabel("pC", color=INK2)
    _legend(axq)
    _title(axq, "Cumulative synaptic charge")
    _save(fig, path, sup)


CHAN_ROWS = (
    ("v", "Membrane potential", "mV", [("v", INK, "v")]),
    ("Na", "Na⁺ current (hha fast Na + persistent Na)", "pA", [("Na", INK, "Na")]),
    ("K", "K⁺ currents by channel", "pA",
     [("K_A", BLUE, "A-type (kap/kad)"), ("K_DR", ORANGE, "delayed rectifier (hha)"),
      ("K_M", AQUA, "M (km)"), ("K_Ca", YELLOW, "Ca-activated (kca + mykca)")]),
    ("Ca", "Ca²⁺ currents", "pA", [("Ca_LR", BLUE, "L + R (cal, calH, car, somacar)"), ("Ca_T", ORANGE, "T (cat)")]),
    ("Ih", "Ih and leak", "pA", [("Ih", BLUE, "Ih (h)"), ("leak", ORANGE, "leak (pas + hha il)")]),
    ("cai", "[Ca²⁺]i", "µM", [("cai", INK, "[Ca]i")]),
)


def fig_channels(r, i, path, sup):
    t, aps = r["t"], r["aps"]
    s = r["model"].synapses[i]
    cols = [(r["syn_chan"][i], f"Synapse compartment {s.sec.hname().split('.')[-1]}({s.sec(s.site.x).x:g}), "
                              f"{r['syn_area'][i]:.0f} µm²"),
            (r["soma_chan"], f"Soma (all {len(r['model'].cell.lists['soma_list'])} soma sections, "
                             f"{r['soma_area']:.0f} µm²)")]
    fig, axes = _fig(len(CHAN_ROWS), 2, figsize=(16, 12), sharex=True)
    for c, (ch, head) in enumerate(cols):
        for k, (_, title, unit, series) in enumerate(CHAN_ROWS):
            ax = axes[k, c]
            _aps(ax, aps)
            for key, col, lab in series:
                ax.plot(t, ch[key], color=col, lw=1.0, label=lab if len(series) > 1 else None)
            ax.set_ylabel(unit)
            if len(series) > 1 and c == 1:
                ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=7, frameon=False)
            _title(ax, (head + "\n" if k == 0 else "") + title)
        axes[-1, c].set_xlabel("time (ms)", color=INK2)
        axes[-1, c].set_xlim(t[0], t[-1])
    _save(fig, path, sup)


def fig_spread(r, path, sup):
    t, aps, cfg = r["t"], r["aps"], r["cfg"]
    vclamp = cfg.mode == "vclamp"
    syn_tot = (r["syn_i_ampa"] + r["syn_i_nmda"]).sum(0)
    fig = plt.figure(figsize=(12, 11))
    fig.patch.set_facecolor(SURFACE)
    gs = fig.add_gridspec(4, 2, width_ratios=[40, 1], height_ratios=[1.2, 1, 1.6, 1.1])
    ax0, ax1, ax2, ax3 = (fig.add_subplot(gs[k, 0]) for k in range(4))
    cax = fig.add_subplot(gs[2, 1])
    for ax in (ax0, ax1, ax2, ax3):
        _st(ax)
    series = [("synaptic (all MFBs)", syn_tot, BLUE), ("axial into soma", r["soma_i_axial"], ORANGE)]
    if vclamp:
        series.append(("clamp (somatic EPSC)", r["soma_i_clamp"], AQUA))
    dt = t[1] - t[0]
    for ax in (ax0, ax1):
        _aps(ax, aps)
        ax.set_xlim(t[0], t[-1])
    for lab, y, col in series:
        ax0.plot(t, y, color=col, lw=1.0, label=lab)
        q = np.cumsum(y) * dt * 1e-3
        ax1.plot(t, q, color=col, lw=1.2, label=f"{lab}: {q[-1]:.2f} pC")
    ax0.set_ylabel("pA")
    _legend(ax0)
    _title(ax0, "Where the synaptic current goes: injected at the synapse, flowing into the soma"
                + (", taken up by the clamp" if vclamp else ""))
    ax1.set_ylabel("pC")
    _legend(ax1, "lower left")
    _title(ax1, "Cumulative charge (the gap between the curves is charge lost to the dendritic membrane)" if vclamp
           else "Cumulative charge (the soma charges its own membrane; during spikes current flows back out)")

    d, V = r["trunk_d"], r["trunk_v"]
    v0 = cfg.v_init
    dv = V - v0
    hi = max(float(np.nanmax(dv)), 0.05)
    du, iu = np.unique(d, return_index=True)          # pcolormesh needs distinct distances
    step = max(1, t.size // 3000)
    im = ax2.pcolormesh(t[::step], du, np.clip(dv[iu, ::step], 0, None), cmap=SEQ, vmin=0, vmax=hi,
                        shading="nearest", rasterized=True)
    ax2.set_ylabel("distance from soma (µm)")
    ax2.grid(False)
    for s in r["model"].synapses:
        ax2.axhline(s.site.distance, color=ORANGE, lw=0.8, ls=(0, (2, 2)))
    cb = fig.colorbar(im, cax=cax)
    cb.set_label(f"v − ({v0:g}) mV", color=INK2, fontsize=8)
    cb.ax.tick_params(labelsize=7, colors=INK2)
    cb.outline.set_visible(False)
    _title(ax2, f"Depolarisation along the apical trunk ({len(d)} segments, soma at the bottom; "
                "orange: synapses)")
    ax2.set_xlabel("time (ms)", color=INK2)

    pk = dv.max(1)
    ax3.plot(d, pk, "-o", color=INK, ms=4, lw=1.0, mfc=INK, mec=SURFACE)
    for i, s in enumerate(r["model"].synapses):
        ax3.axvline(s.site.distance, color=ORANGE, lw=1.0, ls=(0, (2, 2)),
                    label="synapse" if i == 0 else None)
    ax3.set_xlabel("distance from soma (µm)", color=INK2)
    ax3.set_ylabel("mV")
    _legend(ax3, "upper right")
    _title(ax3, "Peak depolarisation along the trunk" + (" (the soma is held by the clamp)" if vclamp else ""))
    _save(fig, path, sup)


# ============================================================================ main
def _closure(ch) -> str:
    """Recomputed K currents use the recorded v, ik used the previous step's v: report the error."""
    k_tot = np.abs(ch["K_A"] + ch["K_DR"] + ch["K_M"] + ch["K_Ca"]).max()
    return f"K closure error {np.abs(ch['K_rest']).max():.2g} pA (peak K {k_tot:.3g} pA)"


def summary(r) -> str:
    t, cfg = r["t"], r["cfg"]
    dt = t[1] - t[0]
    lines = []
    for i, s in enumerate(r["model"].synapses):
        ia, inm = r["syn_i_ampa"][i], r["syn_i_nmda"][i]
        ch = r["syn_chan"][i]
        lines.append(
            f"MFB {i} {s.site}: {r['trains'][i].times.size} vesicles | peak g_AMPA {r['syn_g_ampa'][i].max():.2f} nS,"
            f" g_NMDA {r['syn_g_nmda'][i].max():.2f} nS | min B {r['syn_mg'][i].min():.3f} max B {r['syn_mg'][i].max():.3f}"
            f" | peak i_AMPA {ia.min():.1f} pA, i_NMDA {inm.min():.1f} pA | charge AMPA {ia.sum() * dt * 1e-3:.2f} pC,"
            f" NMDA {inm.sum() * dt * 1e-3:.2f} pC | peak local v {r['syn_v'][i].max():.2f} mV"
            f" | peak [Ca]i {ch['cai'].max():.3f} µM | {_closure(ch)}")
    if "soma_i_clamp" in r:
        lines.append(f"soma: peak clamp current {r['soma_i_clamp'].min():.1f} pA, "
                     f"charge {r['soma_i_clamp'].sum() * dt * 1e-3:.2f} pC")
    lines.append(f"soma: peak v {r['soma_v'].max():.2f} mV, peak axial-in {r['soma_i_axial'].min():.1f} pA, "
                 f"peak [Ca]i {r['soma_chan']['cai'].max():.3f} µM, "
                 f"{_closure(r['soma_chan'])}")
    lines.append(f"trunk: peak depolarisation {(r['trunk_v'] - cfg.v_init).max():.2f} mV "
                 f"(at {r['trunk_d'][np.argmax((r['trunk_v'] - cfg.v_init).max(1))]:.0f} µm)")
    return "\n".join(lines)


def _default_zoom(times, aps, isi) -> tuple[float, float]:
    """Two AP intervals, starting at the AP before the first release of the MFB."""
    t1 = times[0] if times.size else 0.0
    before = aps[aps <= t1]
    t0 = before[-1] if before.size else (aps[0] if aps.size else max(0.0, t1 - 2.0))
    return (t0 - 1.0, t0 + 2 * isi)


def main(argv=None) -> None:
    p = build_parser(__doc__, ves_required=False)
    g = p.add_argument_group("diagnostics")
    g.add_argument("--from", dest="from_npz", default=None, help="results .npz to reproduce (overrides run options)")
    g.add_argument("--rep", type=int, default=0, help="which repetition to rerun (default: 0)")
    g.add_argument("--syn", type=int, default=0, help="which MFB to show in the synapse/channel figures (default: 0)")
    g.add_argument("--zoom", type=float, nargs=2, default=None, metavar=("T0", "T1"),
                   help="zoom window in ms for the synapse figure (default: two AP intervals from the "
                        "AP before the first release)")
    g.add_argument("--out-dir", default=None, help="where to write the figures")
    a = p.parse_args(argv)

    cfg, ves, trials, sites, rep, saved, out_dir = setup(a, p)
    print(f"[diag] {ves.path}: rep {rep}, trials {[int(x) for x in trials]}, mode {cfg.mode}")
    r = run_diagnostics(cfg, ves, trials, sites)
    if saved is not None:       # the rerun must match the saved run
        key, y, ts = saved
        k = max(1, int(cfg.save_every))
        err = float(np.abs(r[key][::k][: y.size] - y).max())
        print(f"[diag] rerun vs saved {key}: max difference {err:.3g} "
              + ("(match)" if err < 1e-3 * max(1.0, np.abs(y).max()) else "(MISMATCH)"))
    i = min(a.syn, len(r["model"].synapses) - 1)
    aps, isi = r["aps"], r["isi"] or 20.0
    zoom = tuple(a.zoom) if a.zoom else _default_zoom(r["trains"][i].times, aps, isi)

    out_dir.mkdir(parents=True, exist_ok=True)
    sup = (f"{Path(cfg.ves).name}  ·  rep {rep}, N = {len(trials)} MFB, seed {cfg.seed}, {cfg.mode}, "
           f"gq_AMPA {cfg.syn.gq_ampa:g} nS, NMDA ratio {cfg.syn.nmda_ratio:g}")
    fig_input(r, out_dir / "1_input.png", sup)
    fig_synapse(r, i, zoom, out_dir / "2_synapse.png", sup + f"  ·  MFB {i}")
    fig_channels(r, i, out_dir / "3_channels.png", sup + f"  ·  MFB {i}")
    fig_spread(r, out_dir / "4_spread.png", sup)
    text = summary(r)
    (out_dir / "summary.txt").write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
