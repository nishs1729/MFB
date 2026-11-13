"""Synapse placement and vesicle-event delivery.

Each MFB becomes one ``MFBSyn`` point process (AMPA + NMDA) at one compartment. The
whole bouton (all of its AZs) sits there. Conductances sum linearly, so this is exactly
equivalent to one synapse per AZ at the same spot.

Placement (PLAN 4.1): proximal apical trunk, i.e. segments of ``apical_trunk_list``
whose centre lies at ``dmin <= distance <= dmax`` um from the soma (the model's own
distance metric). A bouton's segment is drawn at random, weighted by segment length,
so positions are uniform along the trunk. Several MFBs may share a segment; each keeps
its own synapse and recorded current.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass

import numpy as np
from neuron import h, nrn

from .cell import Cell


@dataclass(frozen=True)
class SynParams:
    """Quantal synapse parameters (MF->CA3-like placeholders, PLAN 4.5)."""

    gq_ampa: float = 0.5        # nS, peak AMPA conductance of one vesicle
    tau_r_ampa: float = 0.5     # ms
    tau_d_ampa: float = 5.0     # ms
    nmda_ratio: float = 0.3     # peak g_NMDA / peak g_AMPA of one vesicle (before Mg block)
    tau_r_nmda: float = 3.0     # ms
    tau_d_nmda: float = 70.0    # ms
    mg: float = 1.0             # mM
    e_rev: float = 0.0          # mV

    def apply(self, syn) -> None:
        syn.gq_ampa = self.gq_ampa * 1e-3      # nS -> uS
        syn.tau_r_ampa = self.tau_r_ampa
        syn.tau_d_ampa = self.tau_d_ampa
        syn.nmda_ratio = self.nmda_ratio
        syn.tau_r_nmda = self.tau_r_nmda
        syn.tau_d_nmda = self.tau_d_nmda
        syn.mg = self.mg
        syn.e = self.e_rev

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Site:
    """Where one MFB synapse sits."""

    section: str     # HOC name, e.g. "apical_dendrite[14]"
    x: float         # segment centre
    distance: float  # um from soma (model metric)

    def __str__(self) -> str:
        return f"{self.section}({self.x:g}) @ {self.distance:.1f} um"


def candidate_segments(cell: Cell, dmin: float = 0.0, dmax: float = 100.0,
                       section_list: str = "apical_trunk_list") -> list[tuple[Site, float]]:
    """``(Site, segment length)`` for every segment of ``section_list`` with
    ``dmin <= distance(centre) <= dmax``."""
    out = []
    for sec in cell.lists[section_list]:
        for seg in sec:
            d = cell.distance(sec, seg.x)
            if dmin <= d <= dmax:
                out.append((Site(cell.name(sec), float(seg.x), float(d)), sec.L / sec.nseg))
    if not out:
        raise ValueError(f"no segments of {section_list} within [{dmin}, {dmax}] um")
    return out


def random_sites(cell: Cell, n: int, rng: np.random.Generator,
                 dmin: float = 0.0, dmax: float = 100.0) -> list[Site]:
    """``n`` sites drawn (with replacement) from the candidate segments, weighted by length."""
    cands = candidate_segments(cell, dmin, dmax)
    w = np.array([L for _, L in cands])
    idx = rng.choice(len(cands), size=n, replace=True, p=w / w.sum())
    return [cands[i][0] for i in idx]


_SITE_RE = re.compile(r"^\s*([A-Za-z_]+\[\d+\])\s*(?:\(\s*([0-9.eE+-]+)\s*\))?\s*$")


def parse_site(cell: Cell, spec: str) -> Site:
    """``"apical_dendrite[14](0.5)"`` (x defaults to 0.5) -> Site at that segment's centre."""
    m = _SITE_RE.match(spec)
    if not m:
        raise ValueError(f"bad site {spec!r}; expected e.g. 'apical_dendrite[14](0.5)'")
    sec = cell.section(m.group(1))
    x = float(m.group(2)) if m.group(2) else 0.5
    seg = sec(x)
    return Site(m.group(1), float(seg.x), float(cell.distance(sec, seg.x)))


class MFBSynapse:
    """One ``MFBSyn`` + a source-less ``NetCon`` used to queue vesicle events."""

    def __init__(self, cell: Cell, site: Site, params: SynParams) -> None:
        self.site = site
        self.sec: nrn.Section = cell.section(site.section)
        self.syn = h.MFBSyn(self.sec(site.x))
        params.apply(self.syn)
        self.nc = h.NetCon(None, self.syn)
        self.nc.weight[0] = 1.0        # one vesicle = one quantum
        self.nc.delay = 0.0
        self.times = np.empty(0)

    def queue(self) -> None:
        """Queue every release time (ms) as an event. Called after each finitialize."""
        for t in self.times:
            self.nc.event(float(t))
