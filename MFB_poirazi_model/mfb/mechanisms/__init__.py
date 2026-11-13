"""Loader for the NMODL mechanisms in this directory.

* 15 channel mechanisms, byte-identical copies of ``../poirazi_model/ca1/mechanisms``
  (= the original ``mechanism/*.mod`` of Poirazi et al.).
* ``mfbsyn.mod``: the new event-driven quantal AMPA+NMDA synapse (``MFBSyn``).

The library is compiled automatically (``nrnivmodl``) the first time it is needed, or
by hand with ``cd mfb/mechanisms && nrnivmodl .``. Only fixed-step integration is
used (the original mechanisms are not CVODE-compatible).
"""
from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from pathlib import Path

from neuron import h

MECH_DIR = Path(__file__).resolve().parent
_LOADED = False

#: mechanisms that must exist once the library is loaded
REQUIRED = ("hha2", "hha_old", "h", "kap", "kad", "km", "cal", "calH", "car", "cat",
            "somacar", "kca", "mykca", "cad", "nap", "MFBSyn")


def _lib() -> Path | None:
    arch = platform.machine()
    for lib in (MECH_DIR / arch / ".libs" / "libnrnmech.so", MECH_DIR / arch / "libnrnmech.so",
                MECH_DIR / "nrnmech.dll"):
        if lib.exists():
            return lib
    return None


def _stale(lib: Path) -> bool:
    t = lib.stat().st_mtime
    return any(m.stat().st_mtime > t for m in MECH_DIR.glob("*.mod"))


def compile_mechanisms() -> None:
    """Run ``nrnivmodl`` in this directory (uses the one next to the Python interpreter if present)."""
    exe = Path(sys.executable).with_name("nrnivmodl")
    cmd = str(exe) if exe.exists() else shutil.which("nrnivmodl")
    if cmd is None:
        raise RuntimeError("nrnivmodl not found; install NEURON (pip install neuron==9.0.2)")
    print(f"[mfb] compiling mechanisms in {MECH_DIR} ...", file=sys.stderr)
    r = subprocess.run([cmd, "."], cwd=MECH_DIR, capture_output=True, text=True)
    (MECH_DIR / "nrnivmodl.log").write_text(r.stdout + r.stderr)
    if r.returncode != 0:
        raise RuntimeError(f"nrnivmodl failed, see {MECH_DIR / 'nrnivmodl.log'}")


def load_mechanisms() -> None:
    """Compile (if needed) and load the mechanism library exactly once per process."""
    global _LOADED
    if _LOADED:
        return
    if hasattr(h, "MFBSyn"):
        # NEURON auto-loads an x86_64/ found in the working directory
        _LOADED = True
        return
    lib = _lib()
    if lib is None or _stale(lib):
        compile_mechanisms()
        lib = _lib()
        if lib is None:
            raise RuntimeError(f"compiled library not found in {MECH_DIR} after nrnivmodl")
    h.nrn_load_dll(str(lib))
    missing = [m for m in REQUIRED if not (hasattr(h, m) or _is_density(m))]
    if missing:
        raise RuntimeError(f"mechanisms missing after load: {missing}")
    _LOADED = True


def _is_density(name: str) -> bool:
    mt = h.MechanismType(0)
    sref = h.ref("")
    for i in range(int(mt.count())):
        mt.select(i)
        mt.selected(sref)
        if sref[0] == name:
            return True
    return False
