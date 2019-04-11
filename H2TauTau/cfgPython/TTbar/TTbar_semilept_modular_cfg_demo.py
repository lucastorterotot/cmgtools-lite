import os

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
ComponentCreator.useLyonAAA = True

import logging
logging.shutdown()
#reload(logging)
logging.basicConfig(level=logging.WARNING)

from PhysicsTools.HeppyCore.framework.event import Event
Event.print_patterns = ['*taus*', '*muons*', '*electrons*', 'veto_*', 
                        '*dileptons_*', '*jets*']

###############
# Options
###############

# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False run locally
test = getHeppyOption('test', True)
syncntuple = getHeppyOption('syncntuple', True)
data = getHeppyOption('data', False)
embedded = getHeppyOption('embedded', False)
if embedded:
    data = True
tes_string = getHeppyOption('tes_string', '') # '_tesup' '_tesdown'
reapplyJEC = getHeppyOption('reapplyJEC', True)
# For specific studies
add_iso_info = getHeppyOption('add_iso_info', False)
add_tau_fr_info = getHeppyOption('add_tau_fr_info', False)

###############
# global tags
###############

from CMGTools.H2TauTau.heppy.sequence.common import gt_mc, gt_data, gt_embed

###############
# Components
###############

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex
import CMGTools.H2TauTau.proto.samples.fall17.higgs as higgs
index=ComponentIndex(higgs)

import CMGTools.H2TauTau.proto.samples.fall17.data as data_forindex
dindex = ComponentIndex(data_forindex)

from CMGTools.H2TauTau.proto.samples.fall17.higgs_susy import mssm_signals
from CMGTools.H2TauTau.proto.samples.fall17.higgs import sync_list
import CMGTools.H2TauTau.proto.samples.fall17.backgrounds as backgrounds_forindex
bindex = ComponentIndex( backgrounds_forindex)
backgrounds = backgrounds_forindex.backgrounds
import CMGTools.H2TauTau.proto.samples.fall17.embedded as embedded_forindex
eindex = ComponentIndex( embedded_forindex)
from CMGTools.H2TauTau.proto.samples.fall17.triggers_tauMu import mc_triggers, mc_triggerfilters, embed_triggers, embed_triggerfilters
from CMGTools.H2TauTau.proto.samples.fall17.triggers_tauMu import data_triggers, data_triggerfilters
from CMGTools.H2TauTau.heppy.sequence.common import puFileData, puFileMC

mc_list = backgrounds + sync_list + mssm_signals
data_list = data_forindex.data_single_muon
embedded_list = embedded_forindex.embedded_mt

n_events_per_job = 1e5

for sample in mc_list:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, n_events_per_job)
    sample.puFileData = puFileData
    sample.puFileMC = puFileMC
    sample.channel = 'mt'

for sample in data_list+embedded_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, n_events_per_job)
    era = sample.name[sample.name.find('2017')+4]
    if 'V32' in gt_data and era in ['D','E']:
        era = 'DE'
    sample.dataGT = gt_data.format(era)

for sample in embedded_list:
    sample.triggerobjects = embed_triggerfilters

for sample in embedded_list:
    sample.isEmbed = True

selectedComponents = backgrounds + mssm_signals
if data:
    selectedComponents = data_list
    if embedded:
        selectedComponents = embedded_list


if test:
    cache = True
    # comp = index.glob('HiggsVBF125')[0]
    # comp = eindex.glob('Embedded2017B_mt')[0]
    comp = bindex.glob('TTSemi_pow')[0]
    selectedComponents = [comp]
    comp.files = comp.files[:1]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1
    # comp.files = ['/home/cms/torterotot/CMSSW-MET/CMSSW_9_4_11_cand1/src/JetMETCorrections/Type1MET/test/metv2.root']

events_to_pick = []

from CMGTools.H2TauTau.heppy.sequence.common import debugger
debugger.condition = None # lambda event : len(event.sel_taus)>2

###############
# Analyzers 
###############

from CMGTools.H2TauTau.heppy.analyzers.Selector import Selector
def select_tau(tau):
    return tau.pt()    >= 23  and \
        abs(tau.eta()) <= 2.3 and \
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
one_tau = cfg.Analyzer(
    EventFilter, 
    'one_tau',
    src = 'sel_taus',
    filter_func = lambda x : len(x)>0
)

def select_muon(muon):
    return muon.pt()    >= 21  and \
        abs(muon.eta()) <= 2.1 and \
        abs(muon.dxy()) < 0.045 and \
        abs(muon.dz())  < 0.2 and \
        muon.isMediumMuon()  # muon.muonID("POG_ID_Medium")
sel_muons = cfg.Analyzer(
    Selector, 
    'sel_muons',
    output = 'sel_muons',
    src = 'muons',
    filter_func = select_muon
)

one_muon = cfg.Analyzer(
    EventFilter, 
    'one_muon',
    src = 'sel_muons',
    filter_func = lambda x : len(x)>0
)

# dilepton veto ==============================================================

def select_muon_dilepton_veto(muon):
    return muon.pt() > 15             and \
        abs(muon.eta()) < 2.4         and \
        muon.isLooseMuon()            and \
        abs(muon.dxy()) < 0.045       and \
        abs(muon.dz())  < 0.2         and \
        muon.iso_htt() < 0.3
sel_muons_dilepton_veto = cfg.Analyzer(
    Selector,
    'dileptonveto_muons',
    output = 'sel_muons_dilepton_veto',
    src = 'muons',
    filter_func = select_muon_dilepton_veto
)

from  CMGTools.H2TauTau.heppy.analyzers.DiLeptonVeto import DiLeptonVeto
dilepton_veto = cfg.Analyzer(
    DiLeptonVeto,
    output = 'veto_dilepton_passed',
    src = 'sel_muons_dilepton_veto',
    drmin = 0.15
)

# mu tau pair ================================================================

from CMGTools.H2TauTau.heppy.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer

dilepton = cfg.Analyzer(
    DiLeptonAnalyzer,
    output = 'dileptons',
    l1 = 'sel_muons',
    l2 = 'sel_taus',
    dr_min = 0.5
)

from CMGTools.H2TauTau.heppy.analyzers.Sorter import Sorter
dilepton_sorted = cfg.Analyzer(
    Sorter,
    output = 'dileptons_sorted',
    src = 'dileptons',
    # sort by mu iso, mu pT, tau iso, tau pT
    metric = lambda dl: (dl.leg1().iso_htt(), 
                         -dl.leg1().pt(), 
                         -dl.leg2().tauID('byIsolationMVArun2017v2DBoldDMwLTraw2017'), 
                         -dl.leg2().pt()),
    reverse = False
    )



sequence_dilepton = cfg.Sequence([
        sel_taus,
        one_tau,
        sel_muons,
        one_muon,
        sel_muons_dilepton_veto,
        dilepton_veto,
        dilepton,
        dilepton_sorted,
        ])

# weights ================================================================

from CMGTools.H2TauTau.heppy.analyzers.TauIDWeighter import TauIDWeighter
tauidweighter = cfg.Analyzer(
    TauIDWeighter,
    'TauIDWeighter',
    taus = lambda event: [event.dileptons_sorted[0].leg2()]
)

# from CMGTools.H2TauTau.heppy.analyzers.FakeFactorAnalyzer import FakeFactorAnalyzer
# fakefactor = cfg.Analyzer(
#     FakeFactorAnalyzer,
#     'FakeFactorAnalyzer',
#     channel = 'mt',
#     filepath = '$CMSSW_BASE/src/HTTutilities/Jet2TauFakes/data/MSSM2016/20170628_medium/{}/{}/fakeFactors_20170628_medium.root',
#     met = 'pfmet'
# )

# embedded ================================================================

from CMGTools.H2TauTau.heppy.analyzers.EmbeddedAnalyzer import EmbeddedAnalyzer
embedded_ana = cfg.Analyzer(
    EmbeddedAnalyzer,
    name = 'EmbeddedAnalyzer',
    channel = 'mt'
)


# ntuple ================================================================

from CMGTools.H2TauTau.heppy.analyzers.NtupleProducer import NtupleProducer
from CMGTools.H2TauTau.heppy.ntuple.ntuple_variables import mutau as event_content_mutau
ntuple = cfg.Analyzer(
    NtupleProducer,
    name = 'NtupleProducer',
    outputfile = 'events.root',
    treename = 'events',
    event_content = event_content_mutau
)

from CMGTools.H2TauTau.heppy.sequence.common import sequence_beforedil, sequence_afterdil, trigger, met_filters, trigger_match
sequence = sequence_beforedil
sequence.extend( sequence_dilepton )
sequence.extend( sequence_afterdil )
if embedded:
    sequence.append(embedded_ana)
# if data:
#     sequence.append(fakefactor)
sequence.append(tauidweighter)
sequence.append(ntuple)

if embedded:
    sequence = [x for x in sequence if x.name not in ['JSONAnalyzer']]
    # trigger.triggerResultsHandle = ['TriggerResults','','SIMembedding']

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

