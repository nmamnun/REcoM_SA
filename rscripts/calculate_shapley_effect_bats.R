# Rscript
library(boot)
library(readr)
library(ggplot2)
library(RANN)
library(sensitivity)
library(parallel)
library(foreach)
library(iterators)
library(doParallel)
library(foreach)
library(gtools)

samplesA <- read.csv("/home/hbknama0/param_sample/sample_25p_100k/samplesA", sep="")
X <- samplesA

annual_mean_npp <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_npp.csv")
si_mean_npp <- shapleysobol_knn(model=NULL, X = X, U = NULL, nboot = 100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_npp <- annual_mean_npp[['Year_all']]
tell(si_mean_npp,mean_npp)
write.table(si_mean_npp[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_mean_npp_knn.txt")

annual_mean_npp_nano <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_npp_nano.csv")
si_mean_npp_nano <- shapleysobol_knn(model=NULL, X = X, U = NULL, nboot = 100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_npp_nano <- annual_mean_npp_nano[['Year_all']]
tell(si_mean_npp_nano,mean_npp_nano)
write.table(si_mean_npp_nano[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_mean_npp_nano_knn.txt")

annual_mean_npp_dia <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_npp_dia.csv")
si_mean_npp_dia <- shapleysobol_knn(model=NULL, X = X, U = NULL, nboot = 100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_npp_dia <- annual_mean_npp_dia[['Year_all']]
tell(si_mean_npp_dia,mean_npp_dia)
write.table(si_mean_npp_dia[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_mean_npp_dia_knn.txt")

annual_mean_schl <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_schl.csv")
si_mean_schl <- shapleysobol_knn(model=NULL, X = X, U = NULL, nboot = 100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_schl <- annual_mean_schl[['Year_all']]
tell(si_mean_schl,mean_schl)
write.table(si_mean_schl[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_mean_schl_knn.txt")

annual_mean_surf_nanochl <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_surf_nanochl.csv")
si_mean_surf_nanochl <- shapleysobol_knn(model=NULL, X = X, U = NULL, nboot = 100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_surf_nanochl <- annual_mean_surf_nanochl[['Year_all']]
tell(si_mean_surf_nanochl,mean_surf_nanochl)
write.table(si_mean_surf_nanochl[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_mean_surf_nanochl_knn.txt")

annual_mean_surf_diachl <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_surf_diachl.csv")
si_mean_surf_diachl <- shapleysobol_knn(model=NULL, X = X, U = NULL, nboot = 100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_surf_diachl <- annual_mean_surf_diachl[['Year_all']]
tell(si_mean_surf_diachl,mean_surf_diachl)
write.table(si_mean_surf_diachl[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_mean_surf_diachl_knn.txt")

annual_max_schl <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_max_schl.csv")
si_max_schl <- shapleysobol_knn(model=NULL, X = X, U = NULL, nboot = 100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
max_schl <- annual_max_schl[['Year_all']]
tell(si_max_schl,max_schl)
write.table(si_max_schl[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_max_schl_knn.txt")

annual_max_surf_nanochl <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_max_surf_nanochl.csv")
si_max_surf_nanochl <- shapleysobol_knn(model=NULL, X = X, U = NULL, nboot = 100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
max_surf_nanochl <- annual_max_surf_nanochl[['Year_all']]
tell(si_max_surf_nanochl,max_surf_nanochl)
write.table(si_max_surf_nanochl[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_max_surf_nanochl_knn.txt")

annual_max_surf_diachl <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_max_surf_diachl.csv")
si_max_surf_diachl <- shapleysobol_knn(model=NULL, X = X, U = NULL, nboot = 100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
max_surf_diachl <- annual_max_surf_diachl[['Year_all']]
tell(si_max_surf_diachl,max_surf_diachl)
write.table(si_max_surf_diachl[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_max_surf_diachl_knn.txt")

annual_mean_pCO2surf <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_pCO2surf.csv")
si_mean_pCO2surf <- shapleysobol_knn(model=NULL, X = X, U = NULL, nboot = 100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_pCO2surf <- annual_mean_pCO2surf[['Year_all']]
tell(si_mean_pCO2surf,mean_pCO2surf)
write.table(si_mean_pCO2surf[["conf_int"]],'/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_mean_pCO2surf_knn.txt')

annual_mean_CO2Flx <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_CO2Flx.csv")
si_mean_CO2Flx <- shapleysobol_knn(model=NULL, X = X, U = NULL, nboot = 100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_CO2Flx <- annual_mean_CO2Flx[['Year_all']]
tell(si_mean_CO2Flx,mean_CO2Flx)
write.table(si_mean_CO2Flx[["conf_int"]],"/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_mean_CO2Flx_knn.txt")

annual_mean_EXPORTC <- read_csv("/scratch/usr/hbknama0/GSA/QoI/bats/bats_annual_mean_EXPORTC.csv")
si_mean_EXPORTC <- shapleysobol_knn(model=NULL, X = X, U = NULL, nboot = 100, n.knn=25, noise=TRUE, boot.level=0.7, conf=0.95, parl=96)
mean_EXPORTC <- annual_mean_EXPORTC[['Year_all']]
tell(si_mean_EXPORTC,mean_EXPORTC)
write.table(si_mean_EXPORTC[["conf_int"]],'/scratch/usr/hbknama0/GSA/indices/bats_shapley_effect_annual_mean_EXPORTC_knn.txt')
