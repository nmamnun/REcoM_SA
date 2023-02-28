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
annual_mean_pCO2surf <- read_csv("/scratch/usr/hbknama0/GSA/QoI/dyfamed/dyfamed_annual_mean_pCO2surf.csv")
si_mean_pCO2surf <- shapleysobol_knn(model=NULL, X = X, method = "knn", U = 0, nboot = 50, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_pCO2surf <- annual_mean_pCO2surf[['Year_all']]
tell(si_mean_pCO2surf,mean_pCO2surf)
write.table(si_mean_pCO2surf[["conf_int"]],'/scratch/usr/hbknama0/GSA/indices/dyfamed_stot_annual_mean_pCO2surf_knn.txt')

annual_mean_CO2Flx <- read_csv("/scratch/usr/hbknama0/GSA/QoI/dyfamed/dyfamed_annual_mean_CO2Flx.csv")
si_mean_CO2Flx <- shapleysobol_knn(model=NULL, X = X, method = "knn", U = 0, nboot = 50, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_CO2Flx <- annual_mean_CO2Flx[['Year_all']]
tell(si_mean_CO2Flx,mean_CO2Flx)
write.table(si_mean_CO2Flx[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/dyfamed_stot_annual_mean_CO2Flx_knn.txt")

annual_mean_EXPORTC <- read_csv("/scratch/usr/hbknama0/GSA/QoI/dyfamed/dyfamed_annual_mean_EXPORTC.csv")
si_mean_EXPORTC <- shapleysobol_knn(model=NULL, X = X, method = "knn", U = 0, nboot = 50, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_EXPORTC <- annual_mean_EXPORTC[['Year_all']]
tell(si_mean_EXPORTC,mean_EXPORTC)
write.table(si_mean_EXPORTC[["conf_int"]],'/scratch/usr/hbknama0/GSA/indices/dyfamed_stot_annual_mean_EXPORTC_knn.txt')
