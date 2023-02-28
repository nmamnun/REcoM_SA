import env.util as util

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats
from scipy.stats import lognorm
from scipy.stats import norm


##############   Model Variance estimators

def combinedAB(qoiFullA, qoiFullB):
    return np.var(np.r_[qoiFullA, qoiFullB], axis=0, ddof=1)

def squaredA(qoiFullA, qoiFullB):
    return np.var(np.r_[qoiFullA, qoiFullA], axis=0, ddof=1)    

def squaredB(qoiFullA, qoiFullB):
    return np.var(np.r_[qoiFullB, qoiFullB], axis=0, ddof=1)  

def varA(qoiFullA, qoiFullB):
    return np.var(qoiFullA, axis=0, ddof=1)


##############   S_i estimators

def saltelli_Si(context, qoiFullA, qoiFullB, qoiSingleA):   
    varianceFullAB = context._estimatorFunctionVY(qoiFullA, qoiFullB)
    sensitivities_u = []
    for u in range(len(qoiSingleA)):  
        sens = np.mean(qoiFullB * (qoiSingleA[u] - qoiFullA), axis=0) / varianceFullAB
        sensitivities_u.append(sens)

    return sensitivities_u  

def jansen_Si(context, qoiFullA, qoiFullB, qoiSingleA):   
    varianceFullAB = context._estimatorFunctionVY(qoiFullA, qoiFullB)
    sensitivities_u = []
    for u in range(len(qoiSingleA)):  
        sens = (varianceFullAB - 0.5 * np.mean((qoiFullB - qoiSingleA[u])**2, axis=0)) / varianceFullAB
        sensitivities_u.append(sens)

    return sensitivities_u     


##############   S_Ti estimators

# Note: Estimator is called jansen estimator in thesis. Current notation kept for backwards compatibility 
def saltelli_STi(context, qoiFullA, qoiFullB, qoiSingleA):   
    varianceFullAB = context._estimatorFunctionVY(qoiFullA, qoiFullB)
    sensitivities_u = []
    for u in range(len(qoiSingleA)):  
        sens = 0.5 * np.mean((qoiFullA - qoiSingleA[u]) ** 2, axis=0) / varianceFullAB
        sensitivities_u.append(sens)

    return sensitivities_u  


