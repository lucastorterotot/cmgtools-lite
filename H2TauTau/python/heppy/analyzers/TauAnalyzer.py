from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Tau import Tau

class TauAnalyzer(Analyzer):

    def declareHandles(self):
        super(TauAnalyzer, self).declareHandles()

        self.handles['taus'] = AutoHandle(
            self.cfg_ana.taus,
            'std::vector<pat::Tau>'
        )
        
    def process(self, event):
        self.readCollections(event.input)
        taus = self.handles['taus'].product()
        htaus = []
        for tau in taus:
            htau = Tau(tau)
            htau.associatedVertex = event.goodVertices[0]
            htaus.append(htau)
        # self.correct_energy(taus)
        setattr(event, self.cfg_ana.output, htaus)
 
    def correct_energy(self, taus):
        pass
