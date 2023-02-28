#!/bin/bash
#SBATCH -p standard96
#SBATCH -N 1
#SBATCH -t 05:59:00

source /home/hbknama0/miniconda3/bin/activate
conda activate general
srun python /home/hbknama0/gsa_recom2/code/qoi/get_qoi_dyfamed.py

exit
