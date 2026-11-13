# Python/NEURON port of the Poirazi, Brannon & Mel (2003) CA1 model (github.com/Poirazi-Lab/Poirazi_CA1_detailed @ d2013e7); see NOTICE.md.
"""Port of ``lib/current-balance.hoc``.

"This function is used to balance the membrane potential to v_init (= -70 mV).
written by Yiota Poirazi, July 2001."

Each segment's ``e_pas`` is chosen so that the passive current cancels the ionic
currents at ``v_init``. The original notes that it "does not account for
non-specific ion currents" -- here that is harmless because ``h.mod`` writes its
current as ``ina`` (its ``NONSPECIFIC_CURRENT`` line is commented out) and the
``il`` leaks of ``hha2``/``hha_old`` have ``gl = 0``.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from neuron import h

from .hoc_compat import ismembrane, iter_for_x

if TYPE_CHECKING:
    from .build import Cell


def current_balance(cell: Cell, v_init: float) -> dict[str, int]:
    """Port of ``proc current_balance()``.

    Same branch logic on ``ismembrane`` (na_ion, ca_ion, the custom ``Ca_ion``
    of ``cat.mod`` with current ``iCa``, k_ion), same ``for (x)`` loop including
    the x=0 and x=1 end points (which address the first/last segment for range
    variables, and the end nodes for ``v``), and the same ``fcurrent()`` after
    every assignment.

    Returns counts of how often each branch was taken (for testing).
    """
    h.finitialize(v_init)
    h.fcurrent()
    counts = {"na_ca_Ca_k": 0, "na_ca_k": 0, "na_k": 0, "v_only": 0}
    for sec in cell.all:
        has_na = ismembrane(sec, "na_ion")
        has_ca = ismembrane(sec, "ca_ion")
        has_Ca = ismembrane(sec, "Ca_ion")
        has_k = ismembrane(sec, "k_ion")
        for x, seg in iter_for_x(sec):
            v = sec(x).v
            if has_na and has_ca and has_Ca and has_k:
                seg.e_pas = (seg.ina + seg.ik + seg.ica + seg.iCa + seg.g_pas * v) / seg.g_pas
                counts["na_ca_Ca_k"] += 1
            elif has_na and has_ca and has_k:
                seg.e_pas = (seg.ina + seg.ik + seg.ica + seg.g_pas * v) / seg.g_pas
                counts["na_ca_k"] += 1
            elif has_na and has_k:
                seg.e_pas = (seg.ina + seg.ik + seg.g_pas * v) / seg.g_pas
                counts["na_k"] += 1
            else:
                # print "simply assigning v(x)"
                seg.e_pas = v
                counts["v_only"] += 1
            h.fcurrent()
    return counts
