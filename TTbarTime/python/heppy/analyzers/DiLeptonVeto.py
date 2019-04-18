from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar import deltaR

class DiLeptonVeto(Analyzer):
        
    def process(self, event):
        leptons = getattr(event, self.cfg_ana.src)
        drmin = self.cfg_ana.drmin 
        veto_passed = True
        if len(leptons) >= 2:
            positives = []
            negatives = []
            for lep in leptons:
                if lep.charge() > 0:
                    positives.append(lep)
                else:
                    negatives.append(lep)
            for pos in positives:
                for neg in negatives: 
                    dr = deltaR(pos.eta(), pos.phi(),
                                neg.eta(), neg.phi())
                    if dr > drmin:
                        veto_passed = False
                        break
        setattr(event, self.cfg_ana.output, veto_passed)
