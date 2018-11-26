'''Filter events based on trigger matching.'''

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.statistics.counter import Counter

class TriggerFilter(Analyzer):
    '''Filters events based on the contents of an input collection.
    
    When an event is rejected by the TriggerFilter, the analyzers
    placed after the filter in the sequence will not run. 

    Example: 

    To reject events with :
      (SingleMu24 and pt_1>25)
      or (SingleMu27 and pt_1>28)
      or (Mu20Tau27 and pt_1>21 and pt_1<25 and pt_2>32 and |eta_2|<2.1),
    including trigger matching 
    
    * src : the input collection.

    * filter_func : filtering function, acting on the collection

    * output (optional): if provided this flag will be set on the event,
       and event processing will continue, even if the event is rejected
    '''

    def beginLoop(self, setup):
        super(TriggerFilter, self).beginLoop(setup)
        self.counters.addCounter('efficiency')
        self.counters['efficiency'].register('All events')
        self.counters['efficiency'].register('Selected')
        
    def process(self, event):
        self.counters['efficiency'].inc('All events')
        
        coll1 = getattr(event, self.cfg_ana.src1)
        coll2 = getattr(event, self.cfg_ana.src2)
        out1 = []
        out2 = []
        for ptc1 in coll1:
            for ptc2 in coll2:
                passed = self.cfg_ana.filter_func(ptc1, ptc2)
                if passed and ptc1 not in out1:
                    out1.append(ptc1)
                if passed and ptc2 not in out2:
                    out2.append(ptc2)
        if len(out1) > 0 and len(out2) > 0 :
            self.counters['efficiency'].inc('Selected')
        if hasattr(self.cfg_ana, 'output1'):
            setattr(event, self.cfg_ana.output1, out1)
        if hasattr(self.cfg_ana, 'output2'):
            setattr(event, self.cfg_ana.output2, out2)
        else: 
            return (len(out1) > 0 and len(out2) > 0)
