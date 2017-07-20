import PhysicsTools.HeppyCore.framework.config as cfg

#####COMPONENT CREATOR

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()


# HiggsGGH125   = kreator.makeMyPrivateMCComponent('HiggsGGH125' , '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/manzoni-singleTau2017OpenIsoV3-29f7dae36643210eaec6ab4912c78586/USER'         , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

# HiggsGGH125 = kreator.makeMyPrivateMCComponent('HiggsGGH125' , '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-HLTOpenPT-e0097dbd5f0a065bf54f50c8acffcdc5/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsGGH125 = kreator.makeMyPrivateMCComponent('HiggsGGH125' , '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-notopenpt-0d9a03526378f2613e0a5fa62748c6fb/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsGGH125.dataset_entries = 2862196

# DYJetsToLL = kreator.makeMyPrivateMCComponent('DYJetsToLL' , '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/gtouquet-HLTOpenPT-e0097dbd5f0a065bf54f50c8acffcdc5/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

DYJetsToLL = kreator.makeMyPrivateMCComponent('DYJetsToLL' , '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/gtouquet-notopenpt-06ca11c682a893dd7246eeb48784dcd4/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

DYJetsToLL.dataset_entries = 14412756

# HiggsVBF125 = kreator.makeMyPrivateMCComponent('HiggsVBF125' , '/VBFHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-HLTOpenPT-5eb3065f1cac2ad75a2eb8c65d89642c/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsVBF125 = kreator.makeMyPrivateMCComponent('HiggsVBF125' , '/VBFHToTauTau_M125_13TeV_powheg_pythia8/gtouquet-notopenpt-61c55d6d535edba69d322d993d2e8583/USER' , 'PRIVATE', '.*root', dbsInstance='phys03', xSec=1.)

HiggsVBF125.dataset_entries = 2926456

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
