# Python/NEURON port of the Poirazi, Brannon & Mel (2003) CA1 model (github.com/Poirazi-Lab/Poirazi_CA1_detailed @ d2013e7); see NOTICE.md.
"""Helpers that reproduce HOC range-variable semantics from Python.

HOC facts relied on by the port (verified on NEURON 9.0.2 with toy sections):

* ``for (x) { ... }`` visits ``0``, every segment centre, then ``1``
  (Python ``for seg in sec`` visits only the centres).
* Writing/reading a *density-mechanism* range variable at ``x=0`` (``x=1``)
  addresses the first (last) segment. Python raises for ``sec(0).mech``, so the
  port maps x to a segment explicitly with :func:`seg_at`.
* A range variable assigned *without* ``(x)`` (``Ra = ...``, ``ek = ...``,
  ``gkbar_mykca = ...``) sets the whole section, so inside ``for (x)`` the last
  iteration (x=1) wins.
* ``v(0)`` / ``v(1)`` are the section's end nodes (``sec(0).v`` in Python).
* ``x3d(i)`` truncates a fractional index (``x3d(0.5) == x3d(0)``).
* ``diam(x) = diam(x)*1.0`` is **not** a no-op when 3-D points exist: it
  flattens the 3-D diameters inside the segment and changes area/ri.
"""
from __future__ import annotations

from collections.abc import Iterator

from neuron import h, nrn


def for_x(sec: nrn.Section) -> list[float]:
    """Arc positions visited by HOC ``for (x)``: 0, all segment centres, 1."""
    n = sec.nseg
    return [0.0] + [seg.x for seg in sec] + [1.0]


def interior_x(sec: nrn.Section) -> list[float]:
    """Arc positions visited by ``for (x) if (x > 0 && x < 1)`` (segment centres)."""
    return [seg.x for seg in sec]


def seg_index(nseg: int, x: float) -> int:
    """Index of the segment a density-mechanism range variable at ``x`` refers to."""
    if x < 0.0 or x > 1.0:
        raise ValueError(f"x={x} out of range")
    i = int(x * nseg)
    return nseg - 1 if i >= nseg else i


def seg_at(sec: nrn.Section, x: float) -> nrn.Segment:
    """The segment that HOC ``rangevar(x)`` reads or writes for a density mechanism."""
    segs = list(sec)
    return segs[seg_index(sec.nseg, x)]


def iter_for_x(sec: nrn.Section) -> Iterator[tuple[float, nrn.Segment]]:
    """Yield ``(x, segment)`` pairs in HOC ``for (x)`` order (end points included)."""
    segs = list(sec)
    n = sec.nseg
    for x in for_x(sec):
        yield x, segs[seg_index(n, x)]


def x3d_trunc(sec: nrn.Section, idx: float) -> tuple[float, float, float]:
    """HOC ``(x3d(idx), y3d(idx), z3d(idx))`` with HOC's integer truncation of ``idx``."""
    i = int(idx)
    return (sec.x3d(i), sec.y3d(i), sec.z3d(i))


def ismembrane(sec: nrn.Section, name: str) -> bool:
    """HOC ``ismembrane("name")`` for the given section."""
    return bool(sec.has_membrane(name))


def ion_style(sec: nrn.Section, ion: str, *args: int) -> None:
    """HOC ``ion_style(ion, ...)`` executed with ``sec`` as the accessed section."""
    sec.push()
    try:
        h.ion_style(ion, *args)
    finally:
        h.pop_section()
