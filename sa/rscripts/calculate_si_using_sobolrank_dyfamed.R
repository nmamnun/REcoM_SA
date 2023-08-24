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
perform_analysis <- function(samples, data_file, output_file) {
  # Read data file
  data <- read_csv(data_file)
  
  # Shapley Sobol Rank analysis
  si_result <- sobolrank(
    model = NULL, 
    X = samples, 
    nboot = 100, 
    conf = 0.95
  )
  
  # Tell analysis
  tell(si_result, data[['Year_all']])
  
  # Write results
  write.table(si_result[["S"]], output_file)
}

# Read samples
samples_file <- "/home/hbknama0/sample_shortlist_28param_100k/samplesA"
samples <- read.csv(samples_file, sep="")

# Base directory paths
data_base_path <- "/scratch/usr/hbknama0/GSA/QoI/dyfamed"
output_base_path <- "/scratch/usr/hbknama0/GSA/indices"

# Lists of data and output files
data_files <- c(
  "dyfamed_annual_mean_npp.csv", "dyfamed_annual_mean_npp_nano.csv", "dyfamed_annual_mean_npp_dia.csv", 
  "dyfamed_annual_mean_schl.csv", "dyfamed_annual_mean_surf_nanochl.csv", "dyfamed_annual_mean_surf_diachl.csv",
  "dyfamed_annual_max_schl.csv", "dyfamed_annual_max_surf_nanochl.csv", "dyfamed_annual_max_surf_diachl.csv",
  "dyfamed_annual_mean_pCO2surf.csv", "dyfamed_annual_mean_CO2Flx.csv", "dyfamed_annual_mean_EXPORTC.csv"
)

output_files <- c(
  "dyfamed_sobolranksi_annual_mean_npp.txt", "dyfamed_sobolranksi_annual_mean_npp_nano.txt", "dyfamed_sobolranksi_annual_mean_npp_dia.txt",
  "dyfamed_sobolranksi_annual_mean_schl.txt", "dyfamed_sobolranksi_annual_mean_surf_nanochl.txt", "dyfamed_sobolranksi_annual_mean_surf_diachl.txt",
  "dyfamed_sobolranksi_annual_max_schl.txt", "dyfamed_sobolranksi_annual_max_surf_nanochl.txt", "dyfamed_sobolranksi_annual_max_surf_diachl.txt",
  "dyfamed_sobolranksi_annual_mean_pCO2surf.txt", "dyfamed_sobolranksi_annual_mean_CO2Flx.txt", "dyfamed_sobolranksi_annual_mean_EXPORTC.txt"
)

# Perform analysis for different datasets
for(i in 1:length(data_files)) {
  perform_analysis(
    samples,
    paste0(data_base_path, "/", data_files[i]),
    paste0(output_base_path, "/", output_files[i])
  )
}

