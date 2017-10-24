import PhysicsTools.HeppyCore.framework.config as cfg
   
from PhysicsTools.HeppyCore.framework.config                          import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop                      import getHeppyOption
from PhysicsTools.Heppy.utils.cmsswPreprocessor                       import CmsswPreprocessor
   
from CMGTools.H2TauTau.htt_ntuple_base_cff                            import jsonAna
from CMGTools.H2TauTau.htt_ntuple_base_cff                            import triggerAna
from CMGTools.H2TauTau.htt_ntuple_base_cff                            import vertexAna
from CMGTools.H2TauTau.htt_ntuple_base_cff                            import pileUpAna
from CMGTools.H2TauTau.htt_ntuple_base_cff                            import puFileData, puFileMC, eventSelector
   
from CMGTools.H2TauTau.proto.analyzers.EventAnalyzer                  import EventAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer                import TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.LightTriggerAnalyzer           import LightTriggerAnalyzer
# from CMGTools.H2TauTau.proto.analyzers.L1Stage2TriggerAnalyzer        import L1Stage2TriggerAnalyzer, Stage2L1ObjEnum
from CMGTools.H2TauTau.proto.analyzers.L2TriggerAnalyzer              import L2TriggerAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauDiscriminatorAnalyzer       import TauDiscriminatorAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TauTauRateAnalyzer             import TauTauRateAnalyzer
from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerTauTauRate import H2TauTauTreeProducerTauTauRate

from CMGTools.RootTools.utils.splitFactor                             import splitFactor
   
from CMGTools.H2TauTau.proto.samples.tsg17.tau_open_iso               import HiggsVBF125, QCDPt15to30, QCDPt30to50, QCDPt50to80, QCDPt80to120, QCDPt120to170, QCDPt170to300, QCDPt300to470, QCDPt470to600, DYJetsToLL_M1, TTJets, WJetsToLNu   


# Get all heppy options; set via '-o production' or '-o production=True'

# production = True run on batch, production = False (or unset) run locally
# production = getHeppyOption('production')
production    = False
pick_events   = False
cmssw         = False

samples = [QCDPt15to30, QCDPt30to50, QCDPt50to80, QCDPt80to120, QCDPt120to170, QCDPt170to300, QCDPt300to470, QCDPt470to600, DYJetsToLL_M1, TTJets, WJetsToLNu]

split_factor = 1e5

for sample in samples:
    sample.triggers = ['MC_OpenL2p5Iso_OpenL3Iso_PFTau20_Trk1_Reg_v1', 'MC_OpenL3Iso_PFTau20_Trk0_v1']
    sample.triggerobjects = [
        'hltPFTau20TrackPt1Reg',
        'hltPFTau20Track',
    ]
    sample.splitFactor = 600 #splitFactor(sample, split_factor)
    sample.lumi = 1.

###################################################
###             SET COMPONENTS BY HAND          ###
###################################################
selectedComponents = samples


###################################################
###               EVENT ANALYZER                ###
###################################################
eventAna = cfg.Analyzer(
    EventAnalyzer,
    name='EventAnalyzer',
)

###################################################
###              TRIGGER ANALYZER               ###
###################################################
triggerAna = cfg.Analyzer(
    TriggerAnalyzer,
    name='TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=False,
    usePrescaled=False,
    triggerResultsHandle=('TriggerResults', '', 'TEST'),
    triggerObjectsHandle=('selectedPatTriggerCustom', '', 'TEST'),
)

# triggerAna = cfg.Analyzer(
#     LightTriggerAnalyzer,
#     name='LightTriggerAnalyzer',
#     requireTrigger=False,
#     triggerResultsHandle=('TriggerResults', '', 'TEST')
# )

###################################################
###         TAU DISCRIMINATOR ANALYZER          ###
###################################################
# tauDiscriminatorAna = cfg.Analyzer(
#     TauDiscriminatorAnalyzer,
#     name='TauDiscriminatorAnalyzer',
#     inputs = {
#         'trigger_charged3hits'    : 'hltPFTauCharged3HitsPtSum'           ,
#         'trigger_charged5hits'    : 'hltPFTauCharged5HitsPtSum'           ,
#         'trigger_charged8hits'    : 'hltPFTauCharged8HitsPtSum'           ,
#         'trigger_neutral'         : 'hltPFTauNeutralPtSum'                ,
#         'trigger_photons'         : 'hltPFTauPhotonPtOutsideSignalCone'   ,

#         'trigger_charged3hits_reg': 'hltPFTauCharged3HitsPtSumReg'        ,
#         'trigger_charged5hits_reg': 'hltPFTauCharged5HitsPtSumReg'        ,
#         'trigger_charged8hits_reg': 'hltPFTauCharged8HitsPtSumReg'        ,
#         'trigger_neutral_reg'     : 'hltPFTauNeutralPtSumReg'             ,
#         'trigger_photons_reg'     : 'hltPFTauPhotonPtOutsideSignalConeReg',

#         'trigger_lead_trk_finding': 'hltPFTauTrackFindingDiscriminator'   ,
#         'trigger_lead_trk_reg_pt1': 'hltPFTauTrackPt1DiscriminatorReg'    ,
#     },
#     tomatch=lambda event : [],
#     ptcut=20., 
#     maxTriggerTaus=10,
# )

###################################################
###              TAU RATE ANALYZER              ###
###################################################
# ttRateAna = cfg.Analyzer(
#     TauTauRateAnalyzer,
#     name='TauTauRateAnalyzer',
#     discriminators = [
#         'trigger_charged3hits'    ,
#         'trigger_charged5hits'    ,
#         'trigger_charged8hits'    ,
#         'trigger_neutral'         ,
#         'trigger_photons'         ,

#         'trigger_charged3hits_reg',
#         'trigger_charged5hits_reg',
#         'trigger_charged8hits_reg',
#         'trigger_neutral_reg'     ,
#         'trigger_photons_reg'     ,

#         'trigger_lead_trk_finding',
#         'trigger_lead_trk_reg_pt1',
#     ], 
#     ptcut = 20.,
#     addOfflineTaus=False,
#     filtersToMatch=[
#         'hltPFTau20TrackPt1Reg',
#         'hltPFTau20Track',
#     ],
# )

###################################################
###               TAU L2 ANALYZER               ###
###################################################
# level2Ana = cfg.Analyzer(
#     L2TriggerAnalyzer,
#     name='L2TriggerAnalyzer',
#     tomatch=lambda event : event.trigger_taus, 
#     verbose=False,
# )

###################################################
###               TAU L1 ANALYZER               ###
###################################################
level1Ana = L1Stage2TriggerAnalyzer.defaultConfig
level1Ana.collections = [Stage2L1ObjEnum.Tau]
level1Ana.getter = lambda event : event.trigger_taus
level1Ana.process = 'TEST'
level1Ana.labelcalo = 'hltGtStage2Digis'
level1Ana.labelmuons = 'hltGtStage2Digis'

###################################################
###                TREE PRODUCER                ###
###################################################
# treeProducerAna = cfg.Analyzer(
#     H2TauTauTreeProducerTauTauRate,
#     name='H2TauTauTreeProducerTauTauRate',
# )
 
###################################################
###                  SEQUENCE                   ###
###################################################
sequence = cfg.Sequence([
    eventAna,
    triggerAna, # First analyser that applies selections
    #vertexAna,
    pileUpAna,
    # tauDiscriminatorAna,
    # ttRateAna,
    # level1Ana,
    # level2Ana,
    # treeProducerAna,
])
    
print sequence

###################################################
###             CHERRY PICK EVENTS              ###
###################################################

if pick_events:
    eventSelector.toSelect = [
        719595,
        719604,
        719605,
        719613,
        719614,
        719622,
        719625,
        719628,
        719630,
        719631,
        719632,
        719634,
        719635,
        719636,
        719637,
        719639,
        719642,
        719644,
        719645,
        719648,
        719650,
        719653,
        719657,
        719658,
    ]
    sequence.insert(0, eventSelector)

###################################################
###            SET BATCH OR LOCAL               ###
###################################################
if not production:
    comp                 = samples[0]
    selectedComponents   = [comp]
#     comp.files           = comp.files[:10]
    comp.splitFactor     = 1
    comp.fineSplitFactor = 1
    comp.files           = comp.files[:1]
    comp.files           = [
        'file:/afs/cern.ch/work/g/gtouquet/Trigger/CMSSW_9_2_3_patch1/src/HLTrigger/Configuration/test/test/outputFULL.root'
        # 'file:/afs/cern.ch/work/m/manzoni/tauHLT/2017/CMSSW_9_1_0_pre3/src/HLTrigger/Configuration/test/open_iso/outputFULL_rate1.root'
    ]

preprocessor = None
if cmssw:
    fname = '$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_ditau_data_cfg.py' if data else '$CMSSW_BASE/src/CMGTools/H2TauTau/prod/h2TauTauMiniAOD_ditau_cfg.py'
    #sequence.append(fileCleaner)
    preprocessor = CmsswPreprocessor(fname, addOrigAsSecondary=False)

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(
    components   = selectedComponents,
    sequence     = sequence,
    services     = [],
    preprocessor = preprocessor,
    events_class = Events
)

printComps(config.components, True)

def modCfgForPlot(config):
    config.components = []
