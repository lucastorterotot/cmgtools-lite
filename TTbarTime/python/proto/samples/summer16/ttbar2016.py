import os 
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

json = os.path.expandvars('$CMSSW_BASE/src/CMGTools/TTbarTime/data/2016/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt')
lumi = 35921.875594646


############################################################################
# MC
############################################################################

#signal_MC_dilep = creator.makeMCComponent("MC_a_dilep","/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM","CMS",".*root", 831.76);
#
#signal_MC_dilep2 = creator.makeMCComponent("MC_a_dilep2","/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_backup_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM","CMS",".*root", 831.76);
#
##signal_MC_semilep = creator.makeMCComponent("MC_b_semilep","/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM","CMS",".*root", 365.3);
#
##background_MC_TTW = creator.makeMCComponent("MC_c_TTW","/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM", "CMS", ".*root",0.2043);
##background_MC_TTZ = creator.makeMCComponent("MC_d_TTZ","/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM", "CMS", ".*root",0.2529);
#
##background_MC_ST_s = creator.makeMCComponent("MC_e_ST_s","/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root",3.36);
##background_MC_ST_t_top = creator.makeMCComponent("MC_f_ST_t_top","/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM","CMS",".*root",136.02);
##background_MC_ST_t_antitop = creator.makeMCComponent("MC_g_ST_t_antitop","/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM","CMS",".*root",80.95);
#background_MC_tW_top = creator.makeMCComponent("MC_h_ST_tW_top","/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM","CMS", ".*root",35.85);
#background_MC_tW_antitop = creator.makeMCComponent("MC_i_ST_tW_antitop","/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root",35.85);
#
#background_MC_WW = creator.makeMCComponent("MC_j_WW", "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 118.7)
#background_MC_WZ = creator.makeMCComponent("MC_k_WZ", "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 47.13)
#background_MC_ZZ = creator.makeMCComponent("MC_l_ZZ", "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 16.523)
#
#background_MC_WW2 = creator.makeMCComponent("MC_j_WW2", "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 118.7)
#background_MC_WZ2 = creator.makeMCComponent("MC_k_WZ2", "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 47.13)
#background_MC_ZZ2 = creator.makeMCComponent("MC_l_ZZ2", "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/MINIAODSIM", "CMS", ".*root", 16.523)
#
#
#
#background_MC_WJets = creator.makeMCComponent("MC_m_WJets", "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 61526.7)
#background_MC_WJets2 = creator.makeMCComponent("MC_m_WJets2", "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM", "CMS", ".*root", 61526.7)
#
#
#background_MC_DY_50 = creator.makeMCComponent("MC_n_DY_50", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM", "CMS", ".*root", 6025.2)
#background_MC_DY_502 = creator.makeMCComponent("MC_n_DY_502", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM", "CMS", ".*root", 6025.2)
#background_MC_DY_1050 = creator.makeMCComponent("MC_o_DY_1050", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM", "CMS", ".*root", 22635.1)
#
#




signal_MC_dilep = creator.makeMCComponent("MC_a_dilep","/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM","CMS",".*root", 72.1);
signal_MC_semilep = creator.makeMCComponent("MC_b_semilep","/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM","CMS",".*root", 300.9);

background_MC_ST_s = creator.makeMCComponent("MC_e_ST_s","/ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root",3.74);
background_MC_ST_t_top = creator.makeMCComponent("MC_f_ST_t_top","/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM","CMS",".*root",136.02);
background_MC_ST_t_antitop = creator.makeMCComponent("MC_g_ST_t_antitop","/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM","CMS",".*root",67.91);
background_MC_tW_top = creator.makeMCComponent("MC_h_ST_tW_top","/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM","CMS", ".*root",34.91);
background_MC_tW_antitop = creator.makeMCComponent("MC_i_ST_tW_antitop","/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root",34.91);

#### different tune samples
background_MC_TTW = creator.makeMCComponent("MC_c_TTW","/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",0.1829);
background_MC_TTW2 = creator.makeMCComponent("MC_c_TTW2","/TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM", "CMS", ".*root",0.1829);
background_MC_TTZ = creator.makeMCComponent("MC_d_TTZ","/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root",0.2529);
background_MC_TTZ2 = creator.makeMCComponent("MC_d_TTZ2","/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM", "CMS", ".*root",0.2529);
background_MC_TTZ3 = creator.makeMCComponent("MC_d_TTZ3","/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext3-v1/MINIAODSIM", "CMS", ".*root",0.2529);

background_MC_WW = creator.makeMCComponent("MC_j_WW", "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 63.21)
background_MC_WW2 = creator.makeMCComponent("MC_j_WW2", "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 63.21)

background_MC_WZ = creator.makeMCComponent("MC_k_WZ", "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 22.82)
background_MC_WZ2 = creator.makeMCComponent("MC_k_WZ2", "/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 22.82)

background_MC_ZZ = creator.makeMCComponent("MC_l_ZZ", "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 10.32)
background_MC_ZZ2 = creator.makeMCComponent("MC_l_ZZ2", "/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 10.32)
background_MC_WJets = creator.makeMCComponent("MC_m_WJets", "/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM", "CMS", ".*root", 60290)
background_MC_WJets2 = creator.makeMCComponent("MC_m_WJets2", "/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM", "CMS", ".*root", 60290)
background_MC_DY_50 = creator.makeMCComponent("MC_n_DY_50", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext2-v1/MINIAODSIM", "CMS", ".*root", 5670)
background_MC_DY_1050 = creator.makeMCComponent("MC_o_DY_1050", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM", "CMS", ".*root", 18590)
background_MC_DY_10502 = creator.makeMCComponent("MC_o_DY_10502", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v3/MINIAODSIM", "CMS", ".*root", 18590)
background_MC_DY_10503 = creator.makeMCComponent("MC_o_DY_10503", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3_ext1-v2/MINIAODSIM", "CMS", ".*root", 18590)
###########################

#####################################################################################
## please not the list below should correspond to exact order above, used in PU  ####
##                   TTbarTime/weights/pileup/pu_hist_gen.py                     ####
#####################################################################################
mc_ttbar = [
    signal_MC_dilep,
    signal_MC_semilep,
    background_MC_TTW,
    background_MC_TTW2,
    background_MC_TTZ,
    background_MC_TTZ2,
    background_MC_TTZ3,
    background_MC_ST_s,
    background_MC_ST_t_top,
    background_MC_ST_t_antitop,
    background_MC_tW_top,
    background_MC_tW_antitop,
    background_MC_WW, 
    background_MC_WW2, 
    background_MC_WZ,
    background_MC_WZ2,
    background_MC_ZZ,
    background_MC_ZZ2,
    background_MC_WJets,
    background_MC_WJets2,
    background_MC_DY_50,
    #background_MC_DY_502,
    background_MC_DY_1050,
    background_MC_DY_10502,
    background_MC_DY_10503
]

mc_ttbar_test = [
    signal_MC_dilep,
]

############################################################################
# DATA
############################################################################

# Run2016B 17Jul2018

SingleElectron_Run2016B_17Jul2018 = creator.makeDataComponent("SingleElectron_Run2016B_17Jul2018", "/SingleElectron/Run2016B-17Jul2018_ver2-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_17Jul2018 = creator.makeDataComponent("SingleMuon_Run2016B_17Jul2018", "/SingleMuon/Run2016B-17Jul2018_ver2-v1/MINIAOD", "CMS", ".*root", json)

DoubleEG_Run2016B_17Jul2018 = creator.makeDataComponent("DoubleEG_Run2016B_17Jul2018", "/DoubleEG/Run2016B-17Jul2018_ver2-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2016B_17Jul2018 = creator.makeDataComponent("MuonEG_Run2016B_17Jul2018", "/MuonEG/Run2016B-17Jul2018_ver2-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2016B_17Jul2018 = creator.makeDataComponent("DoubleMuon_Run2016B_17Jul2018", "/DoubleMuon/Run2016B-17Jul2018_ver2-v1/MINIAOD", "CMS", ".*root", json)

# Run2016C 17Jul2018

SingleElectron_Run2016C_17Jul2018 = creator.makeDataComponent("SingleElectron_Run2016C_17Jul2018", "/SingleElectron/Run2016C-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_17Jul2018 = creator.makeDataComponent("SingleMuon_Run2016C_17Jul2018", "/SingleMuon/Run2016C-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)

DoubleEG_Run2016C_17Jul2018 = creator.makeDataComponent("DoubleEG_Run2016C_17Jul2018", "/DoubleEG/Run2016C-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2016C_17Jul2018 = creator.makeDataComponent("MuonEG_Run2016C_17Jul2018", "/MuonEG/Run2016C-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2016C_17Jul2018 = creator.makeDataComponent("DoubleMuon_Run2016C_17Jul2018", "/DoubleMuon/Run2016C-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)

# Run2016D 17Jul2018

SingleElectron_Run2016D_17Jul2018 = creator.makeDataComponent("SingleElectron_Run2016D_17Jul2018", "/SingleElectron/Run2016D-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_17Jul2018 = creator.makeDataComponent("SingleMuon_Run2016D_17Jul2018", "/SingleMuon/Run2016D-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)

DoubleEG_Run2016D_17Jul2018 = creator.makeDataComponent("DoubleEG_Run2016D_17Jul2018", "/DoubleEG/Run2016D-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2016D_17Jul2018 = creator.makeDataComponent("MuonEG_Run2016D_17Jul2018", "/MuonEG/Run2016D-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2016D_17Jul2018 = creator.makeDataComponent("DoubleMuon_Run2016D_17Jul2018", "/DoubleMuon/Run2016D-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)

# Run2016E 17Jul2018

SingleElectron_Run2016E_17Jul2018 = creator.makeDataComponent("SingleElectron_Run2016E_17Jul2018", "/SingleElectron/Run2016E-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016E_17Jul2018 = creator.makeDataComponent("SingleMuon_Run2016E_17Jul2018", "/SingleMuon/Run2016E-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)

DoubleEG_Run2016E_17Jul2018 = creator.makeDataComponent("DoubleEG_Run2016E_17Jul2018", "/DoubleEG/Run2016E-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2016E_17Jul2018 = creator.makeDataComponent("MuonEG_Run2016E_17Jul2018", "/MuonEG/Run2016E-17Jul2018-v2/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2016E_17Jul2018 = creator.makeDataComponent("DoubleMuon_Run2016E_17Jul2018", "/DoubleMuon/Run2016E-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)

# Run2016F 17Jul2018

SingleElectron_Run2016F_17Jul2018 = creator.makeDataComponent("SingleElectron_Run2016F_17Jul2018", "/SingleElectron/Run2016F-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_17Jul2018 = creator.makeDataComponent("SingleMuon_Run2016F_17Jul2018", "/SingleMuon/Run2016F-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)

DoubleEG_Run2016F_17Jul2018 = creator.makeDataComponent("DoubleEG_Run2016F_17Jul2018", "/DoubleEG/Run2016F-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2016F_17Jul2018 = creator.makeDataComponent("MuonEG_Run2016F_17Jul2018", "/MuonEG/Run2016F-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2016F_17Jul2018 = creator.makeDataComponent("DoubleMuon_Run2016F_17Jul2018", "/DoubleMuon/Run2016F-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)



# Run2016G 17Jul2018

SingleElectron_Run2016G_17Jul2018 = creator.makeDataComponent("SingleElectron_Run2016G_17Jul2018", "/SingleElectron/Run2016G-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016G_17Jul2018 = creator.makeDataComponent("SingleMuon_Run2016G_17Jul2018", "/SingleMuon/Run2016G-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)

DoubleEG_Run2016G_17Jul2018 = creator.makeDataComponent("DoubleEG_Run2016G_17Jul2018", "/DoubleEG/Run2016G-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2016G_17Jul2018 = creator.makeDataComponent("MuonEG_Run2016G_17Jul2018", "/MuonEG/Run2016G-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2016G_17Jul2018 = creator.makeDataComponent("DoubleMuon_Run2016G_17Jul2018", "/DoubleMuon/Run2016G-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)

# Run2016H 17Jul2018 

SingleElectron_Run2016H_17Jul2018 = creator.makeDataComponent("SingleElectron_Run2016H_17Jul2018", "/SingleElectron/Run2016H-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
SingleMuon_Run2016H_17Jul2018 = creator.makeDataComponent("SingleMuon_Run2016H_17Jul2018", "/SingleMuon/Run2016H-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)

DoubleEG_Run2016H_17Jul2018 = creator.makeDataComponent("DoubleEG_Run2016H_17Jul2018", "/DoubleEG/Run2016H-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
MuonEG_Run2016H_17Jul2018 = creator.makeDataComponent("MuonEG_Run2016H_17Jul2018", "/MuonEG/Run2016H-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)
DoubleMuon_Run2016H_17Jul2018 = creator.makeDataComponent("DoubleMuon_Run2016H_17Jul2018", "/DoubleMuon/Run2016H-17Jul2018-v1/MINIAOD", "CMS", ".*root", json)


## Run2016H 17Jul2018 ver3
#
#SingleElectron_Run2016Hver3_17Jul2018 = creator.makeDataComponent("SingleElectron_Run2016Hver3_17Jul2018", "/SingleElectron/Run2016H-17Jul2018_ver3-v1/MINIAOD", "CMS", ".*root", json)
#SingleMuon_Run2016Hver3_17Jul2018 = creator.makeDataComponent("SingleMuon_Run2016Hver3_17Jul2018", "/SingleMuon/Run2016H-17Jul2018_ver3-v1/MINIAOD", "CMS", ".*root", json)
#
#DoubleEG_Run2016Hver3_17Jul2018 = creator.makeDataComponent("DoubleEG_Run2016Hver3_17Jul2018", "/DoubleEG/Run2016H-17Jul2018_ver3-v1/MINIAOD", "CMS", ".*root", json)
#MuonEG_Run2016Hver3_17Jul2018 = creator.makeDataComponent("MuonEG_Run2016Hver3_17Jul2018", "/MuonEG/Run2016H-17Jul2018_ver3-v1/MINIAOD", "CMS", ".*root", json)
#DoubleMuon_Run2016Hver3_17Jul2018 = creator.makeDataComponent("DoubleMuon_Run2016Hver3_17Jul2018", "/DoubleMuon/Run2016H-17Jul2018_ver3-v1/MINIAOD", "CMS", ".*root", json)

# les lists 
data_single_electron = [SingleElectron_Run2016B_17Jul2018, SingleElectron_Run2016C_17Jul2018, SingleElectron_Run2016D_17Jul2018, SingleElectron_Run2016E_17Jul2018, SingleElectron_Run2016F_17Jul2018,SingleElectron_Run2016G_17Jul2018, SingleElectron_Run2016H_17Jul2018]
#, SingleElectron_Run2016Hver3_17Jul2018]

data_single_muon = [SingleMuon_Run2016B_17Jul2018, SingleMuon_Run2016C_17Jul2018, SingleMuon_Run2016D_17Jul2018, SingleMuon_Run2016E_17Jul2018, SingleMuon_Run2016F_17Jul2018, SingleMuon_Run2016G_17Jul2018, SingleMuon_Run2016H_17Jul2018]#, SingleMuon_Run2016Hver3_17Jul2018]

data_muon_electron = [MuonEG_Run2016B_17Jul2018, MuonEG_Run2016C_17Jul2018, MuonEG_Run2016D_17Jul2018, MuonEG_Run2016E_17Jul2018, MuonEG_Run2016F_17Jul2018,MuonEG_Run2016G_17Jul2018, MuonEG_Run2016H_17Jul2018]#, MuonEG_Run2016Hver3_17Jul2018]

data_dimuon = [DoubleMuon_Run2016B_17Jul2018, DoubleMuon_Run2016C_17Jul2018, DoubleMuon_Run2016D_17Jul2018, DoubleMuon_Run2016E_17Jul2018, DoubleMuon_Run2016F_17Jul2018,DoubleMuon_Run2016G_17Jul2018, DoubleMuon_Run2016H_17Jul2018]#, DoubleMuon_Run2016Hver3_17Jul2018]

data_dielectron = [DoubleEG_Run2016B_17Jul2018, DoubleEG_Run2016C_17Jul2018, DoubleEG_Run2016D_17Jul2018, DoubleEG_Run2016E_17Jul2018, DoubleEG_Run2016F_17Jul2018,DoubleEG_Run2016G_17Jul2018, DoubleEG_Run2016H_17Jul2018]#, DoubleEG_Run2016Hver3_17Jul2018]

data_elecmuon = data_single_electron + data_single_muon + data_muon_electron
data_ttbar = data_elecmuon + data_dimuon + data_dielectron


