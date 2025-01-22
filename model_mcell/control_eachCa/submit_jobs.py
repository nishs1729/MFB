#!/usr/bin/python
from datetime import datetime
import os, subprocess, time

jobs_th = 1900 # Submit a jobarray if number of running job in ada < jobs_th
n_jobs_to_submit = 100 # number of subjobs in an jobarray
total_jobs = 500 # total number of subjobs to run
job_file = 'job.py'

## set "#PBS -t" option in `job_file` to f"#PBS -t 1-{n_jobs_to_submit}"
os.system(f'sed -i "s/#PBS -t.*/#PBS -t 1-{n_jobs_to_submit}/g" {job_file}')

i = 0
while i < total_jobs:
    ## Get the number of jobs running on ada
    qq = "qstat -q | awk 'END {print $1}'"
    njob = subprocess.check_output(['bash', '-c', qq])
    njob = int(str(njob.decode('utf-8')).strip())

    now = datetime.now().strftime("%d/%m %H:%M")
    print(f'\n{now} | running: {njob} | jobs_th: {jobs_th} | total: {total_jobs}')

    ## Submit `n_jobs_to_submit` jobs whenever the
    ## number of running jobs falls below `jobs_th`
    if njob < jobs_th:
        ## Submit a job array
        query = f'qsub -N job_{i} -v I={str(i)} {job_file}'
        print(query)
        os.system(query)

        i += n_jobs_to_submit

    ## wait for 60 s to check/submit again
    time.sleep(60)
