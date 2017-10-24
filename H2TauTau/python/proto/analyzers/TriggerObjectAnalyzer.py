from itertools import product

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR

import PhysicsTools.HeppyCore.framework.config as cfg


class TriggerObjectAnalyzer(Analyzer):

    def __init__(self, *args, **kwargs):
        super(TriggerObjectAnalyzer, self).__init__(*args, **kwargs)

    def beginLoop(self, setup):
        super(TriggerObjectAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('TriggerObjectAnalyzer')
        count = self.counters.counter('TriggerObjectAnalyzer')
        count.register('all events')

    def declareHandles(self):
        super(TriggerObjectAnalyzer, self).declareHandles()

        self.getter = self.cfg_ana.getter

        if hasattr(self.cfg_ana, 'triggerResultsHandle'):
            myhandle = self.cfg_ana.triggerResultsHandle
            self.handles['triggerResultsHLT'] = AutoHandle(
                (myhandle[0], myhandle[1], myhandle[2]),
                'edm::TriggerResults'
            )
        else:
            self.handles['triggerResultsHLT'] = AutoHandle(
                ('TriggerResults', '', 'HLT'),
                'edm::TriggerResults'
            )

        if hasattr(self.cfg_ana, 'triggerObjectsHandle'):
            myhandle = self.cfg_ana.triggerObjectsHandle
            self.handles['triggerObjects'] = AutoHandle(
                (myhandle[0], myhandle[1], myhandle[2]),
                'std::vector<pat::TriggerObjectStandAlone>'
            )
        else:
            self.handles['triggerObjects'] = AutoHandle(
                'selectedPatTrigger',
                'std::vector<pat::TriggerObjectStandAlone>'
            )

    def process(self, event):
        self.readCollections(event.input)

        triggerObjects = self.handles['triggerObjects'].product()
        triggerBits = self.handles['triggerResultsHLT'].product()

        names = event.input.object().triggerNames(triggerBits)

        legs = self.getter(event)

        for leg in legs:
            for to in triggerObjects:
                if deltaR(to, leg) >= self.cfg_ana.dR:
                    continue

                to.unpackPathNames(names)

                for filter in self.cfg_ana.filters:
                    if filter in to.filterLabels():
                        setattr(leg, filter, to)
        return True

setattr(TriggerObjectAnalyzer, 'defaultConfig',
        cfg.Analyzer(
            class_object=TriggerObjectAnalyzer,
            filters=['hltL2IsoTau26eta2p2', 'hltL2Tau26eta2p2', 'hltL2TauIsoFilter', 'hltL2TauJetsIso'],
            getter=lambda event: [event.leg2],
            dR=0.5
        )
        )
