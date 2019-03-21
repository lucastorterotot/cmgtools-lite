import PhysicsTools.HeppyCore.framework.config as cfg

import ROOT 

# import all analysers:
# Heppy analyzers
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount import SkimAnalyzerCount
from PhysicsTools.Heppy.analyzers.core.EventSelector import EventSelector
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer import PileUpAnalyzer
from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer import LHEWeightAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerAnalyzer

from CMGTools.H2TauTau.heppy.analyzers.Cleaner import Cleaner
from CMGTools.H2TauTau.heppy.analyzers.Selector import Selector
from CMGTools.H2TauTau.heppy.analyzers.EventFilter import EventFilter



puFileMC = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/pudistributions_mc_2017_artur_13Nov.root'
puFileData = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/pudistributions_data_2017.root'


json = cfg.Analyzer(
    JSONAnalyzer,
    name='JSONAnalyzer',
)

skim = cfg.Analyzer(
    SkimAnalyzerCount,
    name='SkimAnalyzerCount'
)


from CMGTools.H2TauTau.heppy.analyzers.Debugger import Debugger
debugger = cfg.Analyzer(
    Debugger,
    name = 'Debugger',
    condition = None
)

trigger = cfg.Analyzer(
    TriggerAnalyzer,
    name='TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=False,
    usePrescaled=False
)

vertex = cfg.Analyzer(
    VertexAnalyzer,
    name='VertexAnalyzer',
    fixedWeight=1,
    keepFailingEvents=True,
    verbose=False
)

from CMGTools.H2TauTau.heppy.analyzers.TauAnalyzer import TauAnalyzer
taus = cfg.Analyzer(
    TauAnalyzer,
    name = 'TauAnalyzer',
    output = 'taus',
    taus = 'slimmedTaus'
)


from CMGTools.H2TauTau.heppy.analyzers.MuonAnalyzer import MuonAnalyzer
muons = cfg.Analyzer(
    MuonAnalyzer,
    name = 'MuonAnalyzer',
    output = 'muons',
    muons = 'slimmedMuons',
)

# setting up an alias for our isolation, now use iso_htt everywhere
from PhysicsTools.Heppy.physicsobjects.Muon import Muon
Muon.iso_htt = lambda x: x.relIso(0.4, 'dbeta', dbeta_factor=0.5, 
                                  all_charged=False)


from CMGTools.H2TauTau.heppy.analyzers.ElectronAnalyzer import ElectronAnalyzer
electrons = cfg.Analyzer(
    ElectronAnalyzer,
    output = 'electrons',
    electrons = 'slimmedElectrons',
)

# setting up an alias for our isolation, now use iso_htt everywhere
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsutils.EffectiveAreas import areas

Electron.EffectiveArea03 = areas['Fall17']['electron']

# Electron.EffectiveArea03 = { 
#     '03' : 
#     [ (1.000, 0.1440),
#       (1.479, 0.1562),
#       (2.000, 0.1032),
#       (2.200, 0.0859),
#       (2.300, 0.1116),
#       (2.400, 0.1321),
#       (2.500, 0.1654) ],
#     'eta' : lambda x: x.superCluster().eta()
#     }
Electron.iso_htt = lambda x: x.relIso(0.3, "EA", 
                                      all_charged=False)

# Gen matcher and tau energy scale ==========================================

def select_leptons(event):
    leptons = []
    leptons.extend(event.taus)
    leptons.extend(event.muons)
    leptons.extend(event.electrons)
    return leptons

from CMGTools.H2TauTau.heppy.analyzers.GenMatcherAnalyzer import GenMatcherAnalyzer
genmatcher = cfg.Analyzer(
    GenMatcherAnalyzer, 
    'genmatcher',
    jetCol='slimmedJets',
    genPtCut=8.,
    genmatching = True,
    filter_func = select_leptons
)

from CMGTools.H2TauTau.heppy.analyzers.TauP4Scaler import TauP4Scaler
tauenergyscale = cfg.Analyzer(
    TauP4Scaler,
    'tauenergyscale',
    src = 'taus',
)

# third lepton veto =========================================================                  
def select_muon_third_lepton_veto(muon):
    return muon.pt() > 10             and \
        abs(muon.eta()) < 2.4         and \
        muon.isMediumMuon()  and \
        abs(muon.dxy()) < 0.045       and \
        abs(muon.dz())  < 0.2         and \
        muon.iso_htt() < 0.3
sel_muons_third_lepton_veto = cfg.Analyzer(
    Selector,
    '3lepv_muons',
    output = 'sel_muons_third_lepton_veto',
    src = 'muons',
    filter_func = select_muon_third_lepton_veto
)

sel_muons_third_lepton_veto_cleaned = cfg.Analyzer(
    Cleaner,
    '3lepv_muons_cleaner',
    output = 'sel_muons_third_lepton_veto_cleaned',
    src = 'sel_muons_third_lepton_veto',
    mask = lambda x : [getattr(x,'dileptons_sorted')[0].leg1(),
                       getattr(x,'dileptons_sorted')[0].leg2()]
)

def select_electron_third_lepton_veto(electron):
    return electron.pt() > 10             and \
        abs(electron.eta()) < 2.5         and \
        electron.id_passes("mvaEleID-Fall17-noIso-V2", "wp90") and \
        abs(electron.dxy()) < 0.045       and \
        abs(electron.dz())  < 0.2         and \
        electron.passConversionVeto()     and \
        electron.gsfTrack().hitPattern().numberOfLostHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1 and \
        electron.iso_htt() < 0.3
sel_electrons_third_lepton_veto = cfg.Analyzer(
    Selector,
    '3lepv_electrons',
    output = 'sel_electrons_third_lepton_veto',
    src = 'electrons',
    filter_func = select_electron_third_lepton_veto
)

sel_electrons_third_lepton_veto_cleaned = cfg.Analyzer(
    Cleaner,
    '3lepv_electrons_cleaner',
    output = 'sel_electrons_third_lepton_veto_cleaned',
    src = 'sel_electrons_third_lepton_veto',
    mask = lambda x : [getattr(x,'dileptons_sorted')[0].leg1(),
                       getattr(x,'dileptons_sorted')[0].leg2()]
)

third_lepton_veto_muons = cfg.Analyzer(
    EventFilter,
    '3lepv_muons',
    src = 'sel_muons_third_lepton_veto_cleaned',
    filter_func = lambda x : len(x) == 0,
    output = 'veto_third_lepton_muons_passed'
)

third_lepton_veto_electrons = cfg.Analyzer(
    EventFilter,
    '3lepv_electrons',
    src = 'sel_electrons_third_lepton_veto_cleaned',
    filter_func = lambda x : len(x) == 0,
    output = 'veto_third_lepton_electrons_passed'
)

sequence_third_lepton_veto = cfg.Sequence([
        sel_muons_third_lepton_veto,
        sel_electrons_third_lepton_veto,
        sel_muons_third_lepton_veto_cleaned,
        sel_electrons_third_lepton_veto_cleaned,
        third_lepton_veto_muons,
        third_lepton_veto_electrons
])


from CMGTools.H2TauTau.heppy.analyzers.TrigMatcher import TrigMatcher    
trigger_match = cfg.Analyzer(
    TrigMatcher,
    src='dileptons_sorted',
    require_all_matched = True
)


# Jet sequence ===========================================================

gt_mc = 'Fall17_17Nov2017_V8_MC'#latest : V32
gt_data = 'Fall17_17Nov2017{}_V6_DATA'#latest: V32
gt_embed = 'Fall17_17Nov2017{}_V6_DATA'

def select_good_jets_FixEE2017(jet):
    return jet.correctedJet("Uncorrected").pt() > 50. or \
        abs(jet.eta()) < 2.65 or \
        abs(jet.eta()) > 3.139

from CMGTools.H2TauTau.heppy.analyzers.JetAnalyzer import JetAnalyzer
jets = cfg.Analyzer(
    JetAnalyzer, 
    output = 'jets',
    jets = 'slimmedJets',
    do_jec = True,
    gt_mc = gt_mc,
    selection = select_good_jets_FixEE2017
)

jets_20_unclean = cfg.Analyzer(
    Selector,
    'jets_20_unclean',
    output = 'jets_20_unclean',
    src = 'jets',
    filter_func = lambda x : x.pt()>20 and abs(x.eta())<4.7 and x.jetID("POG_PFID_Tight")
)


from CMGTools.H2TauTau.heppy.analyzers.JetCleaner import JetCleaner
jet_20 = cfg.Analyzer(
    JetCleaner,
    output = 'jets_20',
    dileptons = 'dileptons_sorted',
    jets = 'jets_20_unclean',
    drmin = 0.5
)

jets_30 = cfg.Analyzer(
    Selector,
    'jets_30',
    output = 'jets_30',
    src = 'jets_20',
    filter_func = lambda x : x.pt()>30 
)

# bjets ==================================================================

from CMGTools.H2TauTau.heppy.analyzers.BJetAnalyzer import BJetAnalyzer
btagger = cfg.Analyzer(
    BJetAnalyzer, 
    'btagger', 
    jets = 'jets_20'
)

#always put after btagger
bjets_20 = cfg.Analyzer(
    Selector, 
    'bjets_20',
    output = 'bjets_20', 
    src = 'jets_20',
    filter_func = lambda x: abs(x.eta())<2.5 and \
        x.is_btagged
)

sequence_jets = cfg.Sequence([
        jets,
        jets_20_unclean,
        jet_20,
        jets_30,
        btagger,
        bjets_20
])

# MET ====================================================================

from CMGTools.H2TauTau.proto.analyzers.METFilter import METFilter
met_filters = cfg.Analyzer(
    METFilter,
    name='METFilter',
    processName='PAT',
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#Moriond_2018
    triggers=[
        'Flag_goodVertices',
        'Flag_globalTightHalo2016Filter',
        'Flag_globalSuperTightHalo2016Filter',
        'Flag_HBHENoiseFilter', 
        'Flag_HBHENoiseIsoFilter', 
        'Flag_EcalDeadCellTriggerPrimitiveFilter',
        'Flag_BadPFMuonFilter',
        'Flag_BadChargedCandidateFilter',
        'Flag_eeBadScFilter',
        'Flag_ecalBadCalibFilter',
    ]
)

from CMGTools.H2TauTau.heppy.analyzers.METAnalyzer import METAnalyzer
pfmetana = cfg.Analyzer(
    METAnalyzer,
    name='PFMetana',
    recoil_correction_file='HTT-utilities/RecoilCorrections/data/Type1_PFMET_2017.root',
    met = 'pfmet',
    apply_recoil_correction= True,#Recommendation states loose pfjetID for jet multiplicity but this WP is not supported anymore?
    runFixEE2017= True
)

# if/when using MVAMET, use this to apply recoilcorrection
# mvametana = cfg.Analyzer(
#     METAnalyzer,
#     name='MVAmetana',
#     recoil_correction_file='CMGTools/H2TauTau/data/Type1_PFMET_2017.root',
#     met = 'mvamet',
#     apply_recoil_correction=True #Recommendation states loose pfjetID for jet multiplicity but this WP is not supported anymore?
# )

# Generator stuff ========================================================

lheweight = cfg.Analyzer(
    LHEWeightAnalyzer, name="LHEWeightAnalyzer",
    useLumiInfo=False
)

pileup = cfg.Analyzer(
    PileUpAnalyzer,
    name='PileUpAnalyzer',
    true=True,
    autoPU=False
)

from CMGTools.H2TauTau.heppy.analyzers.MCWeighter import MCWeighter
mcweighter = cfg.Analyzer(
    MCWeighter,
    'MCWeighter'
)

from CMGTools.H2TauTau.proto.analyzers.NJetsAnalyzer import NJetsAnalyzer
njets_ana = cfg.Analyzer(
    NJetsAnalyzer,
    name='NJetsAnalyzer',
    fillTree=True,
    verbose=False
)

from CMGTools.H2TauTau.heppy.analyzers.HTTGenAnalyzer import HTTGenAnalyzer
httgenana = cfg.Analyzer(
    HTTGenAnalyzer, 
    'httgenana',
    jetCol='slimmedJets',
    genmatching=True,
    genPtCut=8.
)

# Definition of the main sequences =======================================

sequence_beforedil = cfg.Sequence([
        mcweighter,
        json,
        skim,
        vertex,
        taus, 
        muons, 
        electrons,
        genmatcher,
        tauenergyscale,
])


sequence_afterdil = cfg.Sequence([
        trigger, 
        trigger_match,
        met_filters,
        lheweight,
        httgenana,
        pileup, 
        njets_ana
]) 

sequence_afterdil.extend(sequence_jets)
sequence_afterdil.append(pfmetana)
# sequence_afterdil.append(mvametana)
sequence_afterdil.extend(sequence_third_lepton_veto)
sequence_afterdil.append(debugger)
