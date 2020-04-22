from CMGTools.TTbarTime.heppy.analyzers.PileUpARC import PileUpAnalyzerARC
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.HeppyCore.framework.config import printComps

test       = getHeppyOption('test', False)
year       = getHeppyOption('year', '2016' )

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
ComponentCreator.useAAA = True


################################################################################
# Components
################################################################################

if (year == '2016'):
    from CMGTools.TTbarTime.proto.samples.summer16.ttbar2016 import mc_ttbar_test as mc_ttbar
else:
    from CMGTools.TTbarTime.proto.samples.fall17.ttbar2017 import mc_ttbar

events_to_pick = []

selectedComponents = mc_ttbar
################################################################################

############################################################################
# Test
############################################################################
if(year == '2016'):    
    import CMGTools.TTbarTime.proto.samples.summer16.ttbar2016 as backgrounds_forindex
if(year == '2017'):
    import CMGTools.TTbarTime.proto.samples.fall17.ttbar2017 as backgrounds_forindex    
from CMGTools.TTbarTime.proto.samples.component_index import ComponentIndex
bindex = ComponentIndex(backgrounds_forindex)

if test:
    cache = True
    comp = bindex.glob('MC_a_dilep')[0]
    selectedComponents = [comp]
    comp.files = [comp.files[0]]
    comp.splitFactor = 1
    comp.fineSplitFactor = 1

################################################################################


pu = cfg.Analyzer(PileUpAnalyzerARC,
                    name='PileUpARC')


from CMGTools.H2TauTau.heppy.analyzers.NtupleProducer import NtupleProducer
from CMGTools.TTbarTime.heppy.ntuple.NtupleCreator import pileup

ntuple = cfg.Analyzer(NtupleProducer,
                      name = 'NtupleProducer',
                      outputfile = 'events.root',
                      treename = 'events',
                      event_content = pileup)


sequence = cfg.Sequence([
    pu,
    ntuple
])


# the following is declared in case this cfg is used in input to the
# heppy.py script
from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config(components=selectedComponents,
                    sequence=sequence,
                    services=[],
                    events_class=Events)

printComps(config.components, True)

