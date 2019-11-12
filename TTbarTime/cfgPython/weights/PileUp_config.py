from CMGTools.TTbarTime.heppy.analyzers.PileUpARC import PileUpAnalyzerARC
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption
from PhysicsTools.HeppyCore.framework.config import printComps

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
ComponentCreator.useAAA = True


################################################################################
# Components
################################################################################

from CMGTools.TTbarTime.proto.samples.fall17.ttbar2017 import mc_ttbar

events_to_pick = []

selectedComponents = mc_ttbar

################################################################################
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

