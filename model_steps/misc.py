#from . parameters import *

ls = ['-', '--', '-.', ':']
marker = ['.', ',', 'o', 'x', '+', 'd', '>', '<', '^', 'v']

### Fancy print for dictionaries
def printd(*var):
    for d in var:
        if isinstance(d, dict):
            for k,v in d.items():
                print(str(k)+':\t', v)
            print('')
        else:
            print(d)

### decorator function to time functions
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        tf = time.time()
        print('Func: ' + method.__name__ + ' run in ' + str(tf-ts) + 's')
        return result
    return timed

### Get timeseries voltage from file and return interpolated function
def getV(fname='v.txt'):
    data = np.genfromtxt(fname, unpack=True, usecols=(0,1))
    return interp1d(data[0], data[1], kind='cubic')


def getSimInfo(dname, key=None, skip=1):
    infoList = dname.split('_')[skip:]
    if key:
        info = infoList[infoList.index(key)+1]
    else:
        info = dict([[infoList[i], infoList[i+1]] for i in range(0,len(infoList),2)])
    return info