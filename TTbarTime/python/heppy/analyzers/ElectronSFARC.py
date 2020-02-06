import os
import ROOT
import math
from ROOT import TFile, TH2F

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

def eta_binned(eta_param):
    if  (-2.5 <= eta_param and eta_param < -2):
        return 1
    elif(-2 <= eta_param and eta_param < -1.5):
        return 2
    elif(-1.5 <= eta_param and eta_param < -1):
        return 3         
    elif(-1 <= eta_param and eta_param < -0.5):
        return 4
    elif(-0.5 <= eta_param and eta_param < 0):
        return 5 
    elif(0 <= eta_param and eta_param < 0.5):
        return 6 
    elif(0.5 <= eta_param and eta_param < 1):
        return 7     
    elif(1 <= eta_param and eta_param < 1.5):
        return 8
    elif(1.5 <= eta_param and eta_param < 2):
        return 9 
    elif(2 <= eta_param and eta_param <= 2.5):
        return 10 
       
def eta_binned_reco(eta_param):
    if  (-2.5 <= eta_param and eta_param < -2):
        return 1
    elif(-2 <= eta_param and eta_param < -1.566):
        return 2
    elif(-1.566 <= eta_param and eta_param < -1.444):
        return 3         
    elif(-1.444 <= eta_param and eta_param < -1):
        return 4
    elif(-1 <= eta_param and eta_param < -0.5):
        return 5        
    elif(-0.5 <= eta_param and eta_param < 0):
        return 6 
    elif(0 <= eta_param and eta_param < 0.5):
        return 7 
    elif(0.5 <= eta_param and eta_param < 0.1):
        return 8 
    elif(0.1 <= eta_param and eta_param < 1.444):
        return 9     
    elif(1.444 <= eta_param and eta_param < 1.566):
        return 10
    elif(1.566 <= eta_param and eta_param < 2):
        return 11 
    elif(2 <= eta_param and eta_param <= 2.5):
        return 12 

def pt_binned(pt_param):
    if  (10 <= pt_param and pt_param < 20):
        return 1
    elif(20 <= pt_param and pt_param < 35):
        return 2
    elif(35 <= pt_param and pt_param < 50):
        return 3         
    elif(50 <= pt_param and pt_param < 100):
        return 4
    elif(100 <= pt_param and pt_param < 200):
        return 5 
    elif(200 <= pt_param and pt_param <= 500):
        return 6            

def pt_binned_reco(pt_param):
    if(20 <= pt_param and pt_param < 45):
        return 1
    elif(45 <= pt_param and pt_param < 75):
        return 2         
    elif(75 <= pt_param and pt_param < 100):
        return 3
    elif(100 <= pt_param and pt_param <= 500):
        return 4  
            

class ElectronSFARC(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(ElectronSFARC, self).__init__(cfg_ana, cfg_comp, looperName)
        
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
            if(elec.pt()>10 and elec.pt()<500 and elec.superCluster().eta() >= -2.5 and elec.superCluster().eta() <= 2.5):
                sfe_id_weight *= self.mc_sfe_id_hist.GetBinContent(eta_binned(elec.superCluster().eta()), pt_binned(elec.pt()))
                if(elec.pt()>20):
                    sfe_reco_weight *= self.mc_sfe_reco_hist.GetBinContent(eta_binned_reco(elec.superCluster().eta()), pt_binned_reco(elec.pt()))
        
        setattr(event, 'sfeIdWeight', sfe_id_weight)
        setattr(event, 'sfeRecoWeight', sfe_reco_weight)
        event.eventWeight *= event.sfeIdWeight
        event.eventWeight *= event.sfeRecoWeight
        
            
            
            
            
            
