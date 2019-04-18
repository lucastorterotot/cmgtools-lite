import math
import re

import ROOT

from ROOT import gSystem

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Jet import Jet

from PhysicsTools.HeppyCore.utils.deltar import cleanObjectCollection

gSystem.Load("libCMGToolsH2TauTau")

from ROOT import HTTRecoilCorrector as RC

LorentzVector = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzE4D("double"))

def get_final_ptcs(ptc):
    if ptc.numberOfDaughters() == 0 :
        return [ptc]
    else :
        final_ptcs = []
        for i_daughter in range(ptc.numberOfDaughters()):
            l = get_final_ptcs(ptc.daughter(i_daughter))
            final_ptcs += l
        return final_ptcs

class METAnalyzer(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(METAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)

        wpat = re.compile('W\d?Jet.*')
        match = wpat.match(self.cfg_comp.name)
        self.isWJets = not (match is None)

        # Apply recoil correction to signal, DY, and W+jets samples
        self.apply_recoil_correction = getattr(self.cfg_ana, 'apply_recoil_correction', False) and ('Higgs' in self.cfg_comp.name or 'DY' in self.cfg_comp.name or self.isWJets)

        if self.apply_recoil_correction:
            try:
                self.rcMET = RC(self.cfg_ana.recoil_correction_file)
            except AttributeError:
                print 'No recoil correction file provided.'

    def declareHandles(self):
        super(METAnalyzer, self).declareHandles()

        # add MVAMET handling if/when needed

        self.handles['pfMET'] = AutoHandle(
            'slimmedMETs',
            'std::vector<pat::MET>'
        )

        self.handles['photons'] = AutoHandle(
            'slimmedPhotons',
            'std::vector<pat::Photon>'
        )

        self.handles['packedPFCandidates'] = AutoHandle(
            'packedPFCandidates',
            'std::vector<pat::PackedCandidate>'
        )

        self.handles['jets'] = AutoHandle(
            'slimmedJets',
            'std::vector<pat::Jet>'
        )
        

    def getGenP4(self, event):
        leptons_prompt = [p for p in event.genParticles if abs(p.pdgId()) in [11, 12, 13, 14] and p.fromHardProcessFinalState()]
        leptons_prompt_vis = [p for p in leptons_prompt if abs(p.pdgId()) not in [12, 14]]

        taus_prompt = [p for p in event.genParticles if p.statusFlags().isDirectHardProcessTauDecayProduct()]

        taus_prompt_vis = [p for p in taus_prompt if abs(p.pdgId()) not in [12, 14, 16]]

        if 'DY' in self.cfg_comp.name or ('Higgs' in self.cfg_comp.name and 'TTH' not in self.cfg_comp.name) or 'WJ' in self.cfg_comp.name:
            if len(leptons_prompt) != 2 and len(taus_prompt) < 2:
                print 'ERROR: No 2 prompt leptons found'
                # import pdb; pdb.set_trace()

        vis = leptons_prompt_vis + taus_prompt_vis
        all = leptons_prompt + taus_prompt

        if len(vis) == 0 or len(all) == 0:
            return 0., 0., 0., 0.

        taus = []
        for t in taus_prompt:
            if t.mother().pdgId() == 15:
                taus.append(t.mother())
                break

        for t in taus_prompt:
            if t.mother().pdgId() == -15:
                taus.append(t.mother())
                break

        p4 = self.p4sum(all)
        p4_vis = self.p4sum(vis)

        event.parentBoson = p4
        event.parentBoson.detFlavour = 0

        return p4.px(), p4.py(), p4_vis.px(), p4_vis.py()

    def process(self, event):
        self.readCollections(event.input)

        met = None
        if self.cfg_ana.met == 'pfmet':
            met = self.handles['pfMET'].product()[0]
            
        # add MVAMET retrieval when needed
        # if self.cfg_ana.met == 'mvamet':
        #     met = self.handles[''].product()[0]

        setattr(event,self.cfg_ana.met, met)

        # Correct PF MET
        pfmet_px_old = event.pfmet.px()
        pfmet_py_old = event.pfmet.py()

        if hasattr(self.cfg_ana, 'runFixEE2017') and self.cfg_ana.runFixEE2017:
            rawMET = self.runFixEE2017(event)
            pfmet_px_old = rawMET.px()
            pfmet_py_old = rawMET.py()
            if event.type1METCorr :
                pfmet_px_old += event.type1METCorr[0]
                pfmet_py_old += event.type1METCorr[1]
        # JEC
        elif event.metShift :
            pfmet_px_old += event.metShift[0]
            pfmet_py_old += event.metShift[1]

        # recoil corrections
        if not self.cfg_comp.isMC:
            getattr(event, self.cfg_ana.met).setP4(LorentzVector(pfmet_px_old, pfmet_py_old, 0., math.sqrt(pfmet_px_old*pfmet_px_old + pfmet_py_old*pfmet_py_old)))
            return

        # Calculate generator four-momenta even if not applying corrections
        # to save them in final trees
        gen_z_px, gen_z_py, gen_vis_z_px, gen_vis_z_py = self.getGenP4(event)

        dil = event.dileptons_sorted[0]

        # Correct MET for tau energy scale
        for leg in [dil.leg1(), dil.leg2()]:
            if hasattr(leg,'unscaledP4') :
                scaled_diff_for_leg = (leg.unscaledP4 - leg.p4())
                pfmet_px_old += scaled_diff_for_leg.px()
                pfmet_py_old += scaled_diff_for_leg.py()
        
        if not self.apply_recoil_correction:
            return

        n_jets_30 = len(event.jets_30)
        
        if self.isWJets:
            n_jets_30 += 1

        # Correct by mean and resolution as default (otherwise use .Correct(..))
        new = self.rcMET.CorrectByMeanResolution(
        # new = self.rcMET.Correct(    
            pfmet_px_old, 
            pfmet_py_old, 
            gen_z_px,    
            gen_z_py,    
            gen_vis_z_px,    
            gen_vis_z_py,    
            n_jets_30,   
        )

        px_new, py_new = new.first, new.second

        getattr(event, self.cfg_ana.met).setP4(LorentzVector(px_new, py_new, 0., math.sqrt(px_new*px_new + py_new*py_new)))


    def runFixEE2017(self, event):
        '''Run the raw met computation including the cleaning of the noisy ECAL endcap in 2017 data and MC.
        '''
        pt_cut = 50.0
        eta_min = 2.65
        eta_max = 3.139

        # BadPFCandidateJetsEEnoiseProducer
        bad_jets = []
        good_jets = []
        jets = [Jet(jet) for jet in self.handles['jets'].product()]
        for x in jets:
            if ( x.correctedJet("Uncorrected").pt() > pt_cut or abs(x.eta()) < eta_min or abs(x.eta()) > eta_max ) :
                good_jets.append(x)
            else :
                bad_jets.append(x)

        # CandViewMerger, pfcandidateClustered
        if not hasattr(event, 'photons'): # fast construction of photons list
            event.photons = [p for p in self.handles['photons'].product()]

        pfcandidateClustered = event.electrons + event.muons \
            + event.taus  + event.photons + jets

        pfcandidateClustered_ptcs = []
        for ptc in event.electrons :
            for assPFcand in ptc.physObj.associatedPackedPFCandidates():
                pfcandidateClustered_ptcs.append(assPFcand.get())
        for ptc in event.muons + event.taus :
            for k in range(ptc.physObj.numberOfSourceCandidatePtrs()):
                pfcandidateClustered_ptcs.append(ptc.physObj.sourceCandidatePtr(k).get())
        for ptc in event.photons :
            for k in range(ptc.numberOfSourceCandidatePtrs()):
                pfcandidateClustered_ptcs.append(ptc.sourceCandidatePtr(k).get())
        for ptc in jets :
            pfcandidateClustered_ptcs += get_final_ptcs(ptc)

        # "packedPFCandidates"
        cands = [c for c in self.handles['packedPFCandidates'].product()]
        pfcandidateForUnclusteredUnc = [c for c in cands if c not in pfcandidateClustered_ptcs]
        badUnclustered = []
        for x in pfcandidateForUnclusteredUnc :
            if ( abs(x.eta()) > eta_min and abs(x.eta()) < eta_max ) :
                badUnclustered.append(x)

        superbad = [ptc for ptc in badUnclustered]
        for jet in bad_jets:
            superbad += get_final_ptcs(jet)

        pfCandidatesGoodEE2017 = [c for c in cands if c not in superbad]

        LorentzVector = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzE4D("double"))
        my_met = LorentzVector(0., 0., 0., 0.)

        # calc raw met no fix ee 2017
        for ptc in pfCandidatesGoodEE2017:
            my_met -= ptc.p4()

        return my_met
        
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
