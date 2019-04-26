import ROOT
ROOT.gSystem.Load('libCondToolsBTau')
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
import numpy as np

class BJetAnalyzer(Analyzer):
    '''Adds the is_btagged attribute to the jets of the
    given jets collection.

    Example:
       btagger = cfg.Analyzer(
          BJetAnalyzer,
          'btagger',
          jets = 'jets_20',
          tagger_name = 'DeepCSV',
          discriminator = 'pfDeepCSVDiscriminatorsJetTags:BvsAll',
          wp = 'medium',
          csv_cut = 0.4941,
          SF_file = os.path.expandvars("$CMSSW_BASE/src/CMGTools/H2TauTau/data/DeepCSV_94XSF_V3_B_F.csv"),
          method = 'promote_demote',
          efficiency_file = os.path.expandvars('src/CMGTools/H2TauTau/data/tagging_efficiencies_Moriond2017.root'),
          sys = 'central'
       )
    '''
        
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(BJetAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.randm = ROOT.TRandom3(0)
        self.mc_eff_file = ROOT.TFile(self.cfg_ana.efficiency_file)
        self.btag_eff_b = self.mc_eff_file.Get('btag_eff_b')
        self.btag_eff_c = self.mc_eff_file.Get('btag_eff_c')
        self.btag_eff_oth = self.mc_eff_file.Get('btag_eff_oth')
        self.SF_file = ROOT.BTagCalibration(self.cfg_ana.tagger_name,
                                            self.cfg_ana.SF_file)
        op_dict = {
            'loose':0,
            'medium':1,
            'tight':2
        }
        v_sys = getattr(ROOT, 'vector<string>')()
        v_sys.push_back('up')
        v_sys.push_back('down')
        self.reader_bc = ROOT.BTagCalibrationReader(op_dict[self.cfg_ana.wp], 'central', v_sys)
        self.reader_bc.load(self.SF_file, 0, 'comb')
        self.reader_bc.load(self.SF_file, 1, 'comb')
        self.reader_light = ROOT.BTagCalibrationReader(op_dict[self.cfg_ana.wp], 'central', v_sys)
        self.reader_light.load(self.SF_file, 2, 'incl')

    def process(self, event):
        jets = getattr(event, self.cfg_ana.jets)
        for jet in jets:
            jet.is_btagged = self.isBTagged(pt=jet.pt(),
                                            eta=jet.eta(),
                                            csv=jet.btag(self.cfg_ana.discriminator),
                                            jetflavor=abs(jet.hadronFlavour()),
                                            is_data=not self.cfg_comp.isMC,
                                            csv_cut=self.cfg_ana.csv_cut)

    def isBTagged(self, pt, eta, csv, jetflavor, is_data, csv_cut=0.8484):
        jetflavor = abs(jetflavor)

        if is_data or pt < 20. or abs(eta) > 2.5:
            if csv > csv_cut:
                return True
            else:
                return False


        SFb = self.getPOGSFB(pt, abs(eta), jetflavor, self.cfg_ana.sys)
        eff_b = self.getMCBTagEff(pt, abs(eta), jetflavor)

        if self.cfg_ana.method == 'promote_demote':
            return self.promote_demote(eta, csv, csv_cut, SFb, eff_b)


    def promote_demote(self, eta, csv, csv_cut, SF, eff):

        promoteProb_btag = 0. # probability to promote to tagged
        demoteProb_btag = 0. #probability to demote from tagged

        self.randm.SetSeed((int)((np.float32(eta)+5)*100000))
        btagged = False

        if SF < 1.:
            demoteProb_btag = abs(1. - SF)
        else:
            if eff in [0.,1.]:
                promoteProb_btag = 0.
            else:
                promoteProb_btag = abs(SF - 1.)/((1./eff) - 1.)

        if csv > csv_cut:
            btagged = True
            if demoteProb_btag > 0. and self.randm.Uniform() < demoteProb_btag:
                btagged = False
        else:
            btagged = False
            if promoteProb_btag > 0. and self.randm.Uniform() < promoteProb_btag:
                btagged = True

        return btagged
                    
    def getBTVJetFlav(self, flav):
        if abs(flav) == 5:
            return 0
        elif abs(flav) == 4:
            return 1
        return 2

    def getMCBTagEff(self, pt, eta, flavor):
        hist = self.btag_eff_oth
        if flavor == 5:
            hist = self.btag_eff_b
        elif flavor == 4:
            hist = self.btag_eff_c

        binx = hist.GetXaxis().FindFixBin(pt)
        biny = hist.GetYaxis().FindFixBin(abs(eta))
        eff = hist.GetBinContent(binx, biny)
        return eff

    def getPOGSFB(self, pt, eta, flavor, sys='central'):
        if flavor in [4, 5]:
            return self.reader_bc.eval_auto_bounds(sys, self.getBTVJetFlav(flavor), eta, pt)

        return self.reader_light.eval_auto_bounds(sys, self.getBTVJetFlav(flavor), eta, pt)
