import math
import numpy as np

def identity(variableData):
    return variableData

def dropFirstHalf(variableData):   
    return variableData[math.floor(len(variableData)/2):]

def meanPeak(variableData):   

    def chunkData(data, n):
        n = max(1, n)
        return [data[i:i+n] for i in range(0, len(data), n)]

    chunks = chunkData(variableData, 73)[:-1]
    peakSum = sum([max(chunk) for chunk in chunks])

    return peakSum

def bmd(variableData):

    def chunkData(data, n):
        n = max(1, n)
        return [data[i:i+n] for i in range(0, len(data), n)]

    chunks = chunkData(variableData, 73)[:-1]
    peakSum = sum([max(chunk) for chunk in chunks])

    return peakSum