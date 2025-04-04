import sys, os
import numpy as np
import pandas as pd
import pickle as pk
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib.patches as patches
from itertools import product, combinations_with_replacement


# plt.style.use('dark_background')
plt.rcParams.update(plt.rcParamsDefault)

sys.path.insert(0, '../scripts_analysis')
from analysis import *
from peaks import  detect_peaks

dataPath = "../data/"

RRP = {
    'name': 'RRP',
    'val': list(range(5,61,5)),
    'tlabel': [5,30,60],
    'label': 'readily releasable pool',
    'slabel': 'RRP',
    'loc': 3,
    'cat': dict(low= range(5,25,5),
                mid= range(25,45,5),
                high=range(45,65,5))
}
dVAZ = {
    'name': 'dV',
    'val': list(range(60,221,20)),
    'tlabel': [220, 140, 60],
    'label': 'coupling distance b/w AZ and VDCC cluster',
    'slabel': 'dVAZ',
    'loc': 1,
    'cat': dict(low= range(60,120,20),
                mid= range(120,180,20),
                high=range(180,240,20))
}
nVDCC = {
    'name': 'nV',
    'val': list(range(1,16)),
    'tlabel': [1, 8, 15],
    'label': '# of VDCCs in a cluster',
    'slabel': 'nVDCC',
    'loc': 0,
    'cat': dict(low= range(1,6),
                mid= range(6,11),
                high=range(11,16))
}
nAZ = {
    'name': 'nAZ',
    'val': list(range(7,36,2)),
    'tlabel': [7, 21, 35],
    'label': '# of Active zones',
    'slabel': 'nAZ',
    'loc': 2,
    'cat': dict(low= range(7,17,2),
                mid= range(17,27,2),
                high=range(27,37,2))
}
cdiv = {
    0: 'l',
    1: 'm',
    2: 'h'
}

################################################################################
def get_design_category(nvdcc, dvaz, naz, rrp):
    """
    Returns the category of the synaptic design based on its attributes
    low: 0
    mid: 1
    high: 2
    """
    design_cat = {}
    for i,c in enumerate(['low', 'mid', 'high']):
        if nvdcc in nVDCC['cat'][c]: design_cat.update({'nVDCC': i})
        if naz in nAZ['cat'][c]: design_cat.update({'nAZ': i})
        if dvaz in dVAZ['cat'][c]: design_cat.update({'dVAZ': i})
        if rrp in RRP['cat'][c]: design_cat.update({'RRP': i})

    assert 'nVDCC' in design_cat, f"invalid nvdcc value: {nvdcc}"
    assert 'nAZ' in design_cat, f"invalid naz value: {naz}"
    assert 'dVAZ' in design_cat, f"invalid dvaz value: {dvaz}"
    assert 'RRP' in design_cat, f"invalid rrp value: {rrp}"

    return design_cat

################################################################################
def get_designs_in_categories(designs):
    """
    Input: list of synaptic designs
    returns: 4D array containing a list of design directories 
    that fall in the categoty.
    """
    designs_in_categories = np.empty([3,3,3,3], dtype=object)
    for i,j,k,l in product(range(3), repeat=4):
        designs_in_categories[i,j,k,l] = []

    for d in designs:
        nv  = int(getSimInfo(d, 'nVDCC', skip=0))
        dv  = int(getSimInfo(d, 'dVAZ', skip=0))
        naz  = int(getSimInfo(d, 'nAZ', skip=0))
        rrp = int(getSimInfo(d, 'RRP', skip=0))
        
        design_category = get_design_category(nv, dv, naz, rrp)
        # print(nv, dv, naz, rrp, design_category)

        designs_in_categories[
            design_category['nVDCC'],
            design_category['dVAZ'],
            design_category['nAZ'],
            design_category['RRP']
        ].append(d)

    return designs_in_categories

################################################################################
def get_rep_design(category):
    """
    Get a representative design in a category.
    One with max facil_10.
    Other with median facil_10.
    """
    n_designs = len(category)
    if n_designs:
        facil_10 = {}
        for design in category:
            
            data = pd.read_csv(os.path.join(dataPath, 'control', design, 'result.dat'), 
                               usecols=['Pr', 'Rel'], sep='\t')
            data['mvu'] = data['Rel']/data['Pr']
            data['facil'] = data['Rel']*data['Pr'][0]/data['Pr']/data['Rel'][0]

            facil_10[design] = data['facil'][9]

            # print(data['facil'][9])
        # for k,v in facil_10.items(): print(k,v)

        median = np.sort(list(facil_10.values()))[int(np.floor(n_designs/2))]
        median_des = [k for k, v in facil_10.items() if v == median][0]
        
        return {
            'rep_design_max': max(facil_10, key=facil_10.get), 
            'rep_design_min': min(facil_10, key=facil_10.get), 
            'rep_design_median': median_des
        }

    else:
        return {}

################################################################################
def get_release_info(category):
    """
    Get avg pr, rel, mvu, facil for designs in a category
    """
    n_designs = len(category)
    if n_designs:
        avg_pr, avg_rel, avg_mvu, avg_facil = [], [], [], [] # mvu: multi-vesicle usage

        for design in category: ## Loop over each design in the category
            ## Read data from 'result.dat' of the design
            data = pd.read_csv(os.path.join(dataPath, 'control', design, 'result.dat'), sep='\t')
            # print(data)

            avg_pr.append(data['Pr'])
            avg_rel.append(data['Rel'])
            avg_mvu.append(data['Rel']/data['Pr'])
            avg_facil.append(data['Rel']*data['Pr'][0]/data['Pr']/data['Rel'][0])
        
        avg_pr = np.array(avg_pr)
        avg_rel = np.array(avg_rel)
        avg_mvu = np.array(avg_mvu)
        avg_facil = np.array(avg_facil)

        return dict(
            pr = (np.mean(avg_pr, axis=0), np.std(avg_pr, axis=0)),
            rel = (np.mean(avg_rel, axis=0), np.std(avg_rel, axis=0)),
            mvu = (np.mean(avg_mvu, axis=0), np.std(avg_mvu, axis=0)),
            facil = (np.mean(avg_facil, axis=0), np.std(avg_facil, axis=0))
        )
    else:
        return {}
    
################################################################################
def get_calcium_info(category):
    """
    Get avg calcium peak and residual calcium for a category
    """
    n_designs = len(category)
    if n_designs:
        avg_ca_peak, avg_res_ca = [], []
        for design in category: ## Loop over each design in the category
            naz = int(getSimInfo(design, 'nAZ', skip=0))

            ## Read data from 'CaConc.dat' of the design
            data = pd.read_csv(os.path.join(dataPath, 'control', design, 'CaConc.dat'), 
                               usecols=range(naz+1), sep='\t')
            data['mean'] = np.mean(data.iloc[:,1:], axis=1)
            # print(design, '\n', data)
            
            ## Detect peaks and ensure all 10 peaks are detected
            idx = detect_peaks(data['mean'], mph=1, mpd=200, threshold=0, edge='rising', show=False)
            assert len(idx) == 10, f'Peak detecction failed for design {design}'

            ca_peak = [data.loc[id,'mean'] for id in idx]
            ca_res = [np.mean(data.loc[id+100:id+300,'mean']) for id in idx]
            # print(ca_peak, '\n', ca_res)

            if 0: ## for diagnosis
                plt.plot('Seconds', 'mean', data=data)
                for id in idx:
                    plt.plot('Seconds', 'mean', data=data.loc[id+100:id+300,:], color='red')
                    plt.plot('Seconds', 'mean', data=data.loc[id,:], marker='+', color='red')
                # plt.ylim(0.05,0.2)
                plt.show()
            
            avg_ca_peak.append(ca_peak)
            avg_res_ca.append(ca_res)

        avg_ca_peak = np.array(avg_ca_peak)
        avg_res_ca = np.array(avg_res_ca)
        
        return dict(
            avg_ca_peak = (np.mean(avg_ca_peak, axis=0), np.std(avg_ca_peak, axis=0)),
            avg_res_ca = (np.mean(avg_res_ca, axis=0), np.std(avg_res_ca, axis=0))
        )
    else:
        return {}
    
################################################################################
def get_synaptotagmin_info(category):
    """
    Get the avg peak of the fraction of binding sites at syt1 and syt7 occupied 
    by calcium ions.
    """
    n_designs = len(category)
    if n_designs:
        avg_ca_syt7_peak, avg_ca_syt1_peak = [], []
        for design in category: ## Loop over each design in the category

            ca_syt7_peak, ca_syt1_peak = get_ca_syt(design)

            avg_ca_syt7_peak.append(ca_syt7_peak)
            avg_ca_syt1_peak.append(ca_syt1_peak)

        avg_ca_syt7_peak = np.array(avg_ca_syt7_peak)
        avg_ca_syt1_peak = np.array(avg_ca_syt1_peak)
        
        return dict(
            avg_ca_syt7_peak = (np.mean(avg_ca_syt7_peak, axis=0), 
                                np.std(avg_ca_syt7_peak, axis=0)),
            avg_ca_syt1_peak = (np.mean(avg_ca_syt1_peak, axis=0), 
                                np.std(avg_ca_syt1_peak, axis=0))
        )
    else:
        return {}

################################################################################
def get_ca_syt(design):
    naz  = int(getSimInfo(design, 'nAZ', skip=0))
    rrp  = int(getSimInfo(design, 'RRP', skip=0))

    ca_syt7_peak, ca_syt1_peak = [], []
    ## calculate avg bound Ca for each active zone
    for az in range(1,naz+1):
        ## Read data from 'CaConc.dat' of the design
        data = pd.read_csv(os.path.join(dataPath, 'control', design, 
                                        f'AZ_{az}_RRP_{rrp}.dat'), sep='\t')

        ## Fraction of binding sites occupied by Ca
        data['ca_syt7'] = (np.sum(data.iloc[:,[7,8,9,10,11,12]], axis=1) + 
                            2*np.sum(data.iloc[:,[13,14,15,16,17,18]], axis=1))/(2*rrp)
        data['ca_syt1'] =  (np.sum(data.iloc[:,[2,8,14]], axis=1) +  
                            2*np.sum(data.iloc[:,[3,9,15]], axis=1) + 
                            3*np.sum(data.iloc[:,[4,10,16]], axis=1) + 
                            4*np.sum(data.iloc[:,[5,11,17]], axis=1) + 
                            5*np.sum(data.iloc[:,[6,12,18]], axis=1))/(5*rrp)
        
        # print(design, '\n', data.iloc[:,[0,19,20]])

        ## Detect peaks and ensure all 10 peaks are detected
        idx = detect_peaks(data['ca_syt1'], mph=np.max(data['ca_syt1'])/2, 
                            mpd=300, threshold=0, edge='rising', show=False)
        assert len(idx) == 10, f'Peak detecction failed for design {design}'

        ca_syt7_peak.append([data.loc[id,'ca_syt7'] for id in idx])
        ca_syt1_peak.append([data.loc[id+10,'ca_syt1'] for id in idx])

        if len(idx) != 10: ## for diagnosis
            # plt.plot('Seconds', 'ca_syt7', data=data)
            plt.plot('Seconds', 'ca_syt7', data=data)
            for id in idx:
                plt.plot('Seconds', 'ca_syt1', data=data.loc[id,:], 
                            marker='+', markersize=8, color='red')
                plt.plot('Seconds', 'ca_syt7', data=data.loc[id+10,:], marker='+', markersize=8, color='green')
            plt.show()

    return np.mean(np.array(ca_syt7_peak), axis=0), np.mean(np.array(ca_syt1_peak), axis=0)


################################################################################
def get_ca_overlap(design):
    design = design.split('RRP')[0] + 'ISI' + design.split('ISI')[1]
    data = pd.read_csv(os.path.join(dataPath, 'control_eachCa', design, 'CaConc.dat'), sep='\t')
    naz = int(getSimInfo(design, 'nAZ', skip=0))

    id_tot = [4*i+1 for i in range(naz)]
    id_oth = [4*i+4 for i in range(naz)]

    overlap_tot = pd.DataFrame({
        f'{o}_{t}': data.iloc[:,o] / data.iloc[:,t] for o,t in zip(id_oth, id_tot)
    })
    overlap = overlap_tot.mean(axis=1)
    avg_tot = data.iloc[:,id_tot].mean(axis=1)
    avg_oth = data.iloc[:,id_oth].mean(axis=1)

    ## Detect `overlap` peaks. Ensure all 10 peaks are detected
    mph = np.max(sp.signal.savgol_filter(overlap, 301, 3))
    idx = detect_peaks(overlap.to_numpy()[:-400], mph=mph, mpd=300, threshold=0, edge='rising', show=False)
    assert len(idx) == 10, f'Peak detecction failed for design {design}'
    basal_overlap = np.array([np.mean(overlap[id+100:id+300]) for id in idx])

    ## Detect `total` peaks. Ensure all 10 peaks are detected
    idx_tot = detect_peaks(avg_tot, mph=np.max(avg_tot)/2,
                           mpd=300, threshold=0, edge='rising', show=False)
    assert len(idx_tot) == 10, f'Total peak detecction failed for design {design}'
    peak_tot = np.array([avg_tot[id] for id in idx_tot])

    ## Detect `other` peaks. Ensure all 10 peaks are detected
    idx_oth = detect_peaks(avg_oth, mph=np.max(avg_oth)/2,
                           mpd=300, threshold=0, edge='rising', show=False)
    assert len(idx_oth) == 10, f'Other peak detecction failed for design {design}'
    peak_oth = np.array([avg_oth[id] for id in idx_oth])

    peak_overlap = peak_oth/peak_tot
    # print(peak_tot, '\n', peak_oth, '\n', peak_overlap)

    if 0: ## for diagnosis
        fig, ax = plt.subplots(2, 1, figsize=(15, 5), sharex=True)
        ax[0].plot(data['Seconds'], data.iloc[:,id_tot].mean(axis=1), color='orange')
        # ax[0].plot(data['Seconds'], data.iloc[:,id_self].mean(axis=1), color='red')
        ax[0].plot(data['Seconds'], data.iloc[:,id_oth].mean(axis=1), color='green')

        ax[0].plot(data.iloc[idx_tot,0], peak_tot, marker='.', 
                    linestyle='None', color='black', markersize=10)
        ax[0].plot(data.iloc[idx_oth,0], peak_oth, marker='.', 
                    linestyle='None', color='black', markersize=10)
        ax[1].plot(data.iloc[idx_oth,0], peak_overlap*100, marker='.', 
                    color='black', markersize=10)

        ax[1].plot(data['Seconds'], overlap*100)
        for id in idx:
            ax[1].plot(data.iloc[id+100:id+300,0], overlap[id+100:id+300]*100, color='red')

        ax[1].plot(data.iloc[idx+200,0], basal_overlap*100, marker='o',
                    linestyle='None', color='black', markersize=10)
        # plt.ylim(0.05,0.2)
        plt.show()

    return peak_overlap, basal_overlap

################################################################################
def get_ca_overlap_info(category):
    """
    Get peak_overlap, mean_basal_overlap for a category
    """
    n_designs = len(category)
    if n_designs:
        avg_peak_overlap, avg_basal_overlap = [], []
        for design in category: ## Loop over each design in the category
            peak_overlap, basal_overlap = get_ca_overlap(design)
            avg_peak_overlap.append(peak_overlap)
            avg_basal_overlap.append(basal_overlap)

        avg_peak_overlap = np.array(avg_peak_overlap)
        avg_basal_overlap = np.array(avg_basal_overlap)
        
        return dict(
            avg_peak_overlap = (np.mean(avg_peak_overlap, axis=0), np.std(avg_peak_overlap, axis=0)),
            avg_basal_overlap = (np.mean(avg_basal_overlap, axis=0), np.std(avg_basal_overlap, axis=0))
        )
    else:
        return {}
    
################################################################################
def getAPprob(inf, tc=20):
    """
    Calculate the action potential (AP) probability and nth AP probability from simulation data.
    Parameters:
    inf (str): Path to the input file containing AP times.
    tc (float, optional): Time constant for the AP probability calculation. Default is 20 ms.
    Returns:
    tuple: A tuple containing:
        - apProb (numpy.ndarray): Array of AP probabilities for each stimulus time.
        - ap1Prob (numpy.ndarray): Array of 1st AP probabilities for each stimulus time.
    """
    with open(inf, "rb") as infile:
        ca3 = pk.load(infile)
        apTimes = ca3['CA3p_spikes']
        seeds = len(ca3['CA3p_spikes'])
        # print(seeds, ca3.keys())

    # print(apTimes[:10])
    ## Stimulus times
    nAP = 10
    stimTimes = np.sort([1.5 + na*20 for na in range(nAP)])
    # print(stimTimes)
    
    ## AP probability
    apProb = np.zeros(nAP)
    for apts in apTimes:
        temp = np.zeros(nAP)
        for apt in apts:
            for i,st in enumerate(stimTimes):
                if np.ceil((st+tc-apt)/tc)==1:
                    temp[i] = 1
        apProb += temp
    apProb /= seeds

    ## probability of 1st AP
    ap1Prob = np.zeros(nAP)
    for apts in apTimes:
        # print(apts)
        temp = np.zeros(nAP)
        for i,st in enumerate(stimTimes):
            try:
                if np.ceil((st+tc-apts[0])/tc)==1:
                    temp[i] = 1
            except IndexError:
                continue
        ap1Prob += temp
    # print(ap1Prob)
    ap1Prob /= seeds
    
    return apProb, ap1Prob

################################################################################
def change_plot(df, key=0, order=None, color='black', lc='gray', lw=1, axis=None, save_loc=None):
    """
    Plots changes in a dataframe with lines connecting points.

    Args:
        df (pd.DataFrame): DataFrame containing the data to plot.
        key (int or str, optional): Column to use as the reference point for connecting lines. Defaults to 0.
        order (list, optional): Order of columns to plot. Defaults to None.
        axis (matplotlib.axes._axes.Axes, optional): Axis to plot on. Defaults to None.
        color (str or list, optional): Color of the points. Defaults to black.
        lc (str, optional): Line color. Defaults to gray.
        lw (float, optional): Line width. Defaults to 1.
        save_loc (str, optional): Location to save the plot. Defaults to None.
        
    Raises:
        ValueError: If length of color list does not match number of columns in dataframe.
        ValueError: If key is not a valid column index or name.

    Returns:
        None
    """

    # Create a new axis if none is provided
    if not axis:
        fig, axis = plt.subplots(figsize=(3, 5))

    # Set default line color if none is provided
    if lc is None:
        lc = 'gray'

    # Reorder dataframe columns if order is provided
    if order:
        df = df[order]

    ncols = len(df.columns)

    # Handle point color
    if color is None:
        color = ['black'] * ncols
    elif isinstance(color, str):
        color = [color] * ncols
    elif isinstance(color, list):
        if len(color) != ncols:
            raise ValueError("Length of color list must match number of columns in dataframe")

    # Handle key
    if isinstance(key, int):
        if key >= ncols:
            raise ValueError("Key must be less than number of columns in dataframe")
    elif isinstance(key, str):
        if key not in df.columns:
            raise ValueError("Key must be a column in the dataframe")
        key = df.columns.get_loc(key)

    # Plotting points
    for i, col in enumerate(df.columns):
        axis.scatter([i] * len(df), df[col], label=col, color=color[i], zorder=10)
        axis.set_xticks(range(len(df.columns)))
        axis.set_xticklabels(df.columns, rotation=90)

    # Plotting lines
    other_cols = list(range(ncols))
    other_cols.remove(key)

    for i in range(len(df)):
        for j in other_cols:
            axis.plot([key, j], [df.iloc[i, key], df.iloc[i, j]], color=lc, linewidth=lw)

    # Hide top and right spines
    axis.spines[['top', 'right']].set_visible(False)

    # Save plot
    if save_loc:
        plt.savefig(save_loc, dpi=300, bbox_inches='tight', transparent=True)

    plt.show()

################################################################################
if __name__ == '__main__':
    dirs = [a for a in getDirs(os.path.join(dataPath, 'control'), sstr='nVDCC') if "ISI_20" in a]
    dirs.sort(key=natural_keys)
    control_dirs = np.array(dirs)

    ## Get a list of designs in each category 
    designs_in_categories = get_designs_in_categories(control_dirs)

    get_release_info(designs_in_categories[0,0,0,0])
    # get_release_info(['nVDCC_1_dVAZ_60_nAZ_33_RRP_55_ISI_20_nAP_10'])

    get_calcium_info(designs_in_categories[0,0,0,0])
    # get_calcium_info(['nVDCC_1_dVAZ_60_nAZ_33_RRP_55_ISI_20_nAP_10'])

    # get_synaptotagmin_info(designs_in_categories[0,0,0,0])
    # get_synaptotagmin_info(['nVDCC_1_dVAZ_60_nAZ_33_RRP_55_ISI_20_nAP_10'])
    get_synaptotagmin_info(['nVDCC_8_dVAZ_100_nAZ_27_RRP_5_ISI_20_nAP_10'])
