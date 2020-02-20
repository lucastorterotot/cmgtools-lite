import os
import ROOT
import numpy as np

from ROOT import TRandom3, TFile, TH2F
ROOT.gSystem.Load('libCondToolsBTau')

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters

def isBJetSelected(jet_param):
    if jet_param.pt()>30 and abs(jet.eta())<2.4 and jet.jetID("PAG_ttbar_Loose"):
        return True
    else:
        return False 
      
def isBTagged(csv, csv_cut=0.5803): #CSVv2
#def isBTagged(csv, csv_cut=0.1522): #DeepCSV
    if csv>csv_cut:
        return True
    else:
        return False

class BJetEfficiencyCreator(Analyzer):
        
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(BJetEfficiencyCreator, self).__init__(cfg_ana, cfg_comp, looperName)
        
        self.h2_b = TH2F("h2_b","h2_b",19,20,1000,4,0,2.4)
        self.h2_c = TH2F("h2_c","h2_c",19,20,1000,4,0,2.4)
        self.h2_oth = TH2F("h2_oth","h2_oth",19,20,1000,4,0,2.4)
        
        self.btag_eff_b = TH2F("btag_eff_b","btag_eff_b",19,20,1000,4,0,2.4)
        self.btag_eff_c = TH2F("btag_eff_c","btag_eff_c",19,20,1000,4,0,2.4)
        self.btag_eff_oth = TH2F("btag_eff_oth","btag_eff_oth",19,20,1000,4,0,2.4)
        

    def process(self, event):
      '''Adds the is_btagged attribute to the jets of the
      given jets collection.
      '''
      jets = getattr(event, self.cfg_ana.jets)
      for jet in jets:    
        
          jet.is_btagged = isBTagged(csv=jet.btag("pfCombinedInclusiveSecondaryVertexV2BJetTags"),
                                       csv_cut=0.5803) #(loose wp csv2)
#                                       csv_cut=0.1522) #(loose wp deepcsv)                                    
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
          if jet.hadronFlavour() == 5:
              self.h2_b.Fill(jet.pt(), jet.eta())
              if jet.is_btagged:
                  self.btag_eff_b.Fill(jet.pt(), jet.eta())
          elif jet.hadronFlavour() == 4:
              self.h2_c.Fill(jet.pt(), jet.eta())
              if jet.is_btagged:
                  self.btag_eff_c.Fill(jet.pt(), jet.eta())
          elif jet.hadronFlavour() == 0:
              self.h2_oth.Fill(jet.pt(), jet.eta())
              if jet.is_btagged:
                  self.btag_eff_oth.Fill(jet.pt(), jet.eta())

      self.btag_eff_b.Divide(self.h2_b)
      self.btag_eff_c.Divide(self.h2_c)
      self.btag_eff_oth.Divide(self.h2_oth)

    def write(self, setup):

        super(BJetEfficiencyCreator, self).write(setup)

        self.rootfile = TFile('/'.join([self.dirName,
                                            'btag.root']), 'recreate')

        #import pdb; pdb.set_trace()
        self.btag_eff_b.Write()
        self.btag_eff_c.Write()        
        self.btag_eff_oth.Write()
        self.rootfile.Write()
        self.rootfile.Close()


