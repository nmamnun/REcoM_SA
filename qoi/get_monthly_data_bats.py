#!/usr/bin/env python3
import sys, glob, os
from pathlib import Path
import MITgcmutils as mitu
import numpy as np
import pandas as pd

def get_var(filePath, qoiVariable):
    ncFile = mitu.mnc_files(filePath)
    var = ncFile.variables[qoiVariable][:]
    varSqueeze = np.squeeze(var)
    val = np.transpose(varSqueeze)
    ncFile.close()
    return val

month_index = np.array([0,  6,   12,   18,   24,   30,   36,
                            42,  49,   55,   61,   67,   73,
                            79,  85,   91,   97,   103,  109,
                            115, 122,  128,  134,  140,  146,
                            152, 158,  164,  170,  176,  182,
                            188, 195,  201,  207,  213,  219,
                            225, 231,  237,  243,  249,  255,
                            261, 268,  274,  280,  286,  292,
                            298, 304,  310,  316,  322,  328,
                            334, 341,  347,  353,  359,  365])
def get_monthly_data(data):
    monthly_data = np.zeros(60)
    for i in range(60):
        monthly_data[i] = np.mean(data[month_index[i]:month_index[i+1]])
    return monthly_data

sample_size = 100000
ncfile_dir = Path(os.getcwd())
recomDiags3D_files = np.sort(list(ncfile_dir.glob('bats_diags3d*')))

# monthly_surf_nanochl = np.zeros([sample_size, 60])
# monthly_surf_diachl = np.zeros([sample_size, 60])
# monthly_surf_chl = np.zeros([sample_size, 60])

monthly_mean_surf_nanochl = np.zeros([sample_size, 12])
monthly_mean_surf_diachl = np.zeros([sample_size, 12])
monthly_mean_surf_chl = np.zeros([sample_size, 12])

for i in range(sample_size):
    TRAC06 = get_var(str(recomDiags3D_files[i]), 'TRAC06')
    surf_nanochl = TRAC06[0]
    monthly_data = get_monthly_data(surf_nanochl)
    # monthly_surf_nanochl[i] = monthly_data
    monthly_mean_data = np.mean(np.reshape(monthly_data, (5, 12)),axis=0)
    monthly_mean_surf_nanochl[i] = monthly_mean_data
    #
    TRAC15 = get_var(str(recomDiags3D_files[i]), 'TRAC15')
    surf_diachl = TRAC15[0]
    monthly_data = get_monthly_data(surf_diachl)
    # monthly_surf_diachl[i] = monthly_data
    monthly_mean_data = np.mean(np.reshape(monthly_data, (5, 12)),axis=0)
    monthly_mean_surf_diachl[i] = monthly_mean_data
    #
    CHLA = TRAC06 + TRAC15
    SCHLA = CHLA[0]
    monthly_data = get_monthly_data(SCHLA)
    # monthly_surf_chl[i] = monthly_data
    monthly_mean_data = np.mean(np.reshape(monthly_data, (5, 12)),axis=0)
    monthly_mean_surf_chl[i] = monthly_mean_data

monthly_mean_surf_nanochl_dic = {
    'Jan'  : monthly_mean_surf_nanochl[:,0],
    'Feb'  : monthly_mean_surf_nanochl[:,1],
    'Mar'  : monthly_mean_surf_nanochl[:,2],
    'Apr'  : monthly_mean_surf_nanochl[:,3],
    'May'  : monthly_mean_surf_nanochl[:,4],
    'Jun'  : monthly_mean_surf_nanochl[:,5],
    'Jul'  : monthly_mean_surf_nanochl[:,6],
    'Aug'  : monthly_mean_surf_nanochl[:,7],
    'Sep'  : monthly_mean_surf_nanochl[:,8],
    'Oct'  : monthly_mean_surf_nanochl[:,9],
    'Nov'  : monthly_mean_surf_nanochl[:,10],
    'Dec'  : monthly_mean_surf_nanochl[:,11],
}
monthly_mean_surf_nanochl_df = pd.DataFrame(monthly_mean_surf_nanochl_dic)

monthly_mean_surf_diachl_dic = {
    'Jan'  : monthly_mean_surf_diachl[:,0],
    'Feb'  : monthly_mean_surf_diachl[:,1],
    'Mar'  : monthly_mean_surf_diachl[:,2],
    'Apr'  : monthly_mean_surf_diachl[:,3],
    'May'  : monthly_mean_surf_diachl[:,4],
    'Jun'  : monthly_mean_surf_diachl[:,5],
    'Jul'  : monthly_mean_surf_diachl[:,6],
    'Aug'  : monthly_mean_surf_diachl[:,7],
    'Sep'  : monthly_mean_surf_diachl[:,8],
    'Oct'  : monthly_mean_surf_diachl[:,9],
    'Nov'  : monthly_mean_surf_diachl[:,10],
    'Dec'  : monthly_mean_surf_diachl[:,11],
}
monthly_mean_surf_diachl_df = pd.DataFrame(monthly_mean_surf_diachl_dic)

monthly_mean_surf_chl_dic = {
    'Jan'  : monthly_mean_surf_chl[:,0],
    'Feb'  : monthly_mean_surf_chl[:,1],
    'Mar'  : monthly_mean_surf_chl[:,2],
    'Apr'  : monthly_mean_surf_chl[:,3],
    'May'  : monthly_mean_surf_chl[:,4],
    'Jun'  : monthly_mean_surf_chl[:,5],
    'Jul'  : monthly_mean_surf_chl[:,6],
    'Aug'  : monthly_mean_surf_chl[:,7],
    'Sep'  : monthly_mean_surf_chl[:,8],
    'Oct'  : monthly_mean_surf_chl[:,9],
    'Nov'  : monthly_mean_surf_chl[:,10],
    'Dec'  : monthly_mean_surf_chl[:,11],
}
monthly_mean_surf_chl_df = pd.DataFrame(monthly_mean_surf_chl_dic)





recomDiags2D_files = np.sort(list(ncfile_dir.glob('bats_diags2d*')))

monthly_mean_npp_nano = np.zeros([sample_size, 12])
monthly_mean_npp_dia = np.zeros([sample_size, 12])
monthly_mean_npp = np.zeros([sample_size, 12])
monthly_mean_pCO2surf = np.zeros([sample_size, 12])
monthly_mean_CO2Flx = np.zeros([sample_size, 12])
monthly_mean_EXPORTC = np.zeros([sample_size, 12])

for i in range(sample_size):
    NETPPVIS = get_var(str(recomDiags2D_files[i]), 'NETPPVIS')
    monthly_data = get_monthly_data(NETPPVIS)
    monthly_mean_data = np.mean(np.reshape(monthly_data, (5, 12)),axis=0)
    monthly_mean_npp_nano[i] = monthly_mean_data

    NETPPVID = get_var(str(recomDiags2D_files[i]), 'NETPPVID')
    monthly_data = get_monthly_data(NETPPVID)
    monthly_mean_data = np.mean(np.reshape(monthly_data, (5, 12)),axis=0)
    monthly_mean_npp_dia[i] = monthly_mean_data

    NPP = NETPPVIS + NETPPVID
    monthly_data = get_monthly_data(NPP)
    monthly_mean_data = np.mean(np.reshape(monthly_data, (5, 12)),axis=0)
    monthly_mean_npp[i] = monthly_mean_data

    pCO2surf = get_var(str(recomDiags2D_files[i]), 'pCO2surf')
    monthly_data = get_monthly_data(pCO2surf)
    monthly_mean_data = np.mean(np.reshape(monthly_data, (5, 12)),axis=0)
    monthly_mean_pCO2surf[i] = monthly_mean_data

    CO2Flx = get_var(str(recomDiags2D_files[i]), 'CO2Flx')
    monthly_data = get_monthly_data(CO2Flx)
    monthly_mean_data = np.mean(np.reshape(monthly_data, (5, 12)),axis=0)
    monthly_mean_CO2Flx[i] = monthly_mean_data

    EXPORTC = get_var(str(recomDiags2D_files[i]), 'EXPORTC')
    monthly_data = get_monthly_data(EXPORTC)
    monthly_mean_data = np.mean(np.reshape(monthly_data, (5, 12)),axis=0)
    monthly_mean_EXPORTC[i] = monthly_mean_data


monthly_mean_npp_nano_dic = {
    'Jan'  : monthly_mean_npp_nano[:,0],
    'Feb'  : monthly_mean_npp_nano[:,1],
    'Mar'  : monthly_mean_npp_nano[:,2],
    'Apr'  : monthly_mean_npp_nano[:,3],
    'May'  : monthly_mean_npp_nano[:,4],
    'Jun'  : monthly_mean_npp_nano[:,5],
    'Jul'  : monthly_mean_npp_nano[:,6],
    'Aug'  : monthly_mean_npp_nano[:,7],
    'Sep'  : monthly_mean_npp_nano[:,8],
    'Oct'  : monthly_mean_npp_nano[:,9],
    'Nov'  : monthly_mean_npp_nano[:,10],
    'Dec'  : monthly_mean_npp_nano[:,11],
}
monthly_mean_npp_nano_df = pd.DataFrame(monthly_mean_npp_nano_dic)

monthly_mean_npp_dia_dic = {
    'Jan'  : monthly_mean_npp_dia[:,0],
    'Feb'  : monthly_mean_npp_dia[:,1],
    'Mar'  : monthly_mean_npp_dia[:,2],
    'Apr'  : monthly_mean_npp_dia[:,3],
    'May'  : monthly_mean_npp_dia[:,4],
    'Jun'  : monthly_mean_npp_dia[:,5],
    'Jul'  : monthly_mean_npp_dia[:,6],
    'Aug'  : monthly_mean_npp_dia[:,7],
    'Sep'  : monthly_mean_npp_dia[:,8],
    'Oct'  : monthly_mean_npp_dia[:,9],
    'Nov'  : monthly_mean_npp_dia[:,10],
    'Dec'  : monthly_mean_npp_dia[:,11],
}
monthly_mean_npp_dia_df = pd.DataFrame(monthly_mean_npp_dia_dic)

monthly_mean_npp_dic = {
    'Jan'  : monthly_mean_npp[:,0],
    'Feb'  : monthly_mean_npp[:,1],
    'Mar'  : monthly_mean_npp[:,2],
    'Apr'  : monthly_mean_npp[:,3],
    'May'  : monthly_mean_npp[:,4],
    'Jun'  : monthly_mean_npp[:,5],
    'Jul'  : monthly_mean_npp[:,6],
    'Aug'  : monthly_mean_npp[:,7],
    'Sep'  : monthly_mean_npp[:,8],
    'Oct'  : monthly_mean_npp[:,9],
    'Nov'  : monthly_mean_npp[:,10],
    'Dec'  : monthly_mean_npp[:,11],
}
monthly_mean_npp_df = pd.DataFrame(monthly_mean_npp_dic)

monthly_mean_pCO2surf_dic = {
    'Jan'  : monthly_mean_pCO2surf[:,0],
    'Feb'  : monthly_mean_pCO2surf[:,1],
    'Mar'  : monthly_mean_pCO2surf[:,2],
    'Apr'  : monthly_mean_pCO2surf[:,3],
    'May'  : monthly_mean_pCO2surf[:,4],
    'Jun'  : monthly_mean_pCO2surf[:,5],
    'Jul'  : monthly_mean_pCO2surf[:,6],
    'Aug'  : monthly_mean_pCO2surf[:,7],
    'Sep'  : monthly_mean_pCO2surf[:,8],
    'Oct'  : monthly_mean_pCO2surf[:,9],
    'Nov'  : monthly_mean_pCO2surf[:,10],
    'Dec'  : monthly_mean_pCO2surf[:,11],
}
monthly_mean_pCO2surf_df = pd.DataFrame(monthly_mean_pCO2surf_dic)

monthly_mean_CO2Flx_dic = {
    'Jan'  : monthly_mean_CO2Flx[:,0],
    'Feb'  : monthly_mean_CO2Flx[:,1],
    'Mar'  : monthly_mean_CO2Flx[:,2],
    'Apr'  : monthly_mean_CO2Flx[:,3],
    'May'  : monthly_mean_CO2Flx[:,4],
    'Jun'  : monthly_mean_CO2Flx[:,5],
    'Jul'  : monthly_mean_CO2Flx[:,6],
    'Aug'  : monthly_mean_CO2Flx[:,7],
    'Sep'  : monthly_mean_CO2Flx[:,8],
    'Oct'  : monthly_mean_CO2Flx[:,9],
    'Nov'  : monthly_mean_CO2Flx[:,10],
    'Dec'  : monthly_mean_CO2Flx[:,11],
}
monthly_mean_CO2Flx_df = pd.DataFrame(monthly_mean_CO2Flx_dic)

monthly_mean_EXPORTC_dic = {
    'Jan'  : monthly_mean_EXPORTC[:,0],
    'Feb'  : monthly_mean_EXPORTC[:,1],
    'Mar'  : monthly_mean_EXPORTC[:,2],
    'Apr'  : monthly_mean_EXPORTC[:,3],
    'May'  : monthly_mean_EXPORTC[:,4],
    'Jun'  : monthly_mean_EXPORTC[:,5],
    'Jul'  : monthly_mean_EXPORTC[:,6],
    'Aug'  : monthly_mean_EXPORTC[:,7],
    'Sep'  : monthly_mean_EXPORTC[:,8],
    'Oct'  : monthly_mean_EXPORTC[:,9],
    'Nov'  : monthly_mean_EXPORTC[:,10],
    'Dec'  : monthly_mean_EXPORTC[:,11],
}
monthly_mean_EXPORTC_df = pd.DataFrame(monthly_mean_EXPORTC_dic)

import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
pandas2ri.activate()
write_csv = robjects.r('write.csv')
qoi_dir = Path('/scratch/usr/hbknama0/GSA/QoI/bats')
write_csv(monthly_mean_surf_nanochl_df, os.path.join(qoi_dir, 'bats_monthly_mean_surf_nanochl.csv'))
write_csv(monthly_mean_surf_diachl_df, os.path.join(qoi_dir, 'bats_monthly_mean_surf_diachl.csv'))
write_csv(monthly_mean_surf_chl_df, os.path.join(qoi_dir, 'bats_monthly_mean_surf_chl.csv'))

write_csv(monthly_mean_npp_nano_df, os.path.join(qoi_dir, 'bats_monthly_mean_npp_nano.csv'))
write_csv(monthly_mean_npp_dia_df, os.path.join(qoi_dir, 'bats_monthly_mean_npp_dia.csv'))
write_csv(monthly_mean_npp_df, os.path.join(qoi_dir, 'bats_monthly_mean_npp.csv'))

write_csv(monthly_mean_EXPORTC_df, os.path.join(qoi_dir, 'bats_monthly_mean_EXPORTC.csv'))
write_csv(monthly_mean_CO2Flx_df, os.path.join(qoi_dir, 'bats_monthly_mean_CO2Flx.csv'))
write_csv(monthly_mean_pCO2surf_df, os.path.join(qoi_dir, 'bats_monthly_mean_pCO2surf.csv'))
