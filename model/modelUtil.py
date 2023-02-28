import math

import env.util as util
import env.logger as logger

# Parameters loaded from a data.recom are not marked as 'uncertain' -> Compare with parameter settings from the config
def isUncertain(context, inputParameter):
    uncertainParameters = getUncertainParameters(context.parameters)
    for parameter in uncertainParameters:
        if parameter.get('recomKey') == inputParameter:
            return True
    return False

# Parses the input data from the files produced in the uq algorithm
def loadRecomData(context, filePath):
    result = {}
    #read input file and strip comment lines
    f = open(filePath)
    raw = [line.strip() for line in f.readlines() if not line.startswith('#')]

    #build up dict that retains input structure
    currBlock = ''
    for line in raw:
        if line.startswith('&') and len(line) > 1:
            currBlock = line[1:]
            result[currBlock] = {}
        elif '=' in line:
            key = line.split('=')[0].strip()
            value = line.split('=')[1].strip()
            result[currBlock][key] = value
    return result

# Calculates how many preceding zeros we need
def calculateFileNumberPaddingLength(context, numUncertainParameters, numQoiFiles=None):
    numFiles = numQoiFiles if numQoiFiles != None else getNumQoiFiles(context)
    if numFiles == 0:
        return 0
    return 1 + math.floor(math.log10(numFiles))

# Calculates the number of files produced in the uq algorithm
def getNumQoiFiles(context):
    return context.totalIterations * (context.uqFullAPerturbed + context.uqFullBPerturbed + context.uqSingleAPerturbed * context.numUncertainParameters + context.uqSingleBPerturbed * context.numUncertainParameters)

# Checks whether the files in the /data directory roughly conform to the config.json settings
def checkFileConfigIntegrity(context, dataPath):
    uqConfig = "UQ config was [FullA=" + str(context.uqFullAPerturbed) + ", FullB=" + str(context.uqFullBPerturbed) + "SingleA=" + str(context.uqSingleAPerturbed) + ", SingleB=" + str(context.uqSingleBPerturbed) + "]"
    if getNumQoiFiles(context) == 0:
        logger.error("No data files found." + uqConfig, True)

    realNumQoiFiles = getNumQoiFiles(context)
    if context.numUncertainParameters == 1:    # SingleA and SingleB files are ommited in uq generation
        realNumQoiFiles = context.totalIterations
    assertMaxPath = dataPath + str(realNumQoiFiles).zfill(calculateFileNumberPaddingLength(context, context.numUncertainParameters, realNumQoiFiles))
    util.checkPathExists(assertMaxPath, "Expected " + str(realNumQoiFiles) + " data files, found less. [" + assertMaxPath + "]." + uqConfig)
    assertMaxPath = dataPath + str(realNumQoiFiles + 1).zfill(calculateFileNumberPaddingLength(context, context.numUncertainParameters, realNumQoiFiles + 1))
    util.checkPathExists(assertMaxPath, "Expected " + str(realNumQoiFiles) + " data files, found more. [" + assertMaxPath + "]." + uqConfig)

# Gets the uncertain parameters
def getUncertainParameters(parameters):
    return [parameter for parameter in parameters if parameter['uncertain'] == True]
