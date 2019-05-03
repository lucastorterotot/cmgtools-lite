import math
import os
import ROOT
from ROOT import TFile

from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar import bestMatch, deltaR

from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject
from PhysicsTools.Heppy.physicsobjects.GenParticle import GenParticle
from PhysicsTools.Heppy.physicsutils.TauDecayModes import tauDecayModes

from CMGTools.H2TauTau.proto.analyzers.TauGenTreeProducer import TauGenTreeProducer    

class HTTGenAnalyzer(Analyzer):

    '''Add generator information to hard leptons.
    '''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(HTTGenAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.wsfile = TFile(self.cfg_ana.workspace_path)
        self.ws = self.wsfile.Get('w')

    def declareHandles(self):
        super(HTTGenAnalyzer, self).declareHandles()

        self.mchandles['genInfo'] = AutoHandle(('generator','',''), 'GenEventInfoProduct' )
        self.mchandles['genJets'] = AutoHandle('slimmedGenJets', 'std::vector<reco::GenJet>')
        self.mchandles['genParticles'] = AutoHandle('prunedGenParticles', 'std::vector<reco::GenParticle')

        self.handles['jets'] = AutoHandle(self.cfg_ana.jetCol, 'std::vector<pat::Jet>')

    def beginLoop(self, setup):
        super(HTTGenAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('LHEWeights')
        self.count = self.counters.counter('LHEWeights')

        for n_lhe in xrange(1, 11):
            self.count.register('Sum LHEWeight {}'.format(n_lhe))


    def process(self, event):
        event.genmet_pt = -99.
        event.genmet_eta = -99.
        event.genmet_e = -99.
        event.genmet_px = -99.
        event.genmet_py = -99.
        event.genmet_phi = -99.
        event.weight_gen = 1.

        if self.cfg_comp.isData:
            return True

        for n_lhe in xrange(1, 11):
            if hasattr(event, 'LHE_weights') and len(event.LHE_weights) > n_lhe:
                self.count.inc('Sum LHEWeight {}'.format(n_lhe), event.LHE_weights[n_lhe].wgt)

        self.readCollections(event.input)

        event.weight_gen = math.copysign(1., self.mchandles['genInfo'].product().weight())
        event.eventWeight *= math.copysign(1., event.weight_gen)

        # gen MET as sum of the neutrino 4-momenta
        neutrinos = [
            p for p in event.genParticles if abs(p.pdgId()) in (12, 14, 16) and p.status() == 1]

        genmet = ROOT.math.XYZTLorentzVectorD()
        for nu in neutrinos:
            genmet += nu.p4()

        event.genmet_pt = genmet.pt()
        event.genmet_eta = genmet.eta()
        event.genmet_e = genmet.e()
        event.genmet_px = genmet.px()
        event.genmet_py = genmet.py()
        event.genmet_phi = genmet.phi()

        if self.cfg_comp.name.find('TT') != -1 and self.cfg_comp.name.find('Higgs') == -1:
            if not hasattr(self.cfg_ana, 'top_systematic'):
                self.applyTopPtWeight(event)
            else:
                self.applyTopPtWeight(event, up_or_down = self.cfg_ana.top_systematic)

        if self.cfg_comp.name.find('DY') != -1:
            if not hasattr(self.cfg_ana, 'DY_systematic'):
                self.applyDYMassPtWeight(event)
            else:
                self.applyDYMassPtWeight(event, up_or_down = self.cfg_ana.DY_systematic)

        return True

    def applyDYMassPtWeight(self, event, up_or_down = None):
        '''
        DY pT re-weighting
        Uncertainty of 10% of the correction on the
        re-weighting applied to Z to ll events in all channels.
        '''
        if not hasattr(event, 'parentBoson'):
            event.parentBoson = HTTGenAnalyzer.getParentBoson(event)
        self.ws.var('z_gen_mass').setVal(event.parentBoson.mass())
        self.ws.var('z_gen_pt').setVal(event.parentBoson.pt())
        dy_weight = self.ws.function('zptmass_weight_nom').getVal()
        
        shift = dy_weight - 1
        if up_or_down == 'up' :
            factor = 1.1
        elif up_or_down == 'down' :
            factor = 0.9
        else :
            factor = 1.0
        dy_weight = 1 + shift * factor

        event.dy_weight = dy_weight
        event.eventWeight *= dy_weight


    @staticmethod
    def getGenTauJets(event):
        event.genTauJets = []
        event.genTauJetConstituents = []
        for gentau in event.gentaus:
            gentau = HTTGenAnalyzer.getFinalTau(gentau)

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
    def applyTopPtWeight(event, up_or_down = None):
        '''
        Top pT re-weighting
        Uncertainty between no and twice the correction on the
        re-weighting applied to tt events in all channels.
        '''
        ttbar = [p for p in event.genParticles if abs(p.pdgId()) == 6 and p.statusFlags().isLastCopy() and p.statusFlags().fromHardProcess()]

        if len(ttbar) == 2:
            top_1_pt = ttbar[0].pt()
            top_2_pt = ttbar[1].pt()

            if top_1_pt > 400:
                top_1_pt = 400.
            if top_2_pt > 400:
                top_2_pt = 400.

            topweight = math.sqrt(math.exp(0.156-0.00137*top_1_pt)*math.exp(0.156-0.00137*top_2_pt))

            event.top1_pt = top_1_pt
            event.top2_pt = top_2_pt

            shift = topweight - 1
            if up_or_down == 'up' :
                factor = 2.
            elif up_or_down == 'down' :
                factor = 0.
            else :
                factor = 1.
            topweight = 1 + shift * factor

            event.topweight = topweight
            event.eventWeight *= topweight

    @staticmethod
    def p4sum(ps):
        '''Returns four-vector sum of objects in passed list. Returns None
        if empty. Note that python sum doesn't work since p4() + 0/None fails,
        but will be possible in future python'''
        if not ps:
            return None
        p4 = ps[0].p4()
        for i in xrange(len(ps) - 1):
            p4 += ps[i + 1].p4()
        return p4


    @staticmethod
    def getParentBoson(event):
        leptons_prompt = [p for p in event.genParticles if abs(p.pdgId()) in [11, 12, 13, 14] and p.fromHardProcessFinalState()]
        taus_prompt = [p for p in event.genParticles if p.statusFlags().isDirectHardProcessTauDecayProduct()]
        all = leptons_prompt + taus_prompt
        return HTTGenAnalyzer.p4sum(all)

    @staticmethod
    def getSusySystem(event):
        initialSusyParticles = [p for p in event.genParticles if abs(p.pdgId()) in (1000024, 1000023) and p.daughter(0).pdgId() != p.pdgId()]
        if len(initialSusyParticles) != 2:
            import pdb; pdb.set_trace()
        return initialSusyParticles[0].p4() + initialSusyParticles[1].p4()

