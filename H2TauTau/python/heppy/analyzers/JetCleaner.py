from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar import cleanObjectCollection

class JetCleaner(Analyzer):
        
    def process(self, event):
        if hasattr(self.cfg_ana, "dileptons"):
            dileptons = getattr(event, self.cfg_ana.dileptons)
            leptons = [dileptons[0].leg1(), dileptons[0].leg2()]
        elif hasattr(self.cfg_ana, "leptons"):
            leptons = getattr(event, self.cfg_ana.leptons)
        jets = getattr(event, self.cfg_ana.jets)
        clean_jets, dirty_jets = cleanObjectCollection(jets, masks=leptons, 
                                                       deltaRMin=self.cfg_ana.drmin) 
        setattr(event, self.cfg_ana.output, clean_jets)
