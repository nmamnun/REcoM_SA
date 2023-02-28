import sa.qoiExtractorWrapper as qe

import env.util as util
import env.logger as logger
import sa.saUtil as saUtil

import numpy as np


class QoiExtractor(qe.QoiExtractorWrapper):
    """
        Default QoI extraction class
    """
    def __init__(self, **keywordArgs):
        super().__init__(**keywordArgs)

        self.qoiExtractorTemplateName = keywordArgs.get('qoiExtractorTemplateName')

        self.qoiFileName = keywordArgs.get('qoiFileName')
        self.qoiVariableList = keywordArgs.get('qoiVariableList')

        self._extractVariable = util.dynamicImport(keywordArgs.get('variableExtractionFunction'))
        self._qoiOperator = util.dynamicImport(keywordArgs.get('qoiOperatorFunction'))
        self._multiVariableOperator = util.dynamicImport(keywordArgs.get('multiVariableOperatorFunction'))
        self._qoiPostProcessing = util.dynamicImport(keywordArgs.get('qoiPostProcessingFunction'))

        logger.debug("QoiExtractor '" + self.qoiExtractorTemplateName + "' initialized")

    # Handles a generic call to this overriden function
    def extractAggregatedQoIs(self, matrixType):
        
        if matrixType == 'FullA' or matrixType == 'FullB':
            return self.aggregateQoI(matrixType)
        elif matrixType == 'SingleA' or matrixType == 'SingleB':
            aggregatedQoi = []
            for u in range(self.dimension):
                aggregatedQoi.append(self.aggregateQoI(matrixType, u))      
            return np.asarray(aggregatedQoi)
        else:
            logger.error("Invalid matrixType. Expected: [FullA, FullB, SingleA, SingleB]. Given: " + matrixType)

    # Applies the template pipeline for the QoI extraction
    def aggregateQoI(self, matrixType, uncertainParameter=None):
        progressPrefix = "" 
        if uncertainParameter != None:
            progressPrefix = " [" + saUtil.getUncertainParameters(self)[uncertainParameter]["recomKey"] + "]"

        qoiNums = saUtil.getFileNumbers(self, matrixType, uncertainParameter)
        qoi = []
        for i in range(len(qoiNums)):
            util.printProgress(i+1, len(qoiNums), "Extracting " + matrixType + progressPrefix)

            qoiPath = saUtil.buildQoiFilePath(self, self.qoiFileName, qoiNums[i])

            multiVariableQoi = None
            for variableName in self.qoiVariableList:         

                extractedVariable = self._extractVariable(qoiPath, variableName)
                
                qoiOperatedVariable = self._qoiOperator(extractedVariable)
                
                multiVariableQoi = self._multiVariableOperator(multiVariableQoi, qoiOperatedVariable)


            qoi.append(multiVariableQoi)

        processedQoi = self._qoiPostProcessing(self, qoi)

        return np.asarray(processedQoi)
      