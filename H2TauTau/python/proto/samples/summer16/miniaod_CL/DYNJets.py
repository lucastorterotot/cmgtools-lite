import copy

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()
dbsInstance='phys03'


DY1JetsToLL = creator.makeMCComponent(
    "DY1JetsToLL_M-50", 
   "/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)


DY2JetsToLL = creator.makeMCComponent(
    "DY2JetsToLL_M-50", 
   "/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)


DY3JetsToLL = creator.makeMCComponent(
    "DY3JetsToLL_M-50", 
   "/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)


DY4JetsToLL = creator.makeMCComponent(
    "DY4JetsToLL_M-50", 
   "/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)
