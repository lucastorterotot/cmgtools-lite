from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Muon import Muon

class TopAnalyzer(Analyzer):

    def declareHandles(self):
        super(TopAnalyzer, self).declareHandles()

        self.handles['tops'] = AutoHandle(
            self.cfg_ana.tops,
            'std::vector<pat::Top>'
        )
        
    def process(self, event):
        self.readCollections(event.input)
        tops = self.handles['tops'].product()
        output_tops = []
        for top in tops:
            hmu = Top(top)
            hmu.associatedVertex = event.vertices[0]
            output_tops.append(hmu)
        setattr(event, self.cfg_ana.output, output_tops)
        
