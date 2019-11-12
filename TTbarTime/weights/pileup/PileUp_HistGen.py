from ROOT import TFile, TH1D, TTree

dir_pileup_input = "weights/pileup/pileup/"
dir_pileup_output = "weights/pileup/"

pileup = []
pileup.append("#TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2#MINIAODSIM")
pileup.append("#TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM")
pileup.append("#TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM")
pileup.append("#TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM")
pileup.append("#ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1#MINIAODSIM")
pileup.append("#ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1#MINIAODSIM")
pileup.append("#ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM")
pileup.append("#ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1#MINIAODSIM")
pileup.append("#ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM")
pileup.append("#WW_TuneCP5_13TeV-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM")
pileup.append("#WZ_TuneCP5_13TeV-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1#MINIAODSIM")
pileup.append("#ZZ_TuneCP5_13TeV-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2#MINIAODSIM")
pileup.append("#WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3#MINIAODSIM")
pileup.append("#DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1#MINIAODSIM")

# histo name Signal
name_signal_1 = "#TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2#MINIAODSIM"
name_signal_2 = "#TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM"
# histo name Background
name_background_1 = "#TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM"
name_background_2 = "#TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM"
name_background_3 = "#ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1#MINIAODSIM"
name_background_4 = "#ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1#MINIAODSIM"
name_background_5 = "#ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM"
name_background_6 = "#ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1#MINIAODSIM"
name_background_7 = "#ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM"
name_background_8 = "#WW_TuneCP5_13TeV-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2#MINIAODSIM"
name_background_9 = "#WZ_TuneCP5_13TeV-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1#MINIAODSIM"
name_background_10 = "#ZZ_TuneCP5_13TeV-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2#MINIAODSIM"
name_background_11 = "#WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3#MINIAODSIM"
name_background_12 = "#DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8#RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1#MINIAODSIM"

############################# Signal 

file_sig_1 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"signal_MC_dilep/tree.root")
tree_sig_1 = file_sig_1.Get('events')

file_sig_2 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"signal_MC_semilep/tree.root")
tree_sig_2 = file_sig_2.Get('events')


outfile_sig = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_output+"pileupSignal.root","recreate")

hist_sig_1 = TH1D( name_signal_1, "",200,0.,200.)
tree_sig_1.Project( name_signal_1, "pu")
hist_sig_2 = TH1D( name_signal_2, "",200,0.,200.)
tree_sig_2.Project( name_signal_2, "pu")

outfile_sig.Write()

############################# Background


file_bkgd_1 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"background_MC_TTW/tree.root")
tree_bkgd_1 = file_bkgd_1.Get('events')

file_bkgd_2 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"background_MC_TTZ/tree.root")
tree_bkgd_2 = file_bkgd_2.Get('events')

file_bkgd_3 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"background_MC_ST_s/tree.root")
tree_bkgd_3 = file_bkgd_3.Get('events')

file_bkgd_4 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"background_MC_ST_t_top/tree.root")
tree_bkgd_4 = file_bkgd_4.Get('events')

file_bkgd_5 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"background_MC_ST_t_antitop/tree.root")
tree_bkgd_5 = file_bkgd_5.Get('events')

file_bkgd_6 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"background_MC_tW_top/tree.root")
tree_bkgd_6 = file_bkgd_6.Get('events')

file_bkgd_7 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"background_MC_tW_antitop/tree.root")
tree_bkgd_7 = file_bkgd_7.Get('events')

file_bkgd_8 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"background_MC_WW/tree.root")
tree_bkgd_8 = file_bkgd_8.Get('events')

file_bkgd_9 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"background_MC_WZ/tree.root")
tree_bkgd_9 = file_bkgd_9.Get('events')

file_bkgd_10 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"background_MC_ZZ/tree.root")
tree_bkgd_10 = file_bkgd_10.Get('events')

file_bkgd_11 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"background_MC_WJets/tree.root")
tree_bkgd_11 = file_bkgd_11.Get('events')

file_bkgd_12 = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_input+"background_MC_DY_50/tree.root")
tree_bkgd_12 = file_bkgd_12.Get('events')


outfile_bkgd = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/"+dir_pileup_output+"pileupBackground.root","recreate")

hist_bkgd_1 = TH1D( name_background_1, "",200,0.,200.)
tree_bkgd_1.Project( name_background_1, "pu")

hist_bkgd_2 = TH1D( name_background_2, "",200,0.,200.)
tree_bkgd_2.Project( name_background_2, "pu")

hist_bkgd_3 = TH1D( name_background_3, "",200,0.,200.)
tree_bkgd_3.Project( name_background_3, "pu")

hist_bkgd_4 = TH1D( name_background_4, "",200,0.,200.)
tree_bkgd_4.Project( name_background_4, "pu")

hist_bkgd_5 = TH1D( name_background_5, "",200,0.,200.)
tree_bkgd_5.Project( name_background_5, "pu")

hist_bkgd_6 = TH1D( name_background_6, "",200,0.,200.)
tree_bkgd_6.Project( name_background_6, "pu")

hist_bkgd_7 = TH1D( name_background_7 ,"",200,0.,200.)
tree_bkgd_7.Project( name_background_7 ,"pu")

hist_bkgd_8 = TH1D( name_background_8 ,"",200,0.,200.)
tree_bkgd_8.Project( name_background_8 ,"pu")

hist_bkgd_9 = TH1D( name_background_9 ,"",200,0.,200.)
tree_bkgd_9.Project( name_background_9 ,"pu")

hist_bkgd_10 = TH1D( name_background_10 ,"",200,0.,200.)
tree_bkgd_10.Project( name_background_10 ,"pu")

hist_bkgd_11 = TH1D( name_background_11 ,"",200,0.,200.)
tree_bkgd_11.Project( name_background_11 ,"pu")

hist_bkgd_12 = TH1D( name_background_12 ,"",200,0.,200.)
tree_bkgd_12.Project( name_background_12 ,"pu")

outfile_bkgd.Write()
