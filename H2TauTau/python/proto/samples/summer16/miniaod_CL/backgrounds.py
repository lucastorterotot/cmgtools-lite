import copy

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()
dbsInstance='phys03'


TT_pow = creator.makeMCComponent(
    "TT_pow", 
   "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

TTbar = [
TT_pow,
]


DYJetsToLL_M50_LO_ext = creator.makeMCComponent(
    "DYJetsToLL_M50_LO_ext", 
   "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

#DYJetsToLL_M50_LO_ext2

#DYJetsToLL_M10to50_LO

DYJets = [ 
DYJetsToLL_M50_LO_ext,
#DYJetsToLL_M50_LO_ext2,
#DYJetsToLL_M10to50_LO,
]


DY1JetsToLL_M50_LO = creator.makeMCComponent(
    "DY1JetsToLL_M_50_LO", 
   "/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

DY2JetsToLL_M50_LO = creator.makeMCComponent(
    "DY2JetsToLL_M_50_LO", 
   "/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

DY3JetsToLL_M50_LO = creator.makeMCComponent(
    "DY3JetsToLL_M_50_LO", 
   "/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

DY4JetsToLL_M50_LO = creator.makeMCComponent(
    "DY4JetsToLL_M_50_LO", 
   "/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

DYNJets = [ 
DY1JetsToLL_M50_LO,
DY2JetsToLL_M50_LO,
DY3JetsToLL_M50_LO,
DY4JetsToLL_M50_LO,
# NOTAVAILYET # DY1JetsToLL_M10to50,
# NOTAVAILYET # DY2JetsToLL_M10to50,
]


#T_tWch_ext
#TBar_tWch_ext
#TBar_tch_powheg
#T_tch_powheg


WJetsToLNu_LO = creator.makeMCComponent(
    "WJetsToLNu_LO", 
   "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/cbernet-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

# WJetsToLNu_LO_ext

WJets = [
WJetsToLNu_LO,
#WJetsToLNu_LO_ext,
]


W1JetsToLNu_LO = creator.makeMCComponent(
    "W1JetsToLNu_LO", 
   "/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ltortero-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

W2JetsToLNu_LO_all = creator.makeMCComponent(
    "W2JetsToLNu_LO_all", 
   "/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ltortero-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

W3JetsToLNu_LO_all = creator.makeMCComponent(
    "W3JetsToLNu_LO_all", 
   "/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ltortero-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

W4JetsToLNu_LO_all = creator.makeMCComponent(
    "W4JetsToLNu_LO_all", 
   "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ltortero-MINIAOD_CL_2-d197bf72c878bf3ac37f65f1d3341802/USER",
    "CMS", ".*root", 1.0, dbsInstance=dbsInstance)

WNJets = [
W1JetsToLNu_LO,
W2JetsToLNu_LO_all,
W3JetsToLNu_LO_all,
W4JetsToLNu_LO_all,
]

#VVTo2L2Nu
#VVTo2L2Nu_ext

#WWTo1L1Nu2Q

#WZTo1L1Nu2Q
#WZTo1L3Nu
#WZTo2L2Q
#WZTo3LNu_amcatnlo
#WZJToLLLNu

#ZZTo2L2Q
#ZZTo4L



backgrounds = []
backgrounds.extend(TTbar)
backgrounds.extend(WJets)
backgrounds.extend(DYJets)
