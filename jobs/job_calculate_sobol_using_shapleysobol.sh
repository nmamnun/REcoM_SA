#!/bin/bash
sbatch job_calculate_stot_using_shapleysobol_npp_bats.slurm
sbatch job_calculate_stot_using_shapleysobol_npp_dyfamed.slurm
sbatch job_calculate_stot_using_shapleysobol_mean_schl_bats.slurm
sbatch job_calculate_stot_using_shapleysobol_mean_schl_dyfamed.slurm
sbatch job_calculate_stot_using_shapleysobol_max_schl_bats.slurm
sbatch job_calculate_stot_using_shapleysobol_max_schl_dyfamed.slurm
sbatch job_calculate_stot_using_shapleysobol_co2_bats.slurm
sbatch job_calculate_stot_using_shapleysobol_co2_dyfamed.slurm
sbatch job_calculate_si_using_shapleysobol_bats.slurm
sbatch job_calculate_si_using_shapleysobol_dyfamed.slurm