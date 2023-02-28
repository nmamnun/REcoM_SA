import sys
sys.dont_write_bytecode = True
import argparse

import uq
import model
import sa

import env.util as util
from env.util import getConfig
import env.environment as environment
import env.logger as logger


def getCommandLineArgs():
    parser = argparse.ArgumentParser(description='UQ algorithm')
    parser.add_argument('-m', '--message', type=str, help='Optional description')
    parser.add_argument('-p', '--path', type=str, help='Output directory')
    parser.add_argument('-l', '--level', type=int, help='Logger level')

    return parser.parse_args()

def writeOutputInfo(args):
    with open(environment.outPath + 'info', 'w') as f:
        f.write(environment.startTime.isoformat() + '\n')    
        if args.message != None:
            f.write(args.message)

def cleanup():
    """
    Clean temporary data or files
    """
    if environment.isDebugMode():
        with open('normal.txt', 'w') as f:
            f.write("")
        with open('lognormal.txt', 'w') as f:
            f.write("")        
        with open('uniform.txt', 'w') as f:
            f.write("")
        with open('mcFullA.txt', 'w') as f:
            f.write("")
        with open('mcFullB.txt', 'w') as f:
            f.write("")                        
        with open('perturbed.txt', 'w') as f:
            f.write("")        
        with open('sobol.txt', 'w') as f:
            f.write("") 

if __name__ == "__main__":

    args = getCommandLineArgs()

    #Json file containing all MC relevant settings and configurations
    config = util.readJson('resources/config.json')

    #Configurations for each parameter extracted from the top-level config
    parameterDict = getConfig(config, "parameters", [], listResult=True)

    # Initializes the logger module
    loggerSettings = getConfig(config, "logger", [], listResult=True)


    # No parameters needed as we create a fresh outputPath based on current timestamp
    environment.initOutPath(**{'argOutPath': args.path})
    
    #Initialize global environment variables
    environment.initParameters(**{'parameters': parameterDict})

    environment.initLogger(**{'logger': loggerSettings, 'argLevel': args.level})

    logger.debug("Parsed command line arguments: " + str(args))
    logger.result("UQ Start time: " + environment.startTime.isoformat())


    # Write a simple file that shows the execution timestamp and an optional description 
    writeOutputInfo(args)

    # Cleanup files where text will be appended to
    cleanup()

    #Configurations regarding the working process of the UQ algorithm
    outputVectorAPerturbedFile = getConfig(config, "outputVectorAPerturbedFile", True)
    outputVectorBPerturbedFile = getConfig(config, "outputVectorBPerturbedFile", True)
    outputFullAPerturbedFile = getConfig(config, "outputFullAPerturbedFile", True)
    outputFullBPerturbedFile = getConfig(config, "outputFullBPerturbedFile", True)
    outputSingleAPerturbedFile = getConfig(config, "outputSingleAPerturbedFile", True)
    outputSingleBPerturbedFile = getConfig(config, "outputSingleBPerturbedFile", True)
    iterations = getConfig(config, "iterations", 100)
    uqMethodA = getConfig(config, "uqMethodA", 'mc')
    uqMethodB = getConfig(config, "uqMethodB", 'mc')    
    scLevel = getConfig(config, "level", 5)

    uqAlgorithmConfig = {
                'outputVectorA': outputVectorAPerturbedFile,
                'outputVectorB': outputVectorBPerturbedFile,
                'outputFullAPerturbed': outputFullAPerturbedFile,
                'outputFullBPerturbed': outputFullBPerturbedFile,
                'outputSingleAPerturbed': outputSingleAPerturbedFile,
                'outputSingleBPerturbed': outputSingleBPerturbedFile,
                'iterations': iterations,
                'scLevel': scLevel,
                'uqMethodA': uqMethodA,
                'uqMethodB': uqMethodB}


    #Configuration for the random number generation in the sampling process
    randomGeneratorSobolSeedA = getConfig(config, "sobolSeedA", 0) 
    randomGeneratorSobolSeedB = getConfig(config, "sobolSeedB", 0)
    randomGenerators = getConfig(config, "generators", [{"mc":"random.uniform"}, {"qmc": "uq.sobolGenerator.generate_sobol"}], listResult=True)

    randomGeneratorInputDict = {
                'generators': randomGenerators,
                'sobolSeedA': randomGeneratorSobolSeedA,
                'sobolSeedB': randomGeneratorSobolSeedB,
                'uqMethodA': uqMethodA,
                'uqMethodB': uqMethodB}


    #Configuration for the transformation of random numbers onto a specified distribution in the sampling process
    transformerType = getConfig(config, "type", 'inverseTransformWrapper.InverseTransformWrapper')
    transformerOverrideDistribution = getConfig(config["uq"], "overrideParameterDistribution", False)
    transformerPdf = getConfig(config, "pdf", "normal")
    transformerPdfParameters= getConfig(config, "pdfParameters", [0, 0, 0.125], listResult=True)
    transformWrapperInputDict = {
                'overrideParameterDistribution': transformerOverrideDistribution,
                'pdf': transformerPdf,
                'pdfParameters': transformerPdfParameters}

    domainTranslationA = getConfig(config, "domainTranslationA", [0, 1], listResult=True)
    domainTranslationB = getConfig(config, "domainTranslationB", [0, 1], listResult=True)                

    #Accumulates input settings for the sample generator
    samplerInputDict = {
                'randomGenerator': 'uq.randomGeneratorWrapper.RandomGeneratorWrapper',
                'randomGeneratorInputDict':randomGeneratorInputDict,
                'transformWrapper':'uq.classDefs_transformWrapper.' + transformerType,
                'transformWrapperInputDict': transformWrapperInputDict,
                'uqMethodA': uqMethodA,
                'uqMethodB': uqMethodB,
                'domainTranslationA': domainTranslationA,
                'domainTranslationB': domainTranslationB,
                'scLevel': scLevel}

    #Used for actually applying perturbation to uncertain inputs
    perturbatorInputPath = getConfig(config, "inputPath", '../resources/data.recom')
    perturbator = getConfig(config,"perturbator", 'uq.inputPerturbator.InputPerturbator')    
    perturbatorDict = {
                'inputPath': perturbatorInputPath}




    #Accumulates all previous configurations
    uqInputDict = {
                'sampler': 'uq.sampleGenerator.SampleGenerator',
                'samplerInputDict': samplerInputDict,
                'perturbator': perturbator,
                'perturbatorDict': perturbatorDict,
                'uqAlgorithmConfig': uqAlgorithmConfig
    }

    logger.debug("Configuration parsing finished")

    # UQ algorithm
    uqAlgorithm = uq.UQAlgorithm(**uqInputDict)
    uqAlgorithm.run()       