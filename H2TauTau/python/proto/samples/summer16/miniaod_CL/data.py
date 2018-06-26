import copy

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()
dbsInstance='phys03'

data_single_muon_B_to_G = creator.makeMCComponent(
    "data_single_muon", 
   "/SingleMuon/cbernet-MINIAOD_CL_2-3ac6ceef15bb149c4b22dc59e3cfeade/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

data_single_muon = [data_single_muon_B_to_G]
