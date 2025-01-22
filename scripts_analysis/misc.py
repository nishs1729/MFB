import collections, six, operator, re
from collections.abc import Iterable
from functools import reduce

### color palette
cplight = ['#a1d99b', '#a6dcef', '#FF9677', '#bcbddc', '#17becf', '#d6616b', '#e7ba52', 
           '#66c2a5', '#f09ae9', '#c7b198', '#99b898', '#b17a78', '#c168c8', '#bdbdbd',
           '#ffffff']
cplightp = ['#17becf', '#FF9677', '#a1d99b', '#d6616b', '#e7ba52', '#bcbddc', '#66c2a5',
            '#c168c8', '#b17a78', '#a6dcef', '#f09ae9', '#c7b198', '#99b898', '#bdbdbd',
            '#ffffff']
cpdark  = ['#3182bd', '#e6550d', '#31a354', '#900c3f', '#cf7500', '#6b6ecf', '#008080', 
           '#6a2c70', '#843c39', '#305F72', '#fa26a0', '#8c6d31', '#00454a', '#636363',
           '#000000']
cpall   = reduce(operator.add, zip(cpdark, cplight))
cppaired = reduce(operator.add, zip(cpdark, cplightp))

def _iterable(arg):
    return (
        isinstance(arg, collections.Iterable) 
        and not isinstance(arg, six.string_types)
    )

def niceprint(*argv):
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
            
def getSimInfo(dname, key=None, skip=1):
    infoList = dname.split('_')[skip:]
    if key:
        info = infoList[infoList.index(key)+1]
    else:
        info = dict([[infoList[i], infoList[i+1]] for i in range(0,len(infoList),2)])
    return info


def natural_keys(text):
    def atoi(text):
        return int(text) if text.isdigit() else text
    return [atoi(c) for c in re.split(r'(\d+)', text)]