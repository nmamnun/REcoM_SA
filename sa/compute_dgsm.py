#!/usr/bin/env python3

import numpy as np
from SALib.analyze import dgsm

BASE_PATH = '/albedo/work/user/nmamnun/GSA/QoI'
SUB_PATHS = ['bats', 'dyfamed']
QOIS = [
    'annual_mean_schl', 'annual_mean_surf_nanochl', 'annual_mean_surf_diachl',
    'annual_max_schl', 'annual_max_surf_nanochl', 'annual_max_surf_diachl',
    'annual_mean_npp', 'annual_mean_npp_nano', 'annual_mean_npp_dia',
    'annual_mean_EXPORTC', 'annual_mean_CO2Flx', 'annual_mean_pCO2surf'
]


def load_file(sub_path, qoi):
    file_path = f"{BASE_PATH}/{sub_path}/{sub_path}_{qoi}.npy"
    return np.load(file_path)[:, -1]


def analyze_dgsm(X, Y):
    return dgsm.analyze(
        problem={
            'num_vars': len(parameter_names),
            'names': parameter_names,
            'bounds': parameter_ranges,
            'groups': None
        },
        X=X,
        Y=Y
    )


samples_file = np.load('parameter_samples.npy')
print(samples_file.shape)

X_or_samples = np.array([["%.13f" % value for value in row]
                        for row in samples_file]).astype(np.float64)

# Dictionary to store results
results = {}

for qoi in QOIS:
    for sub_path in SUB_PATHS:
        Y = load_file(sub_path, qoi)
        results[f"{sub_path}_{qoi}"] = analyze_dgsm(X_or_samples, Y)
