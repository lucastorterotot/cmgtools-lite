import ROOT

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import bestMatch, deltaR

from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from PhysicsTools.Heppy.physicsobjects.GenParticle import GenParticle
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes

from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer import TauGenTreeProducer

class GenMatcherAnalyzer(Analyzer):

    '''Add generator information to hard leptons.
    '''
    def declareHandles(self):
        super(GenMatcherAnalyzer, self).declareHandles()

        #self.mchandles['genInfo'] = AutoHandle(('generator','',''), 'GenEventInfoProduct' )
        self.mchandles['genJets'] = AutoHandle('slimmedGenJets', 'std::vector<reco::GenJet>')
        if hasattr(self.cfg_comp,'isEmbed') and self.cfg_comp.isEmbed:
            self.handles['genParticles'] = AutoHandle('prunedGenParticles', 'std::vector<reco::GenParticle')
        else:
            self.mchandles['genParticles'] = AutoHandle('prunedGenParticles', 'std::vector<reco::GenParticle')

        self.handles['jets'] = AutoHandle(self.cfg_ana.jetCol, 'std::vector<pat::Jet>')


    def process(self, event):
        if self.cfg_comp.isData and not (hasattr(self.cfg_comp,'isEmbed') and self.cfg_comp.isEmbed):
            return True

        self.readCollections(event.input)
        if not (hasattr(self.cfg_comp,'isEmbed') and self.cfg_comp.isEmbed):
            event.genJets = self.mchandles['genJets'].product()
        event.jets = self.handles['jets'].product()
        if hasattr(self.cfg_comp,'isEmbed') and self.cfg_comp.isEmbed:
            event.genParticles = self.handles['genParticles'].product()
        else:
            event.genParticles = self.mchandles['genParticles'].product()

        event.genleps = [p for p in event.genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isPrompt()]
        event.gentauleps = [p for p in event.genParticles if abs(p.pdgId()) in [11, 13] and p.statusFlags().isDirectPromptTauDecayProduct()]
        event.gentaus = [p for p in event.genParticles if abs(p.pdgId()) == 15 and p.statusFlags().isPrompt() and not any(abs(self.getFinalTau(p).daughter(i_d).pdgId()) in [11, 13] for i_d in xrange(self.getFinalTau(p).numberOfDaughters()))]
        self.getGenTauJets(event)
        
        ptcut = 0.
        # you can apply a pt cut on the gen leptons, electrons and muons
        # in HIG-13-004 it was 8 GeV
        if hasattr(self.cfg_ana, 'genPtCut'):
            ptcut = self.cfg_ana.genPtCut

        event.ptSelGentauleps = [lep for lep in event.gentauleps if lep.pt() > ptcut]
        event.ptSelGenleps = [lep for lep in event.genleps if lep.pt() > ptcut]
        event.ptSelGenSummary = []

        if hasattr(self.cfg_ana, 'genmatching') and self.cfg_ana.genmatching:
            leptons = self.cfg_ana.filter_func(event)
            for lepton in leptons:
                self.genMatch(event, lepton, 
                              event.ptSelGentauleps, 
                              event.ptSelGenleps, 
                              event.ptSelGenSummary)
                self.attachGenStatusFlag(lepton)
        return True        


    @staticmethod
    def attachGenStatusFlag(lepton):        
        flag = 6

        gen_p = lepton.genp if hasattr(lepton, 'genp') else None
        # Check if we matched a generator particle and it's not a gen jet
        if gen_p and not hasattr(gen_p, 'detFlavour'):
            pdg_id = abs(gen_p.pdgId())
            if pdg_id == 15:
                if gen_p.pt() > 15.:
                    flag = 5
            elif gen_p.pt() > 8.:
                if pdg_id == 11:
                    flag = 1
                elif pdg_id == 13:
                    flag = 2
                # else:
                #     print 'Matched gen p with weird pdg ID', pdg_id

                if flag in [1, 2]:
                    if gen_p.statusFlags().isDirectPromptTauDecayProduct():
                        flag += 2
                    elif not gen_p.statusFlags().isPrompt():
                        flag = 6

        lepton.gen_match = flag

    @staticmethod
    def getFinalTau(tau):
        for i_d in xrange(tau.numberOfDaughters()):
            if tau.daughter(i_d).pdgId() == tau.pdgId():
                return GenMatcherAnalyzer.getFinalTau(tau.daughter(i_d))
        return tau        

    @staticmethod
    def getGenTauJets(event):
        event.genTauJets = []
        event.genTauJetConstituents = []
        for gentau in event.gentaus:
            gentau = GenMatcherAnalyzer.getFinalTau(gentau)

            c_genjet = TauGenTreeProducer.finalDaughters(gentau)
            c_genjet = [d for d in c_genjet if abs(d.pdgId()) not in [12, 14, 16]]
            p4_genjet = sum((d.p4() for d in c_genjet if abs(d.pdgId()) not in [12, 14, 16]), ROOT.math.XYZTLorentzVectorD())

            genjet = GenParticle(gentau)
            genjet.setP4(p4_genjet)
            genjet.daughters = c_genjet
            genjet.decayMode = tauDecayModes.genDecayModeInt(c_genjet)

            if p4_genjet.pt() > 15.:
                if any(deltaR(p4_genjet, stored_genjet)<0.002 for stored_genjet in event.genTauJets):
                    continue # Remove duplicates
                event.genTauJets.append(genjet)
                event.genTauJetConstituents.append(c_genjet)

    @staticmethod
    def genMatch(event, leg, ptSelGentauleps, ptSelGenleps, ptSelGenSummary, 
                 dR=0.2, matchAll=True):

        dR2 = dR * dR

        leg.isTauHad = False
        leg.isTauLep = False
        leg.isPromptLep = False
        leg.genp = None

        best_dr2 = dR2

        # The following would work for pat::Taus, but we also want to flag a 
        # muon/electron as coming from a hadronic tau with the usual definition
        # if this happens

        # if hasattr(leg, 'genJet') and leg.genJet():
        #     if leg.genJet().pt() > 15.:
        #         dr2 = deltaR2(leg.eta(), leg.phi(), leg.genJet().eta(), leg.genJet().phi())
        #         if dr2 < best_dr2:
        #             best_dr2 = dr2
        #             leg.genp = leg.genJet()
        #             leg.genp.setPdgId(-15 * leg.genp.charge())
        #             leg.isTauHad = True
        
        # RM: needed to append genTauJets to the events,
        #     when genMatch is used as a static method
        if not hasattr(event, 'genTauJets'):
            GenMatcherAnalyzer.getGenTauJets(event)

        l1match, dR2best = bestMatch(leg, event.genTauJets)
        if dR2best < best_dr2:
            best_dr2 = dR2best
            # leg.genp = GenParticle(l1match)
            leg.genp = l1match
            leg.genp.setPdgId(-15 * leg.genp.charge())
            leg.isTauHad = True
            # if not leg.genJet():
            #     print 'Warning, tau does not have matched gen tau'
            # elif leg.genJet().pt() < 15.:
            #     print 'Warning, tau has matched gen jet but with pt =', leg.genJet().pt()

        # to generated leptons from taus
        l1match, dR2best = bestMatch(leg, ptSelGentauleps)
        if dR2best < best_dr2:
            best_dr2 = dR2best
            leg.genp = l1match
            leg.isTauLep = True
            leg.isTauHad = False

        # to generated prompt leptons
        l1match, dR2best = bestMatch(leg, ptSelGenleps)
        if dR2best < best_dr2:
            best_dr2 = dR2best
            leg.genp = l1match
            leg.isPromptLep = True
            leg.isTauLep = False
            leg.isTauHad = False

        if best_dr2 < dR2:
            return

        # match with any other relevant gen particle
        if matchAll:
            l1match, dR2best = bestMatch(leg, ptSelGenSummary)
            if dR2best < best_dr2:
                leg.genp = l1match
                return

            # Ok do one more Pythia 8 trick...
            # This is to overcome that the GenAnalyzer doesn't like particles
            # that have daughters with same pdgId and status 71
            if not hasattr(event, 'pythiaQuarksGluons'):
                event.pythiaQuarksGluons = []
                for gen in event.genParticles:
                    pdg = abs(gen.pdgId())
                    status = gen.status()
                    if pdg in [1, 2, 3, 4, 5, 21] and status > 3:
                        if gen.isMostlyLikePythia6Status3():
                            event.pythiaQuarksGluons.append(gen)

            
            l1match, dR2best = bestMatch(leg, event.pythiaQuarksGluons)
            if dR2best < best_dr2:
                leg.genp = l1match
                return

            
            # Now this may be a pileup lepton, or one whose ancestor doesn't
            # appear in the gen summary because it's an unclear case in Pythia 8
            # To check the latter, match against jets as well...
            l1match, dR2best = bestMatch(leg, getattr(event, 'genJets', []))
            # Check if there's a gen jet with pT > 10 GeV (otherwise it's PU)
            if dR2best < dR2 and l1match.pt() > 10.:
                leg.genp = PhysicsObject(l1match)

                jet, dR2best = bestMatch(l1match, getattr(event, 'jets', []))

                if dR2best < dR2:
                    leg.genp.detFlavour = jet.partonFlavour()
                # else:
                #     print 'no match found', leg.pt(), leg.eta()

