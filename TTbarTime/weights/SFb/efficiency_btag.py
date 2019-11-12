from ROOT import TH2F, TFile, TCanvas
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("btag", help="btag algorithm (CSVv2 or DeepCSV)", choices=("CSVv2","DeepCSV"))
args = parser.parse_args()
algo = args.btag

path = "$CMSSW_BASE/src/CMGTools/TTbarTime/weights/SFb/"

print(algo)

MC_sample = []
MC_sample.append("signal_MC_dilep")
MC_sample.append("signal_MC_semilep")
MC_sample.append("background_MC_TTW")
MC_sample.append("background_MC_TTZ")
MC_sample.append("background_MC_ST_s")
MC_sample.append("background_MC_ST_t_top")
MC_sample.append("background_MC_ST_t_antitop")
MC_sample.append("background_MC_tW_top")
MC_sample.append("background_MC_tW_antitop")
MC_sample.append("background_MC_WW")
MC_sample.append("background_MC_WZ")
MC_sample.append("background_MC_ZZ")
MC_sample.append("background_MC_WJets")
MC_sample.append("background_MC_DY_50")

btag_file = "btag.root"

rootfile = []
eff_b    = TH2F("btag_eff_b","btag_eff_b",19,20,1000,4,0,2.4)
eff_c    = TH2F("btag_eff_c","btag_eff_c",19,20,1000,4,0,2.4)
eff_oth  = TH2F("btag_eff_oth","btag_eff_oth",19,20,1000,4,0,2.4)

for i in range (len(MC_sample)):
    rootfile.append(TFile(path+algo+"/"+MC_sample[i]+"/"+btag_file))
    eff_b.Add(rootfile[i].Get("btag_eff_b"))
    eff_c.Add(rootfile[i].Get("btag_eff_c"))
    eff_oth.Add(rootfile[i].Get("btag_eff_oth"))
    
eff_b.Scale((1./len(rootfile)))
eff_c.Scale((1./len(rootfile)))
eff_oth.Scale((1./len(rootfile)))
  
newfile = TFile("btag_efficiency_"+algo+".root", "RECREATE")
eff_b.Write()
eff_c.Write()
eff_oth.Write()
rootfile[0].Get("btag_eff_c").Write("test")
newfile.Close()

print ("fini !")
