# Rscript
library(parallel)
library(doParallel)
library(foreach)
library(ggplot2)
library(boot)
library(RANN)
library(gtools)
library(readr)
library(sensitivity)
library(iterators)
library(foreach)


samplesA <- read.csv("/home/hbknama0/param_sample/sample_shortlist_100k/samplesA", sep="")
X <- samplesA

annual_mean_npp <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_npp.csv")
si_mean_npp <- shapleysobol_knn(model=NULL, X = X, method = "knn", U = 0, nboot = 50, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_npp <- annual_mean_npp[['Year_all']]
tell(si_mean_npp,mean_npp)
write.table(si_mean_npp[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_stot_annual_mean_npp_knn.txt")

annual_mean_npp_nano <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_npp_nano.csv")
si_mean_npp_nano <- shapleysobol_knn(model=NULL, X = X, method = "knn", U = 0, nboot = 50, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_npp_nano <- annual_mean_npp_nano[['Year_all']]
tell(si_mean_npp_nano,mean_npp_nano)
write.table(si_mean_npp_nano[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_stot_annual_mean_npp_nano_knn.txt")

annual_mean_npp_dia <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_npp_dia.csv")
si_mean_npp_dia <- shapleysobol_knn(model=NULL, X = X, method = "knn", U = 0, nboot = 50, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_npp_dia <- annual_mean_npp_dia[['Year_all']]
tell(si_mean_npp_dia,mean_npp_dia)
write.table(si_mean_npp_dia[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_stot_annual_mean_npp_dia_knn.txt")
