# Python/NEURON port of the Poirazi, Brannon & Mel (2003) CA1 model (github.com/Poirazi-Lab/Poirazi_CA1_detailed @ d2013e7); see NOTICE.md.
"""The model's distance metric.

The model does **not** use path distance. Every gradient (Rm, Ra, I_h, I_A, Ca
channels, Na attenuation) uses the absolute length of the projection of a
segment's 3-D position onto the soma-to-apex axis, plus a 41.1 um adjustment so
that distances are measured from the cell body.

Ports of:

* ``lib/vector-distance.hoc``: ``vector_distance``, ``find_vector_distance_precise``
  ("written by Terrence Brannon, last modified by Yiota Poirazi, July 2001")
* ``lib/map-segments-to-3d.hoc``: ``map_segments_to_3d`` (``endpt``, ``fracpt``),
  which in the original stores per-segment coordinates in the ``d3`` mechanism
  (``x_d3``, ``y_d3``, ``z_d3``). The port keeps them in a Python dict instead;
  ``d3.mod`` is compiled but never inserted.
* ``morphology/n123/cell-analysis.hoc``: choice of reference point (3-D point 0 of
  ``apical_dendrite[4]``) and apex (``vcreate2(vAPEX, 0.5)`` on
  ``apical_dendrite[92]``; ``x3d(0.5)`` truncates to point 0).
"""
from __future__ import annotations

import math
from collections.abc import Sequence

from neuron import nrn

from .hoc_compat import for_x, seg_index, x3d_trunc

Vec3 = tuple[float, float, float]


def vector_distance(rp: Sequence[float], apex: Sequence[float], poi: Sequence[float],
                    adjustment: float) -> float:
    """Port of ``func vector_distance()`` (lib/vector-distance.hoc).

    Same operation order as the HOC Vector calls: ``APEX.sub(RP)``,
    ``POI.sub(RP)``, ``APEX_BAR = sqrt((APEX*APEX).sum())``, ``APEX.div(APEX_BAR)``,
    ``H = abs(POI.dot(APEX) + adjustment)``.
    """
    a = [apex[i] - rp[i] for i in range(3)]
    p = [poi[i] - rp[i] for i in range(3)]
    s = 0.0
    for v in a:
        s += v * v
    bar = math.sqrt(s)
    u = [v / bar for v in a]
    dot = 0.0
    for i in range(3):
        dot += p[i] * u[i]
    return abs(dot + adjustment)


def map_segments_to_3d(sec: nrn.Section) -> list[Vec3]:
    """Port of ``proc map_segments_to_3d()`` for one section.

    Returns the coordinate stored per segment *after* all of the original's
    writes. The original writes ``x_d3(0)`` (= first segment) with 3-D point 0,
    then every segment centre with a linear interpolation along ``arc3d``, then
    ``x_d3(1)`` (= last segment) with the last 3-D point. Hence the **last
    segment holds the section's end point, not its centre** (and a 1-segment
    section holds its end point).
    """
    nseg = sec.nseg
    n3d = int(sec.n3d())
    L = sec.L
    out: list[Vec3 | None] = [None] * nseg

    def endpt(x: float) -> None:              # proc endpt()
        P = (n3d - 1) * x
        out[seg_index(nseg, x)] = x3d_trunc(sec, P)

    i = 0
    endpt(0.0)
    for x in for_x(sec):
        if not (0.0 < x < 1.0):
            continue
        while sec.arc3d(i) / L < x:
            i += 1
        D = sec.arc3d(i) - sec.arc3d(i - 1)
        if D <= 0:
            raise ValueError(f"{sec.name()} had a D <= 0")  # original only printed a warning
        alpha = (x * L - sec.arc3d(i - 1)) / D
        # proc fracpt(alpha, x)
        p0 = (sec.x3d(i - 1), sec.y3d(i - 1), sec.z3d(i - 1))
        p1 = (sec.x3d(i), sec.y3d(i), sec.z3d(i))
        out[seg_index(nseg, x)] = tuple(p0[k] + (p1[k] - p0[k]) * alpha for k in range(3))  # type: ignore[assignment]
    endpt(1.0)
    assert all(o is not None for o in out)
    return out  # type: ignore[return-value]


class DistanceMetric:
    """Holds RP/APEX and the per-segment 3-D map; answers ``find_vector_distance_precise``."""

    def __init__(self, rp: Vec3, apex: Vec3, adjustment: float) -> None:
        self.rp = rp
        self.apex = apex
        self.adjustment = adjustment
        self._coords: dict[nrn.Section, list[Vec3]] = {}

    def map_section(self, sec: nrn.Section) -> None:
        """Store the d3 coordinates for ``sec`` at its current nseg."""
        self._coords[sec] = map_segments_to_3d(sec)

    def coords(self, sec: nrn.Section, x: float) -> Vec3:
        """HOC ``(x_d3(x), y_d3(x), z_d3(x))`` -- ``vcreate3(vec, x)``."""
        c = self._coords[sec]
        return c[seg_index(len(c), x)]

    def precise(self, sec: nrn.Section, x: float) -> float:
        """Port of ``find_vector_distance_precise(secname(), x)``."""
        return vector_distance(self.rp, self.apex, self.coords(sec, x), self.adjustment)

    def raw(self, poi: Sequence[float]) -> float:
        """``vector_distance(vRP, vAPEX, poi, adjustment)`` for an arbitrary point."""
        return vector_distance(self.rp, self.apex, poi, self.adjustment)
