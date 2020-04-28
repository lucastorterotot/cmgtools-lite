import os
import ROOT
from ROOT import TFile, TH2F

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer


class MuonSFARC(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(MuonSFARC, self).__init__(cfg_ana, cfg_comp, looperName)
        self.lumi_BCDEF = 19695.422958521
        self.lumi_GH    = 16226.452636126
        self.year       = self.cfg_ana.year

        if self.year == 2016 :
            rootfname_id_1 = '/'.join([os.environ["CMSSW_BASE"],
                                     'src/CMGTools/TTbarTime/data/2016/muonSF/RunBCDEF_SF_ID.root'])                       
            rootfname_iso_1 = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/2016/muonSF/RunBCDEF_SF_ISO.root'])
            rootfname_id_2 = '/'.join([os.environ["CMSSW_BASE"],
                           'src/CMGTools/TTbarTime/data/2016/muonSF/RunGH_SF_ID.root'])                       
            rootfname_iso_2 = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/2016/muonSF/RunGH_SF_ISO.root'])
                

                              
            self.mc_sfm_id_file1 = TFile(rootfname_id_1)
            self.mc_sfm_id_hist1 = self.mc_sfm_id_file1.Get('NUM_TightID_DEN_genTracks_pt_abseta')                              
                
            self.mc_sfm_iso_file1 = TFile(rootfname_iso_1)
            self.mc_sfm_iso_hist1 = self.mc_sfm_iso_file1.Get('NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta')                              

            self.mc_sfm_id_file2 = TFile(rootfname_id_2)
            self.mc_sfm_id_hist2 = self.mc_sfm_id_file2.Get('NUM_TightID_DEN_genTracks_pt_abseta')                              
                
            self.mc_sfm_iso_file2 = TFile(rootfname_iso_2)
            self.mc_sfm_iso_hist2 = self.mc_sfm_iso_file2.Get('NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta')                              
        
        else:
            rootfname_id_1 = '/'.join([os.environ["CMSSW_BASE"],
                                     'src/CMGTools/TTbarTime/data/RunBCDEF_SF_ID.root'])                       
            rootfname_iso_1 = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/RunBCDEF_SF_ISO.root'])
            self.mc_sfm_id_file1 = TFile(rootfname_id_1)
            self.mc_sfm_id_hist1 = self.mc_sfm_id_file1.Get('NUM_TightID_DEN_genTracks_pt_abseta')                              
            
            self.mc_sfm_iso_file1 = TFile(rootfname_iso_1)
            self.mc_sfm_iso_hist1 = self.mc_sfm_iso_file1.Get('NUM_TightRelIso_DEN_TightIDandIPCut_pt_abseta')                              
        
    def process(self, event):

        sfm_id_weight = 1.    
        sfm_iso_weight = 1.

        if self.year == 2016:
            sfm_id_weight1  = 1.    
            sfm_iso_weight1 = 1.
            sfm_id_weight2  = 1.    
            sfm_iso_weight2 = 1.

        muons = getattr(event, self.cfg_ana.muons)    

        for muon in muons:
            if(muon.pt() <= 120):
                if self.year == 2016:
                    sfm_id_weight1  *= self.mc_sfm_id_hist1.GetBinContent(self.mc_sfm_id_hist1.FindBin(muon.eta(), muon.pt()))
                    sfm_iso_weight1 *= self.mc_sfm_iso_hist1.GetBinContent(self.mc_sfm_iso_hist1.FindBin(muon.eta(), muon.pt()))
                    
                    sfm_id_weight2  *= self.mc_sfm_id_hist2.GetBinContent(self.mc_sfm_id_hist2.FindBin(muon.eta(), muon.pt()))
                    sfm_iso_weight2 *= self.mc_sfm_iso_hist2.GetBinContent(self.mc_sfm_iso_hist2.FindBin(muon.eta(), muon.pt()))

                    sfm_id_weight  *= (sfm_id_weight1*self.lumi_BCDEF + sfm_id_weight2*self.lumi_GH)/(self.lumi_BCDEF + self.lumi_GH)
                    sfm_iso_weight *= (sfm_iso_weight1*self.lumi_BCDEF + sfm_iso_weight2*self.lumi_GH)/(self.lumi_BCDEF + self.lumi_GH)
      
                else : 
                    sfm_id_weight  *= self.mc_sfm_id_hist1.GetBinContent(self.mc_sfm_id_hist1.FindBin(muon.eta(), muon.pt()))
                    sfm_iso_weight *= self.mc_sfm_iso_hist1.GetBinContent(self.mc_sfm_iso_hist1.FindBin(muon.eta(), muon.pt()))


        setattr(event, 'sfmIdWeight', sfm_id_weight)
        setattr(event, 'sfmIsoWeight', sfm_iso_weight)
        event.eventWeight *= event.sfmIdWeight
        event.eventWeight *= event.sfmIsoWeight
        
       
#scale factor = (L(BCDEF)*sf(BCDEF) + L(GH)*sf(GH))/(L(BCDEF)+L(GH)) 
        
        
