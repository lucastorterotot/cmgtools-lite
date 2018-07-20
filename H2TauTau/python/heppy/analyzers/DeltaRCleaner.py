from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar import deltaR

class DeltaRCleaner(Analyzer):
        
    def process(self, event):
        to_clean = getattr(event, self.cfg_ana.to_clean)
        mask = getattr(event, self.cfg_ana.mask)
        clean = []
        drmax = self.cfg_ana.drmax 
        for ptc in to_clean:
            masked = False
            for mptc in mask:
                if deltaR(ptc.eta(), ptc.phi(), mptc.eta(), mptc.phi()) < drmax:
                    masked = True
                    break
            if not masked: 
                clean.append(ptc)
        setattr(event, self.cfg_ana.output, clean)

