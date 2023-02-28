import math

import env.util as util
import env.logger as logger


# Calculates how many preceding zeros we need
def calculateFileNumberPaddingLength(context, dimension, numQoiFiles=None):
    numFiles = numQoiFiles if numQoiFiles != None else getNumQoiFiles(context)
    if numFiles == 0:
        return 0
    return 1 + math.floor(math.log10(numFiles))

# Calculates the number of files produced in the UQ algorithm
def getNumQoiFiles(context):
    return context.totalIterations * (context.uqFullAPerturbed + context.uqFullBPerturbed + context.uqSingleAPerturbed * context.dimension + context.uqSingleBPerturbed * context.dimension)

# Returns the QoI file numbers corresponding to a given matrixType and parameter
def getFileNumbers(context, matrixType, uncertainParameter=None):
    if matrixType == 'FullA' or matrixType == 'FullB':
        offset = calculateFileNumberOffset(context, matrixType)
        return [val for val in range(offset, offset + context.totalIterations)]
    elif matrixType == 'SingleA' or matrixType == 'SingleB':
        offset = calculateFileNumberOffset(context, matrixType)
        res = [val for val in range(offset, offset + context.totalIterations * context.dimension)]
        return res[uncertainParameter::context.dimension]

# Sample matrix output order: A -> B -> A_B^i -> B_A^i. 
# If a sample matrix output is omitted, shift back the following file indices accordingly
def calculateFileNumberOffset(context, matrixType):
    if matrixType == 'FullA':
        return 1
    elif matrixType == 'FullB':
        return 1 + context.totalIterations * context.uqFullAPerturbed
    if matrixType == 'SingleA':
        return 1 + context.totalIterations * (context.uqFullAPerturbed + context.uqFullBPerturbed)
    elif matrixType == 'SingleB':
        return 1 + context.totalIterations * (context.uqFullAPerturbed + context.uqFullBPerturbed) + context.uqSingleAPerturbed * context.totalIterations * context.dimension

# Checks whether the files in the /qoi directory roughly conform to the config.json settings
def checkFileConfigIntegrity(context, qoiPath):
    logger.debug("Iterations=" + str(context.totalIterations) + " - FullA=" + str(context.uqFullAPerturbed) + ", FullB=" + str(context.uqFullBPerturbed) + ", SingleA=" + str(context.uqSingleAPerturbed) + ", SingleB=" + str(context.uqSingleBPerturbed))
    
    uqConfig = "UQ config was [FullA=" + str(context.uqFullAPerturbed) + ", FullB=" + str(context.uqFullBPerturbed) + ", SingleA=" + str(context.uqSingleAPerturbed) + ", SingleB=" + str(context.uqSingleBPerturbed) + "]"
    if getNumQoiFiles(context) == 0:
        logger.error("No QoI files found." + uqConfig, True)

# Gets the uncertain parameters
def getUncertainParameters(context):
    return [parameter for parameter in context.parameters if parameter['uncertain']==True]

# Builds up path to qoi file
def buildQoiFilePath(context, fileName, qoiPathNumber):
    return context.qoiPath + fileName + str(qoiPathNumber).zfill(calculateFileNumberPaddingLength(context, context.dimension))

# Check if given sample matrix type uses SC method
def isUqMethodSC(context, matrixType):
    if (matrixType == "FullA" or matrixType == "SingleA") and context.uqMethodA == "sc":
        return True
    if (matrixType == "FullB" or matrixType == "SingleB") and context.uqMethodB == "sc":
        return True          
    return False      