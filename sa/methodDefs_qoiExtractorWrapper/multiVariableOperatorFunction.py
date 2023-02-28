"""

"""
import numpy as np


def addList(priorQoiData, newQoiData):       
    return newQoiData if priorQoiData == None else [v1 + v2 for v1, v2 in zip(priorQoiData, newQoiData)]

def addNpList(priorQoiData, newQoiData):  
    return newQoiData if priorQoiData is None else np.add(priorQoiData, newQoiData)

def addValue(priorQoiData, newQoiData):
    return newQoiData if priorQoiData == None else priorQoiData + newQoiData

def identity(priorQoiData, newQoiData):   
    return newQoiData