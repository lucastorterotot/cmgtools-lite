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
        if hasattr(event, 'dileptons_sorted') and event.dileptons_sorted:
            event.dileptons_sorted[0].met = event.pfmet

	# TODO recoilcorrections
        return True
