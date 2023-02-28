from datetime import datetime
import env.util as util

"""
Holds global variables and methods
"""

# Output directory definition
# UQ: Generate new directory based on program argument
# model/SA: 'outPath' serves as input path
def initOutPath(**keywordArgs):
    global startTime
    startTime = datetime.now()

    global outPath
    refTimestamp = keywordArgs.get('refTimestamp')
    argOutPath = keywordArgs.get('argOutPath')
    if refTimestamp:
    	# refTimestamp is the amdLineArgs input of the SA that references a specific UQ output
        outPath = './out/' + refTimestamp + '/'
        util.checkPathExists(outPath)
    elif argOutPath:
        outPath = './out/' + argOutPath + '/'
        util.makeDirs(outPath)        
    else:
        outPath = './out/' + util.dateTimeFormat(startTime) + '/'
        util.makeDirs(outPath)

def initParameters(**keywordArgs):
    # Only available in UQ scope
    global parameters
    parameters = keywordArgs.get('parameters')

# Initializes the logger module
def initLogger(**keywordArgs):
    global logLevel
    global logToFile  
    global logTimeStamp  
    loggerVal = keywordArgs.get('logger')
    argLevel = keywordArgs.get('argLevel')

    if argLevel != None:
        logLevel = argLevel
    elif loggerVal:
        logLevel = loggerVal["level"]
    else:
        logLevel = 1

    if loggerVal:
        logToFile = loggerVal["writeToFile"]
        logTimeStamp = loggerVal["timeStamp"]
    else:
        logToFile = False
        logTimeStamp = False

def isDebugMode():
	# see logger.py
	return logLevel == 0

def getUncertainParameters():
    return [parameter for parameter in parameters if parameter['uncertain'] == True]