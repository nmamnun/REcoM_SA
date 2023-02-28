#!/usr/bin/env python3
import sys, glob, os
from pathlib import Path
import MITgcmutils as gcm
import numpy as np
import pandas as pd

def get_var(filePath, qoiVariable):
    ncFile = gcm.mnc_files(filePath)
    var = ncFile.variables[qoiVariable][:]
    varSqueeze = np.squeeze(var)
    val = np.transpose(varSqueeze)
    ncFile.close()
    return val

def chunkData(data, n):
        n = max(1, n)
        return [data[i:i+n] for i in range(0, len(data), n)]


sample_size = 100000
ncfile_dir = Path('/scratch/usr/hbknama0/GSA/model_outputs/bats')
recomDiags3D_files = np.sort(list(ncfile_dir.glob('bats_diags3d*')))

annual_max_schl = np.zeros([sample_size, 5])
annual_min_schl = np.zeros([sample_size, 5])
annual_mean_schl = np.zeros([sample_size, 5])

annual_max_surf_nanochl = np.zeros([sample_size, 5])
annual_min_surf_nanochl = np.zeros([sample_size, 5])
annual_mean_surf_nanochl = np.zeros([sample_size, 5])

annual_max_surf_diachl = np.zeros([sample_size, 5])
annual_min_surf_diachl = np.zeros([sample_size, 5])
annual_mean_surf_diachl = np.zeros([sample_size, 5])

for i in range(sample_size):
    TRAC06 = get_var(str(recomDiags3D_files[i]), 'TRAC06')
    surf_nanochl = TRAC06[0]
    chunks_surf_nanochl = chunkData(surf_nanochl, 73)[:-1]
    annual_max_surf_nanochl[i] = np.max(chunks_surf_nanochl, axis=1)
    annual_min_surf_nanochl[i] = np.min(chunks_surf_nanochl, axis=1)
    annual_mean_surf_nanochl[i] = np.mean(chunks_surf_nanochl, axis=1)
    #
    TRAC15 = get_var(str(recomDiags3D_files[i]), 'TRAC15')
    surf_diachl = TRAC15[0]
    chunks_surf_diachl = chunkData(surf_diachl, 73)[:-1]
    annual_max_surf_diachl[i] = np.max(chunks_surf_diachl, axis=1)
    annual_min_surf_diachl[i] = np.min(chunks_surf_diachl, axis=1)
    annual_mean_surf_diachl[i] = np.mean(chunks_surf_diachl, axis=1)
    #
    CHLA = TRAC06 + TRAC15
    SCHLA = CHLA[0]
    chunks_SCHLA = chunkData(SCHLA, 73)[:-1]
    annual_max_schl[i] = np.max(chunks_SCHLA, axis=1)
    annual_min_schl[i] = np.min(chunks_SCHLA, axis=1)
    annual_mean_schl[i] = np.mean(chunks_SCHLA, axis=1)

annual_max_surf_nanochl_dic = {
    'Year_1'  : annual_max_surf_nanochl[:,0],
    'Year_2'  : annual_max_surf_nanochl[:,1],
    'Year_3'  : annual_max_surf_nanochl[:,2],
    'Year_4'  : annual_max_surf_nanochl[:,3],
    'Year_5'  : annual_max_surf_nanochl[:,4],
    'Year_all': np.mean(annual_max_surf_nanochl, axis=1)
}
annual_max_surf_nanochl_df = pd.DataFrame(data=annual_max_surf_nanochl_dic)

annual_min_surf_nanochl_dic = {
    'Year_1'  : annual_min_surf_nanochl[:,0],
    'Year_2'  : annual_min_surf_nanochl[:,1],
    'Year_3'  : annual_min_surf_nanochl[:,2],
    'Year_4'  : annual_min_surf_nanochl[:,3],
    'Year_5'  : annual_min_surf_nanochl[:,4],
    'Year_all': np.mean(annual_min_surf_nanochl, axis=1)
}
annual_min_surf_nanochl_df = pd.DataFrame(data=annual_min_surf_nanochl_dic)

annual_mean_surf_nanochl_dic = {
    'Year_1'  : annual_mean_surf_nanochl[:,0],
    'Year_2'  : annual_mean_surf_nanochl[:,1],
    'Year_3'  : annual_mean_surf_nanochl[:,2],
    'Year_4'  : annual_mean_surf_nanochl[:,3],
    'Year_5'  : annual_mean_surf_nanochl[:,4],
    'Year_all': np.mean(annual_mean_surf_nanochl, axis=1)
}
annual_mean_surf_nanochl_df = pd.DataFrame(data=annual_mean_surf_nanochl_dic)

annual_max_surf_diachl_dic = {
    'Year_1'  : annual_max_surf_diachl[:,0],
    'Year_2'  : annual_max_surf_diachl[:,1],
    'Year_3'  : annual_max_surf_diachl[:,2],
    'Year_4'  : annual_max_surf_diachl[:,3],
    'Year_5'  : annual_max_surf_diachl[:,4],
    'Year_all': np.mean(annual_max_surf_diachl, axis=1)
}
annual_max_surf_diachl_df = pd.DataFrame(data=annual_max_surf_diachl_dic)

annual_min_surf_diachl_dic = {
    'Year_1'  : annual_min_surf_diachl[:,0],
    'Year_2'  : annual_min_surf_diachl[:,1],
    'Year_3'  : annual_min_surf_diachl[:,2],
    'Year_4'  : annual_min_surf_diachl[:,3],
    'Year_5'  : annual_min_surf_diachl[:,4],
    'Year_all': np.mean(annual_min_surf_diachl, axis=1)
}
annual_min_surf_diachl_df = pd.DataFrame(data=annual_min_surf_diachl_dic)

annual_mean_surf_diachl_dic = {
    'Year_1'  : annual_mean_surf_diachl[:,0],
    'Year_2'  : annual_mean_surf_diachl[:,1],
    'Year_3'  : annual_mean_surf_diachl[:,2],
    'Year_4'  : annual_mean_surf_diachl[:,3],
    'Year_5'  : annual_mean_surf_diachl[:,4],
    'Year_all': np.mean(annual_mean_surf_diachl, axis=1)
}
annual_mean_surf_diachl_df = pd.DataFrame(data=annual_mean_surf_diachl_dic)

annual_max_schl_dic = {
    'Year_1'  : annual_max_schl[:,0],
    'Year_2'  : annual_max_schl[:,1],
    'Year_3'  : annual_max_schl[:,2],
    'Year_4'  : annual_max_schl[:,3],
    'Year_5'  : annual_max_schl[:,4],
    'Year_all': np.mean(annual_max_schl, axis=1)
}
annual_max_schl_df = pd.DataFrame(data=annual_max_schl_dic)

annual_min_schl_dic = {
    'Year_1'  : annual_min_schl[:,0],
    'Year_2'  : annual_min_schl[:,1],
    'Year_3'  : annual_min_schl[:,2],
    'Year_4'  : annual_min_schl[:,3],
    'Year_5'  : annual_min_schl[:,4],
    'Year_all': np.mean(annual_min_schl, axis=1)
}
annual_min_schl_df = pd.DataFrame(data=annual_min_schl_dic)

annual_mean_schl_dic = {
    'Year_1'  : annual_mean_schl[:,0],
    'Year_2'  : annual_mean_schl[:,1],
    'Year_3'  : annual_mean_schl[:,2],
    'Year_4'  : annual_mean_schl[:,3],
    'Year_5'  : annual_mean_schl[:,4],
    'Year_all': np.mean(annual_mean_schl, axis=1)
}
annual_mean_schl_df = pd.DataFrame(data=annual_mean_schl_dic)


recomDiags2D_files = np.sort(list(ncfile_dir.glob('bats_diags2d*')))

annual_mean_npp_nano = np.zeros([sample_size, 5])
annual_mean_npp_dia = np.zeros([sample_size, 5])
annual_mean_npp = np.zeros([sample_size, 5])
annual_mean_pCO2surf = np.zeros([sample_size, 5])
annual_mean_CO2Flx = np.zeros([sample_size, 5])
annual_mean_EXPORTC = np.zeros([sample_size, 5])

for i in range(sample_size):
    NETPPVIS = get_var(str(recomDiags2D_files[i]), 'NETPPVIS')
    chunks_NETPPVIS = chunkData(NETPPVIS, 73)[:-1]
    annual_mean_npp_nano[i] = np.mean(chunks_NETPPVIS, axis=1)

    NETPPVID = get_var(str(recomDiags2D_files[i]), 'NETPPVID')
    chunks_NETPPVID = chunkData(NETPPVID, 73)[:-1]
    annual_mean_npp_dia[i] = np.mean(chunks_NETPPVID, axis=1)

    NPP = NETPPVIS + NETPPVID
    chunks_NPP = chunkData(NPP, 73)[:-1]
    annual_mean_npp[i] = np.mean(chunks_NPP, axis=1)

    pCO2surf = get_var(str(recomDiags2D_files[i]), 'pCO2surf')
    chunks_pCO2surf = chunkData(pCO2surf, 73)[:-1]
    annual_mean_pCO2surf[i] = np.mean(chunks_pCO2surf, axis=1)

    CO2Flx = get_var(str(recomDiags2D_files[i]), 'CO2Flx')
    chunks_CO2Flx = chunkData(CO2Flx, 73)[:-1]
    annual_mean_CO2Flx[i] = np.mean(chunks_CO2Flx, axis=1)

    EXPORTC = get_var(str(recomDiags2D_files[i]), 'EXPORTC')
    chunks_EXPORTC = chunkData(EXPORTC, 73)[:-1]
    annual_mean_EXPORTC[i] = np.mean(chunks_EXPORTC, axis=1)

annual_mean_npp_nano_dic = {
    'Year_1'  : annual_mean_npp_nano[:,0],
    'Year_2'  : annual_mean_npp_nano[:,1],
    'Year_3'  : annual_mean_npp_nano[:,2],
    'Year_4'  : annual_mean_npp_nano[:,3],
    'Year_5'  : annual_mean_npp_nano[:,4],
    'Year_all': np.mean(annual_mean_npp_nano, axis=1)
}
annual_mean_npp_nano_df = pd.DataFrame(data=annual_mean_npp_nano_dic)

annual_mean_npp_dia_dic = {
    'Year_1'  : annual_mean_npp_dia[:,0],
    'Year_2'  : annual_mean_npp_dia[:,1],
    'Year_3'  : annual_mean_npp_dia[:,2],
    'Year_4'  : annual_mean_npp_dia[:,3],
    'Year_5'  : annual_mean_npp_dia[:,4],
    'Year_all': np.mean(annual_mean_npp_dia, axis=1)
}
annual_mean_npp_dia_df = pd.DataFrame(data=annual_mean_npp_dia_dic)


annual_mean_npp_dic = {
    'Year_1'  : annual_mean_npp[:,0],
    'Year_2'  : annual_mean_npp[:,1],
    'Year_3'  : annual_mean_npp[:,2],
    'Year_4'  : annual_mean_npp[:,3],
    'Year_5'  : annual_mean_npp[:,4],
    'Year_all': np.mean(annual_mean_npp, axis=1)
}
annual_mean_npp_df = pd.DataFrame(data=annual_mean_npp_dic)


annual_mean_pCO2surf_dic = {
    'Year_1'  : annual_mean_pCO2surf[:,0],
    'Year_2'  : annual_mean_pCO2surf[:,1],
    'Year_3'  : annual_mean_pCO2surf[:,2],
    'Year_4'  : annual_mean_pCO2surf[:,3],
    'Year_5'  : annual_mean_pCO2surf[:,4],
    'Year_all': np.mean(annual_mean_pCO2surf, axis=1)
}
annual_mean_pCO2surf_df = pd.DataFrame(data=annual_mean_pCO2surf_dic)

annual_mean_CO2Flx_dic = {
    'Year_1'  : annual_mean_CO2Flx[:,0],
    'Year_2'  : annual_mean_CO2Flx[:,1],
    'Year_3'  : annual_mean_CO2Flx[:,2],
    'Year_4'  : annual_mean_CO2Flx[:,3],
    'Year_5'  : annual_mean_CO2Flx[:,4],
    'Year_all': np.mean(annual_mean_CO2Flx, axis=1)
}
annual_mean_CO2Flx_df = pd.DataFrame(data=annual_mean_CO2Flx_dic)

annual_mean_EXPORTC_dic = {
    'Year_1'  : annual_mean_EXPORTC[:,0],
    'Year_2'  : annual_mean_EXPORTC[:,1],
    'Year_3'  : annual_mean_EXPORTC[:,2],
    'Year_4'  : annual_mean_EXPORTC[:,3],
    'Year_5'  : annual_mean_EXPORTC[:,4],
    'Year_all': np.mean(annual_mean_EXPORTC, axis=1)
}
annual_mean_EXPORTC_df = pd.DataFrame(data=annual_mean_EXPORTC_dic)





import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
pandas2ri.activate()
write_csv = robjects.r('write.csv')
qoi_dir = Path('/scratch/usr/hbknama0/GSA/QoI/bats')
write_csv(annual_max_surf_nanochl_df, os.path.join(qoi_dir, 'bats_annual_max_surf_nanochl.csv'))
write_csv(annual_min_surf_nanochl_df, os.path.join(qoi_dir, 'bats_annual_min_surf_nanochl.csv'))
write_csv(annual_mean_surf_nanochl_df, os.path.join(qoi_dir, 'bats_annual_mean_surf_nanochl.csv'))

write_csv(annual_max_surf_diachl_df, os.path.join(qoi_dir, 'bats_annual_max_surf_diachl.csv'))
write_csv(annual_min_surf_diachl_df, os.path.join(qoi_dir, 'bats_annual_min_surf_diachl.csv'))
write_csv(annual_mean_surf_diachl_df, os.path.join(qoi_dir, 'bats_annual_mean_surf_diachl.csv'))

write_csv(annual_max_schl_df, os.path.join(qoi_dir, 'bats_annual_max_schl.csv'))
write_csv(annual_min_schl_df, os.path.join(qoi_dir, 'bats_annual_min_schl.csv'))
write_csv(annual_mean_schl_df, os.path.join(qoi_dir, 'bats_annual_mean_schl.csv'))

write_csv(annual_mean_npp_nano_df, os.path.join(qoi_dir, 'bats_annual_mean_npp_nano.csv'))
write_csv(annual_mean_npp_dia_df, os.path.join(qoi_dir, 'bats_annual_mean_npp_dia.csv'))
write_csv(annual_mean_npp_df, os.path.join(qoi_dir, 'bats_annual_mean_npp.csv'))

write_csv(annual_mean_pCO2surf_df, os.path.join(qoi_dir, 'bats_annual_mean_pCO2surf.csv'))
write_csv(annual_mean_CO2Flx_df, os.path.join(qoi_dir, 'bats_annual_mean_CO2Flx.csv'))
write_csv(annual_mean_EXPORTC_df, os.path.join(qoi_dir, 'bats_annual_mean_EXPORTC.csv'))
