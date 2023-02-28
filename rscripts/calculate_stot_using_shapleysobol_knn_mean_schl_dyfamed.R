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

annual_mean_schl <- read_csv("/scratch/usr/hbknama0/GSA/QoI/dyfamed/dyfamed_annual_mean_schl.csv")
si_mean_schl <- shapleysobol_knn(model=NULL, X = X, method = "knn", U = 0, nboot = 50, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_schl <- annual_mean_schl[['Year_all']]
tell(si_mean_schl,mean_schl)
write.table(si_mean_schl[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/dyfamed_stot_annual_mean_schl_knn.txt")

annual_mean_surf_nanochl <- read_csv("/scratch/usr/hbknama0/GSA/QoI/dyfamed/dyfamed_annual_mean_surf_nanochl.csv")
si_mean_surf_nanochl <- shapleysobol_knn(model=NULL, X = X, method = "knn", U = 0, nboot = 50, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_surf_nanochl <- annual_mean_surf_nanochl[['Year_all']]
tell(si_mean_surf_nanochl,mean_surf_nanochl)
write.table(si_mean_surf_nanochl[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/dyfamed_stot_annual_mean_surf_nanochl_knn.txt")

annual_mean_surf_diachl <- read_csv("/scratch/usr/hbknama0/GSA/QoI/dyfamed/dyfamed_annual_mean_surf_diachl.csv")
si_mean_surf_diachl <- shapleysobol_knn(model=NULL, X = X, method = "knn", U = 0, nboot = 50, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_surf_diachl <- annual_mean_surf_diachl[['Year_all']]
tell(si_mean_surf_diachl,mean_surf_diachl)
write.table(si_mean_surf_diachl[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/dyfamed_stot_annual_mean_surf_diachl_knn.txt")
