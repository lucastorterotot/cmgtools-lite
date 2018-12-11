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

        if self.cfg_ana.channel == 'tt':
            l1_pt = event.dileptons_sorted[0].leg1().pt()
            l1_eta = event.dileptons_sorted[0].leg1().eta()
            l2_pt = event.dileptons_sorted[0].leg2().pt()
            l2_eta = event.dileptons_sorted[0].leg2().eta()
            genl1, dR2l1 = bestMatch(event.dileptons_sorted[0].leg1(), event.gentaus_hadronic)
            genl2, dR2l2 = bestMatch(event.dileptons_sorted[0].leg2(), event.gentaus_hadronic)
            if genl1 == genl2 or dR2l1>0.04 or dR2l2>0.04:
                import pdb;pdb.set_trace()
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
            self.ws.var('t_pt').setVal(l1_pt)
            event.weight_embed_DoubleTauHLT_eff_l1 = self.ws.function('tt_emb_PFTau35OR40_tight_kit_ratio').getVal()
            self.ws.var('t_pt').setVal(l2_pt)
            event.weight_embed_DoubleTauHLT_eff_l2 = self.ws.function('tt_emb_PFTau35OR40_tight_kit_ratio').getVal()


    def getFinalTau(self, tau):
        for i_d in xrange(tau.numberOfDaughters()):
            if tau.daughter(i_d).pdgId() == tau.pdgId():
                return self.getFinalTau(tau.daughter(i_d))
        return tau        
