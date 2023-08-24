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

samplesA <- read.csv("/home/hbknama0/sample_shortlist_28param_100k/samplesA", sep="")
X <- samplesA

annual_mean_npp <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_npp.csv")
si_mean_npp <- shapleysobol_knn(model=NULL, X = X, method = "knn", U = NULL, nboot = 50, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_npp <- annual_mean_npp[['Year_all']]
tell(si_mean_npp,mean_npp)
write.table(si_mean_npp[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_mean_npp_knn.txt")
