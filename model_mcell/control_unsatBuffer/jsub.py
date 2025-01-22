#!/usr/bin/python
import os
import re

mdlPath = os.getcwd()
files = [[a, os.path.join(mdlPath, a)] for a in os.listdir(mdlPath) \
				if os.path.isfile(os.path.join(mdlPath, a)) and 'xmain_n' in a]

#print(len(files))
for file in files:
	query = 'qsub -N ' + str(file[0]) + ' -v I=' + str(file[1]) + ' jscript.py'
	print(query)
	os.system(query)