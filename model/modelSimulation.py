from datetime import datetime

import env.environment as environment
import env.util as util
import env.logger as logger
import model.modelUtil as modelUtil

class ModelSimulation():
    """
    Test Model Simulation class that produces some custom output files.
    """

    def __init__(self, **keywordArgs):
        self._simulationFunction = util.dynamicImport(keywordArgs.get('simulationFunction'))

        self.uqFullAPerturbed = keywordArgs.get("uqAlgorithmConfig")["outputFullAPerturbed"]
        self.uqFullBPerturbed = keywordArgs.get("uqAlgorithmConfig")["outputFullBPerturbed"]
        self.uqSingleAPerturbed = keywordArgs.get("uqAlgorithmConfig")["outputSingleAPerturbed"]
        self.uqSingleBPerturbed = keywordArgs.get("uqAlgorithmConfig")["outputSingleBPerturbed"]
        self.totalIterations = keywordArgs.get("uqAlgorithmConfig")["iterations"]
        self.uqMethodA = keywordArgs.get("uqAlgorithmConfig")["uqMethodA"]
        self.uqMethodB = keywordArgs.get("uqAlgorithmConfig")["uqMethodB"]

        self.qoiFileName = keywordArgs.get("qoiFileName")

        self.parameters = environment.parameters
        self.dataPath = environment.outPath + "data/data.recom-" 
        self.outputPath = environment.outPath + "qoi/"

        self.numUncertainParameters = len(modelUtil.getUncertainParameters(self.parameters))

        logger.debug("ModelSimulation initialized")
  
    def run(self):

        if self.uqMethodA == "sc" or self.uqMethodB == "sc":
            # Configured iterations in config JSON node /uq/uqAlgorithm/iterations may be incorrect
            # Overriden number of iterations has been written to file 'totalIterations' during UQ
            with open(environment.outPath + "totalIterations", "r") as f:
                val = f.read()
            logger.info("Overriding sample size with sparse grid node count (" + str(self.totalIterations) + " -> " + str(val) + ")")
            self.totalIterations = int(val)

        modelUtil.checkFileConfigIntegrity(self, self.dataPath)

        numberOfInputFiles = modelUtil.getNumQoiFiles(self)

        # Calculates how many preceding zeros we have to expect for the files
        paddingLength = modelUtil.calculateFileNumberPaddingLength(self, self.numUncertainParameters)

        for i in range(numberOfInputFiles):

            # Path to the actual data.recom file
            inputPath = self.dataPath + str(i + 1).zfill(paddingLength)
            # Parses the file contents to dict object
            inputData = modelUtil.loadRecomData(self, inputPath)
            
            # Perform model calculations
            result, equation = self._simulationFunction(self, inputData)

            if i == 0:
                # Only output simulation description (equation) once
                logger.info("Simulation function: " + equation)

            util.printProgress(i+1, numberOfInputFiles, "Model simulation " + str(i+1))
            logger.debug("Result for iteration " + str(i+1) + ": " + str(result))

            # Output result as QoI
            self.writeQoi(i, result, paddingLength)

        delta = (datetime.now() - environment.startTime)
        logger.result("Model Terminated at " + datetime.now().isoformat() + " after " + util.timeDeltaFormat(delta))

    # Write the qoi values to the corresponding output file
    def writeQoi(self, iteration, qoi, fileNumberPadding):
        # Build up directory for the output of the result
        qoiPath = self.outputPath + self.qoiFileName + str(iteration + 1).zfill(fileNumberPadding)
        # Silent overwrite of existing files
        util.overwriteFile(qoiPath, str(qoi))