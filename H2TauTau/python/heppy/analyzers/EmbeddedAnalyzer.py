from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import bestMatch

from ROOT import TFile

class EmbeddedAnalyzer(Analyzer):
    '''Applies all needed corrections and weights for embedding.
    For more information see:
    https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauTauEmbeddingSamples2017#Corrections_for_lepton_efficienc
    '''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(EmbeddedAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.wsfile = TFile('$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_v17_5.root')
        self.ws = self.wsfile.Get('w')

    def declareHandles(self):
        super(EmbeddedAnalyzer, self).declareHandles()
        self.handles['genInfo'] = AutoHandle(('generator','',''), 'GenEventInfoProduct' )
        self.handles['genParticles'] = AutoHandle('prunedGenParticles', 'std::vector<reco::GenParticle')
        
    def process(self, event):
        if not hasattr(self.cfg_comp, 'isEmbed') or not self.cfg_comp.isEmbed:
            return True
        

        self.readCollections(event.input)

        embedding_weight = self.handles['genInfo'].product().weight()
        event.weight_gen = embedding_weight
        event.eventWeight *= event.weight_gen

        event.genParticles = self.handles['genParticles'].product()
        event.gentaus_elec = [p for p in event.genParticles if abs(p.pdgId()) in [11] and p.statusFlags().isDirectPromptTauDecayProduct()]
        event.gentaus_muon = [p for p in event.genParticles if abs(p.pdgId()) in [13] and p.statusFlags().isDirectPromptTauDecayProduct()]
        event.gentaus_hadronic = [p for p in event.genParticles if abs(p.pdgId()) == 15 and p.statusFlags().isPrompt() and not any(abs(self.getFinalTau(p).daughter(i_d).pdgId()) in [11, 13] for i_d in xrange(self.getFinalTau(p).numberOfDaughters()))]

        l1_pt = event.dileptons_sorted[0].leg1().pt()
        l1_eta = event.dileptons_sorted[0].leg1().eta()
        l2_pt = event.dileptons_sorted[0].leg2().pt()
        l2_eta = event.dileptons_sorted[0].leg2().eta()

        if self.cfg_ana.channel == 'tt':
            genl1 = event.gentaus_hadronic[0]
            genl2 = event.gentaus_hadronic[1]

        if self.cfg_ana.channel == 'mt':
            genl1 = event.gentaus_muon[0]
            genl2 = event.gentaus_hadronic[0]
            l1_iso = event.dileptons_sorted[0].leg1().iso_htt()

        if self.cfg_ana.channel == 'et':
            genl1 = event.gentaus_elec[0]
            genl2 = event.gentaus_hadronic[0]
            l1_iso = event.dileptons_sorted[0].leg1().iso_htt()

        l1_genpt = genl1.pt()
        l1_geneta = genl1.eta()
        l2_genpt = genl2.pt()
        l2_geneta = genl2.eta()
            
        self.ws.var('gt1_pt').setVal(l1_genpt)
        self.ws.var('gt2_pt').setVal(l2_genpt)
        self.ws.var('gt1_eta').setVal(l1_geneta)
        self.ws.var('gt2_eta').setVal(l2_geneta)
        event.weight_embed_DoubleMuonHLT_eff = self.ws.function('m_sel_trg_ratio').getVal()

        self.ws.var('gt_pt').setVal(l1_genpt)
        self.ws.var('gt_eta').setVal(l1_geneta)
        event.weight_embed_muonID_eff_l1 = self.ws.function('m_sel_idEmb_ratio').getVal()

        self.ws.var('gt_pt').setVal(l2_genpt)
        self.ws.var('gt_eta').setVal(l2_geneta)
        event.weight_embed_muonID_eff_l2 = self.ws.function('m_sel_idEmb_ratio').getVal()

        if self.cfg_ana.channel == 'tt':
            self.ws.var('t_pt').setVal(l1_pt)
            self.ws.var('t_eta').setVal(l1_eta)
            event.weight_embed_DoubleTauHLT_eff_l1 = self.ws.function('t_trg_tight_tt_data').getVal()/self.ws.function('t_trg_tight_tt_embed').getVal()
            self.ws.var('t_pt').setVal(l2_pt)
            self.ws.var('t_eta').setVal(l2_eta)
            event.weight_embed_DoubleTauHLT_eff_l2 = self.ws.function('t_trg_tight_tt_data').getVal()/self.ws.function('t_trg_tight_tt_embed').getVal()
        
        if self.cfg_ana.channel == 'mt':
            self.ws.var('t_pt').setVal(l2_pt)
            self.ws.var('m_pt').setVal(l1_pt)
            self.ws.var('m_eta').setVal(l1_eta)
            self.ws.var('m_iso').setVal(l1_iso)
            event.weight_embed_muonID_iso_sf = self.ws.function('m_iso_binned_embed_kit_ratio').getVal() # Rel. PFIsolation < 0.15
            event.weight_embed_muonID_id_sf = self.ws.function('m_id_embed_kit_ratio').getVal()
            event.weight_embed_muonID_HLT_sf = self.ws.function('m_trg24_27_embed_kit_ratio').getVal() # Mu 24 OR Mu 27 
            event.weight_embed_muonID_HLT_21_to_25_sf = self.ws.function('m_trg_MuTau_Mu20Leg_kit_ratio_embed').getVal() # IsoMu20_LooseChargedIsoPFTau27
            event.weight_embed_tauID_HLT_21_to_25_sf = self.ws.function('mt_emb_LooseChargedIsoPFTau27_kit_ratio').getVal() # IsoMu20_LooseChargedIsoPFTau27
        
        if self.cfg_ana.channel == 'et':
            self.ws.var('t_pt').setVal(l2_pt)
            self.ws.var('e_pt').setVal(l1_pt)
            self.ws.var('e_eta').setVal(l1_eta)
            self.ws.var('e_iso').setVal(l1_iso)
            event.weight_embed_eleID_iso_sf = self.ws.function('e_iso_binned_embed_kit_ratio').getVal() # Rel. PFIsolation < 0.15
            event.weight_embed_eleID_id_sf = self.ws.function('e_id90_embed_kit_ratio').getVal() # MVA ID 17 v2 wp90 
            # For endcap electrons (abs(eta_electron)>1.479) do not apply the electron triggers for embedded and scale with data efficiency instead.
            str_weight_embed_eleID_HLT_sf = 'e_trg27_trg32_trg35_embed_kit_ratio'
            if abs(l1_eta)>1.479:
                str_weight_embed_eleID_HLT_sf = 'e_trg27_trg32_trg35_kit_data'
            event.weight_embed_eleID_HLT_sf = self.ws.function(str_weight_embed_eleID_HLT_sf).getVal() # Ele 27 OR Ele 32 OR Ele35 
            event.weight_embed_eleID_HLT_lept_leg_sf = self.ws.function('e_trg_EleTau_Ele24Leg_kit_ratio_embed').getVal() # Ele24_LooseChargedIsoPFTau30 
            event.weight_embed_tauID_HLT_lept_leg_sf = self.ws.function('et_emb_LooseChargedIsoPFTau30_kit_ratio').getVal() # Ele24_LooseChargedIsoPFTau30 
            event.weight_embed_eleID_HLT_27_to_32_eff = self.ws.function('e_trg27_trg32_trg35_kit_data').getVal() # Ele 27 OR Ele 32 OR Ele35 
            event.weight_embed_eleID_HLT_24_eff = self.ws.function('e_trg_EleTau_Ele24Leg_desy_data').getVal() # Ele24_LooseChargedIsoPFTau30 

        dm_corr_dict = {0: 0.975,
                        1: 0.975*1.051,
                        10:0.975*0.975*0.975,
                        11:1.}
        
        if self.cfg_ana.channel == 'tt':
            event.weight_embed_track_l1 = dm_corr_dict[event.dileptons_sorted[0].leg1().decayMode()]
        event.weight_embed_track_l2 = dm_corr_dict[event.dileptons_sorted[0].leg2().decayMode()]


    def getFinalTau(self, tau):
        for i_d in xrange(tau.numberOfDaughters()):
            if tau.daughter(i_d).pdgId() == tau.pdgId():
                return self.getFinalTau(tau.daughter(i_d))
        return tau        
