from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Muon import Muon

class MuonAnalyzer(Analyzer):

    def declareHandles(self):
        super(MuonAnalyzer, self).declareHandles()

        self.handles['muons'] = AutoHandle(
            self.cfg_ana.muons,
            'std::vector<pat::Muon>'
        )
        
    def process(self, event):
        self.readCollections(event.input)
        muons = self.handles['muons'].product()
        muons = map(Muon, muons)
        setattr(event, self.cfg_ana.output, muons)
        
    def evaluate_tauid(self, muons):
        pass
    
