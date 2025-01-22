import collections, six, operator
from functools import reduce
from collections.abc import Iterable

### My color palette
cplight = [
    '#a1d99b', '#a6dcef', '#FF9677', '#bcbddc', '#17becf', '#d6616b', '#e7ba52', 
    '#66c2a5', '#f09ae9', '#c7b198', '#99b898', '#b17a78', '#c168c8', '#bdbdbd', '#ffffff'
]
cplightp = [
    '#17becf', '#FF9677', '#a1d99b', '#d6616b', '#e7ba52', '#bcbddc', '#66c2a5',
    '#c168c8', '#b17a78', '#a6dcef', '#f09ae9', '#c7b198', '#99b898', '#bdbdbd', '#ffffff'
]
cpdark  = [
    '#3182bd', '#e6550d', '#31a354', '#900c3f', '#cf7500', '#6b6ecf', '#008080', 
    '#6a2c70', '#843c39', '#305F72', '#fa26a0', '#8c6d31', '#00454a', '#636363', '#000000'
]
cpall   = reduce(operator.add, zip(cpdark, cplight))
cppaired = reduce(operator.add, zip(cpdark, cplightp))


def _iterable(arg):
    return (
        isinstance(arg, collections.Iterable) 
        and not isinstance(arg, six.string_types)
    )

def niceprint(*argv):
    """
    Recursively prints elements of the given arguments in an easy-to-see (nice) format.

    This function accepts multiple arguments and recursively prints their elements.
    If an argument is a dictionary, it prints each key followed by its associated value(s).
    If an argument is an iterable (excluding strings), it prints each element on a new line.
    Otherwise, it prints the argument followed by a newline.

    Parameters
    ----------
    *argv : iterable
        Variable length argument list that can contain any type of elements,
        including dictionaries and other iterables.
    """
    for a in argv:
        if _iterable(a):
            if isinstance(a, dict):
                for k,v in a.items():
                    print(k+':')
                    niceprint(v)
            else:
                for e in a:
                    print(e)
                print()
        else:
            print(a,'\n')
            
def get_info(name, key=None, skip=0, delim='_', dtype=str):
    """
    Extracts information from a name.

    The name is expected in the following convention: 
    <prefix>_<key1>_<value1>_<key2>_<value2>_<...>. 
    The function returns a dictionary with the key-value pairs. 
    If a key is specified, the corresponding value is returned instead.

    Parameters
    ----------
    name : str
        The name of the directory to extract information from.
    key : str, optional
        The key to extract the value for. If unspecified, a dictionary
        with all key-value pairs is returned.
    skip : int, optional
        The number of initial prefixes to ignore. Defaults to 0.
    delim : str, optional
        The delimiter between the information parts. Defaults to '_'.

    Returns
    -------
    info : dict or str
        A dictionary with the key-value pairs, or the value corresponding
        to the specified key.
    """

    info_list = name.split(delim)[skip:]
    if key:
        info = dtype(info_list[info_list.index(key)+1])
    else:
        info = dict([[info_list[i], dtype(info_list[i+1])] for i in range(0,len(info_list),2)])
    return info


def is_notebook(more=False):
    """
    Checks if code is running in a Jupyter notebook, IPython, or standard Python environment.

    Parameters
    ----------
    more : bool, optional
        If True, returns the environment name instead of a boolean.

    Returns
    -------
    environment : str or bool
        The environment name, or a boolean indicating if this is a notebook or not.
    """
    try:
        shell = get_ipython().__class__.__name__

        ## Jupyter notebook or qtconsole
        if shell == 'ZMQInteractiveShell':
            if more:
                return 'notebook'
            else:
                return True
        
        ## Terminal running IPython
        elif shell == 'TerminalInteractiveShell':
            if more:
                return 'IPython'
            else:
                return False
        
        ## Other type (?)
        else:
            return False
        
    ## Probably standard Python interpreter
    except NameError:
        if more:
            return 'Probably standard Python interpreter'
        else:
            return False
        
def flatten(target):
    """
    Recursively flatten a list of lists or other iterables.

    Flattens a list of lists or other iterables into a single list.
    If the target is not iterable, returns a list containing the target.

    Parameters
    ----------
    target : iterable or other
        The target to be flattened.

    Returns
    -------
    flattened_list : list
        The flattened list.
    """
    return sum(
        (flatten(sub) if isinstance(sub, Iterable) and not isinstance(sub, (str, bytes)) else [sub] for sub in target), 
        []
    )
        

if __name__ == '__main__':
    ## test is_notebook
    # print(get_info('abc_1_def_2.3_ghi_3.txt', key=None, dtype=str))
    # is_notebook(more=True)

    ## test flatten
    import numpy as np
    l = [1,2,[2,3],[[[[['we', 'e', 7], 'w']]]], np.array([2,3,4]), dict({'a':1, 'b':2, 'c':3})]
    print(flatten(l))