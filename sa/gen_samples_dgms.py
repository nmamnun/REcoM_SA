#!/usr/bin/env python3

import numpy as np
from SALib.sample import finite_diff
from string import Template

BASE_PATH = '/albedo/work/user/nmamnun/GSA'


def str2num_noneg(s):
    try:
        return float(s)
    except ValueError:
        return None


def extract_parameters_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.readline().strip().split()


def load_samples_from_file(file_path, D):
    samples = []
    with open(file_path, 'r') as f:
        f.readline()  # skip header
        for line in f:
            data = line.split()[:D]
            samples.append([str2num_noneg(val) for val in data])
    return np.array(samples)


def generate_data_recom_files(template_file, parameter_names, samples):
    with open(template_file, 'r') as T:
        template = Template(T.read())
    N, D = samples.shape
    for i in range(N):
        data = {parameter_names[j]: '%.13f' % samples[i, j] for j in range(D)}
        content = template.safe_substitute(data)
        with open(f'{BASE_PATH}/recom_data/data.recom-{i+1:05}', 'w') as f:
            f.write(content)


file_path = f'{BASE_PATH}/plot_sensi/plot_si/samplesA'
parameter_names = extract_parameters_from_file(file_path)
parameter_num = len(parameter_names)

samples = load_samples_from_file(file_path, parameter_num)
min_values = np.min(samples, axis=0)
max_values = np.max(samples, axis=0)

parameter_ranges = list(zip(min_values, max_values))

num_trajectories = 1000
X_or_samples = finite_diff.sample(problem={
    'num_vars': parameter_num,
    'names': parameter_names,
    'bounds': parameter_ranges,
    'groups': None
}, N=num_trajectories)

np.save('parameter_samples.npy', X_or_samples)

generate_data_recom_files(
    f'{BASE_PATH}/reorg_data.recom', parameter_names, X_or_samples)
