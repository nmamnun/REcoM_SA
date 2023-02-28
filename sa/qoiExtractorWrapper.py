import env.environment as environment
import sa.saUtil as saUtil


class QoiExtractorWrapper():
    """
        Abstract class for the extraction of QoIs
        Contains several environment variables
    """

    def __init__(self, **keywordArgs):

        self.parameters = keywordArgs.get('parameters')

        self.qoiPath = environment.outPath + 'qoi/'
        self.totalIterations = keywordArgs.get("totalIterations")
        self.dimension = len(saUtil.getUncertainParameters(self))
        self.uqFullAPerturbed = keywordArgs.get("outputFullAPerturbed")
        self.uqFullBPerturbed = keywordArgs.get("outputFullBPerturbed")
        self.uqSingleAPerturbed = keywordArgs.get("outputSingleAPerturbed")
        self.uqSingleBPerturbed = keywordArgs.get("outputSingleBPerturbed")

    def extractAggregatedQoIs(self, matrixType):
        pass
