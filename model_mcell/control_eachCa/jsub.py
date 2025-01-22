#!/usr/bin/python
import os, re, time
import numpy as np

mdlPath = os.getcwd()

setupLoc = '/home/nishant/mcell/'

fnames = np.sort([f for f in os.listdir(os.path.join(setupLoc, 'control_eachCa')) if 'xmain_nVDCC_1' in f])

files = [[f, os.path.join(mdlPath, f)] for f in fnames[::-1]]
print(len(files))
# for f in files: print(f)

for i,file in enumerate(files):
    query = 'qsub -N ' + '_'.join([a for a in re.findall(r'\d+', file[0])[:-1]]) + ' -v I=' + str(file[1]) + ' jscript.py'
    print(i, query)
    os.system(query)

    if (i+1)%1 == 0:
        print(i)
        time.sleep(1800)
