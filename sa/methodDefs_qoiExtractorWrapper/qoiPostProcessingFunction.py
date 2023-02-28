import numpy as np
"""
    Most of the calculations for the QoI generation is in this post processing step
"""


def identity(context, qoiData):
    return qoiData

def transpose(qoiData):   
    return np.transpose(qoiData)


#####       Processing steps for BMP, BMV, BMD QoI generation       #####


def meanData2D(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [0], axis=1)   
    meanData = np.mean(meanData, axis=0)
    meanData = np.reshape(meanData, (365))
    return meanData

def meanData3D(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [0], axis=2)   
    meanData = np.mean(meanData, axis=0)
    meanData = np.reshape(meanData, (30, 365))
    return meanData    

def meanData3DSurface(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [0], axis=2)   
    meanData = np.mean(meanData, axis=0)
    for i in range(29):
        meanData = np.delete(meanData, [1], axis=0)      
    meanData = np.reshape(meanData, (365))
    return meanData 

def meanData3DAverage(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [0], axis=2)   
    meanData = np.mean(meanData, axis=0)
    meanData = np.mean(meanData, axis=0)   
    meanData = np.reshape(meanData, (365))
    return meanData      


###################################         

def bloomMeanPeak2D(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [0], axis=1)

    return calcBloomMeanPeak(context, meanData) 

def bloomMeanPeak3DAverage(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [1], axis=2)

    layermean = np.mean(meanData, axis=1)

    return calcBloomMeanPeak(context, layermean) 

def bloomMeanPeak3DSurface(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [1], axis=2)

    for i in range(29):
        meanData = np.delete(meanData, [1], axis=1)

    return calcBloomMeanPeak(context, meanData) 
    

def calcBloomMeanPeak(context, data):
    sampleSize = np.shape(data)[0]
    yearData = np.reshape(data, (sampleSize, 5, 73))

    result = np.empty(sampleSize)
    for i in range(sampleSize):
        peakSum = 0
        for y in range(5):
            bloomPeak = getBloomPeak(yearData[i][y])
            peakSum += bloomPeak
        peakMean = peakSum / 5
        result[i] = peakMean

    return result


#####################################################

def bloomMeanValue2D(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [0], axis=1)

    return calcBloomMeanValue(context, meanData)

def bloomMeanValue3DAverage(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [1], axis=2)

    layermean = np.mean(meanData, axis=1)
 
    return calcBloomMeanValue(context, layermean)

def bloomMeanValue3DSurface(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [1], axis=2)

    for i in range(29):
        meanData = np.delete(meanData, [1], axis=1)

    return calcBloomMeanValue(context, meanData)     

def calcBloomMeanValue(context, data):
    sampleSize = np.shape(data)[0]
    yearData = np.reshape(data, (sampleSize, 5, 73))


    result = np.empty(sampleSize)
    for i in range(sampleSize):
        valueSum = 0
        for y in range(5):
            bloomValue = getBloomMean(yearData[i][y])
            valueSum += bloomValue
        valueSum = valueSum / 5
        result[i] = valueSum

    return result


####################################################

def bloomMeanDuration2D(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [0], axis=1)

    return calcBloomMeanDuration(context, meanData)
    
def bloomMeanDuration3DAverage(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [1], axis=2)

    layermean = np.mean(meanData, axis=1)
 
    return calcBloomMeanDuration(context, layermean)

def bloomMeanDuration3DSurface(context, qoiData):
    meanData = [sampleData / len(context.qoiVariableList) for sampleData in qoiData]
    meanData = np.delete(meanData, [1], axis=2)

    for i in range(29):
        meanData = np.delete(meanData, [1], axis=1)

    return calcBloomMeanDuration(context, meanData)     

   

def calcBloomMeanDuration(context, data):
    sampleSize = np.shape(data)[0]
    yearData = np.reshape(data, (sampleSize, 5, 73))

    result = np.empty(sampleSize)
    for i in range(sampleSize):
        valueSum = 0
        for y in range(5):
            bloomDuration = getBloomDuration(yearData[i][y])
            valueSum += bloomDuration
        valueSum = valueSum / 5
        result[i] = valueSum

    return result








##################################


#### Year data helper functions ####
def chunkData(data, n):
    n = max(1, n)
    return [data[i:i+n] for i in range(0, len(data), n)]

#### Bloom helper functions ####

def getBloomPeak(yearData):
    bloomStart = getBloomStart(yearData)
    bloomEnd = getBloomEnd(yearData)

    if bloomStart == -1 or bloomEnd == -1:
        return -1

    maxVal = max(yearData[bloomStart:bloomEnd])

    maxIndex = np.argwhere(yearData[bloomStart:bloomEnd] == maxVal).flatten()[0]

    if bloomStart > maxIndex  + bloomStart:
        return -1
    if bloomEnd < maxIndex + bloomStart:      
        return -1

    return maxVal

def getBloomStart(yearData):
    median = np.median(yearData)
    threshold = median * 1.05

    currStart = -1
    for i in range(len(yearData)):
        if yearData[i] > threshold:
            if currStart == -1:
                currStart = i
            elif i - currStart == 3:
                return currStart
        else:
            currStart = -1

    return -1

def getBloomEnd(yearData):
    median = np.median(yearData)
    bloomStart = getBloomStart(yearData)
    if bloomStart == -1:
        return -1
    threshold = median * 1.05

    currEnd = -1
    for i in range(bloomStart, len(yearData)):
        if yearData[i] < threshold:
            if currEnd == -1:
                currEnd = i
            elif i - currEnd == 2:
                return currEnd
        else:
            currEnd = -1

    return len(yearData)



def getBloomMean(yearData):
    bloomStart = getBloomStart(yearData)
    bloomEnd = getBloomEnd(yearData)

    if bloomStart == -1 or bloomEnd == -1:
        return -1

    meanData = np.mean(yearData[bloomStart : bloomEnd])
    return meanData

def getBloomDuration(yearData):
    bloomStart = getBloomStart(yearData)
    bloomEnd = getBloomEnd(yearData)

    if bloomStart == -1 or bloomEnd == -1:
        return -1
    return bloomEnd - bloomStart