"""Load vesicle-release times from an MCell ``vesData.dat`` pickle.

One trial of the MCell simulation = one mossy-fibre bouton (MFB). Its release
times are all releases of all its active zones (AZs) in that trial, as in
``scripts_analysis/analysis.py`` (``relStat``).

Two layouts exist in ``data/``:

* **per-AZ** (``control_buffer``, ``control_unsatBuffer``, ``syt7KO``, ...)::

      {'AZ1': {'sync': [trial_0, ...], 'async': [...], 'spont': [...]}, ..., 'AZn': {...}}

* **flat** (``control``, ``findPr``): ``{key: [trial_0, ...]}``. The AZs are already
  merged and the release type is not stored. ``control`` has one key, ``findPr`` has 12
  (pick one with ``key``).

``trial_k`` is a list of release times in **seconds**. Everything returned here is
in **ms**.
"""
from __future__ import annotations

import pickle
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

TYPES = ("sync", "async", "spont")
#: integer code of each release type in saved event tables (-1 = unknown, flat layout)
TYPE_CODE = {t: i for i, t in enumerate(TYPES)}


@dataclass(frozen=True)
class Train:
    """Release times of one bouton (one trial), sorted, in ms."""

    trial: int
    times: np.ndarray       # ms, sorted
    az: np.ndarray          # AZ number (1-based) of each release; -1 if unknown
    kind: np.ndarray        # TYPE_CODE of each release; -1 if unknown


class VesicleData:
    """A loaded ``vesData.dat`` file.

    Parameters
    ----------
    path:
        The pickle file (or the directory that holds ``vesData.dat``).
    types:
        Release types to include (per-AZ layout only).
    key:
        Which key to use for a flat layout with several keys (e.g. ``findPr``).
    """

    def __init__(self, path: str | Path, types: tuple[str, ...] = TYPES, key: str | None = None) -> None:
        path = Path(path)
        if path.is_dir():
            path = path / "vesData.dat"
        self.path = path
        with open(path, "rb") as f:
            raw = pickle.load(f)
        if not isinstance(raw, dict) or not raw:
            raise ValueError(f"{path}: expected a non-empty dict")
        bad = set(types) - set(TYPES)
        if bad or not types:
            raise ValueError(f"types must be a non-empty subset of {TYPES}, got {types}")
        first = next(iter(raw.values()))
        if isinstance(first, dict):
            self.layout = "per-AZ"
            self._load_per_az(raw, tuple(types))
            self.key = None
        else:
            self.layout = "flat"
            if tuple(types) != TYPES:
                raise ValueError(f"{path}: flat layout has no release types; "
                                 f"only all types ({','.join(TYPES)}) can be used")
            if key is None:
                if len(raw) > 1:
                    raise ValueError(f"{path}: flat layout with keys {list(raw)}; choose one with key=/--key")
                key = next(iter(raw))
            if key not in raw:
                raise ValueError(f"{path}: key {key!r} not in {list(raw)}")
            self.key = key
            self._load_flat(raw[key])
        self.types = tuple(types)

    # ------------------------------------------------------------------ layouts
    def _load_per_az(self, raw: dict, types: tuple[str, ...]) -> None:
        az_names = sorted(raw, key=lambda s: int(re.sub(r"\D", "", s) or 0))
        n_trials = {len(raw[a][t]) for a in az_names for t in TYPES if t in raw[a]}
        if len(n_trials) != 1:
            raise ValueError(f"{self.path}: AZs/types have different trial counts {n_trials}")
        self.n_trials = n_trials.pop()
        self.n_az = len(az_names)
        self._trials: list[tuple[np.ndarray, np.ndarray, np.ndarray]] = []
        for k in range(self.n_trials):
            t, az, kind = [], [], []
            for a in az_names:
                a_id = int(re.sub(r"\D", "", a))
                for typ in types:
                    rel = raw[a][typ][k]
                    t.extend(float(x) for x in rel)
                    az.extend([a_id] * len(rel))
                    kind.extend([TYPE_CODE[typ]] * len(rel))
            self._trials.append(self._sorted(t, az, kind))

    def _load_flat(self, trials: list) -> None:
        self.n_trials = len(trials)
        self.n_az = None
        self._trials = [self._sorted([float(x) for x in tr], [-1] * len(tr), [-1] * len(tr))
                        for tr in trials]

    @staticmethod
    def _sorted(t, az, kind) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        t = np.asarray(t, dtype=float) * 1e3          # s -> ms
        o = np.argsort(t, kind="stable")
        return t[o], np.asarray(az, dtype=int)[o], np.asarray(kind, dtype=int)[o]

    # --------------------------------------------------------------------- access
    def train(self, trial: int) -> Train:
        t, az, kind = self._trials[trial]
        return Train(trial, t.copy(), az.copy(), kind.copy())

    def n_releases(self, trials=None) -> int:
        """Total number of releases (selected types) in the given trials (default: all)."""
        idx = range(self.n_trials) if trials is None else trials
        return int(sum(self._trials[k][0].size for k in idx))

    def draw_trials(self, n: int, reps: int, rng: np.random.Generator) -> np.ndarray:
        """``reps x n`` trial indices.

        Without replacement over the whole run if ``n*reps <= n_trials`` (every bouton in
        every repetition is a different trial); otherwise without replacement within
        each repetition only.
        """
        if n > self.n_trials:
            raise ValueError(f"n_mfb={n} > {self.n_trials} trials in {self.path}")
        if n * reps <= self.n_trials:
            return rng.choice(self.n_trials, size=n * reps, replace=False).reshape(reps, n)
        return np.stack([rng.choice(self.n_trials, size=n, replace=False) for _ in range(reps)])


def protocol_from_path(path: str | Path) -> dict[str, float | None]:
    """AP protocol from the data directory name (``..._ISI_20_nAP_10...``).

    APs are at ``1.5 + k*ISI`` ms (k = 0..nAP-1), as in ``analysis.py``.
    """
    s = str(Path(path))
    isi = re.search(r"ISI_(\d+(?:\.\d+)?)", s)
    nap = re.search(r"nAP_(\d+)", s)
    return {"isi": float(isi.group(1)) if isi else None, "n_ap": int(nap.group(1)) if nap else None}


def ap_times(isi: float | None, n_ap: int | None, t0: float = 1.5) -> np.ndarray:
    if n_ap is None:
        return np.array([t0])
    return t0 + np.arange(n_ap) * (isi or 0.0)
