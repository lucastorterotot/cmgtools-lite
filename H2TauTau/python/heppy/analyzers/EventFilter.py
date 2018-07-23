'''Filter events based on the number of objects in the input collection.'''

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.statistics.counter import Counter

class EventFilter(Analyzer):
    '''Filters events based on the contents of an input collection.
    
    When an event is rejected by the EventFilter, the analyzers
    placed after the filter in the sequence will not run. 

    Example: 

    To reject events with 1 lepton or more: 

    from heppy.analyzers.EventFilter   import EventFilter  
    lepton_filter = cfg.Analyzer(
      EventFilter  ,
      'lepton_filter',
      src = 'leptons',
      filter_func = lambda x: len(x) == 0, 
      output = 'lepton_filter_passed' # optional
    )
    
    * src : the input collection.

    * filter_func : filtering function, acting on the collection

    * output (optional): if provided this flag will be set on the event,
       and event processing will continue, even if the event is rejected
    '''

    def beginLoop(self, setup):
        super(EventFilter, self).beginLoop(setup)
        self.counters.addCounter('efficiency')
        self.counters['efficiency'].register('All events')
        self.counters['efficiency'].register('Selected')
        
    def process(self, event):
        '''event should contain:
        
        * self.cfg_ana.collection:
           the collection used to take a decision
        '''
        coll = getattr(event, self.cfg_ana.src)
        passed = self.cfg_ana.filter_func(coll) 
        self.counters['efficiency'].inc('All events')
        if passed: 
            self.counters['efficiency'].inc('Selected')
        if hasattr(self.cfg_ana, 'output'):
            setattr(event, self.cfg_ana.output, passed)
        else: 
            return passed 
