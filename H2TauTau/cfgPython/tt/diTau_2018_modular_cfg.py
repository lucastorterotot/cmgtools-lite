import os

import ROOT

import PhysicsTools.HeppyCore.framework.config as cfg

from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
ComponentCreator.useLyonAAA = True

import logging
logging.shutdown()
reload(logging)
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
tes_string = getHeppyOption('tes_string', '') # '_tesup' '_tesdown'
reapplyJEC = getHeppyOption('reapplyJEC', True)
correct_recoil = getHeppyOption('correct_recoil', True)
# For specific studies
add_iso_info = getHeppyOption('add_iso_info', False)
add_tau_fr_info = getHeppyOption('add_tau_fr_info', False)

###############
# global tags
###############

from CMGTools.H2TauTau.heppy.sequence.common import gt_mc, gt_data

###############
# Components
###############

from CMGTools.RootTools.utils.splitFactor import splitFactor
from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex
import CMGTools.H2TauTau.proto.samples.fall17.higgs as higgs
index=ComponentIndex(higgs)

from CMGTools.H2TauTau.proto.samples.fall17.data import data_tau
from CMGTools.H2TauTau.proto.samples.fall17.higgs_susy import mssm_signals
from CMGTools.H2TauTau.proto.samples.fall17.higgs import sync_list
from CMGTools.H2TauTau.proto.samples.fall17.backgrounds import backgrounds
from CMGTools.H2TauTau.proto.samples.fall17.triggers_tauTau import mc_triggers, mc_triggerfilters
from CMGTools.H2TauTau.proto.samples.fall17.triggers_tauTau import data_triggers, data_triggerfilters
from CMGTools.H2TauTau.htt_ntuple_base_cff import puFileData, puFileMC

mc_list = backgrounds + sync_list + mssm_signals
data_list = data_tau

n_events_per_job = 1e5

for sample in mc_list:
    sample.triggers = mc_triggers
    sample.triggerobjects = mc_triggerfilters
    sample.splitFactor = splitFactor(sample, n_events_per_job)
    sample.puFileData = puFileData
    sample.puFileMC = puFileMC

for sample in data_list:
    sample.triggers = data_triggers
    sample.triggerobjects = data_triggerfilters
    sample.splitFactor = splitFactor(sample, n_events_per_job)
    sample.dataGT = gt_data.format(sample.name[sample.name.find('2017')+4])

selectedComponents = data_list if data else backgrounds + mssm_signals


if test:
    cache = True
    comp = index.glob('HiggsVBF125')[0]
    #comp.files = comp.files[:1]
    #comp.splitFactor = 1
    #comp.fineSplitFactor = 1
    selectedComponents = [comp]
    #comp.files = ['file1.root']

events_to_pick = []

from CMGTools.H2TauTau.heppy.sequence.common import debugger
debugger.condition = None # lambda event : len(event.sel_taus)>2
###############
# Analyzers 
###############

from CMGTools.H2TauTau.heppy.sequence.common import metana
if correct_recoil:
    metana.apply = True

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

from CMGTools.H2TauTau.heppy.analyzers.TauIDWeighter import TauIDWeighter
tauidweighter = cfg.Analyzer(
    TauIDWeighter,
    'TauIDWeighter',
    taus = lambda event: [event.dileptons_sorted[0].leg1(),event.dileptons_sorted[0].leg2()]
)

from CMGTools.H2TauTau.heppy.analyzers.FakeFactorAnalyzer import FakeFactorAnalyzer
fakefactor = cfg.Analyzer(
    FakeFactorAnalyzer,
    'FakeFactorAnalyzer',
    channel = 'tt',
    filepath = '$CMSSW_BASE/src/HTTutilities/Jet2TauFakes/data/MSSM2016/20170628_medium/{}/{}/fakeFactors_20170628_medium.root',
    met = 'pfmet'
)

# ntuple ================================================================

from CMGTools.H2TauTau.heppy.analyzers.NtupleProducer import NtupleProducer
from CMGTools.H2TauTau.heppy.ntuple.ntuple_variables import tautau as event_content_tautau
ntuple = cfg.Analyzer(
    NtupleProducer,
    name = 'NtupleProducer',
    outputfile = 'events.root',
    treename = 'events',
    event_content = event_content_tautau
)

from CMGTools.H2TauTau.heppy.sequence.common import sequence_beforedil, sequence_afterdil
sequence = sequence_beforedil
sequence.extend( sequence_dilepton )
sequence.extend( sequence_afterdil )
if data:
    sequence.append(fakefactor)
sequence.append(tauidweighter)
sequence.append(ntuple)

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

