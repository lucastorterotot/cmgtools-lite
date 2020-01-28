import os
import ROOT
from ROOT import TFile, TH2F

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

def pt_binned(pt_param):
    if(20 <= pt_param and pt_param < 40):
        return 1
    elif(40 <= pt_param and pt_param < 60):
        return 2         
    elif(60 <= pt_param and pt_param < 80):
        return 3
    elif(80 <= pt_param and pt_param < 100):
        return 4 
    elif(100 <= pt_param and pt_param < 150):
        return 5 
    elif(150 <= pt_param and pt_param <= 200):
        return 6   


class DilepTriggerSFARC(Analyzer):
    
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(DilepTriggerSFARC, self).__init__(cfg_ana, cfg_comp, looperName)
        
        rootfname_ee = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/TriggerSF_ee2017_pt.root'])                       
        rootfname_em = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/TriggerSF_emu2017_pt.root'])
        rootfname_mm = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/TriggerSF_mumu2017_pt.root'])
        
        self.mc_sf_ee_trig_file = TFile(rootfname_ee)
        self.mc_sf_em_trig_file = TFile(rootfname_em)
        self.mc_sf_mm_trig_file = TFile(rootfname_mm)
                        
        self.mc_sf_ee_trig_hist = self.mc_sf_ee_trig_file.Get('h_lep1Pt_lep2Pt_Step6')                              
        self.mc_sf_em_trig_hist = self.mc_sf_em_trig_file.Get('h_lep1Pt_lep2Pt_Step3')                              
        self.mc_sf_mm_trig_hist = self.mc_sf_mm_trig_file.Get('h_lep1Pt_lep2Pt_Step9')                              

                
    def process(self, event):
    
        sf_ee_trig_weight = 1.    
        sf_em_trig_weight = 1.    
        sf_mm_trig_weight = 1.    
        
        dilepton = getattr(event, self.cfg_ana.dilepton)
        for dilep in dilepton:
            if(dilep.pt_lead() <= 200 and dilep.pt_sublead() <= 200): 
                sf_ee_trig_weight *= self.mc_sf_ee_trig_hist.GetBinContent(pt_binned(dilep.pt_lead()), pt_binned(dilep.pt_sublead()))
                sf_em_trig_weight *= self.mc_sf_em_trig_hist.GetBinContent(pt_binned(dilep.pt_lead()), pt_binned(dilep.pt_sublead()))
                sf_mm_trig_weight *= self.mc_sf_mm_trig_hist.GetBinContent(pt_binned(dilep.pt_lead()), pt_binned(dilep.pt_sublead()))

#        setattr(event, 'sfEETrigWeight', sf_ee_trig_weight)
        setattr(event, 'sfEMTrigWeight', sf_em_trig_weight)
#        setattr(event, 'sfMMTrigWeight', sf_mm_trig_weight)
#        event.eventWeight *= event.sfEETrigWeight
        event.eventWeight *= event.sfEMTrigWeight
#        event.eventWeight *= event.sfMMTrigWeight
  
  
          
