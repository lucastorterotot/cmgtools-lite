import PhysicsTools.HeppyCore.framework.config as cfg

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

HLTPhysics35 = kreator.makeMyPrivateDataComponent('HLTPhysics35' , '/HLTPhysics1/gtouquet-HLTditau35_HLTPhysics-14753f7701c4d1d5ca710fe6396985f8/USER' , 'PRIVATE', '.*root', dbsInstance='phys03')

HLTPhysics35.dataset_entries = 7481018


HLTPhysics26 = kreator.makeMyPrivateDataComponent('HLTPhysics26' , '/HLTPhysics1/gtouquet-HLTditau26_HLTPhysics-d4d93a817ced19cd7ed12a11347d6b5c/USER' , 'PRIVATE', '.*root', dbsInstance='phys03')

HLTPhysics26.dataset_entries = 7533907

HLTPhysicsbothpath = kreator.makeMyPrivateDataComponent('HLTPhysicsbothpath' , '/HLTPhysics1/gtouquet-HLTditauboth_paths_HLTPhysics19oct-14753f7701c4d1d5ca710fe6396985f8/USER' , 'PRIVATE', '.*root', dbsInstance='phys03')

HLTPhysicsbothpath.dataset_entries = 9741267

# HiggsGGH125   = kreator.makeMyPrivateMCComponent('HiggsGGH125' , '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/manzoni-singleTau2017OpenIsoV3-29f7dae36643210eaec6ab4912c78586/USER'         , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

# HiggsGGH125 = kreator.makeMyPrivateMCComponent('HiggsGGH125' , '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-HLTOpenPT-e0097dbd5f0a065bf54f50c8acffcdc5/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

# HiggsGGH125 = kreator.makeMyPrivateMCComponent('HiggsGGH125' , '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-notopenpt-0d9a03526378f2613e0a5fa62748c6fb/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsGGH125 = kreator.makeMyPrivateMCComponent('HiggsGGH125' , '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-H2tautau_offlineSelection-537b943c839ca15bac0128ebafe0c093/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsGGH125.dataset_entries = 7675

HiggsGGH125testeos = kreator.makeMyPrivateMCComponent('HiggsGGH125' , '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-HLTditau26Tight-fce65d1d17edbd256a6217a96ea18a6c/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsGGH125testeos.dataset_entries = 2367792

HiggsGGH125test2 = kreator.makeMyPrivateMCComponent('HiggsGGH125' , '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-HLTOPEN27sept-6fdf59d9c74e9922214b3f3d435bc39f/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsGGH125test2.dataset_entries = 2312228

HiggsGGH125test3 = kreator.makeMyPrivateMCComponent('HiggsGGH125' , '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-HLTditau26Tight_35-df569cd9c65816648c8639bceca85db3/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsGGH125test3.dataset_entries = 2840340

HiggsGGH125test10oct = kreator.makeMyPrivateMCComponent('HiggsGGH125' , '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-HLTditau26oct10-1b0f58956896d1208c2d1f4ec01119f2/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsGGH125test10oct.dataset_entries = 2683628



# DYJetsToLL = kreator.makeMyPrivateMCComponent('DYJetsToLL' , '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/gtouquet-HLTOpenPT-e0097dbd5f0a065bf54f50c8acffcdc5/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

DYJetsToLL = kreator.makeMyPrivateMCComponent('DYJetsToLL' , '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/gtouquet-H2tautau_offlineSelection-537b943c839ca15bac0128ebafe0c093/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

DYJetsToLL.dataset_entries = 865

# HiggsVBF125 = kreator.makeMyPrivateMCComponent('HiggsVBF125' , '/VBFHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-HLTOpenPT-5eb3065f1cac2ad75a2eb8c65d89642c/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsVBF125 = kreator.makeMyPrivateMCComponent('HiggsVBF125' , '/VBFHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-H2tautau_offlineSelection-537b943c839ca15bac0128ebafe0c093/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsVBF125.dataset_entries = 12424

HiggsVBF125test = kreator.makeMyPrivateMCComponent('HiggsVBF125' , '/VBFHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-HLTOPEN27sept-60180a43517ab273d0ee92577e6f510f/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsVBF125test.dataset_entries = 2561360

ZeroBias = kreator.makeMyPrivateMCComponent('ZeroBias' , '/ZeroBias/gtouquet-rate_openpt-13439358fe2d549fcaf39cee5a6dd668/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

ZeroBias.dataset_entries = 140567

all_signal = [
    HiggsGGH125,
    HiggsVBF125
]

all_sm     = [
    DYJetsToLL
]


all_mc = all_signal + all_sm

for comp in all_mc:
    comp.splitFactor = 1000000
    comp.isMC = True
    comp.isData = False
