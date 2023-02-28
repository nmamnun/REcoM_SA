#!/bin/bash
#SBATCH -p standard96
#SBATCH -N 1
#SBATCH -n 96
#SBATCH -t 03:59:00
cat $0
module load gcc/8.3.0
module load R/4.0.2
module load udunits/gcc.8/2.2.26
export BASE_DIR=/home/hbknama0/gsa_recom2/code/sa/rscripts
Rscript $BASE_DIR/calculate_si_using_shapleysobol_knn_dyfamed.R
exit
