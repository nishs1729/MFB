#!/usr/bin/python
import os
import re

mdlPath = os.getcwd()
files = [[a, os.path.join(mdlPath, a)] for a in os.listdir(mdlPath) \
		  if os.path.isfile(os.path.join(mdlPath, a)) and 'xmain_nVDCC_' in a \
		  and '.o' not in a]

print(len(files), mdlPath)
for file in files[:2]:
	query = 'qsub -N ' + '_'.join([a for a in re.findall(r'\d+', file[0])[:-1]]) + ' -v I=' + str(file[1]) + ' jscript.py'
	print(query)

	submit = input("\nSubmit the job? [y/n]\t")
	if submit=='y':
		print('submit')
		# os.system(query)
	else:
		print('Job was not submited!')
