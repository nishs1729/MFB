# Python/NEURON port of the Poirazi, Brannon & Mel (2003) CA1 model (github.com/Poirazi-Lab/Poirazi_CA1_detailed @ d2013e7); see NOTICE.md.
"""Model parameters.

Replaces the ``$o1.defvar(...)`` string-evaluated globals of
``experiment/cell-setup.hoc`` (and ``morphology/n123/cell-analysis.hoc``) with an explicit frozen dataclass.
(Trimmed copy: only the cell parameters; run control lives in ``mfb.experiment``.)

Derived quantities are computed with the *same expression and operation order*
as the HOC defvar strings, so the floating-point values are identical
(e.g. ``kdr_div = 10.0/1.24``, ``gkdrbar_trunk = gna_trunk/kdr_div_trunk``).

HOC quirk preserved: several procedures re-``defvar`` a variable that was set
earlier (``Rm_sigmoid`` sets ``Rm_soma = Rm_default``; ``Ra_sigmoid`` sets
``Ra_soma = Ra_default``). Those re-definitions are modelled by the
``sig_*`` properties below, which deliberately ignore ``rm_soma``/``ra_soma``.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CellParams:
    """All cell_setup() parameters (cell-setup.hoc, ``proc cell_setup`` and helpers)."""

    # ---- general --------------------------------------------------------------
    v_init: float = -70.0          # "Initial voltage of sections."
    celsius: float = 34.0          # "Temperature of slice." -- SEVERELY affects experiment results
    maximum_segment_length: float = 75.0   # cut_sections(maximum_segment_length)
    adjustment: float = 41.1       # cell-analysis.hoc: vector-distance adjustment (soma reference)

    # ---- passive ("passive" defvars) -------------------------------------------
    rm_default: float = 200000.0   # Specific membrane resistance
    ra_default: float = 50.0       # Specific axial resistance  (35 commented out in original)
    cm_default: float = 1.0        # Default specific capacitance

    # ---- Na / Kdr ("channel:na", "channel:na-kdr") ---------------------------------
    gna_default: float = 0.007
    trunk_non_trunk_ratio: float = 1.0
    gna_axon: float = 0.1

    # ---- initial conductance values (plain assignments in cell_setup) -----------
    soma_caL: float = 0.014
    soma_car: float = 0.0003
    gsomacar: float = 0.003
    soma_caLH: float = 0.95 * 0.000333
    soma_caT: float = 0.0001
    soma_kca: float = 0.0001
    soma_km: float = 0.06
    mykca_init: float = 1.1 * 0.015
    soma_hbar: float = 1.872e-5
    soma_kap: float = 0.0075
    kad_init: float = 1.04 * 0.0072

    # ---- Rm_sigmoid (Stuart & Spruston 1998) --------------------------------------
    rm_end: float = 12e3           # (5e3 commented out in original)
    rm_dhalf: float = 200.0
    rm_steep: float = 50.0
    # ---- Ra_sigmoid ("obsolete in this case") ----------------------------------
    ra_end: float = 35.0
    ra_dhalf: float = 210.0
    ra_steep: float = 50.0
    # ---- apical_h_insert_sig (Magee 1998) ----------------------------------------
    gh_end_factor: float = 9.0     # gh_end = soma_hbar*9
    h_dhalf: float = 280.0
    h_steep: float = 50.0
    soma_h_K: float = 8.8          # K_h in soma
    soma_h_vhalf: float = -82.0    # vhalf_h in soma
    # ---- A_insert ------------------------------------------------------------
    kap_distal_maxfactor: float = 1.0
    kap_distal_distance: float = 100.0
    kad_distal_maxfactor: float = 6.5   # (8 commented out in original)
    kad_distal_distance: float = 350.0
    ek_A: float = -80.0
    # ---- apical_km_insert / apical_kca_insert / apical_caT_insert -------------
    km_distal_maxfactor: float = 1.0
    km_distal_distance: float = 350.0
    kca_distal_maxfactor: float = 1.0
    kca_distal_distance: float = 200.0
    caT_distal_maxfactor: float = 4.0
    caT_distal_distance: float = 350.0
    # ---- Na+ spike attenuation (ar2) on the trunk ------------------------------
    max_ar2: float = 0.95
    min_ar2: float = 0.30
    decay_end: float = 300.0
    decay_start: float = 50.0
    # ---- obliques / basal ------------------------------------------------------
    oblique_khsection: str = "apical_dendrite[46]"
    peri_trunkl: float = 50.0
    basal_khsection: str = "apical_dendrite[14]"
    # ---- reversal potentials ---------------------------------------------------
    ena: float = 50.0
    ek_final: float = -77.0        # forall if (ismembrane("hha_*")) ek = -77
    eca: float = 140.0
    # ---- spines (obsolete; multiplies diam by 1.0) ----------------------------
    spine_factor: float = 1.0

    # ---- derived values: same expression as the defvar strings ---------------
    @property
    def rm_soma(self) -> float: return self.rm_default
    @property
    def rm_trunk(self) -> float: return self.rm_default
    @property
    def rm_non_trunk(self) -> float: return self.rm_default
    @property
    def rm_basal(self) -> float: return self.rm_default
    @property
    def rm_axon(self) -> float: return self.rm_default
    @property
    def ra_soma(self) -> float: return self.ra_default
    @property
    def ra_trunk(self) -> float: return self.ra_default
    @property
    def ra_non_trunk(self) -> float: return self.ra_default
    @property
    def ra_basal(self) -> float: return self.ra_default
    @property
    def ra_axon(self) -> float: return self.ra_default
    @property
    def cm_axon(self) -> float: return self.cm_default
    @property
    def cm_trunk(self) -> float: return self.cm_default
    @property
    def cm_non_trunk(self) -> float: return self.cm_default
    @property
    def cm_basal(self) -> float: return self.cm_default
    # re-defvar'd inside Rm_sigmoid / Ra_sigmoid / apical_h_insert_sig
    @property
    def sig_rm_soma(self) -> float: return self.rm_default
    @property
    def sig_ra_soma(self) -> float: return self.ra_default
    @property
    def gh_soma(self) -> float: return self.soma_hbar
    @property
    def gh_end(self) -> float: return self.soma_hbar * self.gh_end_factor

    @property
    def gna_trunk(self) -> float: return self.gna_default
    @property
    def gna_non_trunk(self) -> float: return self.trunk_non_trunk_ratio * self.gna_default
    @property
    def gna_basal(self) -> float: return self.gna_default
    @property
    def gna_soma(self) -> float: return self.gna_default
    @property
    def kdr_div(self) -> float: return 10.0 / 1.24
    @property
    def kdr_div_soma(self) -> float: return 10.0 / 2.0
    @property
    def kdr_div_axon(self) -> float: return self.kdr_div_soma
    @property
    def kdr_div_trunk(self) -> float: return self.kdr_div
    @property
    def kdr_div_non_trunk(self) -> float: return self.kdr_div
    @property
    def kdr_div_basal(self) -> float: return self.kdr_div
    @property
    def gkdrbar_axon(self) -> float: return self.gna_axon / self.kdr_div_axon
    @property
    def gkdrbar_basal(self) -> float: return self.gna_basal / self.kdr_div_basal
    @property
    def gkdrbar_soma(self) -> float: return self.gna_soma / self.kdr_div_soma
    @property
    def gkdrbar_trunk(self) -> float: return self.gna_trunk / self.kdr_div_trunk
    @property
    def gkdrbar_non_trunk(self) -> float: return self.gna_non_trunk / self.kdr_div_non_trunk
