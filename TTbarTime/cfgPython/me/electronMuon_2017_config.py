import os
import ROOT

import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import printComps
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.HeppyCore.framework.looper import Looper
from PhysicsTools.HeppyCore.framework.event import Event
Event.print_patterns = ['*taus*', 
                        '*muons*', 
                        '*electrons*', 
                        'veto_*', 
                        '*dileptons_*', 
                        '*jets*']

#import pdb; pdb.set_trace()

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
#ComponentCreator.useAAA = True
ComponentCreator.useLyonAAA = True

from CMGTools.H2TauTau.heppy.analyzers.Cleaner import Cleaner


import logging
logging.shutdown()
#reload(logging)
logging.basicConfig(level=logging.WARNING)



############################################################################
# Options
############################################################################

# Get all heppy options; set via "-o production" or "-o production=True"

# production = True run on batch, production = False run locally
test = getHeppyOption('test', True)
syncntuple = getHeppyOption('syncntuple', True)
data = getHeppyOption('data', False)
tes_string = getHeppyOption('tes_string', '') # '_tesup' '_tesdown'
reapplyJEC = getHeppyOption('reapplyJEC', True)


############################################################################
# Components
############################################################################
from CMGTools.TTbarTime.proto.samples.fall17.ttbar2017 import mc_ttbar
from CMGTools.TTbarTime.proto.samples.fall17.ttbar2017 import data_elecmuon
from CMGTools.TTbarTime.proto.samples.fall17.trigger import data_triggers
from CMGTools.TTbarTime.proto.samples.fall17.trigger import mc_triggers

events_to_pick = []

# Global Tag
gt_mc = 'Fall17_17Nov2017_V32_MC'
gt_data = 'Fall17_17Nov2017{}_V32_DATA'
#https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC


# PileUp
puFileData = '$CMSSW_BASE/src/CMGTools/TTbarTime/data/pudistributions_data_2017.root'
puFileMC = '$CMSSW_BASE/src/CMGTools/TTbarTime/data/pileup.root'

for sample in mc_ttbar:
    sample.triggers = mc_triggers
    sample.puFileMC = puFileMC
    sample.puFileData = puFileData
 
for sample in data_elecmuon:
    # sample.name[sample.name.find('2017')+4] are era A,B,C,D,E and F
    sample.triggers = data_triggers[sample.name[sample.name.find('2017')+4]]
    era = sample.name[sample.name.find('2017')+4]
    if 'V32' in gt_data and era in ['D','E']:
        era = 'DE'
    sample.dataGT = gt_data.format(era)

if (not data):
    selectedComponents = mc_ttbar
elif (data):
    selectedComponents = data_elecmuon

############################################################################
# Test
############################################################################
import CMGTools.TTbarTime.proto.samples.fall17.ttbar2017 as backgrounds_forindex
from CMGTools.TTbarTime.proto.samples.component_index import ComponentIndex
bindex = ComponentIndex( backgrounds_forindex)

if test:
    cache = True
    if (not data):
        comp = bindex.glob('MC_a_dilep')[0]
    else:
        comp = selectedComponents[9]
    selectedComponents = [comp]
    comp.files = [comp.files[0]]#10 bug on semilep
    comp.splitFactor = 1
    comp.fineSplitFactor = 1


############################################################################
# Analyzers 
############################################################################
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount import SkimAnalyzerCount
from CMGTools.TTbarTime.proto.analyzers.TriggerAnalyzer import TriggerAnalyzer
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
from CMGTools.TTbarTime.heppy.analyzers.Debugger import Debugger

json = cfg.Analyzer(JSONAnalyzer,
                    name='JSONAnalyzer',)

skim = cfg.Analyzer(SkimAnalyzerCount,
                    name='SkimAnalyzerCount')

trigger = cfg.Analyzer(TriggerAnalyzer,
                       name='TriggerAnalyzer',
                       addTriggerObjects=True,
                       requireTrigger=False,
                       usePrescaled=False)

vertex = cfg.Analyzer(VertexAnalyzer,
                      name='VertexAnalyzer',
                      fixedWeight=1,
                      keepFailingEvents=False,
                      verbose=False)


debugger = cfg.Analyzer(Debugger,
                        name = 'Debugger',
                        condition = lambda x: True)

############################################################################
# Time
############################################################################
from CMGTools.TTbarTime.heppy.analyzers.TimeAnalyzerARC import TimeAnalyzerARC

time = cfg.Analyzer(TimeAnalyzerARC,
                     name = 'TimeAnalyzer')

############################################################################
# Muon 
############################################################################
# setting up an alias for our isolation, now use iso_htt everywhere
from PhysicsTools.Heppy.physicsobjects.Muon import Muon
from CMGTools.TTbarTime.heppy.analyzers.MuonSFARC import MuonSFARC
from CMGTools.TTbarTime.heppy.analyzers.MuonAnalyzer import MuonAnalyzer
from CMGTools.TTbarTime.heppy.analyzers.EventFilter import EventFilter
from CMGTools.TTbarTime.heppy.analyzers.Selector import Selector

Muon.iso_htt = lambda x: x.relIso(0.4, 
                                  'dbeta', 
                                  dbeta_factor = 0.5, 
                                  all_charged = False)

muons = cfg.Analyzer(MuonAnalyzer,
                     name = 'MuonAnalyzer',
                     output = 'muons',
                     muons = 'slimmedMuons',)

def select_muon_function(muon): #boolean use to select good muons
    return muon.pt() > 20 and \
           abs(muon.eta()) < 2.4 and\
           muon.tightId() and\
           muon.iso_htt() < 0.15 
    # https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2

def exclude_muon_function(muon):
    return muon.pt() > 10 and \
           abs(muon.eta()) < 2.4 and\
           muon.looseId() and\
           muon.iso_htt() < 0.25 and\
           not(select_muon_function(muon))

select_muon = cfg.Analyzer(Selector,
                           'select_muon',
                           output = 'select_muon',
                           src = 'muons',
                           filter_func = select_muon_function)

exclude_muon = cfg.Analyzer(Selector,
                           'exclude_muon',
                           output = 'exclude_muon',
                           src = 'muons',
                           filter_func = exclude_muon_function)

reweight_muon = cfg.Analyzer(MuonSFARC, 
                             'reweight_muon', 
                             muons = 'select_muon')

one_muon = cfg.Analyzer(EventFilter, 
                        'one_muon',
                        src = 'select_muon',
                        filter_func = lambda x : len(x)>0)
                        
exclude_loose_muon = cfg.Analyzer(EventFilter,
                                 'exlude_loose_muon',
                                 src='exclude_muon',
                                 filter_func = lambda x : len(x)==0)
                        
############################################################################
# Electron 
############################################################################
# setting up an alias for our isolation, now use iso_htt everywhere
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsutils.EffectiveAreas import areas
from CMGTools.TTbarTime.heppy.analyzers.ElectronSFARC import ElectronSFARC
from CMGTools.TTbarTime.heppy.analyzers.ElectronAnalyzer import ElectronAnalyzer
from CMGTools.TTbarTime.heppy.analyzers.EventFilter import EventFilter
from CMGTools.TTbarTime.heppy.analyzers.Selector import Selector

Electron.EffectiveArea03 = areas['Fall17']['electron']

Electron.iso_htt = lambda x: x.relIso(0.3,
                                      "EA", #effective area
                                      all_charged=False)

electrons = cfg.Analyzer(ElectronAnalyzer,
                         output = 'electrons',
                         electrons = 'slimmedElectrons',) #name in MiniAOD


def is_out_gap_ECAL(electron):
    return abs(electron.superCluster().eta()) >= 1.5660 or\
           abs(electron.superCluster().eta()) <= 1.4442

def select_electron_function(electron): #function use in the next Analyzer
    return electron.pt() > 20 and\
           abs(electron.eta()) < 2.4 and\
           is_out_gap_ECAL(electron) and\
           electron.id_passes("cutBasedElectronID-Fall17-94X-V2","tight") 
           
def exclude_electron_function(electron): #function use in the next Analyzer
    return electron.pt() > 10 and\
           abs(electron.eta()) < 2.4 and\
           is_out_gap_ECAL(electron) and\
           electron.id_passes("cutBasedElectronID-Fall17-94X-V2","veto") and\
           not(select_electron_function(electron))

select_electron = cfg.Analyzer(Selector,
                               'select_electron',
                               output = 'select_electron',
                               src = 'electrons',
                               filter_func = select_electron_function)

exclude_electron = cfg.Analyzer(Selector,
                              'exclude_electron',
                              output = 'exclude_electron',
                              src = 'electrons',
                              filter_func = exclude_electron_function)
                         
reweight_electron = cfg.Analyzer(ElectronSFARC, 
                                 'reweight_electron', 
                                 electrons = 'select_electron')
                               
one_electron = cfg.Analyzer(EventFilter, 
                            'one_electron',
                            src = 'select_electron',
                            filter_func = lambda x : len(x)>0)

exclude_loose_electron = cfg.Analyzer(EventFilter,
                                     'exclude_loose_electron',
                                     src='exclude_electron',
                                     filter_func = lambda x : len(x)==0)
 
############################################################################
# Dilepton 
############################################################################
from CMGTools.TTbarTime.heppy.analyzers.DiLeptonAnalyzer import DiLeptonAnalyzer
from CMGTools.TTbarTime.heppy.analyzers.DilepTriggerSFARC import DilepTriggerSFARC
#DiLeptonAnalyzer change (rajout de fonction lead/sublead)
from CMGTools.TTbarTime.heppy.analyzers.Selector import Selector
from CMGTools.TTbarTime.heppy.analyzers.EventFilter import EventFilter


dilepton = cfg.Analyzer(DiLeptonAnalyzer,
                        output = 'dileptons',
                        l1 = 'select_muon',
                        l2 = 'select_electron',
                        dr_min = 0.5) #unspecified


def select_dilepton_function(dilep): #function use in the next Analyzer
    return dilep.mass() > 20 and \
           (dilep.leg1().charge() + dilep.leg2().charge()) == 0 and\
           ((dilep.leg1().pt()>25 and dilep.leg2().pt()>20) == True or\
           (dilep.leg1().pt()>20 and dilep.leg2().pt()>25) == True)

select_dilepton = cfg.Analyzer(Selector,
                         'select_dilepton',
                         output = 'select_dilepton',
                         src = 'dileptons',
                         filter_func = select_dilepton_function)

reweight_dilepton_trig = cfg.Analyzer(DilepTriggerSFARC, 
                                      'reweight_dilepton', 
                                      dilepton = 'select_dilepton')

only_one_dilepton = cfg.Analyzer(EventFilter, 
                            name = 'OneDilepton',
                            src = 'select_dilepton',
                            filter_func = lambda x : len(x)==1)

from CMGTools.H2TauTau.heppy.analyzers.Sorter import Sorter
#completely useless with 1 dilepton but in case of ..
dilepton_sorted = cfg.Analyzer(
    Sorter,
    output = 'dileptons_sorted',
    src = 'dileptons',
    metric = lambda x : x.pt(),
    reverse = False
    )

############################################################################
# Jets 
############################################################################
from CMGTools.TTbarTime.heppy.analyzers.JetAnalyzer import JetAnalyzer
from CMGTools.TTbarTime.heppy.analyzers.JetCleaner import JetCleaner
from CMGTools.TTbarTime.heppy.analyzers.EventFilter import EventFilter


def select_good_jets_FixEE2017(jet): #function use in the next Analyzer
    return jet.correctedJet("Uncorrected").pt() > 50. or\
           abs(jet.eta()) < 2.65 or\
           abs(jet.eta()) > 3.139

jets = cfg.Analyzer(JetAnalyzer, 
                    output = 'jets',
                    jets = 'slimmedJets',
                    do_jec = True,
                    gt_mc = gt_mc,
                    selection = select_good_jets_FixEE2017)

# From https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2017
def select_jets_IDpt(jet): #function use in the next Analyzer
    return  jet.pt()>20 and\
            abs(jet.eta())<2.4 and\
            jet.jetID("PAG_ttbarID_Loose")

jets_20_unclean = cfg.Analyzer(Selector,
                               'jets_20_unclean',
                               output = 'jets_20_unclean',
                               src = 'jets',
                               filter_func = select_jets_IDpt)

jet_20_electron_clean = cfg.Analyzer(JetCleaner,
                      output = 'jets_20_electron_clean',
                      leptons = 'select_electron',
                      jets = 'jets_20_unclean',
                      drmin = 0.4)
                      
jet_20_clean = cfg.Analyzer(JetCleaner,
                      output = 'jets_20_clean',
                      leptons = 'select_muon',
                      jets = 'jets_20_electron_clean',
                      drmin = 0.4)

jets_30 = cfg.Analyzer(Selector,
                       'jets_30',
                       output = 'jets_30',
                       src = 'jets_20_clean',
                       filter_func = lambda x : x.pt()>30)
                       
two_jets = cfg.Analyzer(EventFilter, 
                        name = 'TwoJets',
                        src = 'jets_30',
                        filter_func = lambda x : len(x)>1)

############################################################################
# b-Jets 
############################################################################
from CMGTools.TTbarTime.heppy.analyzers.BJetAnalyzerARC import BJetAnalyzerARC
from CMGTools.TTbarTime.heppy.analyzers.EventFilter import EventFilter


btagger = cfg.Analyzer(BJetAnalyzerARC, 
                       'btagger', 
                       jets = 'jets_30')

one_bjets = cfg.Analyzer(EventFilter, 
                         name = 'OneBJets',
                         src = 'bjets_30',
                         filter_func = lambda x : len(x)>0)

#always put after btagger
bjets_30 = cfg.Analyzer(Selector, 
                        'bjets_30',
                        output = 'bjets_30', 
                        src = 'jets_30',
                        filter_func = lambda x: x.is_btagged)

############################################################################
# Generator stuff 
############################################################################
from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer import LHEWeightAnalyzer
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer import PileUpAnalyzer
from CMGTools.TTbarTime.heppy.analyzers.MCWeighter import MCWeighter
from CMGTools.TTbarTime.proto.analyzers.NJetsAnalyzer import NJetsAnalyzer
from CMGTools.TTbarTime.heppy.analyzers.METAnalyzer import METAnalyzer
from CMGTools.TTbarTime.heppy.analyzers.GenAnalyzer import GenAnalyzer

pfmetana = cfg.Analyzer(METAnalyzer,
                        name='PFMetana',
                        recoil_correction_file='HTT-utilities/RecoilCorrections/data/Type1_PFMET_2017.root',
                        met = 'pfmet',
                        apply_recoil_correction= True,#Recommendation states loose pfjetID for jet multiplicity but this WP is not supported anymore?
                        runFixEE2017= True)

lheweight = cfg.Analyzer(LHEWeightAnalyzer,
                         name="LHEWeightAnalyzer",
                         useLumiInfo=False)

pileup = cfg.Analyzer(PileUpAnalyzer,
                      name='PileUpAnalyzer',
                      true=True,
                      autoPU=False)

mcweighter = cfg.Analyzer(MCWeighter,
                          'MCWeighter')

njets_ana = cfg.Analyzer(NJetsAnalyzer,
                         name='NJetsAnalyzer',
                         fillTree=True,
                         verbose=False)


############################################################################
# Ntuples 
############################################################################
from CMGTools.TTbarTime.heppy.analyzers.NtupleProducer import NtupleProducer
from CMGTools.TTbarTime.heppy.ntuple.NtupleCreator import common as event_content_test

ntuple = cfg.Analyzer(NtupleProducer,
                      name = 'NtupleProducer',
                      outputfile = 'events.root',
                      treename = 'events',
                      event_content = event_content_test)

sequence = cfg.Sequence([
# Analyzers
    json,
    vertex,
# Time
    time,
# Muon
    muons,
    select_muon,
    exclude_muon,
    reweight_muon,
    one_muon,
    exclude_loose_muon,
# Electron
    electrons,
    select_electron,
    exclude_electron,
    reweight_electron,
    one_electron,
    exclude_loose_electron,
# Dilepton
    dilepton,
    select_dilepton,
    only_one_dilepton,
    reweight_dilepton_trig,
    dilepton_sorted,
# Jets
    jets,
    jets_20_unclean,
    jet_20_electron_clean,
    jet_20_clean,
    jets_30,
    two_jets,
# b-Jets
    btagger,
    bjets_30,
    one_bjets,
# Rescaling
    trigger, 
    # trigger_match,
    # met_filters,
    lheweight,
    pileup, 
    njets_ana,
# Mets
    pfmetana,
# Ntuple
    #debugger,
    ntuple
])


############################################################################
from PhysicsTools.Heppy.analyzers.core.EventSelector import EventSelector

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
                    events_class=Events)

printComps(config.components, True)


