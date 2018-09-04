from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle


class METAnalyzer(Analyzer):

    def declareHandles(self):
        super(METAnalyzer, self).declareHandles()

        self.handles['pfMET'] = AutoHandle(
            'slimmedMETs',
            'std::vector<pat::MET>'
        )

    def process(self, event):
        self.readCollections(event.input)

        event.pfmet = self.handles['pfMET'].product()[0]

	# TODO recoilcorrections
        return True
