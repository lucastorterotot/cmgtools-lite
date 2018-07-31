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
        output_muons = []
        for muon in muons:
            hmu = Muon(muon)
            hmu.associatedVertex = event.vertices[0]
            output_muons.append(hmu)
        setattr(event, self.cfg_ana.output, output_muons)
        
