import os
import re

import ROOT

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption


import logging
logging.shutdown()
# reload(logging)
logging.basicConfig(level=logging.WARNING)

from PhysicsTools.HeppyCore.framework.event import Event
Event.print_patterns = ['*taus*', '*muons*', '*electrons*', 'veto_*', 
                        '*dileptons_*', '*jets*']

###############
# Options
###############

# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False run locally
test = getHeppyOption('test', False)
syncntuple = getHeppyOption('syncntuple', False)
data = getHeppyOption('data', False)
embedded = getHeppyOption('embedded', False)
if embedded:
    data = True
add_sys = getHeppyOption('add_sys', True)
reapplyJEC = getHeppyOption('reapplyJEC', True)
samples_name = getHeppyOption('samples_name', 'mc_higgs_susy_bb_amcatnlo') # options : DY, TTbar, generic_background, data_tau, data_single_muon, data_single_electron, embedded_tt, embedded_mt, embedded_et, sm_higgs, mssm_signals, mc_higgs_susy_bb_amcatnlo
AAA = getHeppyOption('AAA', 'Lyon') # options : global, Lyon

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
if AAA == 'Lyon':
    ComponentCreator.useLyonAAA = True
else:
    ComponentCreator.useAAA = True

if 'data' in samples_name:
    data = True
elif 'embedded' in samples_name:
    data=True
    embedded=True
else:
    data=False
    embedded=False

###############
# Components
###############

from CMGTools.H2TauTau.heppy.sequence.common import samples_lists
from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.fall17.triggers_tauTau import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.fall17.triggers_tauTau import data_triggers, data_triggerfilters, embedded_triggerfilters

selectedComponents = samples_lists[samples_name]

n_events_per_job = 1e6
if test:
    n_events_per_job = 1e5
    if embedded:
        n_events_per_job = 3e4

for sample in selectedComponents:
    if data:
        sample.triggers = data_triggers
        sample.triggerobjects = data_triggerfilters
        if embedded:
            sample.triggerobjects = embedded_triggerfilters
    else:
        sample.triggers = mc_triggers
        sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, n_events_per_job)
    sample.channel = 'tt'

if test:
    cache = True
    selectedComponents = [selectedComponents[0]]
    for comp in selectedComponents:
       comp.files = comp.files[:1]
       comp.splitFactor = 1
       comp.fineSplitFactor = 1

events_to_pick = []

#KIT's skimming function
def skim_KIT(event):
    flags = [
        'Flag_goodVertices',
        'Flag_globalTightHalo2016Filter',
        'Flag_globalSuperTightHalo2016Filter',
        'Flag_HBHENoiseFilter',
        'Flag_HBHENoiseIsoFilter',
        'Flag_EcalDeadCellTriggerPrimitiveFilter',
        'Flag_BadPFMuonFilter',
        'Flag_BadChargedCandidateFilter',
        'Flag_eeBadScFilter',
        'Flag_ecalBadCalibFilter']
    if embedded or data:
        flags = ['Flag_goodVertices','Flag_globalSuperTightHalo2016Filter','Flag_HBHENoiseFilter','Flag_HBHENoiseIsoFilter','Flag_EcalDeadCellTriggerPrimitiveFilter','Flag_BadPFMuonFilter','Flag_BadChargedCandidateFilter','Flag_eeBadScFilter','Flag_ecalBadCalibFilter']
    ids = [
        'againstElectronVLooseMVA6',
        'againstMuonLoose3',
        'byVLooseIsolationMVArun2017v2DBoldDMwLT2017']
    return all([getattr(event,x)==1 for x in flags]) and\
        event.veto_third_lepton_electrons_passed and\
        event.veto_third_lepton_muons_passed and\
        all([event.dileptons_sorted[0].leg2().tauID(x) for x in ids]) and\
        all([event.dileptons_sorted[0].leg1().tauID(x) for x in ids])


from CMGTools.H2TauTau.heppy.sequence.common import debugger
debugger.condition = None#skim_KIT#lambda event : True # lambda event : len(event.sel_taus)>2
###############
# Analyzers 
###############

from CMGTools.H2TauTau.heppy.analyzers.Selector import Selector
def select_tau(tau):
    return tau.pt()    > 40  and \
        abs(tau.eta()) < 2.1 and \
        abs(tau.leadChargedHadrCand().dz()) < 0.2 and \
        tau.tauID('decayModeFinding') > 0.5 and \
        abs(tau.charge()) == 1. and \
        tau.tauID('byVVLooseIsolationMVArun2017v2DBoldDMwLT2017')
sel_taus = cfg.Analyzer(
    Selector,
    'sel_taus',
    output = 'sel_taus',
    src = 'taus',
    filter_func = select_tau  
)

from CMGTools.H2TauTau.heppy.analyzers.EventFilter import EventFilter
two_tau = cfg.Analyzer(
    EventFilter, 
    'two_tau',
    src = 'sel_taus',
    filter_func = lambda x : len(x)>1
)

# ditau pair ================================================================

from CMGTools.H2TauTau.heppy.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer

dilepton = cfg.Analyzer(
    DiLeptonAnalyzer,
    output = 'dileptons',
    l1 = 'sel_taus',
    l2 = 'sel_taus',
    dr_min = 0.5
)

def sorting_metric(dilepton):
    leg1_iso = dilepton.leg1().tauID('byIsolationMVArun2017v2DBoldDMwLTraw2017')
    leg2_iso = dilepton.leg2().tauID('byIsolationMVArun2017v2DBoldDMwLTraw2017')
    if leg1_iso > leg2_iso:
        most_isolated_tau_isolation = leg1_iso
        most_isolated_tau_pt = dilepton.leg1().pt()
        least_isolated_tau_isolation = leg2_iso
        least_isolated_tau_pt = dilepton.leg2().pt()
    else:
        most_isolated_tau_isolation = leg2_iso
        most_isolated_tau_pt = dilepton.leg2().pt()
        least_isolated_tau_isolation = leg1_iso
        least_isolated_tau_pt = dilepton.leg1().pt()
    return (-most_isolated_tau_isolation,
             -most_isolated_tau_pt,
             -least_isolated_tau_isolation,
             -least_isolated_tau_pt)

from CMGTools.H2TauTau.heppy.analyzers.Sorter import Sorter
dilepton_sorted = cfg.Analyzer(
    Sorter,
    output = 'dileptons_sorted',
    src = 'dileptons',
    metric = sorting_metric,
    reverse = False
    )



sequence_dilepton = cfg.Sequence([
        sel_taus,
        two_tau,
        dilepton,
        dilepton_sorted,
        ])

# weights ================================================================

# id weights
from CMGTools.H2TauTau.heppy.analyzers.TauIDWeighter import TauIDWeighter
tauidweighter_general = cfg.Analyzer(
    TauIDWeighter,
    'TauIDWeighter_general',
    taus = lambda event: [event.dileptons_sorted[0].leg1(),event.dileptons_sorted[0].leg2()]
)

tauidweighter = cfg.Analyzer(
    TauIDWeighter,
    'TauIDWeighter',
    taus = lambda event: [event.dileptons_sorted[0].leg1(),event.dileptons_sorted[0].leg2()],
    WPs = {'JetToTau':'Tight', # dummy, no weights for jet fakes
           'TauID':'Tight',
           'MuToTaufake':'Loose',
           'EToTaufake':'VLoose'}
)


# trigger weights
ws_tau_vars_dict = {'t_pt':lambda tau:tau.pt(),
                    't_eta':lambda tau:tau.eta(),
                    't_phi':lambda tau:tau.phi()}
ws_tau_func_dict = {'tt':'t_trg_tight_tt_ratio'}
from CMGTools.H2TauTau.heppy.analyzers.TriggerWeighter import TriggerWeighter
triggerweighter = cfg.Analyzer(
    TriggerWeighter,
    'TriggerWeighter',
    workspace_path = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_2017_v2.root',
    legs = lambda event: [event.dileptons_sorted[0].leg1(),event.dileptons_sorted[0].leg2()],
    leg1_vars_dict = ws_tau_vars_dict,
    leg2_vars_dict = ws_tau_vars_dict,
    leg1_func_dict = ws_tau_func_dict,
    leg2_func_dict = ws_tau_func_dict
)


# from CMGTools.H2TauTau.heppy.analyzers.FakeFactorAnalyzer import FakeFactorAnalyzer
# fakefactor = cfg.Analyzer(
#     FakeFactorAnalyzer,
#     'FakeFactorAnalyzer',
#     channel = 'tt',
#     filepath = '$CMSSW_BASE/src/HTTutilities/Jet2TauFakes/data/MSSM2016/20170628_medium/{}/{}/fakeFactors_20170628_medium.root',
#     met = 'pfmet'
# )

# ntuple ================================================================

if syncntuple:
    skim_func = lambda x: True
else:
    skim_func = lambda x: skim_KIT

from CMGTools.H2TauTau.heppy.analyzers.NtupleProducer import NtupleProducer
from CMGTools.H2TauTau.heppy.ntuple.ntuple_variables import tautau as event_content_tautau
ntuple = cfg.Analyzer(
    NtupleProducer,
    name = 'NtupleProducer',
    treename = 'events',
    event_content = event_content_tautau,
    skim_func = skim_func
)

# recoil correction =======================================================
wpat = re.compile('W\d?Jet.*')
for comp in selectedComponents:
    if any(x in comp.name for x in ['ZZ','WZ','VV','WW','T_','TBar_']):
        comp.recoil_correct = False
    match = wpat.match(comp.name)
    if any(x in comp.name for x in ['DY','Higgs']) or not (match is None):
        comp.recoil_correct = True
        comp.METSysFile = 'HTT-utilities/RecoilCorrections/data/PFMEtSys_2017.root'
    if any(x in comp.name for x in ['TT']):
        comp.recoil_correct = False

# embedded ================================================================

from CMGTools.H2TauTau.heppy.analyzers.EmbeddedAnalyzer import EmbeddedAnalyzer
embedded_ana = cfg.Analyzer(
    EmbeddedAnalyzer,
    name = 'EmbeddedAnalyzer',
    channel = 'tt'
)


from CMGTools.H2TauTau.heppy.sequence.common import sequence_beforedil, sequence_afterdil, trigger, met_filters, trigger_match, httgenana
sequence = sequence_beforedil
sequence.extend( sequence_dilepton )
sequence.extend( sequence_afterdil )
if embedded:
    sequence.append(embedded_ana)
# if data:
#     sequence.append(fakefactor)
sequence.append(tauidweighter_general)
sequence.append(tauidweighter)
sequence.append(triggerweighter)
sequence.append(ntuple)

# if embedded:
#     sequence = [x for x in sequence if x.name not in ['JSONAnalyzer']]

if events_to_pick:
    from CMGTools.H2TauTau.htt_ntuple_base_cff import eventSelector
    eventSelector.toSelect = events_to_pick
    sequence.insert(0, eventSelector)

# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events
                    )

printComps(config.components, True)

### systematics

from CMGTools.H2TauTau.heppy.analyzers.Calibrator import Calibrator
import copy
nominal = config
configs = {'nominal':nominal}
up_down = ['up','down']

### top pT reweighting

def config_top_pT_reweighting(up_or_down):
    new_config = copy.deepcopy(nominal)
    for cfg in new_config.sequence:
        if cfg.name == 'httgenana':
            cfg.top_systematic = up_or_down
    return new_config

if samples_name=='TTbar':
    for up_or_down in up_down:
        configs['top_pT_reweighting_{}'.format(up_or_down)] = config_top_pT_reweighting(up_or_down)

### DY pT reweighting

def config_DY_pT_reweighting(up_or_down):
    new_config = copy.deepcopy(nominal)
    for cfg in new_config.sequence:
        if cfg.name == 'httgenana':
            cfg.DY_systematic = up_or_down
    return new_config

if samples_name=='DY':
    for up_or_down in up_down:
        configs['DY_pT_reweighting_{}'.format(up_or_down)] = config_DY_pT_reweighting(up_or_down)

### MET recoil

def config_METrecoil(response_or_resolution, up_or_down):
    equivalency_dict = {'response':0,
                        'resolution':1,
                        'up':0,
                        'down':1}
    response_or_resolution = equivalency_dict[response_or_resolution]
    up_or_down = equivalency_dict[up_or_down]
    new_config = copy.deepcopy(nominal)
    for cfg in new_config.sequence:
        if cfg.name == 'PFMetana':
            cfg.METSys = [response_or_resolution, up_or_down]
    return new_config

response_or_resolution = ['response','resolution']

if not data:
    for sys in response_or_resolution:
        for up_or_down in up_down:
            configs['METrecoil_{}_{}'.format(sys,up_or_down)] = config_METrecoil(sys, up_or_down)

### MET unclustered uncertainty
from CMGTools.H2TauTau.heppy.sequence.common import pfmetana
def config_METunclustered(up_or_down):
    new_config = copy.deepcopy(nominal)
    for cfg in new_config.sequence:
        if cfg.name == 'PFMetana':
            cfg.unclustered_sys = up_or_down
    return new_config

if not data:
    for up_or_down in up_down:
        configs['METunclustered_{}'.format(up_or_down)] = config_METunclustered(up_or_down)

### tau energy scale 
from CMGTools.H2TauTau.heppy.sequence.common import tauenergyscale

def config_TauEnergyScale(dm_name, gm_name, up_or_down):
    tau_energyscale_ana_index = nominal.sequence.index(tauenergyscale)
    new_config = copy.deepcopy(nominal)

    tau_calibrator = cfg.Analyzer(
        Calibrator,
        src = 'taus',
        calibrator_factor_func = lambda x: getattr(x,'TES_{}_{}_{}'.format(gm_name,dm_name,up_or_down),1.)
    )

    new_config.sequence.insert(tau_energyscale_ana_index+1, tau_calibrator)
    return new_config

TES = [['HadronicTau','1prong0pi0'],
       ['HadronicTau','1prong1pi0'],
       ['HadronicTau','3prong0pi0'],
       ['HadronicTau','3prong1pi0'],
       ['promptMuon','1prong0pi0'],
       ['promptEle','1prong0pi0'],
       ['promptEle','1prong1pi0']]

TES_embed = [['HadronicTau','1prong0pi0'],
             ['HadronicTau','1prong1pi0'],
             ['HadronicTau','3prong0pi0']]

if (not data):
    for gm_name, dm_name in TES:
        configs['TES_{}_{}_up'.format(gm_name, dm_name)] = config_TauEnergyScale(dm_name, gm_name, 'up')
        configs['TES_{}_{}_down'.format(gm_name, dm_name)] = config_TauEnergyScale(dm_name, gm_name, 'down')

elif (data and embedded):
    for gm_name, dm_name in TES_embed:
        configs['TES_{}_{}_up'.format(gm_name, dm_name)] = config_TauEnergyScale(dm_name, gm_name, 'up')
        configs['TES_{}_{}_down'.format(gm_name, dm_name)] = config_TauEnergyScale(dm_name, gm_name, 'down')

### Jet energy scale
from CMGTools.H2TauTau.heppy.sequence.common import jets
def config_JetEnergyScale(group, up_or_down):
    jets_ana_index = nominal.sequence.index(jets)
    new_config = copy.deepcopy(nominal)

    jet_calibrator = cfg.Analyzer(
        Calibrator,
        src = 'jets',
        calibrator_factor_func = lambda x: getattr(x,"corr_{}_JEC_{}".format(group,up_or_down), 1./x.rawFactor()) * x.rawFactor()
    )

    new_config.sequence.insert(jets_ana_index+1, jet_calibrator)
    return new_config

JES = ['CMS_scale_j_eta0to5_13Tev',
       'CMS_scale_j_eta0to3_13TeV',
       'CMS_scale_j_eta3to5_13TeV',
       'CMS_scale_j_RelativeBal_13TeV',
       'CMS_scale_j_RelativeSample_13TeV']

if not data:
    for source in JES:
        configs['{}_up'.format(source)] = config_JetEnergyScale(source,'up')
        configs['{}_down'.format(source)] = config_JetEnergyScale(source,'down')

### BTagging
from CMGTools.H2TauTau.heppy.sequence.common import btagger
def config_Btagging(up_or_down):
    new_config = copy.deepcopy(nominal)
    for cfg in new_config.sequence:
        if cfg.name == 'btagger':
            cfg.sys = up_or_down
    return new_config

if not data:
    for up_or_down in up_down:
        configs['Btagging_{}'.format(up_or_down)] = config_Btagging(up_or_down)

# config = configs['Btagging_up']
# configs = {'Btagging_up':configs['Btagging_up'],'Btagging_down':configs['Btagging_down'],'nominal':nominal}

# config = configs['DY_pT_reweighting_up']
# configs = {'DY_pT_reweighting_up':configs['DY_pT_reweighting_up'],'DY_pT_reweighting_down':configs['DY_pT_reweighting_down'],'nominal':nominal}

# configs.pop('nominal')

# resubmit_configs = {'Btagging_up': configs['Btagging_up'],
#                     'TES_promptEle_1prong0pi0_up': configs['TES_promptEle_1prong0pi0_up']
# }

# resubmit_configs['Btagging_up'].components = [comp for comp in resubmit_configs['Btagging_up'].components if comp.name in ['WZ']]
# # resubmit_configs['TES_HadronicTau_1prong0pi0_up'].components = [comp for comp in resubmit_configs['TES_HadronicTau_1prong0pi0_up'].components if comp.name in ['WJetsToLNu_LO','WJetsToLNu_LO_ext','T_tWch','WW']]
# # resubmit_configs['TES_promptEle_1prong0pi0_down'].components = [comp for comp in resubmit_configs['TES_promptEle_1prong0pi0_down'].components if comp.name in ['TBar_tch','TBar_tWch','T_tch']]
# resubmit_configs['TES_promptEle_1prong0pi0_up'].components = [comp for comp in resubmit_configs['TES_promptEle_1prong0pi0_up'].components if comp.name in ['WZ']]


# configs = {'nominal': configs['nominal']}
# configs = resubmit_configs


# dirset = set()

# for dirpath, dirnames, filenames in os.walk('/gridgroup/cms/touquet/crab_submission_dirs/'):
#     for dirname in dirnames:
#         dirset.add(dirname)   

# newconfigs = {}

# for confname, conf in configs.iteritems():
#     print confname
#     print 'added comp:'
#     comps = []
#     for comp in conf.components:
#         if not any([(confname in d and comp.name in d) for d in dirset]):
#             print comp.name
#             comps.append(comp)
#     if comps:
#         newconf = copy.copy(conf)
#         newconf.components = comps
#         newconfigs[confname] = newconf

# configs = newconfigs

# print configs
