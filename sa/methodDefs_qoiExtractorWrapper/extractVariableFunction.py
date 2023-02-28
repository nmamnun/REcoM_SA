import env.util as util

import MITgcmutils as gcm
import numpy as np


# Default method for .nc files
# ncFile.close()!!
def full(filePath, qoiVariable):   
    util.checkFileExists(filePath)
    ncFile = gcm.mnc_files(filePath)
    var = ncFile.variables[qoiVariable][:]
    varSqueeze = np.squeeze(var)
    val = np.transpose(varSqueeze)
    ncFile.close()
    return val  

# Default method for pure text files with single float value
def scalar(filePath, qoiVariable):
    util.checkFileExists(filePath)
    with open(filePath, 'r') as f:
        value = f.read()  
    value = float(value.strip())
    return value
