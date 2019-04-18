from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
import collections

class Sorter(Analyzer):
    '''Sort objects according to a given criterion

    Example::
        leptons = cfg.Analyzer(
          Sorter,
          'sorted_leptons',
          output = 'sorted_leptons',
          src = 'leptons',
          metric = lambda x : x.pt()
          reverse = True
          )
    
    This sorts the leptons by decreasing pT

    @param src: the input collection.

    @param output: the output collection.

    @param metric: a function object, giving the key on which to sort

    @param reverse: sort in reverse order
    '''

    def process(self, event):
        '''event must contain
        
        * self.cfg_ana.src: collection of objects to be selected
           These objects must be usable by the metric function
           self.cfg_ana.metric.
        '''
        input_collection = getattr(event, self.cfg_ana.src)
        output_collection = sorted(input_collection, 
                                   key=self.cfg_ana.metric,
                                   reverse=self.cfg_ana.reverse)
        setattr(event, self.cfg_ana.output, output_collection)
