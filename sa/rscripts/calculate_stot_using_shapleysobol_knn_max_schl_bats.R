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

# Function to automate repetitive tasks
process_data <- function(data_path, output_path, X) {
  # Read the data
  data <- read_csv(data_path)
  
  # Calculate sensitivity indices
  si <- shapleysobol_knn(model=NULL, X=X, method="knn", U=0, nboot=50, n.knn=25, 
                          noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
  
  # Extract the 'Year_all' column
  year_all <- data[['Year_all']]
  
  # Print the sensitivity indices
  tell(si, year_all)
  
  # Write the confidence intervals to file
  write.table(si[["conf_int"]], output_path)
}

# Define root directory for easier path management
root_dir <- "/scratch/usr/hbknama0/GSA"

# Define paths for the datasets
data_paths <- c(
  paste0(root_dir, "/QoI/bats/bats_annual_max_schl.csv"),
  paste0(root_dir, "/QoI/bats/bats_annual_max_surf_nanochl.csv"),
  paste0(root_dir, "/QoI/bats/bats_annual_max_surf_diachl.csv")
)

# Define paths for the output files
output_paths <- c(
  paste0(root_dir, "/indices/bats_stot_annual_max_schl_knn.txt"),
  paste0(root_dir, "/indices/bats_stot_annual_max_surf_nanochl_knn.txt"),
  paste0(root_dir, "/indices/bats_stot_annual_max_surf_diachl_knn.txt")
)

# Read the samples
samplesA <- read.csv("/home/hbknama0/sample_shortlist_28param_100k/samplesA", sep="")
X <- samplesA

# Process each dataset
for (i in 1:length(data_paths)) {
  process_data(data_paths[i], output_paths[i], X)
}
