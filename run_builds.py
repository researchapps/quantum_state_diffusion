#!/usr/bin/env python

# This script will automatically make a trivial change to the spec file,
# and push to github once every 10 minutes to build a new image
# This script will be added (commit) to the repo at the end,
# after we disable builds

import os
import sys
import time

def write_file(filename,content,mode="w"):
    '''write_file will open a file, "filename" and write content, "content"
    and properly close the file
    '''
    with open(filename,mode) as filey:
        filey.writelines(content)
    return filename


def read_file(filename,mode="r"):
    '''write_file will open a file, "filename" and write content, "content"
    and properly close the file
    '''
    with open(filename,mode) as filey:
        content = filey.readlines()
    return content


specfile = read_file('Singularity')
delay_minutes = 30

# We will alternate the last echo line to change the build file
last_lines = ['    echo "To run, ./qsd.img --help"\n','   echo "To run, ./qsd.img --help"\n']
idx = 1
iters = range(0,100)
for i in iters:
    print('Running iteration %s' %(i))
    specfile[-1] = last_lines[idx]
    write_file('Singularity',specfile)
    os.system('git commit -a -m "pushing image %s"' %(i))
    if idx == 0:
        idx = 1
    else:
        idx = 0
    os.system('git push origin master')
    time.sleep(60*delay_minutes) # sleep 10 minutes
