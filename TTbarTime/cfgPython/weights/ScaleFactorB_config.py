import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.HeppyCore.framework.config import printComps


test = getHeppyOption('test', False)

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
ComponentCreator.useLyonAAA = True

################################################################################
# Analyzers 
################################################################################
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount import SkimAnalyzerCount
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerAnalyzer
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
from CMGTools.H2TauTau.heppy.analyzers.Debugger import Debugger

json = cfg.Analyzer(JSONAnalyzer,
                    name='JSONAnalyzer',)

vertex = cfg.Analyzer(VertexAnalyzer,
                      name='VertexAnalyzer',
                      fixedWeight=1,
                      keepFailingEvents=True,
                      verbose=False)


################################################################################
# Components
################################################################################

from CMGTools.TTbarTime.proto.samples.fall17.ttbar2017 import mc_ttbar

events_to_pick = []
selectedComponents = mc_ttbar

import CMGTools.TTbarTime.proto.samples.fall17.ttbar2017 as backgrounds_forindex
from CMGTools.H2TauTau.proto.samples.component_index import ComponentIndex
bindex = ComponentIndex( backgrounds_forindex)

if test:
    cache = True
    comp = bindex.glob('signal_MC_dilep')[0]
    selectedComponents = [comp]
    comp.files = comp.files[:1]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1


################################################################################
################################################################################
from CMGTools.H2TauTau.heppy.analyzers.JetAnalyzer import JetAnalyzer
from CMGTools.H2TauTau.heppy.analyzers.JetCleaner import JetCleaner
from CMGTools.H2TauTau.heppy.analyzers.EventFilter import EventFilter
from CMGTools.H2TauTau.heppy.analyzers.Selector import Selector
from CMGTools.TTbarTime.heppy.analyzers.BJetEfficiencyCreator import BJetEfficiencyCreator

gt_mc = 'Fall17_17Nov2017_V32_MC'

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

btag = cfg.Analyzer(BJetEfficiencyCreator,
                    name='BJetEfficiencyCreator',
                    jets = 'jets_20_unclean')

sequence = cfg.Sequence([
# Analyzers
    json,
    vertex,
    jets,
    jets_20_unclean,
    btag
])


# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events)

printComps(config.components, True)
