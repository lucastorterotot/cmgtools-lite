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
            

class ElectronSFARC(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(ElectronSFARC, self).__init__(cfg_ana, cfg_comp, looperName)
        
        rootfname = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/2017_ElectronTight.root'])
                              
        self.mc_sfe_file = TFile(rootfname)
        self.mc_sfe_hist = self.mc_sfe_file.Get('EGamma_SF2D')
        
    
    def process(self, event):
        
        sfe_weight = 1.
        
        electrons = getattr(event, self.cfg_ana.electrons)
        for elec in electrons:
            if(elec.pt()>10 and elec.pt()<500):
                sfe_weight *= self.mc_sfe_hist.GetBinContent(eta_binned(elec.superCluster().eta()), pt_binned(elec.pt()))
        
        setattr(event, 'sfeWeight', sfe_weight)
        event.eventWeight *= event.sfeWeight
        
            
            
            
            
            
