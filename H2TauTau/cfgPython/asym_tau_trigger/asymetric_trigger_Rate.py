import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop                      import getHeppyOption
from PhysicsTools.HeppyCore.framework.config                          import printComps

from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer

from CMGTools.H2TauTau.proto.analyzers.TauTauTriggerAnalyzerObjectsRate import TauTauTriggerAnalyzer

from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauTauTriggerObjects import H2TauTauTreeProducerTrigger

from CMGTools.RootTools.utils.splitFactor                             import splitFactor

from CMGTools.H2TauTau.proto.samples.tsg17.doubletau_open_pt               import  HiggsGGH125, HiggsVBF125, DYJetsToLL

from CMGTools.H2TauTau.proto.samples.tsg17.doubletau_open_pt import HiggsVBF125test, HiggsGGH125testeos, HiggsGGH125test2, HiggsGGH125test10oct, HLTPhysics35, HLTPhysics26, HLTPhysicsbothpath

# Get all heppy options; set via '-o production' or '-o production=True'

# production = True run on batch, production = False (or unset) run locally
# production = getHeppyOption('production')
production    = True
pick_events   = False
cmssw         = False

# import pdb; pdb.set_trace()

samples = [HLTPhysicsbothpath]#HiggsGGH125test10oct]## [ HiggsVBF125, DYJetsToLL, HiggsGGH125]

split_factor = 1e5

for sample in samples:
    # sample.triggers = ['HLT_DoubleMediumChargedIsoPFTauOPEN_Trk1_eta2p1_Reg_v1']# 'MC_OpenL2p5Iso_OpenL3Iso_PFTau20_Trk1_Reg_v1', 'MC_OpenL3Iso_PFTau20_Trk0_v1']
    # sample.triggerobjects = ['hltDoublePFTau35TrackPt1MediumChargedIsolationReg']
    #     'hltPFTau20TrackPt1Reg',
    #     'hltPFTau20Track',
    # ]
    sample.splitFactor = splitFactor(sample, split_factor)
    sample.lumi = 1.


###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
selectedComponents = samples


###################################################
###              TRIGGER ANALYZER               ###
###################################################
triggerAna = cfg.Analyzer(
    TauTauTriggerAnalyzer,
    threshold = 0,
    isolation='byVTightIsolationMVArun2v1DBoldDMwLT',
    triggerResultsHandle=('TriggerResults', '', 'MYHLT'),
    triggerObjectsHandle=('selectedPatTriggerCustom', '', 'MYHLT'),
)

vertexAna = cfg.Analyzer(
    VertexAnalyzer,
    name='VertexAnalyzer',
    fixedWeight=1,
    keepFailingEvents=True,
    verbose=False
)

from CMGTools.H2TauTau.proto.analyzers.EventAnalyzer                  import EventAnalyzer
eventAna = cfg.Analyzer(
    EventAnalyzer,
    name='EventAnalyzer',
)

###################################################
###                TREE PRODUCER                ###
###################################################
treeProducerAna = cfg.Analyzer(
    H2TauTauTreeProducerTrigger,
    name='H2TauTauTreeProducerTauTauTrigger'
)

###################################################
###                  SEQUENCE                   ###
###################################################
sequence = cfg.Sequence([
    eventAna,
    vertexAna,
    triggerAna,
    treeProducerAna
])

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
#     comp                 = samples[0]
#     selectedComponents   = [comp]
# #     comp.files           = comp.files[:10]
#     comp = samples
#     for com in comp:
#         com.splitFactor     = 1
#         com.fineSplitFactor = 1
    selectedComponents = [selectedComponents[0]]
    selectedComponents[0].splitFactor     = 1
    selectedComponents[0].fineSplitFactor = 1
    # import pdb;pdb.set_trace()
    selectedComponents[0].files = [selectedComponents[0].files[0]]
    
    # selectedComponents[0].files = ['file:/afs/cern.ch/work/g/gtouquet/Trigger/Prod/CMSSW_9_2_12_patch1/src/HLTrigger/Configuration/test/outputFULL.root']
    # comp.files           = ['root://eoscms.cern.ch//eos/cms/store/mc/RunIISummer16MiniAODv2/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/D662E4EE-8DC8-E611-91C3-008CFA00317C.root']
#'/afs/cern.ch/work/g/gtouquet/training/CMSSW_9_2_2/src/offlineselection/offlinesel.root'
    # comp.files           = [
    #     'file:/afs/cern.ch/work/g/gtouquet/Trigger/Prod/CMSSW_9_2_3_patch1/src/HLTrigger/Configuration/test/outputFULL.root'
    #     # 'file:/afs/cern.ch/work/m/manzoni/tauHLT/2017/CMSSW_9_1_0_pre3/src/HLTrigger/Configuration/test/open_iso/outputFULL_rate1.root'
    # ]


# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(
    components   = selectedComponents,
    sequence     = sequence,
    services     = [],
    preprocessor = None,
    events_class = Events
)

printComps(config.components, True)

def modCfgForPlot(config):
    config.components = []
