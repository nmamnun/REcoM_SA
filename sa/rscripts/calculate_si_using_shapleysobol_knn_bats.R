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



# Define function for repetitive operations
process_data <- function(filename_suffix) {
  # Construct paths
  input_path <- paste0("/scratch/usr/hbknama0/GSA/QoI/bats/bats_", filename_suffix, ".csv")
  output_path <- paste0("/scratch/usr/hbknama0/GSA/indices/bats_si_", filename_suffix, "_knn.txt")
  
  # Read data
  data <- read_csv(input_path)
  
  # Calculation
  si_data <- shapleysobol_knn(model=NULL, X=X, U=1, nboot=100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
  tell_data <- data[['Year_all']]
  tell(si_data, tell_data)
  
  # Write to file
  write.table(si_data[["conf_int"]], output_path)
}

# Read samplesA
samplesA <- read.csv("/home/hbknama0/sample_shortlist_28param_100k/samplesA", sep="")
X <- samplesA

# File suffixes to be processed
file_suffixes <- c("annual_mean_npp", "annual_mean_npp_nano", "annual_mean_npp_dia", "annual_mean_schl", 
                   "annual_mean_surf_nanochl", "annual_mean_surf_diachl", "annual_max_schl", 
                   "annual_max_surf_nanochl", "annual_max_surf_diachl", "annual_mean_pCO2surf", 
                   "annual_mean_CO2Flx", "annual_mean_EXPORTC")

# Process each file
sapply(file_suffixes, process_data)

