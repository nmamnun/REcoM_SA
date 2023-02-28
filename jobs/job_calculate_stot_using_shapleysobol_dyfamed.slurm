#!/bin/bash
#SBATCH -p large96
#SBATCH -N 1
#SBATCH -n 96
#SBATCH -t 11:29:00
cat $0
module load gcc/8.3.0
module load R/4.0.2
module load udunits/gcc.8/2.2.26
export BASE_DIR=/home/hbknama0/gsa_recom2/code/sa/rscripts
Rscript $BASE_DIR/calculate_st_using_shapleysobol_knn_dyfamed.R
exit
