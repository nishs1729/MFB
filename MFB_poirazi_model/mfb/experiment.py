"""Build the cell with MFB synapses, run it, and save the EPSCs.

Two recording modes (PLAN 4.6):

* ``vclamp`` (default): an SEClamp holds the soma at ``v_hold``. The somatic EPSC is the
  clamp current. The local EPSC is the synaptic current at each synapse.
* ``iclamp``: no clamp. You get the local synaptic currents and the EPSPs at each
  synapse and at the soma.

In both modes the axial current from the dendrite into the soma is also recorded
(``soma_i_axial``).

Sign convention: every current is saved in pA, with inward / depolarising = negative,
like a measured EPSC. The clamp current is SEClamp ``i`` (electrode convention, so it
is negative while it cancels an inward synaptic current). ``soma_i_axial`` is minus
the current that flows from the dendrite into the soma.
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
from neuron import h

from .cell import Cell, CellParams
from .cell.hoc_compat import ismembrane
from .synapses import MFBSynapse, Site, SynParams, parse_site, random_sites
from .vesicles import TYPES, VesicleData, ap_times, protocol_from_path


@dataclass(frozen=True)
class RunConfig:
    """Everything that defines one run (saved with the results)."""

    ves: str                          # path to vesData.dat (or its directory)
    n_mfb: int = 1                    # N boutons = N synapses
    reps: int = 1                     # M independent realisations
    seed: int = 0                     # RNG seed (trial choice and placement)
    types: tuple[str, ...] = TYPES    # release types to include
    key: str | None = None            # flat layout with several keys (findPr)
    mode: str = "vclamp"              # "vclamp" | "iclamp"
    dmin: float = 0.0                 # placement window on the apical trunk (um)
    dmax: float = 100.0
    sites: tuple[str, ...] = ()       # explicit sites; overrides random placement
    tstop: float = 300.0              # ms
    dt: float = 0.025                 # ms
    celsius: float = 34.0
    v_init: float = -70.0             # rest (current_balance target)
    v_hold: float = -70.0             # SEClamp holding potential (vclamp)
    rs: float = 0.01                  # SEClamp series resistance (MOhm); ~ideal clamp
    isi: float | None = None          # AP protocol; default parsed from the path
    n_ap: int | None = None
    save_every: int = 1               # keep every k-th sample in the saved traces
    syn: SynParams = field(default_factory=SynParams)

    def to_json(self) -> str:
        d = asdict(self)
        return json.dumps(d, indent=1)


class MFBModel:
    """The cell + one MFBSyn per bouton + recordings. Reusable across repetitions.

    Build it, then call :meth:`add_synapses` once (sites as :class:`Site` objects or
    strings like ``"apical_dendrite[14](0.5)"``), then :meth:`run` any number of times.
    """

    def __init__(self, syn: SynParams = SynParams(), mode: str = "vclamp", v_init: float = -70.0,
                 v_hold: float = -70.0, rs: float = 0.01, cell_params: CellParams | None = None) -> None:
        if mode not in ("vclamp", "iclamp"):
            raise ValueError(f"mode must be 'vclamp' or 'iclamp', got {mode!r}")
        self.cell = cell = Cell(cell_params or CellParams(v_init=v_init))
        self.v_init = v_init
        self.mode = mode
        self.syn_params = syn
        self.synapses: list[MFBSynapse] = []
        self.sites: list[Site] = []
        self._syn: list[dict] = []
        self.soma_entries: list = []
        self._axial: list = []
        # Initial [Ca]i of every segment, restored before each run. ion_style("ca_ion",0,1,0,0,0)
        # in cell_setup means finitialize does not reset cai (ISSUES I6 of the full port),
        # so without this a run would start from the previous run's final cai.
        self._cai0 = [(seg, seg.cai) for sec in cell.all if ismembrane(sec, "ca_ion") for seg in sec]

        soma = cell.soma(0.5)
        self.clamp = None
        if mode == "vclamp":
            self.clamp = h.SEClamp(soma)
            self.clamp.dur1 = 1e9
            self.clamp.amp1 = v_hold
            self.clamp.rs = rs
        self._t = _rec(h._ref_t)
        self._v_soma = _rec(soma._ref_v)
        self._i_clamp = _rec(self.clamp._ref_i) if self.clamp is not None else None
        self._fih = h.FInitializeHandler(1, self._queue_events)

    def add_synapses(self, sites: list[Site] | list[str]) -> None:
        """Add one MFBSyn (and its recordings) per site."""
        if self.synapses:
            raise RuntimeError("synapses already added")
        cell = self.cell
        self.sites = [parse_site(cell, s) if isinstance(s, str) else s for s in sites]
        self.synapses = [MFBSynapse(cell, s, self.syn_params) for s in self.sites]
        self._syn = [{
            "i_ampa": _rec(s.syn._ref_i_ampa), "i_nmda": _rec(s.syn._ref_i_nmda),
            "g_ampa": _rec(s.syn._ref_g_ampa), "g_nmda": _rec(s.syn._ref_g_nmda),
            "v": _rec(s.sec(s.site.x)._ref_v),
        } for s in self.synapses]
        # Axial current into the soma: for each section that joins a soma section and
        # leads to a synapse, (v_child_first_node - v_parent_node) / ri (MOhm) -> nA.
        self.soma_entries = self._soma_entries()
        self._axial = [(_rec(sec(x0)._ref_v), _rec(psec(px)._ref_v), sec(x0).ri())
                       for sec, x0, psec, px in self.soma_entries]

    def _soma_entries(self):
        soma = set(self.cell.lists["soma_list"])
        out = {}
        for s in self.synapses:
            sec = s.sec
            if sec in soma:
                continue
            while sec.parentseg() is not None and sec.parentseg().sec not in soma:
                sec = sec.parentseg().sec
            ps = sec.parentseg()
            if ps is None:
                continue
            first = next(iter(sec))
            out[self.cell.name(sec)] = (sec, first.x, ps.sec, ps.x)
        return list(out.values())

    def _queue_events(self) -> None:
        for s in self.synapses:
            s.queue()

    # ------------------------------------------------------------------ running
    def run(self, trains: list[np.ndarray], tstop: float = 300.0, dt: float = 0.025,
            celsius: float = 34.0) -> dict[str, np.ndarray]:
        """Run once with ``trains[i]`` = release times (ms) of synapse i.

        All state is reset (finitialize + restored cai). Returns traces in
        pA / nS / mV / ms, with inward currents negative.
        """
        if len(trains) != len(self.synapses):
            raise ValueError(f"{len(trains)} trains for {len(self.synapses)} synapses")
        for s, tr in zip(self.synapses, trains):
            s.times = np.sort(np.asarray(tr, dtype=float))
        h.cvode_active(0)
        h.celsius = celsius
        h.dt = dt
        h.steps_per_ms = 1.0 / dt
        h.tstop = tstop
        h.setdt()
        for seg, c in self._cai0:
            seg.cai = c
        h.finitialize(self.v_init)   # queues the events (FInitializeHandler)
        h.fcurrent()
        h.continuerun(tstop)

        a = np.array
        out = {"t": a(self._t), "soma_v": a(self._v_soma)}
        if self._i_clamp is not None:
            out["soma_i_clamp"] = 1e3 * a(self._i_clamp)      # nA -> pA; SEClamp i < 0 for an EPSC
        ax = np.zeros_like(out["t"])
        for vc, vp, ri in self._axial:
            ax += (a(vc) - a(vp)) / ri                        # nA, + = into soma
        out["soma_i_axial"] = -1e3 * ax
        for k, conv in (("i_ampa", 1e3), ("i_nmda", 1e3), ("g_ampa", 1e3), ("g_nmda", 1e3), ("v", 1.0)):
            out[f"syn_{k}"] = np.stack([conv * a(r[k]) for r in self._syn]) if self._syn else np.empty((0, out["t"].size))
        out["syn_nev"] = np.array([s.syn.nev for s in self.synapses])
        return out


# ---------------------------------------------------------------------------- experiment
def run_experiment(cfg: RunConfig, out: str | Path | None = None, verbose: bool = True) -> Path:
    """Load vesicles, place N synapses, run M repetitions, save one ``.npz``."""
    rng = np.random.default_rng(cfg.seed)
    ves = VesicleData(cfg.ves, types=cfg.types, key=cfg.key)
    trials = ves.draw_trials(cfg.n_mfb, cfg.reps, rng)
    proto = protocol_from_path(ves.path)
    isi = cfg.isi if cfg.isi is not None else proto["isi"]
    n_ap = cfg.n_ap if cfg.n_ap is not None else proto["n_ap"]
    aps = ap_times(isi, n_ap)

    model = MFBModel(syn=cfg.syn, mode=cfg.mode, v_init=cfg.v_init, v_hold=cfg.v_hold, rs=cfg.rs)
    if cfg.sites:
        if len(cfg.sites) != cfg.n_mfb:
            raise ValueError(f"{len(cfg.sites)} sites given for n_mfb={cfg.n_mfb}")
        model.add_synapses(list(cfg.sites))
    else:
        model.add_synapses(random_sites(model.cell, cfg.n_mfb, rng, cfg.dmin, cfg.dmax))
    if verbose:
        print(f"[mfb] {ves.path} ({ves.layout}, {ves.n_trials} trials"
              + (f", {ves.n_az} AZs" if ves.n_az else "") + f", types {','.join(ves.types)})")
        for i, s in enumerate(model.sites):
            print(f"[mfb] MFB {i}: {s}")

    k = max(1, int(cfg.save_every))
    rec: dict[str, list] = {}
    events = []
    t0 = time.time()
    for r in range(cfg.reps):
        trains = [ves.train(int(tr)) for tr in trials[r]]
        res = model.run([tr.times for tr in trains], cfg.tstop, cfg.dt, cfg.celsius)
        expected = [int(np.sum(tr.times < cfg.tstop)) for tr in trains]
        if list(res["syn_nev"].astype(int)) != expected:
            print(f"[mfb] WARNING rep {r}: delivered {res['syn_nev']} vesicles, expected {expected}")
        for i, tr in enumerate(trains):
            for t, az, kind in zip(tr.times, tr.az, tr.kind):
                events.append((r, i, tr.trial, t, az, kind))
        for name, arr in res.items():
            if name in ("t", "syn_nev"):
                continue
            rec.setdefault(name, []).append(arr[..., ::k].astype(np.float32))
        if verbose:
            n = sum(len(tr.times) for tr in trains)
            pk = res["soma_i_clamp"].min() if "soma_i_clamp" in res else res["soma_v"].max()
            lab = "peak somatic EPSC %.1f pA" % pk if "soma_i_clamp" in res else "peak soma V %.2f mV" % pk
            print(f"[mfb] rep {r + 1}/{cfg.reps}: trials {[int(x) for x in trials[r]]}, {n} vesicles, {lab}")
    if verbose:
        print(f"[mfb] {cfg.reps} rep(s) in {time.time() - t0:.1f} s")

    ev = np.array(events, dtype=float).reshape(-1, 6)
    data = {name: np.stack(v) for name, v in rec.items()}
    data.update({
        "t": res["t"][::k],
        "trials": trials,
        "ap_times": aps,
        "syn_section": np.array([s.section for s in model.sites]),
        "syn_x": np.array([s.x for s in model.sites]),
        "syn_distance": np.array([s.distance for s in model.sites]),
        "ev_rep": ev[:, 0].astype(int), "ev_syn": ev[:, 1].astype(int),
        "ev_trial": ev[:, 2].astype(int), "ev_t": ev[:, 3],
        "ev_az": ev[:, 4].astype(int), "ev_type": ev[:, 5].astype(int),
        "config": np.array(cfg.to_json()),
        "meta": np.array(json.dumps({
            "units": {"t": "ms", "current": "pA (inward negative)", "conductance": "nS", "v": "mV"},
            "layout": ves.layout, "n_trials_in_file": ves.n_trials, "n_az": ves.n_az,
            "ev_type_codes": {t: i for i, t in enumerate(TYPES)} | {"unknown": -1},
            "isi": isi, "n_ap": n_ap,
            "soma_entries": [model.cell.name(e[0]) for e in model.soma_entries],
        })),
    })
    out = Path(out) if out is not None else default_out(cfg)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out, **data)
    if verbose:
        print(f"[mfb] saved {out}")
    return out


def _rec(ref) -> h.Vector:
    """Record ``ref`` every time step from t = 0."""
    v = h.Vector()
    v.record(ref)
    return v


def default_out(cfg: RunConfig) -> Path:
    p = Path(cfg.ves)
    name = (p.name if p.is_dir() else p.parent.name) or "ves"
    key = f"_key{cfg.key}" if cfg.key else ""
    return Path("results") / f"{name}{key}_N{cfg.n_mfb}_M{cfg.reps}_seed{cfg.seed}_{cfg.mode}.npz"
