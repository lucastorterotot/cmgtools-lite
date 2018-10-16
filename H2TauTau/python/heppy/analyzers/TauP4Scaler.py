from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

class TauP4Scaler(Analyzer):

    def process(self, event):
        taus = getattr(event, self.cfg_ana.src)
        for tau in taus:
            self.correct_energy(tau)
 
    def correct_energy(self, tau):
        if hasattr(tau, 'gen_match') :
            if tau.gen_match == 5 :
                if tau.decayMode() == 0 : # h
                    tau.scaleEnergy(0.97)
                elif tau.decayMode() == 1 : # h p0
                    tau.scaleEnergy(0.98)
                elif tau.decayMode() == 10 : # hhh
                    tau.scaleEnergy(0.99)
                # elif tau.decayMode == 11 ? : # hhh p0
        else:
            print 'No gen match for tau lepton!'

