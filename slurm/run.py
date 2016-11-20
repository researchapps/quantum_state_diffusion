#!/usr/bin/python env

'''
Quantum State Diffusion: Submit jobs on SLURM

'''

import os

# Variables to run jobs
basedir = os.path.abspath(os.getcwd())
output_dir = '/scratch/users/vsochat/IMAGES/singularity/quantumsd/result'

# Variables for each job
memory = 32000
partition = 'normal'
delta_t = 5e-3
duration = 10000
downsample = 1000

# Create subdirectories for job, error, and output files
job_dir = "%s/.job" %(basedir)
out_dir = "%s/.out" %(basedir)
for new_dir in [output_dir,job_dir,out_dir]:
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

# We are going to vary the seed argument, and generate and submit a job for each
seeds = range(1,1000)

for seed in seeds: 
    print "Processing seed %s" %(seed)
    # Write job to file
    filey = ".job/qsd_%s.job" %(seed)
    filey = open(filey,"w")
    filey.writelines("#!/bin/bash\n")
    filey.writelines("#SBATCH --job-name=qsd_%s\n" %(seed))
    filey.writelines("#SBATCH --output=%s/qsd_%s.out\n" %(out_dir,seed))
    filey.writelines("#SBATCH --error=%s/qsd_%s.err\n" %(out_dir,seed))
    filey.writelines("#SBATCH --time=2-00:00\n")
    filey.writelines("#SBATCH --mem=%s\n" %(memory))
    filey.writelines("module load singularity\n")
    command = "singularity run --bind %s:/data qsd.img --delta_t %s --output_dir /data --duration %s --downsample %s --seed %s --save2pkl\n" %(output_dir,delta_t,duration,downsample,seed)
    print(command)
    filey.writelines(command)
    filey.close()
    os.system("sbatch -p %s .job/qsd_%s.job" %(partition,seed))
