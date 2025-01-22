import os
import re
import time
from itertools import product

# nvdcc = range(2, 15, 2)
# dvdcc = range(60, 230, 20)
# naz   = range(7, 30, 2)
# rrp   = range(5, 41, 5)

siminfo = []
with open('newsims', 'r') as nf:
	for line in nf:
		siminfo.append([int(a) for a in line.split(' ')])
# print(siminfo, len(siminfo))


files = []
# for nVDCC, dVDCC, nAZ in product(nvdcc, dvdcc, naz):
for nVDCC, dVDCC, nAZ, RRP in siminfo[:10]:
    f = "xmain_nVDCC_" + str(nVDCC) + "_dVDCC_" + str(dVDCC) + "_nAZ_" + str(nAZ) + "_RRP_" + str(RRP) + "_ISI_20_nAP_10.mdl"
    files.append(f)

mdlPath = os.getcwd()

# files = [['_'.join([n for n in re.findall(r'\d+', a)]), os.path.join(mdlPath, a)] for a in files]
print(files)
