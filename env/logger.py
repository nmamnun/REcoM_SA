import importlib
import json
import traceback
import os
import env.util as util
import env.environment as environment

def log(level, msg):
    # Method may be called before environment is initialized
    # Print output nonetheless, but do not log (no output path is set)
    environmentInitialized = True
    try:
        environment.logLevel
    except AttributeError:
        environmentInitialized = False

    if not environmentInitialized or environment.logLevel <= level:
        print(msg)
        if environmentInitialized and environment.logToFile:
            prefixMsg = "[" + levelToString(level) + "]"
            if environment.logTimeStamp:
                prefixMsg += " at " + util.currTimeFormat()
            prefixMsg += ": " + msg
            util.appendFile(environment.outPath + "log", prefixMsg)

def info(msg):
    log(LogLevel.INFO, msg)

def debug(msg):
    log(LogLevel.DEBUG, msg)

def result(msg):
    log(LogLevel.RESULT, msg)

def error(msg, critical=False):
    log(LogLevel.ERROR, msg)
    if critical:
        util.trace()
        quit()

def levelToString(level):
    if level == 0:
        return "DEBUG"
    elif level == 1:
        return "INFO"
    elif level == 2:
        return "RESULT"
    elif level == 3:
        return "ERROR"  

class LogLevel():
    DEBUG = 0
    INFO = 1
    RESULT = 2
    ERROR = 3

