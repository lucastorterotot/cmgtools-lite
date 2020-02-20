import sys,os
from ROOT import TFile, TH1D, TTree

dir_input  = "./files/"
dir_output = "./"

file_names = os.listdir(dir_input)
file_names.sort()
print file_names

name_list = [
    "#TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2#MINIAODSIM",
    "#TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM",
    "#TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM",
    "#TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM",
    "#ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1#MINIAODSIM",
    "#ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1#MINIAODSIM",
    "#ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM",
    "#ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1#MINIAODSIM",
    "#ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM",
    "#WW_TuneCP5_13TeV-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM",
    "#WZ_TuneCP5_13TeV-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1#MINIAODSIM",
    "#ZZ_TuneCP5_13TeV-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2#MINIAODSIM",
    "#WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3#MINIAODSIM",
    "#DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1#MINIAODSIM",
    "#DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2#MINIAODSIM"
]

rootfile = TFile(dir_output+"pileup.root", "RECREATE")
pu_file = []
pu_tree = []
pu_hist = []

for i in range(len(file_names)):
    pu_file.append(TFile(dir_input+file_names[i]+"/tree.root"))
    pu_tree.append(pu_file[i].Get('events'))

rootfile = TFile(dir_output+"pileup.root", "RECREATE")
for i in range(len(file_names)):
    pu_hist.append(TH1D(name_list[i], "",200,0.,200.))
    pu_tree[i].Project(name_list[i], "pu")
    pu_hist[i].Write()



