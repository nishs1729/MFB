# Python/NEURON port of the Poirazi, Brannon & Mel (2003) CA1 model (github.com/Poirazi-Lab/Poirazi_CA1_detailed @ d2013e7); see NOTICE.md.
"""Trimmed copy of the CA1 cell from ``../poirazi_model`` (morphology + cell_setup only)."""
from .build import Cell
from .params import CellParams

__all__ = ["Cell", "CellParams"]
