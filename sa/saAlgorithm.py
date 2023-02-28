from datetime import datetime
from shutil import copyfile
import math

import env.util as util
import env.environment as environment
import env.logger as logger
import sa.saUtil as saUtil

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats
from scipy.stats import lognorm
from scipy.stats import norm

class SensitivityAnalysis():
    """
    This top-level class handles the overall algorithm that is independent of the QoI itself:
    Aggregating the QoI and calculating statistics
    """

    def __init__(self, **keywordArgs):

        self.qoiPath = environment.outPath + 'qoi/'    

        # If '--path' argument is not given, create output path with current timestamp
        if keywordArgs.get('saInstancePath'):
            self.outPath = environment.outPath + 'sa/' + keywordArgs.get('saInstancePath') + '/'
        else:
            self.outPath = environment.outPath + 'sa/' + util.dateTimeFormat(environment.startTime) + '/'    

        self.uqAlgorithmConfig = keywordArgs.get('uqAlgorithmConfig')

        self.totalIterations = self.uqAlgorithmConfig["iterations"]
        self.uqFullAPerturbed = self.uqAlgorithmConfig["outputFullAPerturbed"]
        self.uqFullBPerturbed = self.uqAlgorithmConfig["outputFullBPerturbed"]
        self.uqSingleAPerturbed = self.uqAlgorithmConfig["outputSingleAPerturbed"]
        self.uqSingleBPerturbed = self.uqAlgorithmConfig["outputSingleBPerturbed"]
        self.uqMethodA = self.uqAlgorithmConfig["uqMethodA"]
        self.uqMethodB = self.uqAlgorithmConfig["uqMethodB"]


        self._estimatorFunctionSi = util.dynamicImport(keywordArgs.get('estimators')["estimatorFunctionSi"])
        self._estimatorFunctionSTi = util.dynamicImport(keywordArgs.get('estimators')["estimatorFunctionSTi"])
        self._estimatorFunctionVY = util.dynamicImport(keywordArgs.get('estimators')["estimatorFunctionVY"])

        self.bootstrapReplicas = keywordArgs.get('confidenceIntervalInput')["bootstrapReplicas"]
        self.subsampleFactor = keywordArgs.get('confidenceIntervalInput')["subsampleFactor"]
        self.confidenceInterval = keywordArgs.get('confidenceIntervalInput')["confidenceInterval"] 

        self.parameters = environment.parameters
        self.dimension = len(saUtil.getUncertainParameters(self))

        self.qoiTemplatesDict = keywordArgs.get('qoiExtractorTemplates')
        self.qoiInputDirectory = keywordArgs.get('qoiInputDirectory')

        logger.debug("SA algorithm initialized")

    def run(self):
        """
        Main program loop for the SA algorithm
        """
        
        if self.uqMethodA == "sc" or self.uqMethodB == "sc":
            # Weights computed during UQ have to be parsed from file
            weightsPath = environment.outPath + "weights"
            with open(weightsPath, 'r') as file:
                lines = file.readlines()
                self.weights = [float(line.strip()) for line in lines]
            logger.info("Weights parsed from " + weightsPath)

            # 'totalIterations' file contains overriden number of nodes in the sparse grid
            with open(environment.outPath + "totalIterations", "r") as f:
                val = f.read()
            logger.info("Overriding sample size with sparse grid node count (" + str(self.totalIterations) + " -> " + str(val) + ")")
            self.totalIterations = int(val)


        self.qoiExtractors = self.initQoiExtractorTemplates(self.qoiTemplatesDict)
        self.initOutput(self.qoiExtractors)

        # If qoiInputDirectory is given the QoI extraction process is skipped and data is read from files
        # residing in that directory instead
        if self.qoiInputDirectory:
            self.qoiInputDirectory = environment.outPath + self.qoiInputDirectory
            if not self.qoiInputDirectory.endswith("/"):
                self.qoiInputDirectory = self.qoiInputDirectory + "/"
            logger.info("QoI extractors overriden by input directory '" + self.qoiInputDirectory + "'")
            util.checkPathExists(self.qoiInputDirectory)


        saUtil.checkFileConfigIntegrity(self, self.qoiPath)

        for qoiExtractor in self.qoiExtractors:

            logger.info("Starting SA template '" + qoiExtractor.qoiExtractorTemplateName + "'")

            qoiFullA = None
            qoiFullB = None
            qoiSingleA = None   
            qoiSingleB = None

            if self.uqFullAPerturbed:
                # 'FullA': All uncertain parameters from matrix A are perturbed
                # Shape: (qoiDimension, sampleSize)
                qoiFullA = self.extractQoIs(qoiExtractor, 'FullA')

                # Shape: (qoiDimension)
                meansFullA = self.getMeans('FullA', qoiFullA)
                variancesFullA = self.getVariances('FullA', qoiFullA, meansFullA)
                
                self.outputResults('FullA', qoiExtractor, qoiFullA, meansFullA, variancesFullA)

            if self.uqFullBPerturbed:
                # 'FullB': All uncertain parameters from matrix B are perturbed
                # Shape: (qoiDimension, sampleSize)
                qoiFullB = self.extractQoIs(qoiExtractor, 'FullB')

                # Shape: (qoiDimension)
                meansFullB = self.getMeans('FullB', qoiFullB)
                variancesFullB = self.getVariances('FullB', qoiFullB, meansFullB)
                
                self.outputResults('FullB', qoiExtractor, qoiFullB, meansFullB, variancesFullB)

            if self.uqSingleAPerturbed: 
                # 'SingleA': Matrix A where each column is replaced with column from B
                # Shape: (numberOfUncertainties, qoiDimension, sampleSize)
                qoiSingleA = self.extractQoIs(qoiExtractor, 'SingleA')

                # Shape: (numberOfUncertainties, qoiDimension)
                meansSingleA = self.getMeans('Single', qoiSingleA)
                variancesSingleA = self.getVariances('Single', qoiSingleA, meansSingleA)

                self.outputResults('SingleA', qoiExtractor, qoiSingleA, meansSingleA, variancesSingleA)       

            if self.uqSingleBPerturbed:
                # 'SingleB': Matrix B where each column is replaced with column from A
                # Shape: (numberOfUncertainties, qoiDimension, sampleSize)
                qoiSingleB = self.extractQoIs(qoiExtractor, 'SingleB')

                # Shape: (numberOfUncertainties, qoiDimension)
                meansSingleB = self.getMeans('Single', qoiSingleB)
                variancesSingleB = self.getVariances('Single', qoiSingleB, meansSingleB)
    

                self.outputResults('SingleB', qoiExtractor, qoiSingleB, meansSingleB, variancesSingleB)   

            # Calculating sensitivities is only possible if at least one of these output options were set
            if (self.uqSingleAPerturbed or self.uqSingleBPerturbed):
                # Used as V[y], but recalculated inside estimatorfunction individually again
                varianceFullAB = self._estimatorFunctionVY(qoiFullA, qoiFullB)
                self.outputModelVariance(qoiExtractor, varianceFullAB)

                ### S_i
                sensitivities_S_i = self._estimatorFunctionSi(self, qoiFullA, qoiFullB, qoiSingleA)
                self.outputSensitivity("S_i", qoiExtractor, sensitivities_S_i)

                if self.bootstrapReplicas > 0:
                    subSensitivities_S_i = self.getSubSensitivity(self.getSensitivitySi, qoiFullA, qoiFullB, qoiSingleA)
                    self.outputSubSensitivity("S_i", qoiExtractor, subSensitivities_S_i)

                    confidenceIntervals_S_i = self.calcConfidenceIntervals(subSensitivities_S_i)
                    self.outputConfidenceIntervals("S_i", qoiExtractor, confidenceIntervals_S_i)

                ### S_Ti
                sensitivities_S_Ti = self._estimatorFunctionSTi(self, qoiFullA, qoiFullB, qoiSingleA)
                self.outputSensitivity("S_Ti", qoiExtractor, sensitivities_S_Ti)

                if self.bootstrapReplicas > 0:
                    subSensitivities_S_Ti = self.getSubSensitivity(self.getSensitivitySTi, qoiFullA, qoiFullB, qoiSingleA)
                    self.outputSubSensitivity("S_Ti", qoiExtractor, subSensitivities_S_Ti)        

                    confidenceIntervals_S_Ti = self.calcConfidenceIntervals(subSensitivities_S_Ti)
                    self.outputConfidenceIntervals("S_Ti", qoiExtractor, confidenceIntervals_S_Ti)        

        delta = (datetime.now() - environment.startTime)
        logger.result("SA Terminated at " + datetime.now().isoformat() + " after " + util.timeDeltaFormat(delta))


    # Calculates the normalized Sensitivities S_i 
    def getSensitivitySi(self, qoiFullA, qoiFullB, qoiSingleA):
        return self._estimatorFunctionSi(self, qoiFullA, qoiFullB, qoiSingleA)

    # Calculates the normalized Sensitivities S_Ti
    def getSensitivitySTi(self, qoiFullA, qoiFullB, qoiSingleA):
        return self._estimatorFunctionSTi(self, qoiFullA, qoiFullB, qoiSingleA)

    # Calculates the subsample sensitivities
    def getSubSensitivity(self, sensitivityFunction, qoiFullA, qoiFullB, qoiSingleA):
        subSensitivities = np.empty((self.bootstrapReplicas, qoiSingleA.shape[0]))
        n = len(qoiFullA)
        subSampleSize = math.floor(n * self.subsampleFactor)
        logger.info("Bootstrap CI [" + str(self.confidenceInterval) + "] with sub-samplesize " + str(subSampleSize) + " and " + str(self.bootstrapReplicas) + " replicas")

        for i in range(self.bootstrapReplicas):
            util.printProgress(i+1, self.bootstrapReplicas, "Calculating subsampled Sensitivities")
            
            rndVector = np.random.choice(n, subSampleSize, replace=False)
            newQoiFullA = qoiFullA[rndVector]
            newQoiFullB = qoiFullB[rndVector]
            newQoiSingleA = qoiSingleA[: , rndVector]

            # Compute sensitivity with same estimatorFunction as full sensitivities
            subSensitivity = sensitivityFunction(newQoiFullA, newQoiFullB, newQoiSingleA)
            
            for u in range(qoiSingleA.shape[0]):
                subSensitivities[i][u] = subSensitivity[u]

        return subSensitivities

    # Transform the calculates subsampled sensitivities to confidence intervals
    def calcConfidenceIntervals(self, subSensitivities):
        subSensitivities = np.transpose(subSensitivities)
        confidenceIntervals = []
        for u in range(self.dimension):
            data = np.sort(subSensitivities[u])
            cutCount = math.floor(((1 - self.confidenceInterval) / 2) * len(data))
            if cutCount == 0:
                logger.error("Error: cutCount==0. Please increase replica count.", True)
            data = data[cutCount:-cutCount]

            confidenceIntervals.append([min(data), max(data)])
        return confidenceIntervals


    def extractQoIs(self, qoiExtractor, matrixType):
        if self.qoiInputDirectory:
            # Parse QoIs from previous SA runs
            # Warning: Volatile and not checked for invalid input
            filePath = self.qoiInputDirectory + qoiExtractor.qoiExtractorTemplateName + "/qoi" + matrixType
            util.checkPathExists(filePath)
            qois = np.loadtxt(filePath, delimiter='\n')
            if matrixType == 'SingleA' or matrixType == 'SingleB':
                qois = np.reshape(qois, (self.dimension, -1))
            return qois
        else:
            # Extract QoIs from model output results
            aggregatedQoIs = qoiExtractor.extractAggregatedQoIs(matrixType)
            return aggregatedQoIs

    # Aggregates mean value for a list of QoIs
    # Normally, we expect 0-dimensional QoIs (=not lists)
    def getMeans(self, matrixType, qoiList):
        if matrixType == 'FullA' or matrixType == 'FullB':          
            if isinstance(qoiList[0], list):
                means = []
                numQoIs = np.shape(qoiList)[0]
                for i in range(numQoIs):                
                    mean = self.calcExpectation(qoiList[i])
                    means.append(mean)
                return means
            else:
                return self.calcExpectation(qoiList, matrixType)
        else:
            if isinstance(qoiList[0][0], list):              
                means = []
                numQoIs = np.shape(qoiList[0])[0]
                for u in range(self.dimension):
                    means_u = []
                    for q in range(numQoIs):
                        mean = self.calcExpectation(qoiList[u][q])
                        means_u.append(mean)
                    means.append(means_u)
            else:
                means_u = []
                for u in range(self.dimension):
                    mean = self.calcExpectation(qoiList[u], matrixType)       
                    means_u.append(mean)  
                return means_u

    # Aggregates variance for a list of QoIs
    # Normally, we expect 0-dimensional QoIs (=not lists)
    def getVariances(self, matrixType, qoiList, means):
        if matrixType == 'FullA' or matrixType == 'FullB':
            if isinstance(qoiList[0], list):
                numQoIs = np.shape(qoiList)[0]
                for i in range(numQoIs):     
                    variance = self.calcVariance(qoiList[i], means[i])
                    variances.append(variance)
            else:
                return self.calcVariance(qoiList, means, matrixType)                     
        else:
            if isinstance(qoiList[0][0], list):            
                variances = []            
                numQoIs = np.shape(qoiList[0])[0]
                for u in range(self.dimension):
                    variances_u = []
                    for q in range(numQoIs):
                        variance = self.calcVariance(qoiList[u][q], means[u][q])
                        variances_u.append(variance)
                    variances.append(variances_u)
                return variances
            else:
                variances_u = []
                for u in range(self.dimension):
                    variance = self.calcVariance(qoiList[u], means[u], matrixType)      
                    variances_u.append(variance)  
                return variances_u
        

    # Calculates the mean from a given set of data
    # SC mean calculation is dependent on parsed weights
    def calcExpectation(self, qoi, matrixType):
        if saUtil.isUqMethodSC(self, matrixType):
            mean = sum(qoi*self.weights)
        else:
            mean = sum(qoi) / len(qoi)
        return mean

    # Calculates the variance from a given set of data
    # SC variance calculation is dependent on parsed weights
    def calcVariance(self, qoi, mean, matrixType):
        variance = 0
        if saUtil.isUqMethodSC(self, matrixType):
            variance = sum(self.weights * qoi**2) - self.calcExpectation(qoi, matrixType)**2
        else:
            for i in range(len(qoi)):
                variance += (qoi[i] - mean)**2        
            variance = variance / (len(qoi) - 1)
        
        return variance


    # Initializes the templates for the QoI extraction
    def initQoiExtractorTemplates(self, qoiExtractorTemplates):        
        qoiExtractors = []
        for template in qoiExtractorTemplates:
            templateAndUqConfig = dict(template, **self.uqAlgorithmConfig)
            templateAndUqConfig = dict(templateAndUqConfig, **{'parameters': self.parameters})
            templateAndUqConfig = dict(templateAndUqConfig, **{'totalIterations': self.totalIterations})
            extractorWrapper = util.instantiateObject(template['qoiExtractor'],**templateAndUqConfig)
            qoiExtractors.append(extractorWrapper)
        return qoiExtractors




    #####     Output area     #####




    # Inilializes output directory and files
    def initOutput(self, qoiExtractors):
        util.makeDirs(self.outPath)
        for qoiExtractor in qoiExtractors:
            path = self.outPath + qoiExtractor.qoiExtractorTemplateName + "/"
            util.makeDirs(path)          
            self.initOutputFile(path, "sensitivities_S_i") 
            self.initOutputFile(path, "sensitivities_S_Ti")
            self.initOutputFile(path, "subSensitivities_S_i")
            self.initOutputFile(path, "subSensitivities_S_Ti")
            self.initOutputFile(path, "confidenceIntervals_S_i")
            self.initOutputFile(path, "confidenceIntervals_S_Ti")                             
        copyfile(environment.outPath + 'config.json', self.outPath + 'config.json')
        logger.debug("Initialized output directory")

    # Writes list of uncertain parameters to a file
    def initOutputFile(self, path, fileName):
        with open(path + fileName, "w") as f:
            for u in range(self.dimension):
                f.write(saUtil.getUncertainParameters(self)[u]["recomKey"] + ' ')
            f.write("\n")    


    # Handles output of means, variance, QoIs output
    def outputResults(self, matrixType, qoiExtractor, qoi, means, variances):
        logger.result("Means " + matrixType + ": " + str(means))
        logger.result("Variance " + matrixType + ": " + str(variances))   

        basePath = self.outPath + qoiExtractor.qoiExtractorTemplateName + "/"
        if matrixType == 'FullA' or matrixType == 'FullB':
            with open(basePath + "means" + str(matrixType), "w+") as f:
                f.write(str(means))
            with open(basePath + "variances" + str(matrixType), "w+") as f:
                f.write(str(variances))  
            with open(basePath + "qoi" + str(matrixType), "w+") as f:
                for i in range(len(qoi)):
                    if qoi.ndim == 1:
                        f.write(str(qoi[i]) + '\n')                
                    else:
                        for j in range(len(qoi[i])):
                            f.write(str(qoi[i][j]) + " ")
                        f.write("\n")
        elif matrixType == 'SingleA' or matrixType == 'SingleB':
            with open(basePath + "qoi" + str(matrixType), "w+") as f:
                for u in range(len(qoi)):
                    for i in range(len(qoi[u])):
                        if qoi.ndim == 2:
                            f.write(str(qoi[u][i]) + '\n')                
                        else:
                            for j in range(len(qoi[u][i])):
                                f.write(str(qoi[u][i][j]) + " ")
                            f.write("\n")
            with open(basePath + "means" + str(matrixType), "w+") as f:
                for u in range(len(means)):
                    f.write(str(means[u]) + '\n')
            with open(basePath + "variances" + str(matrixType), "w+") as f:
                for u in range(len(variances)):
                    f.write(str(variances[u]) + '\n') 
        else:
            logger.error("Unknown matrixType '" + str(matrixType) + "'")

    # Handles the output of sensitivity indices
    def outputSensitivity(self, sensType, qoiExtractor, sensitivities): 
        logger.result("Sensitivities " + sensType + ":")
        parameters = ""
        for u in range(self.dimension):
            parameters += saUtil.getUncertainParameters(self)[u]["recomKey"] + ' '
        logger.result(parameters)

        for u in range(len(sensitivities)):
            logger.result(str(sensitivities[u]) + ' ') 
        logger.result("Σ(" + sensType + "): " + str(np.sum(sensitivities)))                
        path = self.outPath + qoiExtractor.qoiExtractorTemplateName  + "/" + "sensitivities_" + str(sensType)
        with open(path, "a") as f:
            for u in range(len(sensitivities)):
                f.write(str(sensitivities[u]) + ' ')  

    # Handles the output of subsampled sensitivity indices (for confidence intervals)
    def outputSubSensitivity(self, sensType, qoiExtractor, sensitivities): 
        if not type(sensitivities) == np.ndarray:
            return

        sensitivities = np.transpose(sensitivities)   
        path = self.outPath + qoiExtractor.qoiExtractorTemplateName  + "/" + "subSensitivities_" + str(sensType)
        with open(path, "a") as f:
            for u in range(len(sensitivities)):
                line = ""
                for i in range(len(sensitivities[u])):
                    line += str(sensitivities[u][i]) + ' ' 
                f.write(line + "\n")   

    # Handles the output of confidence intervals
    def outputConfidenceIntervals(self, sensType, qoiExtractor, confidenceIntervals):
        logger.result("Confidence Intervals [" + str(self.confidenceInterval) + "] for " + sensType + ":")
        path = self.outPath + qoiExtractor.qoiExtractorTemplateName  + "/" + "confidenceIntervals_" + str(sensType)
        with open(path, "a") as f:
            for u in range(len(confidenceIntervals)):
                line = ""
                for i in range(len(confidenceIntervals[u])):
                    line += str(confidenceIntervals[u][i]) + ' ' 
                logger.result(line)
                f.write(line + "\n")   

    # Handles the output of estimated model variance V[y]
    def outputModelVariance(self, qoiExtractor, varianceFullAB):
        logger.result("Model variance V[y]: " + str(varianceFullAB))
        path = self.outPath +  qoiExtractor.qoiExtractorTemplateName  + "/" + "variancesFullAB"
        with open(path, "w+") as f:
            f.write(str(varianceFullAB) + "\n")