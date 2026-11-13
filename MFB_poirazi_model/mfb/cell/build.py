# Python/NEURON port of the Poirazi, Brannon & Mel (2003) CA1 model (github.com/Poirazi-Lab/Poirazi_CA1_detailed @ d2013e7); see NOTICE.md.
"""The CA1 pyramidal cell (Poirazi, Brannon & Mel 2003): morphology + ``cell_setup``.

Trimmed copy of ``ca1/morphology.py`` and ``ca1/cell.py`` from ``../poirazi_model``.
It contains the ports of ``morphology/n123/cell.hoc`` (morphology),
``morphology/n123/cell-analysis.hoc`` (distance reference points, section lists)
and ``experiment/cell-setup.hoc`` (biophysics, in :mod:`.biophys`).
The block procedures, tuning and synapse code of the full port are left out.
"""
from __future__ import annotations

import itertools
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from neuron import h, nrn

from ..mechanisms import load_mechanisms
from . import biophys
from .distance import DistanceMetric
from .hoc_compat import x3d_trunc
from .params import CellParams

DATA_DIR = Path(__file__).resolve().parent / "data"

LIST_NAMES = (
    "soma_list", "axon_sec_list", "basal_tree_list", "apical_trunk_list",
    "apical_non_trunk_list", "apical_tip_list", "apical_tip_list_addendum",
    "peri_trunk_list", "peri_trunk_addl",
)

_ids = itertools.count()


@lru_cache(maxsize=None)
def load_json(name: str) -> dict[str, Any]:
    """Load (and cache) one of the data files in ``mfb/cell/data``."""
    return json.loads((DATA_DIR / name).read_text())


def build_sections(owner: object) -> dict[str, nrn.Section]:
    """Create all sections of ``cell.hoc`` (``create``/``connect``/``pt3dadd``).

    Sections are created in HOC creation order and connected in the file's
    connect order, so ``forall`` order and node ordering match the original.
    """
    data = load_json("morphology.json")
    secs: dict[str, nrn.Section] = {}
    for entry in data["sections"]:
        secs[entry["name"]] = h.Section(name=entry["name"], cell=owner)
    for c in data["connections"]:
        # HOC: {parent connect child(child_x), parent_x}
        secs[c["child"]].connect(secs[c["parent"]](c["parent_x"]), c["child_x"])
    for entry in data["sections"]:
        sec = secs[entry["name"]]
        sec.pt3dclear()
        for x, y, z, d in entry["points"]:
            sec.pt3dadd(x, y, z, d)
    return secs


class Cell:
    """One instance of the n123 CA1 pyramidal cell, fully set up (``cell_setup()``).

    The resting potential is balanced to ``params.v_init`` (-70 mV) by
    ``current_balance``, exactly as in the original.
    """

    def __init__(self, params: CellParams | None = None) -> None:
        load_mechanisms()
        h.load_file("stdrun.hoc")
        self.params = params or CellParams()
        self.gid = next(_ids)
        self.secs: dict[str, nrn.Section] = build_sections(self)
        self.all: list[nrn.Section] = list(self.secs.values())   # HOC forall order
        self._names = {sec: name for name, sec in self.secs.items()}
        lists = load_json("section_lists.json")
        self.lists: dict[str, list[nrn.Section]] = {
            k: [self.secs[n] for n in lists[k]] for k in LIST_NAMES
        }
        self.oblique_paths = [[self.secs[n] for n in p] for p in lists["oblique_paths"]]
        self.basal_paths = [[self.secs[n] for n in p] for p in lists["basal_paths"]]
        # access apical_dendrite[4]; vcreate(vRP): point of reference (soma with adjustment)
        rp = x3d_trunc(self.secs["apical_dendrite[4]"], 0)
        # access apical_dendrite[92]; vcreate2(vAPEX,0.5): x3d(0.5) truncates to point 0
        apex = x3d_trunc(self.secs["apical_dendrite[92]"], 0.5)
        self.dist = DistanceMetric(rp, apex, self.params.adjustment)
        biophys.cell_setup(self)

    def __repr__(self) -> str:
        return f"CA1Cell[{self.gid}]"

    @property
    def soma(self) -> nrn.Section:
        """``soma`` in HOC (``access soma`` == ``soma[0]``)."""
        return self.secs["soma[0]"]

    def section(self, name: str) -> nrn.Section:
        """Section by its HOC name, e.g. ``"apical_dendrite[14]"``."""
        return self.secs[name]

    def name(self, sec: nrn.Section) -> str:
        """HOC name of one of this cell's sections."""
        return self._names[sec]

    def distance(self, sec: nrn.Section, x: float) -> float:
        """The model's distance metric (``find_vector_distance_precise``), in um."""
        return self.dist.precise(sec, x)
