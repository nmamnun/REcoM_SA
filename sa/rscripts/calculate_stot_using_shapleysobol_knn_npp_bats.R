# Rscript
# Libraries
library(parallel)
library(doParallel)
library(foreach)
library(gtools)
library(boot)
library(RANN)
library(whitening)
library(TSP)
library(iterators)
library(readr)
library(sensitivity)
# library(ggplot2)  

# Function to streamline repetitive tasks
perform_analysis <- function(samples_file, data_file, output_file) {
  # Read samples
  samples <- read.csv(samples_file, sep="")
  
  # Shapley Sobol KNN analysis
  si_result <- shapleysobol_knn(
    model = NULL, 
    X = samples, 
    method = "knn", 
    U = 0, 
    nboot = 50, 
    n.knn = 25, 
    noise = TRUE, 
    boot.level = 0.7, 
    conf = 0.95, 
    parl = 96
  )
  
  # Read data file
  data <- read_csv(data_file)
  
  # Tell analysis
  tell(si_result, data[['Year_all']])
  
  # Write results
  write.table(si_result[["conf_int"]], output_file)
}

# Base directory paths
samples_file <- "/home/hbknama0/sample_shortlist_28param_100k/samplesA"
data_base_path <- "/scratch/usr/hbknama0/GSA/QoI/bats"
output_base_path <- "/scratch/usr/hbknama0/GSA/indices"

# Data and output file names
data_files <- c("/bats_annual_mean_npp.csv", "/bats_annual_mean_npp_nano.csv", "/bats_annual_mean_npp_dia.csv")
output_files <- c("/bats_stot_annual_mean_npp_knn.txt", "/bats_stot_annual_mean_npp_nano_knn.txt", "/bats_stot_annual_mean_npp_dia_knn.txt")

# Perform analysis for different datasets
for(i in 1:length(data_files)) {
  perform_analysis(
    samples_file,
    paste0(data_base_path, data_files[i]),
    paste0(output_base_path, output_files[i])
  )
}

