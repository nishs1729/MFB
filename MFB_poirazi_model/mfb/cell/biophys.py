# Python/NEURON port of the Poirazi, Brannon & Mel (2003) CA1 model (github.com/Poirazi-Lab/Poirazi_CA1_detailed @ d2013e7); see NOTICE.md.
"""Port of ``experiment/cell-setup.hoc`` (``proc cell_setup`` and the procedures it calls).

Every function mirrors one HOC procedure, statement by statement, including the
HOC semantics that make the original behave the way it does:

* ``for (x)`` visits x=0 and x=1 as well as the segment centres; writes at 0/1
  land in the first/last segment (see :mod:`mfb.cell.hoc_compat`).
* Range variables assigned without ``(x)`` (``Ra``, ``ek``, ``e_pas``,
  ``gkbar_mykca``) set the whole section; inside ``for (x)`` the last iteration
  wins. Each such occurrence is marked ``# HOC whole-section assignment``.
* Odd formulas are kept as written (e.g. ``ar2 = max_ar2 + m_ar2*xdist``).
"""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

from neuron import h, nrn

from .balance import current_balance
from .hoc_compat import for_x, ion_style, ismembrane, iter_for_x, seg_at

if TYPE_CHECKING:
    from .build import Cell


def set_section(sec: nrn.Section, attr: str, value: float) -> None:
    """HOC ``rangevar = value`` without ``(x)``: assign every segment of ``sec``."""
    for seg in sec:
        setattr(seg, attr, value)


# =============================================================================
#   PROCEDURES USED IN CELL SETUP
# =============================================================================

def Rm_sigmoid(cell: Cell, sec: nrn.Section) -> None:
    """Port of ``proc Rm_sigmoid()`` (cell-setup.hoc).

    To make the distal membrane less conductive, vis-a-vis Stuart G. and
    Spruston N., J. Neuroscience 18(10) 3501-3510, 1998, we decay Rm from
    proximal to distal sigmoidally.
    """
    p = cell.params
    rm_soma = p.sig_rm_soma   # defvar("channel:pas","Rm_soma","Rm_default")
    for x, seg in iter_for_x(sec):
        xdist = cell.dist.precise(sec, x)   # calc. perpendicular distance
        rm = rm_soma + (p.rm_end - rm_soma) / (1.0 + math.exp((p.rm_dhalf - xdist) / p.rm_steep))
        seg.g_pas = 1.0 / rm


def Ra_sigmoid(cell: Cell, sec: nrn.Section) -> None:
    """Port of ``proc Ra_sigmoid()`` (cell-setup.hoc).

    Changing Ra sigmoidally along the apical trunk (obsolete in this case).
    ``Ra`` is a section variable, so the value computed at x=1 (the section's
    end point in the d3 map) is the one that remains.
    """
    p = cell.params
    ra_soma = p.sig_ra_soma
    for x in for_x(sec):
        xdist = cell.dist.precise(sec, x)   # calc. perpendicular distance
        sec.Ra = ra_soma + (p.ra_end - ra_soma) / (1.0 + math.exp((p.ra_dhalf - xdist) / p.ra_steep))  # HOC whole-section assignment


def apical_h_insert_sig(cell: Cell, sec: nrn.Section) -> None:
    """Port of ``proc apical_h_insert_sig()`` (cell-setup.hoc).

    To make the distal trunk h-current conductance, g_h, about 7 times higher
    (at 300 um) than the somatic value vis-a-vis Magee J., J. of Neuroscience
    18(19) 7613-7624, 1998, we vary I_h conductance sigmoidally along the
    apical trunk.
    """
    p = cell.params
    gh_soma, gh_end = p.gh_soma, p.gh_end
    for x, seg in iter_for_x(sec):
        xdist = cell.dist.precise(sec, x)   # calc. perpendicular distance
        sec.insert("h")
        seg.gbar_h = gh_soma + (gh_end - gh_soma) / (1.0 + math.exp((p.h_dhalf - xdist) / p.h_steep))


def A_insert(cell: Cell, sec: nrn.Section) -> None:
    """Port of ``proc A_insert()`` (cell-setup.hoc).

    Inserting proximal (kap) and distal (kad) A-type channels along the apical
    trunk. Proximal I_A is distributed in a fixed conductance over the first
    100 um from the cell body. Distal-type I_A is distributed in a linearly
    increasing manner for distances 100 < xdist < 350. For xdist < 100,
    g_A_distal(x) = 0 and for xdist > 350 g_A_distal(x) = constant =
    g_A_distal(350).
    """
    p = cell.params
    for x, seg in iter_for_x(sec):
        xdist = cell.dist.precise(sec, x)
        fr = xdist / p.kad_distal_distance
        sec.insert("kap")
        sec.insert("kad")
        set_section(sec, "ek", p.ek_A)   # HOC whole-section assignment: ek = -80
        if xdist < p.kap_distal_distance:
            seg.gkabar_kad = 0
            seg.gkabar_kap = p.soma_kap
        elif xdist < p.kad_distal_distance:
            seg.gkabar_kap = 0
            seg.gkabar_kad = p.kad_distal_maxfactor * p.kad_init * fr
        else:
            seg.gkabar_kap = 0
            seg.gkabar_kad = p.kad_distal_maxfactor * p.kad_init


def apical_km_insert(cell: Cell, sec: nrn.Section) -> None:
    """Port of ``proc apical_km_insert()``: m-type K+ current with a fixed
    conductance along the apical trunk."""
    p = cell.params
    for x, seg in iter_for_x(sec):
        xdist = cell.dist.precise(sec, x)
        fr = xdist / p.km_distal_distance  # computed but unused in the original
        sec.insert("km")
        seg.gbar_km = p.soma_km


def apical_kca_insert(cell: Cell, sec: nrn.Section) -> None:
    """Port of ``proc apical_kca_insert()``.

    Inserting K(Ca++)-type channels and calcium pumps along the apical trunk
    with maximum conductances in 50 < xdist < 200.
    """
    p = cell.params
    for x, seg in iter_for_x(sec):
        xdist = cell.dist.precise(sec, x)
        fr = xdist / p.kca_distal_distance  # computed but unused in the original
        sec.insert("cad")     # calcium pump/buffering mechanism
        sec.insert("kca")     # slow AHP K++ current
        sec.insert("mykca")   # medium AHP K++ current
        if xdist < p.kca_distal_distance and xdist > 50:
            seg.gbar_kca = 5 * p.soma_kca
            set_section(sec, "gkbar_mykca", 2 * p.mykca_init)      # HOC whole-section assignment
        else:
            seg.gbar_kca = 0.5 * p.soma_kca
            set_section(sec, "gkbar_mykca", 0.25 * p.mykca_init)   # HOC whole-section assignment


def apical_caT_insert(cell: Cell, sec: nrn.Section) -> None:
    """Port of ``proc apical_caT_insert()``.

    Inserting LVA Ca++ T-type channels along the apical trunk in a linearly
    increasing manner, for xdist > 100 um.
    """
    p = cell.params
    for x, seg in iter_for_x(sec):
        xdist = cell.dist.precise(sec, x)
        fr = xdist / p.caT_distal_distance
        sec.insert("cat")
        if xdist < 100:
            seg.gcatbar_cat = 0
        else:
            seg.gcatbar_cat = p.caT_distal_maxfactor * p.soma_caT * fr


def apical_caR_caLH_insert(cell: Cell, sec: nrn.Section) -> None:
    """Port of ``proc apical_caR_caLH_insert()``.

    Inserting HVAm Ca++ R-type and HVA L-type channels along the apical trunk.
    The R-type current is distributed in a fixed conductance while the L-type
    current is distributed in a maximum fixed conductance for distances
    xdist > 50 um and in a very small conductance for xdist < 50 um.
    """
    p = cell.params
    for x, seg in iter_for_x(sec):
        xdist = cell.dist.precise(sec, x)
        sec.insert("car")
        seg.gcabar_car = 0.1 * p.soma_car
        sec.insert("calH")
        if xdist > 50:
            seg.gcalbar_calH = 4.6 * p.soma_caLH
        else:
            seg.gcalbar_calH = 0.1 * p.soma_caLH


def khoblique_peri_decay(cell: Cell) -> None:
    """Port of ``proc khoblique_peri_decay()`` (cell-setup.hoc).

    Setting conductances in all apical oblique dendrites so that the values of
    all dendrites after an initial section are the same (or a multiple) as the
    values in apical_dendrite[46]. The values in the initial section of 50 um
    from the parent trunk are set equal to the parent trunk conductances. For
    dendrites located beyond 300 (or/and 350) um, we increase the Na+-persistent
    current, the A current, the Ca++ and K(Ca++) conductances and reduce the
    spike attenuation coefficient.

    Faithful quirks:

    * ``xdist`` is computed once per path, at x=0 of the path's *trunk* section
      (``find_vector_distance_precise(secname(),0)``), not per segment; the
      ``> 300`` / ``> 350`` tests therefore apply path-wise.
    * ``distance(1,x)`` is the NEURON path distance from the trunk section's x=1.
    * Paths overlap; later paths overwrite earlier ones.
    """
    p = cell.params
    ks = cell.section(p.oblique_khsection)
    k1 = seg_at(ks, 1.0)
    # Holding the conductance values from apical_dendrite[46]
    hold_cat = k1.gcatbar_cat
    hold_car = p.soma_car
    hold_calH = p.soma_caLH
    hold_nap = 0.0004 * seg_at(ks, 0.5).gnabar_hha_old   # HOC rvalue without (x) reads x=0.5
    hold_h = k1.gbar_h
    hold_ar2_hha_old = k1.ar2_hha_old
    hold_kdr = k1.gkbar_hha_old
    hold_g_pas = k1.g_pas
    hold_Ra = ks.Ra  # noqa: F841  (held but unused in the original)
    hold_kap = k1.gkabar_kap
    hold_kad = k1.gkabar_kad
    hold_mykca = k1.gkbar_mykca  # noqa: F841
    hold_kca = k1.gbar_kca
    hold_km = k1.gbar_km

    for path in cell.oblique_paths:
        trunk = path[0]
        # set the origin to the currently accessed section
        xdist = cell.dist.precise(trunk, 0.0)
        origin = trunk(1.0)          # distance(0,1)
        t1 = seg_at(trunk, 1.0)
        trunk_kap = t1.gkabar_kap    # holding the parent trunk values
        trunk_kad = t1.gkabar_kad
        trunk_h = t1.gbar_h
        trunk_pas = t1.g_pas
        trunk_Ra = trunk.Ra  # noqa: F841
        trunk_car = t1.gcabar_car
        trunk_calH = t1.gcalbar_calH
        trunk_cat = t1.gcatbar_cat
        trunk_kca = t1.gbar_kca
        trunk_mykca = t1.gkbar_mykca  # noqa: F841
        trunk_km = t1.gbar_km
        trunk_nap = 0.2 * hold_nap   # No persistent I_Na at the trunk => hold a small percent of hold_nap value
        trunk_ar2_hha_old = t1.ar2_hha_old  # spike attenuation variable

        for sec in path[1:]:         # skip the trunk section (sec_count == 0)
            for mech in ("kap", "kad", "h", "pas", "car", "calH", "cat", "kca", "mykca", "km",
                         "nap", "cad"):
                sec.insert(mech)
            set_section(sec, "e_pas", p.v_init)   # HOC whole-section assignment
            set_section(sec, "ek", p.ek_A)        # HOC whole-section assignment: ek = -80
            segs = list(sec)
            for x in for_x(sec):
                if not (0.0 < x < 1.0):
                    continue
                seg = seg_at(sec, x)
                d = h.distance(origin, sec(x))
                if d < p.peri_trunkl:   # close to the parent trunk section: keep trunk values
                    sec.Ra = p.ra_default                          # HOC whole-section assignment
                    seg.gkabar_kap = trunk_kap
                    seg.gkabar_kad = trunk_kad
                    seg.gbar_h = trunk_h
                    seg.g_pas = trunk_pas
                    seg.gcabar_car = trunk_car
                    seg.gcalbar_calH = trunk_calH
                    seg.gcatbar_cat = trunk_cat
                    seg.gbar_kca = trunk_kca
                    set_section(sec, "gkbar_mykca", p.mykca_init)  # HOC whole-section assignment
                    seg.gbar_km = trunk_km
                    seg.gnabar_nap = trunk_nap
                    seg.ar2_hha_old = trunk_ar2_hha_old
                else:   # further away: apical_dendrite[46] values (or a multiple)
                    seg.gkabar_kap = hold_kap
                    seg.gkabar_kad = 1.25 * hold_kad
                    seg.gbar_h = hold_h
                    seg.g_pas = hold_g_pas
                    sec.Ra = p.ra_default                          # HOC whole-section assignment
                    seg.gcabar_car = hold_car
                    seg.gcalbar_calH = hold_calH
                    seg.gcatbar_cat = hold_cat
                    seg.ar2_hha_old = 0.8 * hold_ar2_hha_old       # set to 80% of dend. 46 value
                    seg.gbar_kca = hold_kca
                    set_section(sec, "gkbar_mykca", 1.1 * p.mykca_init)  # HOC whole-section assignment
                    seg.gnabar_nap = hold_nap
                    seg.gbar_km = 2 * hold_km                      # set to 2 times the dend 46 value
                    if xdist > 300:            # for xdist > 300 um increase:
                        seg.gkabar_kad = 1.3 * 1.9 * hold_kad      # A-current,
                        seg.gcabar_car = 13 * hold_car             # Ca++-R current,
                        seg.gcalbar_calH = 14 * hold_calH          # Ca++-L current,
                        seg.gbar_kca = 5 * p.soma_kca              # slow AHP current
                        seg.gkbar_hha_old = 1.07 * hold_kdr        # delayed rectifier
                    if xdist > 350:            # for xdist > 350 um increase even more:
                        seg.gcalbar_calH = 15 * hold_calH          # Ca++-L current,
                        seg.gcabar_car = 13 * hold_car             # Ca++-R current,
                        seg.ar2_hha_old = 0.95                     # less spike attenuation
                        seg.gnabar_nap = 2 * hold_nap              # Na+ persistent
            del segs


def khbasal_fixed(cell: Cell) -> None:
    """Port of ``proc khbasal_fixed()`` (cell-setup.hoc).

    Setting conductance values in all basal dendrites to be the same as the
    values in apical_dendrite[14], except for the A current conductance which
    is 0.6 times higher.
    """
    p = cell.params
    ks = cell.section(p.basal_khsection)
    k1 = seg_at(ks, 1.0)
    hold_g_pas = k1.g_pas
    hold_kap = k1.gkabar_kap
    hold_kad = k1.gkabar_kad
    hold_h = k1.gbar_h  # noqa: F841  (held but unused: gbar_h is set to soma_hbar)
    for sec in cell.lists["basal_tree_list"]:
        sec.insert("kap")
        sec.insert("kad")
        sec.insert("h")
        sec.insert("pas")
        for x, seg in iter_for_x(sec):
            seg.gkabar_kap = 1.6 * hold_kap
            seg.gkabar_kad = 1.6 * hold_kad
            seg.gbar_h = p.soma_hbar
            seg.g_pas = hold_g_pas
            sec.Ra = p.ra_default                   # HOC whole-section assignment
            set_section(sec, "e_pas", p.v_init)     # HOC whole-section assignment
            set_section(sec, "ek", p.ek_A)          # HOC whole-section assignment: ek = -80


def ar2_trunk(cell: Cell, sec: nrn.Section) -> None:
    """Na+ spike attenuation variable on a trunk section (inline code in ``cell_setup``).

    Linearly decreasing from soma to 300 um. The formula for the middle range
    is kept exactly as written in the original (``max_ar2 + m_ar2*xdist``),
    which is discontinuous at ``decay_start``.
    """
    p = cell.params
    m_ar2 = (p.max_ar2 - p.min_ar2) / (p.decay_start - p.decay_end)
    for x, seg in iter_for_x(sec):
        xdist = cell.dist.precise(sec, x)
        if xdist < p.decay_start:
            seg.ar2_hha_old = p.max_ar2
        elif xdist > p.decay_end:
            seg.ar2_hha_old = p.min_ar2
        else:
            seg.ar2_hha_old = p.max_ar2 + m_ar2 * xdist
    # ar2_log(...) only wrote a log file in the original; omitted (see DEVIATIONS.md)


# =============================================================================
#   CELL SET-UP PROCEDURE
# =============================================================================

def cut_sections(cell: Cell, maximum_segment_length: float) -> None:
    """Port of ``proc cut_sections()`` (lib/cut-sections.hoc): ``nseg = 1+int(L/$1)``."""
    for sec in cell.all:
        sec.nseg = 1 + int(sec.L / maximum_segment_length)


def cell_setup(cell: Cell) -> None:
    """Port of ``proc cell_setup()`` (experiment/cell-setup.hoc), in the original order."""
    p = cell.params
    # defvar("general", "v_init"/"celsius"): global in NEURON, set explicitly here
    h.v_init = p.v_init
    h.celsius = p.celsius

    cut_sections(cell, p.maximum_segment_length)
    # make 3-d mapping of cell sections (map_segments_to_3d; d3.mod replaced)
    for sec in cell.all:
        cell.dist.map_section(sec)
    # ($o1.tmpo2 = new Shape(): GUI only, omitted)

    # ---- Start inserting mechanisms in cell --------------------------------
    for sec in cell.lists["soma_list"]:   # forsec "soma"
        sec.insert("hha2")      # HH mechanism with low threshold for Na spikes (-57 mV)
        set_section(sec, "gnabar_hha2", p.gna_soma)
        set_section(sec, "gkbar_hha2", p.gkdrbar_soma)
        set_section(sec, "gl_hha2", 0)
        set_section(sec, "el_hha2", p.v_init)
        set_section(sec, "ena", p.ena)
        sec.insert("pas")       # leak conductance
        set_section(sec, "g_pas", 1 / p.rm_soma)
        set_section(sec, "e_pas", p.v_init)
        sec.Ra = p.ra_soma
        sec.insert("h")         # h current
        set_section(sec, "gbar_h", p.soma_hbar)
        set_section(sec, "K_h", p.soma_h_K)
        set_section(sec, "vhalf_h", p.soma_h_vhalf)
        sec.insert("kap")       # proximal A current
        set_section(sec, "gkabar_kap", p.soma_kap)
        set_section(sec, "ek", p.ek_A)
        sec.insert("km")        # m-type potassium current
        set_section(sec, "gbar_km", p.soma_km)
        set_section(sec, "ek", p.ek_A)
        sec.insert("cal")       # HVA Ca++-L type current
        set_section(sec, "gcalbar_cal", p.soma_caL / 2)
        sec.insert("cat")       # LVA Ca++-T type current
        set_section(sec, "gcatbar_cat", p.soma_caT / 2)
        sec.insert("somacar")   # HVAm Ca++-R type current
        set_section(sec, "gcabar_somacar", p.gsomacar)
        sec.insert("kca")       # K(Ca) sAHP potassium type current
        set_section(sec, "gbar_kca", 5 * p.soma_kca)
        sec.insert("mykca")     # K(Ca) mAHP potassium type current
        set_section(sec, "gkbar_mykca", 5.5 * p.mykca_init)
        sec.insert("cad")       # calcium pump/buffering mechanism

    # Configure Axon
    for sec in cell.lists["axon_sec_list"]:
        sec.insert("hha2")      # HH mechanism with low threshold for Na spikes (-57 mV)
        set_section(sec, "gnabar_hha2", p.gna_axon)
        set_section(sec, "gkbar_hha2", p.gkdrbar_axon)
        set_section(sec, "gl_hha2", 0)
        set_section(sec, "el_hha2", p.v_init)
        set_section(sec, "ena", p.ena)
        sec.insert("pas")       # leak conductance
        set_section(sec, "g_pas", 1 / p.rm_axon)
        set_section(sec, "e_pas", p.v_init)
        sec.Ra = p.ra_axon
        set_section(sec, "cm", p.cm_axon)
        sec.insert("km")        # m-type potassium current
        set_section(sec, "gbar_km", 0.5 * p.soma_km)
        set_section(sec, "ek", p.ek_A)

    # Configure apical trunk
    for sec in cell.lists["apical_trunk_list"]:
        apical_h_insert_sig(cell, sec)      # Inserting h-current
        apical_caR_caLH_insert(cell, sec)   # Inserting Ca++ R-type and Ca++ L-type currents
        apical_caT_insert(cell, sec)        # Inserting Ca++ T-type current
        apical_kca_insert(cell, sec)        # Inserting K(Ca) sAHP and mAHP potassium currents
        apical_km_insert(cell, sec)         # Inserting m-type potassium current
        A_insert(cell, sec)                 # Inserting A-current
        sec.insert("hha_old")   # HH mechanism with high threshold for Na spikes (-50 mV)
        set_section(sec, "gnabar_hha_old", p.gna_trunk)
        set_section(sec, "gkbar_hha_old", p.gkdrbar_trunk)
        set_section(sec, "ena", p.ena)
        sec.insert("pas")       # leak conductance
        set_section(sec, "e_pas", p.v_init)
        set_section(sec, "el_hha_old", p.v_init)
        sec.Ra = p.ra_trunk
        set_section(sec, "cm", p.cm_trunk)
        Rm_sigmoid(cell, sec)   # configure Rm along apical trunk
        Ra_sigmoid(cell, sec)   # configure Ra along apical trunk
        # Set the Na+ spike attenuation variable (linearly decreasing from soma to 300 um)
        ar2_trunk(cell, sec)

    # Configure the apical-non-trunk section: insert basic mechanisms
    for sec in cell.lists["apical_non_trunk_list"]:
        sec.insert("hha_old")   # HH mechanism with high threshold for Na spikes (-50 mV)
        set_section(sec, "gnabar_hha_old", p.gna_non_trunk)
        set_section(sec, "gkbar_hha_old", p.gkdrbar_non_trunk)
        set_section(sec, "el_hha_old", p.v_init)
        set_section(sec, "ena", p.ena)
        sec.insert("pas")       # passive properties
        set_section(sec, "g_pas", 1 / p.rm_non_trunk)
        set_section(sec, "e_pas", p.v_init)
        sec.Ra = p.ra_non_trunk
        set_section(sec, "cm", p.cm_non_trunk)
    khoblique_peri_decay(cell)  # Configure the apical oblique dendrites

    # Configure the basal dendrites
    for sec in cell.lists["basal_tree_list"]:
        sec.insert("hha_old")   # HH mechanism with high threshold for Na spikes (-50 mV)
        set_section(sec, "gnabar_hha_old", p.gna_basal)
        set_section(sec, "gkbar_hha_old", p.gkdrbar_basal)
        set_section(sec, "el_hha_old", p.v_init)
        set_section(sec, "gl_hha_old", 0)
        sec.insert("pas")       # passive properties
        set_section(sec, "g_pas", 1 / p.rm_basal)
        set_section(sec, "e_pas", p.v_init)
        sec.Ra = p.ra_basal
        set_section(sec, "cm", p.cm_basal)
        sec.insert("kap")       # Insert proximal A current
        set_section(sec, "gkabar_kap", 2.5 * p.soma_kap)
        Ra_sigmoid(cell, sec)   # configure Ra
    khbasal_fixed(cell)         # Configure basal dendrites

    for sec in cell.lists["soma_list"]:   # force Rm at all soma sections
        set_section(sec, "g_pas", 1 / p.rm_soma)

    for sec in cell.all:   # zero out gl (leak conductance) since g_pas is taking its place
        if ismembrane(sec, "hha_old"):
            set_section(sec, "gl_hha_old", 0)
            set_section(sec, "ek", p.ek_final)
    for sec in cell.all:
        if ismembrane(sec, "hha2"):
            set_section(sec, "gl_hha2", 0)
            set_section(sec, "ek", p.ek_final)

    for sec in cell.all:
        if ismembrane(sec, "ca_ion"):
            set_section(sec, "eca", p.eca)
            ion_style(sec, "ca_ion", 0, 1, 0, 0, 0)
            # vshift_ca = 0: no mechanism defines vshift; it only created an unused HOC global

    # Account for spines (obsolete in this case). NOT a no-op in NEURON: assigning
    # diam with 3-D points present flattens the 3-D diameters inside each segment.
    for sec in cell.all:
        for x in for_x(sec):
            if 0.0 < x < 1.0:
                seg = sec(x)
                seg.diam = seg.diam * p.spine_factor

    # (configure_sections.eps printout omitted: GUI only)
    current_balance(cell, p.v_init)   # balance current to -70 mV
