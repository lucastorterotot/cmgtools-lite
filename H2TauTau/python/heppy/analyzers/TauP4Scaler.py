from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from CMGTools.H2TauTau.heppy.utils.TauEnergyScales import TauEnergyScales_dict
import copy

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

class TauP4Scaler(Analyzer):


    def process(self, event):
        if self.cfg_comp.isData and not (hasattr(self.cfg_comp, 'isEmbed') and self.cfg_comp.isEmbed) :
            return True
        taus = getattr(event, self.cfg_ana.src)
        process_type = 'MC'
        if (hasattr(self.cfg_comp, 'isEmbed') and self.cfg_comp.isEmbed):
            process_type = 'EMB'
        for tau in taus:
            self.correct_energy(tau,process_type)
 
    def correct_energy(self, tau, process_type):
        if hasattr(tau, 'gen_match') :
            gen_match = tau.gen_match
            decayMode = tau.decayMode()

            energy_scale = 1.
            
            if gen_match in gen_match_dict.keys():
                if decayMode in decay_modes_dict.keys():
                    energy_scale = TauEnergyScales_dict[process_type][ gen_match_dict[gen_match] ][ decay_modes_dict[decayMode] ]
            tau.unscaledP4 = copy.copy(tau.p4())
            tau.energyScale = energy_scale
            # call isolation before energy scale to match score derived and stored in MINIAOD/NANOAOD
            tau.tauID('byIsolationMVArun2017v2DBoldDMwLTraw2017')
            tau.tauID('byVVLooseIsolationMVArun2017v2DBoldDMwLT2017')
            tau.scaleEnergy(energy_scale)
            if hasattr(self.cfg_ana, 'systematics') and self.cfg_ana.systematics:
                self.add_up_down_TES(tau, energy_scale, process_type)
        else:
            print 'No gen match for tau lepton!'

    def add_up_down_TES(self, tau, base_energy_scale, process_type):
        tau.up_down_TES = {}
        decayMode = tau.decayMode()
        gen_match = tau.gen_match
        # as of 2017 data analysis, single systematic for l->tauh ES whether prompt or from tau decay
        if gen_match == 3:
            gen_match == 1
        if gen_match == 4:
            gen_match == 2
        gm_name = gen_match_dict[gen_match]
        # as of 2017 data analysis, single systematic for mu->tauh ES whatever decaymode is
        if gen_match == 2:
            decayMode == 0
        if decayMode not in decay_modes_dict:
            TES_up = 1.
            TES_down = 1.
            dm_name = decayMode
        else:
            dm_name = decay_modes_dict[decayMode]
            TES_up = TauEnergyScales_dict[process_type+'_up'][gm_name][dm_name]
            TES_down = TauEnergyScales_dict[process_type+'_down'][gm_name][dm_name]
        setattr(tau,'TES_{}_{}_{}'.format(gm_name,dm_name,'up'),TES_up/base_energy_scale)
        setattr(tau,'TES_{}_{}_{}'.format(gm_name,dm_name,'down'),TES_down/base_energy_scale)
