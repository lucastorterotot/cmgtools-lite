from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from CMGTools.H2TauTau.heppy.utils.TauEnergyScales import TauEnergyScales
import copy

class TauP4Scaler(Analyzer):

    gen_match_dict = {6:'JetToTau',
                      5:'HadronicTau',
                      4:'TauDecayedToMuon',
                      3:'TauDecayedToEle',
                      2:'promptMuon',
                      1:'promptEle'}

    decay_modes_dict = {0: '1prong0pi0',
                        1: '1prong1pi0',
                        10:'3prong0pi0',
                        11:'3prong1pi0'}


    def process(self, event):
        if self.cfg_comp.isData:
            return True
        taus = getattr(event, self.cfg_ana.src)
        for tau in taus:
            self.correct_energy(tau)

 
    def correct_energy(self, tau):
        if hasattr(tau, 'gen_match') :
            gen_match = tau.gen_match
            decayMode = tau.decayMode()

            energy_scale = 1.
            
            if gen_match in self.gen_match_dict.keys():
                if decayMode in self.decay_modes_dict.keys():
                    energy_scale = TauEnergyScales[ self.gen_match_dict[gen_match] ][ self.decay_modes_dict[decayMode] ]
            tau.unscaledP4 = copy.copy(tau.p4())
            # call isolation before energy scale to match score derived and stored in MINIAOD/NANOAOD
            tau.tauID('byIsolationMVArun2017v2DBoldDMwLTraw2017')
            tau.tauID('byVVLooseIsolationMVArun2017v2DBoldDMwLT2017')
            tau.scaleEnergy(energy_scale)
        else:
            print 'No gen match for tau lepton!'

