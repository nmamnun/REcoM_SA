#!/usr/bin/env python

import numpy as np
from scipy.stats import norm

parameters = [
'alpha', 'P_cm', 'deg_CHL', 'alpha_d', 'P_cm_d', 'deg_CHL_d', \
'graz_max', 'grazEff', 'agg_PD', 'agg_PP'
]

#"""Read Sample Matrices provided by Marvin."""
sampleA = []
with open('samplesA') as f:
    for line in f:
        linearr = line.split()
        sampleA.append(linearr)
f.close()

sampleB = []
with open('samplesB') as f:
    for line in f:
        linearr = line.split()
        sampleB.append(linearr)
f.close()

# """Prepare sample matrix, X for (P+2)*N model evaluation
# actually at end I do not need X"""
nP = len(parameters)                # number of factor (parameter)
nS = 7500                           # number of sample
X1 = np.zeros((nS,nP))
X2 = np.zeros((nS,nP))
for i in range(nS):
    for j in range(nP):
        a = float(sampleA[i+1][j])
        X1[i][j] = a
for i in range(nS):
    for j in range(nP):
        b = float(sampleA[i+1][j])
        X2[i][j] = b
X = np.concatenate((X1, X2), axis=0)
for i in range(nP):
    Xb = X1
    Xb[:,i] = X2[:,i]
    X = np.concatenate((X, Xb), axis=0 )

data = np.load('npps.npy') # load simulated net primery production for entire time dimension (366)
Y = data[:,0] # try for one time step first
# normalize the data
Y = (Y - Y.mean()) / Y.std()
# prepare matrices for f(A_j), f(B_j) and f(AB_J)
Y_A = Y[0:nS]  # nS = number of sample
Y_B = Y[nS:nS*2]
Y_AB = np.zeros((nS, nP)) # nP = number of paramenter
step = nP + 2
for i in range(nP):
        Y_AB[:, i] = Y[(i + 2):Y.size:step]

# Calculate the variece of output data V(Y)
V_Y = np.var(np.r_[Y_A, Y_B], axis=0) # model evaluation for both sample matrix A and B
print(V_Y)

# implement equetion b of table 2 of Saltelli et al 2010
V_x_saltelli2010 = np.zeros(nP)
for i in range(nP):
    V = np.mean(Y_B * (Y_AB[:, i] - Y_A), axis=0)
    V_x_saltelli2010[i] = V

print(V_x_saltelli2010)
print("------------------------------")

# implement equetion c of table 2 of Saltelli et al 2010
V_x_jansen = np.zeros(nP)
for i in range(nP):
    V = np.var(np.r_[Y_A, Y_B], axis=0) - 0.5 * np.mean((Y_B - Y_AB[:, i]) ** 2, axis=0)
    V_x_jansen[i] = V

print(V_x_jansen)
print("------------------------------")

# implement equetion e of table 2 of Saltelli et al 2010
E_x_sobol2007 = np.zeros(nP)
for i in range(nP):
    E = np.mean(Y_A * (Y_A - Y_AB[:, i]), axis=0)
    E_x_sobol2007[i] = E

print(E_x_sobol2007)
print("------------------------------")

# implement equetion f of table 2 Saltelli et al 2010
E_x_saltelli2010 = np.zeros(nP)
for i in range(nP):
    E =  0.5 * np.mean((Y_A - Y_AB[:, i]) ** 2, axis=0)
    E_x_saltelli2010[i] = E
print(E_x_saltelli2010)

mSI_saltelli2010 = V_x_saltelli2010/V_Y
print(mSI_saltelli2010)
print("------------------------------")
mSI_jansen = V_x_jansen/V_Y
print(mSI_jansen)
print("------------------------------")
tSI_sobol2007 = E_x_sobol2007/V_Y
print(tSI_sobol2007)
print("------------------------------")
tSI_saltelli2010 = E_x_saltelli2010/V_Y
print(tSI_saltelli2010)
