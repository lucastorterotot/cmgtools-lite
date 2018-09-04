from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
import collections

class Cleaner(Analyzer):
    '''Select objects from the input_objects collection 
    that are not in the mask collection and store them 
    in the output collection. The objects are not copied
    in the process. 

    Example::
         sel_muons_third_lepton_veto_cleaned = cfg.Analyzer(
           Cleaner,
           '3lepv_muons_cleaner',
           output = 'sel_muons_third_lepton_veto_cleaned',
           src = 'sel_muons_third_lepton_veto',
           mask = lambda x : [getattr(x,'dileptons_sorted')[0].leg1(),
                              getattr(x,'dileptons_sorted')[0].leg2()]
         )

    @param src: the input collection.
        If a dictionary, the filtering function is applied to the dictionary values,
        and not to the keys.

    @param output: the output collection.

    @param mask: If a string: used as name of mask collection.
        If a function: used on event and should return the mask collection.
    '''

    def process(self, event):
        '''event must contain
        
        * self.cfg_ana.src: collection of objects to be selected
        * self.cfg_ana.mask: either collection of object to be used as mask or function to be evaluated on event to retrieve the collection of object to be used as mask
        '''
        input_collection = getattr(event, self.cfg_ana.src)
        if isinstance(self.cfg_ana.mask, basestring):
            mask = getattr(event, self.cfg_ana.mask)
        else:
            mask = self.cfg_ana.mask(event)
        output_collection = None
        if isinstance(input_collection, collections.Mapping):
            output_collection = dict( [(key, val) for key, val in input_collection.iteritems()
                                       if val not in mask] ) 
        else:
            output_collection = [obj for obj in input_collection \
                                 if obj not in mask]
        setattr(event, self.cfg_ana.output, output_collection)
