import copy

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()
dbsInstance='phys03'

data_single_muon_B_to_G = creator.makeMCComponent(
    "data_single_muon", 
   "/SingleMuon/cbernet-MINIAOD_CL_2-3ac6ceef15bb149c4b22dc59e3cfeade/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

data_single_muon = [data_single_muon_B_to_G]


data_single_electron = [] #[SingleElectron_Run2016B_23Sep2016, SingleElectron_Run2016C_23Sep2016, SingleElectron_Run2016D_23Sep2016, SingleElectron_Run2016E_23Sep2016, SingleElectron_Run2016F_23Sep2016, SingleElectron_Run2016G_23Sep2016]


data_muon_electron = [] #[MuonEG_Run2016B_23Sep2016, MuonEG_Run2016C_23Sep2016, MuonEG_Run2016D_23Sep2016, MuonEG_Run2016E_23Sep2016, MuonEG_Run2016F_23Sep2016, MuonEG_Run2016G_23Sep2016]


data_tau = [] #[Tau_Run2016B_03Feb2017_v2, Tau_Run2016C_03Feb2017, Tau_Run2016D_03Feb2017, Tau_Run2016E_03Feb2017, Tau_Run2016F_03Feb2017, Tau_Run2016G_03Feb2017, Tau_Run2016H_03Feb2017_v2, Tau_Run2016H_03Feb2017_v3]
