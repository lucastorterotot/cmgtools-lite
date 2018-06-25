import copy

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()
dbsInstance='phys03'


DYJetsToLL = creator.makeMCComponent(
    "DYJetsToLL_M-50", 
   "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)
