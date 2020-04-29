import os
import ROOT
from ROOT import TFile, TH2F

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer


class ElectronSFARC(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(ElectronSFARC, self).__init__(cfg_ana, cfg_comp, looperName)
        self.year       = self.cfg_ana.year

        if self.year == 2016 :
            rootfname_id = '/'.join([os.environ["CMSSW_BASE"],
                                     'src/CMGTools/TTbarTime/data/2016/eleSF/2016LegacyReReco_ElectronTight_Fall17V2.root'])
            
            rootfname_reco = '/'.join([os.environ["CMSSW_BASE"],
                                       'src/CMGTools/TTbarTime/data/2016/eleSF/EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root'])
                
        else:
            rootfname_id = '/'.join([os.environ["CMSSW_BASE"],
                                     'src/CMGTools/TTbarTime/data/2017_ElectronTight.root'])
            
            rootfname_reco = '/'.join([os.environ["CMSSW_BASE"],
                                       'src/CMGTools/TTbarTime/data/egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root'])


        self.mc_sfe_id_file = TFile(rootfname_id)
        self.mc_sfe_id_hist = self.mc_sfe_id_file.Get('EGamma_SF2D')
        
        self.mc_sfe_reco_file = TFile(rootfname_reco)
        self.mc_sfe_reco_hist = self.mc_sfe_reco_file.Get('EGamma_SF2D')
        
        
    def process(self, event):

        sfe_id_weight = 1.    
        sfe_reco_weight = 1.


        electrons = getattr(event, self.cfg_ana.electrons)    
        for elec in electrons:
            if(elec.pt()>10 and elec.pt()<500 and abs(elec.superCluster().eta()) <= 2.5):
                sfe_id_weight *= self.mc_sfe_id_hist.GetBinContent(self.mc_sfe_id_hist.FindBin(elec.superCluster().eta(), elec.pt()))
                if(elec.pt()>20):
                    sfe_reco_weight *= self.mc_sfe_reco_hist.GetBinContent(self.mc_sfe_reco_hist.FindBin(elec.superCluster().eta(), elec.pt()))

        setattr(event, 'sfeIdWeight', sfe_id_weight)
        setattr(event, 'sfeRecoWeight', sfe_reco_weight)
        event.eventWeight *= event.sfeIdWeight
        event.eventWeight *= event.sfeRecoWeight
        
       
        
        
