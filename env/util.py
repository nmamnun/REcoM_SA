import importlib
import json
import traceback
import os
import errno
from datetime import datetime
import env.logger as logger
import env.environment as environment

def printProgress(iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '#', printEnd = "\r"):
    if not environment.isDebugMode():
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        if iteration == total: 
            print()

def timeDeltaFormat(delta):
    secs = delta.seconds
    hours, rem = divmod(secs, 3600)
    minutes, seconds = divmod(rem, 60)
    return str(hours).zfill(2) + "h " + str(minutes).zfill(2) + "m " + str(seconds).zfill(2) + "s"

def dateTimeFormat(time, format=None):
    if format:
        return time.strftime(format)
    else:
        return time.strftime("%Y-%m-%d_%H-%M-%S")

def currTimeFormat():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def appendFile(file, content):
    mode = "a"
    if not os.path.isfile(file):
        mode = "w+"
    with open(file, mode) as f:
        f.write(content + "\n")

def writeFile(file, content):
    makeDirs(file)
    with open(file, "w+") as f:
        f.write(content)

def overwriteFile(file, content):
    makeDirs(file)
    with open(file, "w") as f:
        f.write(content)        

def makeDirs(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

def checkPathExists(path, msg=None):
    if not os.path.exists(os.path.dirname(path)):
        if msg==None:
            logger.error("Path '" + path + "' does not exist.", True)
        else:
            logger.error(msg, True)

def checkFileExists(filePath, msg=None):
    if not os.path.isfile(filePath):
        if msg==None:
            logger.error("File '" + filePath + "' does not exist.", True)
        else:
            logger.error(msg, True)        

def getConfig(obj, key, default, exact=False, listResult=False, dictResult=False):
    """
    Searches the value in a dict object based on a key
    - obj: dictionary object to be searched
    - key: sub-key that contains the searched value
    - default: returned if no entry was found
    - exact: Omit a depth-first search and return entry as specified by obj and key
    - listResult: boolean whether to return result as a list
    - dictResult: boolean whether to return result as a dict    
    """
    if exact:
        if key in obj:
            return obj[key]
        else:
            logger.error("Key '" + key + "' was not found in dict. Returning default value: '" + str(default) + "'")
            return default

    arr = []

    def extract(obj, arr, key):

        def containsDictObj(obj):
            for item in obj:
                if isinstance(item, dict):
                    return True
            return False

        if isinstance(obj, dict):
            #print("is dict")
            for k, v in obj.items():
                #print(k + " " + str(v))
                if isinstance(v, dict) and k == key and dictResult:
                    #print("#append3 " + str(v))
                    arr.append(v)
                if isinstance(v, (dict, list)):
                    if k == key and listResult:
                        #print("#append3 " + str(v))
                        arr.append(v)
                    else:
                        #print("#extract1 " + str(v))
                        extract(v, arr, key)
                elif k == key:
                    #print("#append1 " + str(v))
                    arr.append(v)
        elif isinstance(obj, list):
            #print("is list")
            if containsDictObj(obj):
                for item in obj:
                    #print("#extract2 " + str(item))
                    extract(item, arr, key)
            else:
                if listResult:
                    for item in obj:
                        pass#print("#append2 " + str(item))
                        #arr.append(item)

        return arr


    values = extract(obj, arr, key)
    if not values:
        logger.error("Key '" + key + "' was not found in dict. Returning default value: '" + str(default) + "'")
        return default
    #if listResult:
     #   return values
    return values[0]
    
def trace():
    """
    stacktrace for debug purposes
    """
    for line in traceback.format_stack():
        print(line.strip())

        
def jsonToRecomData(data):
    fullData = ''
    for block in data:
        blockData = ''
        for parameter in data[block]:
            blockData = blockData + parameter + "=" + str(data[block][parameter]) + "\n"
        fullData += "&" + block + "\n" + blockData + "&" + "\n"
    return fullData

def readJson(path):
    """
    Read Json from file and return as dict
    """
    with open(path) as f:
        return json.load(f)

def jsonDump(obj, indent=4):
    """
    Convert a json object to string format
    """
    return json.dumps(obj, indent=indent)


def jsonToDict(str):
    """
    Parse json object from string
    """
    return json.loads(str)

def dynamicImport(fullName):
    """
    This function returns the requested attribute of a module; it manages the necessary imports.
    The input argument is the full name as a string, e.g. 'module.package.method'.
    Alternatively, the input argument may be a list of such full names. The output will then be a list of same size containing the requested attributes in the same order.
    This only works for modern Python (at least Python > 3).
    """
    if fullName is None: #safety
        return None
    elif fullName is list or fullName is tuple:
        requested_attributes = []
        for name in fullName:
            requested_attributes.append(dynamicImport(name))
        return requested_attributes
    else:
        split_name = fullName.split('.')
        module_name = '.'.join(split_name[0:-1])
        attribute_name = split_name[-1]
        module = importlib.import_module(module_name)
        requested_attribute = getattr(module,attribute_name)
        return requested_attribute
   
def instantiateObject(fullName, **kwargs):
    """
    Get the object handle described by the path in fullName and return an instance of it by 
    passing **kwargs to its constructor
    """
    object_type = dynamicImport(fullName)
    return object_type(**kwargs)
 