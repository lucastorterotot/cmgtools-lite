import PhysicsTools.HeppyCore.framework.config as cfg
import os
import ROOT 

#########################
### pu files & global tags
#########################

puFileMC = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/pudistributions_mc_2017_artur_13Nov.root'
puFileMC_bbhamcatnlo = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/pudistributions_mc_2017_artur_Jul9_update_bbhamcatnlo.root'
puFileData = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/pudistributions_data_2017.root'

gt_mc = 'Fall17_17Nov2017_V32_MC'
gt_data = 'Fall17_17Nov2017{}_V32_DATA'
gt_embed = 'Fall17_17Nov2017{}_V32_DATA'

#########################
### samples #############
#########################

from CMGTools.H2TauTau.proto.samples.fall17.backgrounds import DY, TTbar, generic_backgrounds
from CMGTools.H2TauTau.proto.samples.fall17.data import data_tau, data_single_muon, data_single_electron
from CMGTools.H2TauTau.proto.samples.fall17.higgs import mc_higgs
from CMGTools.H2TauTau.proto.samples.fall17.higgs_susy import mssm_signals, mc_higgs_susy_bb_amcatnlo
from CMGTools.H2TauTau.proto.samples.fall17.embedded import embedded_tt, embedded_mt, embedded_et

for sample in embedded_tt+embedded_mt+embedded_et:
    sample.isEmbed = True

for sample in DY+TTbar+generic_backgrounds+mc_higgs+mssm_signals:
    sample.puFileData = puFileData
    sample.puFileMC = puFileMC

for sample in mc_higgs_susy_bb_amcatnlo:
    sample.puFileData = puFileData
    sample.puFileMC = puFileMC_bbhamcatnlo

for sample in data_tau+data_single_muon+data_single_electron+embedded_tt+embedded_mt+embedded_et:
    era = sample.name[sample.name.find('2017')+4]
    if 'V32' in gt_data and era in ['D','E']:
        era = 'DE'
    sample.dataGT = gt_data.format(era)


samples_lists = {'DY': DY,
                 'TTbar': TTbar,
                 'generic_background': generic_backgrounds,
                 'data_tau': data_tau,
                 'data_single_muon': data_single_muon,
                 'data_single_electron': data_single_electron,
                 'embedded_tt': embedded_tt,
                 'embedded_mt': embedded_mt,
                 'embedded_et': embedded_et,
                 'sm_higgs': mc_higgs,
                 'mssm_signals': mssm_signals,
                 'mc_higgs_susy_bb_amcatnlo': mc_higgs_susy_bb_amcatnlo}

#########################
### analyzers ###########
#########################

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
    systematics = True
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


def select_good_jets_FixEE2017(jet):
        return jet.correctedJet("Uncorrected").pt() >50. or \
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

from CMGTools.H2TauTau.heppy.analyzers.Sorter import Sorter
jet_sorter = cfg.Analyzer(
    Sorter,
    output = 'jets_sorted',
    src = 'jets',
    metric = lambda jet: (jet.pt()),
    reverse = True
    )

jets_20_unclean = cfg.Analyzer(
    Selector,
    'jets_20_unclean',
    output = 'jets_20_unclean',
    src = 'jets_sorted',
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
    jets = 'jets_20',
    tagger_name = 'DeepCSV',
    discriminator = 'pfDeepCSVDiscriminatorsJetTags:BvsAll',
    wp = 'medium',
    csv_cut = 0.4941,
    SF_file = os.path.expandvars("$CMSSW_BASE/src/CMGTools/H2TauTau/data/DeepCSV_94XSF_V3_B_F.csv"),
    method = 'promote_demote',
    efficiency_file = os.path.expandvars('$CMSSW_BASE/src/CMGTools/H2TauTau/data/tagging_efficiencies_march2018.root'),
    sys = 'central'
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
        jet_sorter,
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
    fillTree=False,
    verbose=False
)

from CMGTools.H2TauTau.heppy.analyzers.HTTGenAnalyzer import HTTGenAnalyzer
httgenana = cfg.Analyzer(
    HTTGenAnalyzer, 
    'httgenana',
    jetCol='slimmedJets',
    genmatching=True,
    genPtCut=8.,
    workspace_path='$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_2017_v2.root'
)

#########################
### sequences ###########
#########################

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
sequence_afterdil.extend(sequence_third_lepton_veto)
sequence_afterdil.append(debugger)
