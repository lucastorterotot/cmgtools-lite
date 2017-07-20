import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop                      import getHeppyOption
from PhysicsTools.HeppyCore.framework.config                          import printComps

from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer

from CMGTools.H2TauTau.proto.analyzers.TauTauTriggerAnalyzerObjects import TauTauTriggerAnalyzer

from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauTauTriggerObjects import H2TauTauTreeProducerTrigger

from CMGTools.RootTools.utils.splitFactor                             import splitFactor

from CMGTools.H2TauTau.proto.samples.tsg17.doubletau_open_pt               import  HiggsGGH125, HiggsVBF125, DYJetsToLL

# Get all heppy options; set via '-o production' or '-o production=True'

# production = True run on batch, production = False (or unset) run locally
# production = getHeppyOption('production')
production    = True
pick_events   = False
cmssw         = False

samples = [HiggsGGH125, HiggsVBF125]#, DYJetsToLL]

split_factor = 1e4

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
    comp                 = samples[0]
    selectedComponents   = [comp]
#     comp.files           = comp.files[:10]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
    comp.files           = [comp.files[0], comp.files[1], comp.files[2], comp.files[3], comp.files[4]]
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
