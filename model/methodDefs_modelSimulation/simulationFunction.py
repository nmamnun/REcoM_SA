import math

import env.util as util
import env.logger as logger

import model.modelUtil as modelUtil

import numpy as np

'''
# All functions must return a value in the form 'result, description'
'''

def squareValue(context, inputData):
    # Extract from the data.recom object only thos in the REcoM_parameters block
    inputData = inputData.get('REcoM_parameters')
    # Consider only uncertain parameters. 
    # 'inputData' is loaded from a data.recom file where one cannot distinguish certain and uncertain parameters
    uncertainKeys = [uncertainParameter for uncertainParameter in inputData if modelUtil.isUncertain(context, uncertainParameter)] 

    result = 0
    
    for i in range(len(uncertainKeys)):
        val = float(inputData.get(uncertainKeys[i]))
        if i == 0:
            result += val**2
        elif i == 1:
            result += 3*val
        elif i == 2:
            result += val**2
        else:
            result += val
        result += 2

    description = "x_0² + 3*x_1 + x_2² + x_i + 2"

    return result, description
    
def tripleValue(context, inputData):
    # Extract from the data.recom object only thos in the REcoM_parameters block
    inputData = inputData.get('REcoM_parameters')
    # Consider only uncertain parameters. 
    # 'inputData' is loaded from a data.recom file where one cannot distinguish certain and uncertain parameters
    uncertainKeys = [uncertainParameter for uncertainParameter in inputData if modelUtil.isUncertain(context, uncertainParameter)] 

    result = 0

    for i in range(len(uncertainKeys)):
        val = float(inputData.get(uncertainKeys[i]))
        if i == 0:
            result += 2*(val**2)
        elif i == 1:
            result += val**2
        elif i == 2:
            result += 99*val
        elif i == 3:
            result += val
        elif i == 4:
            result += 0                                     

    description = "2*x_0² + x_1² + 99*x_2 + x_3 + 0*x_4"

    return result, description  

def convergenceTest(context, inputData):
    # Extract from the data.recom object only thos in the REcoM_parameters block
    inputData = inputData.get('REcoM_parameters')
    # Consider only uncertain parameters. 
    # 'inputData' is loaded from a data.recom file where one cannot distinguish certain and uncertain parameters
    uncertainKeys = [uncertainParameter for uncertainParameter in inputData if modelUtil.isUncertain(context, uncertainParameter)] 

    val = float(inputData.get(uncertainKeys[0]))
    result = val**2                             

    description = "x_0²"

    return result, description  

def saModelTest(context, inputData):
    # Extract from the data.recom object only thos in the REcoM_parameters block
    inputData = inputData.get('REcoM_parameters')
    # Consider only uncertain parameters. 
    # 'inputData' is loaded from a data.recom file where one cannot distinguish certain and uncertain parameters
    uncertainKeys = [uncertainParameter for uncertainParameter in inputData if modelUtil.isUncertain(context, uncertainParameter)] 

    result = 0

    for i in range(len(uncertainKeys)):
        val = float(inputData.get(uncertainKeys[i]))
        if i == 0:
            result += 3*val
        elif i == 1:
            result += val
        elif i == 2:
            result += 0                                 

    description = "3*x_0 + x_1 + 0*x_2"

    return result, description  

def ishigami(context, inputData):
    # Extract from the data.recom object only thos in the REcoM_parameters block
    inputData = inputData.get('REcoM_parameters')
    # Consider only uncertain parameters. 
    # 'inputData' is loaded from a data.recom file where one cannot distinguish certain and uncertain parameters
    uncertainKeys = [uncertainParameter for uncertainParameter in inputData if modelUtil.isUncertain(context, uncertainParameter)] 
    x1 = float(inputData.get(uncertainKeys[0]))
    x2 = float(inputData.get(uncertainKeys[1]))
    x3 = float(inputData.get(uncertainKeys[2]))
    result = np.sin(x1) + 7 * np.sin(x2)**2 + 0.1 * (x3**4) * np.sin(x1)                            
    description = "sin(x_0) + 7 * sin(x_1)**2 + 0.1 * (x_2**4) * sin(x_0)"

    return result, description  
