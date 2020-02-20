import os
import ROOT
from ROOT import TFile, TH2F

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

def eta_binned(eta_param):
    if(0 <= eta_param and eta_param < 0.9):
        return 1
    elif(0.9 <= eta_param and eta_param < 1.2):
        return 2   
    elif(1.2 <= eta_param and eta_param < 2.1):
        return 3
    elif(2.1 <= eta_param and eta_param < 2.4):
        return 4
        
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

def pt_binned_IsoMu27(pt_param):
    if(29 <= pt_param and pt_param < 32):
        return 1       
    elif(32 <= pt_param and pt_param < 40):
        return 2
    elif(40 <= pt_param and pt_param < 50):
        return 3 
    elif(50 <= pt_param and pt_param < 60):
        return 4 
    elif(60 <= pt_param and pt_param < 120):
        return 5 
    elif(120 <= pt_param and pt_param < 200):
        return 6
    elif(200 <= pt_param and pt_param <= 1200):
        return 7 
        
def pt_binned_Mu50(pt_param):
    if(52 <= pt_param and pt_param < 55):
        return 1
    elif(55 <= pt_param and pt_param < 60):
        return 2         
    elif(60 <= pt_param and pt_param < 120):
        return 3
    elif(120 <= pt_param and pt_param < 200):
        return 4 
    elif(200 <= pt_param and pt_param <= 1200):
        return 5

class DilepTriggerSFARC(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(DilepTriggerSFARC, self).__init__(cfg_ana, cfg_comp, looperName)
        
        rootfname_ee = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/TriggerSF_ee2017_pt.root'])                       
        rootfname_em = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/TriggerSF_emu2017_pt.root'])
        rootfname_mm = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/TriggerSF_mumu2017_pt.root'])

        rootfname_muon = '/'.join([os.environ["CMSSW_BASE"],
                              'src/CMGTools/TTbarTime/data/EfficienciesAndSF_RunBtoF_Nov17Nov2017.root'])

        self.mc_sf_ee_trig_file = TFile(rootfname_ee)
        self.mc_sf_em_trig_file = TFile(rootfname_em)
        self.mc_sf_mm_trig_file = TFile(rootfname_mm)
        self.mc_sf_muon_isomu27_file = TFile(rootfname_muon)
          
        self.mc_sf_ee_trig_hist = self.mc_sf_ee_trig_file.Get('h_lep1Pt_lep2Pt_Step6')                              
        self.mc_sf_em_trig_hist = self.mc_sf_em_trig_file.Get('h_lep1Pt_lep2Pt_Step3')                              
        self.mc_sf_mm_trig_hist = self.mc_sf_mm_trig_file.Get('h_lep1Pt_lep2Pt_Step9')                              

        self.mc_sf_muon_isomu27_hist = self.mc_sf_muon_isomu27_file.Get('IsoMu27_PtEtaBins/pt_abseta_ratio')
        self.mc_sf_muon_mu50_hist    = self.mc_sf_muon_isomu27_file.Get('Mu50_PtEtaBins/pt_abseta_ratio')
                
    def process(self, event):
    
        sf_ee_trig_weight = 1.    
        sf_em_trig_weight = 1.    
        sf_mm_trig_weight = 1.    
        
        sf_muon_isomu27_weight = 1.
        sf_muon_mu50_weight    = 1.
        dilepton = getattr(event, self.cfg_ana.dilepton)
        muon = event.dileptons[0]._l1
        if(muon.pt() <= 1200):
            if(muon.pt() >= 29):
                sf_muon_isomu27_weight *= self.mc_sf_muon_isomu27_hist.GetBinContent(pt_binned_IsoMu27(muon.pt()), eta_binned(abs(muon.eta())))
            if(muon.pt() >= 52):
                sf_muon_mu50_weight    *= self.mc_sf_muon_mu50_hist.GetBinContent(pt_binned_Mu50(muon.pt()), eta_binned(abs(muon.eta())))

        for dilep in dilepton:
            if(dilep.pt_lead() <= 200 and dilep.pt_sublead() <= 200): 
                sf_ee_trig_weight *= self.mc_sf_ee_trig_hist.GetBinContent(pt_binned(dilep.pt_lead()), pt_binned(dilep.pt_sublead()))
                sf_em_trig_weight *= self.mc_sf_em_trig_hist.GetBinContent(pt_binned(dilep.pt_lead()), pt_binned(dilep.pt_sublead()))
                sf_mm_trig_weight *= self.mc_sf_mm_trig_hist.GetBinContent(pt_binned(dilep.pt_lead()), pt_binned(dilep.pt_sublead()))



#        setattr(event, 'sfEETrigWeight', sf_ee_trig_weight)
        setattr(event, 'sfEMTrigWeight', sf_em_trig_weight)
#        setattr(event, 'sfMMTrigWeight', sf_mm_trig_weight)

        setattr(event, 'sfmTrigIsoMu27Weight', sf_muon_isomu27_weight)
        setattr(event, 'sfmTrigMu50Weight', sf_muon_mu50_weight)

#        event.eventWeight *= event.sfEETrigWeight
        event.eventWeight *= event.sfEMTrigWeight
#        event.eventWeight *= event.sfMMTrigWeight
        event.eventWeight *= event.sfmTrigIsoMu27Weight
        event.eventWeight *= event.sfmTrigMu50Weight
  
          
