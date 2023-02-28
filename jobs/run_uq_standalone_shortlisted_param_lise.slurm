#!/bin/bash

#SBATCH -p standard96
#SBATCH -N 1
#SBATCH -t 06:00:00

source /home/hbknama0/miniconda3/bin/activate
conda activate general

cd /home/hbknama0/gsa_recom2/code

python uq_standalone.py -p "sample_shortlist_100k"

exit
