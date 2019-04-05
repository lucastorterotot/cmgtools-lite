from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

class Calibrator(Analyzer):
    '''Calibrates objects from the src collection
    using their attribute named calibration_factor_name. Then
    re-orders the collection with given ordering criteria.
    !!! This modifies the src collection, as it
    is useful in the case of systematic shifts.

    @param src: the input collection.
        If a dictionary, the filtering function is applied to the dictionary values,
        and not to the keys.

    @param calibrator_factor_func: function that takes one of the object as only argument, and returns the calibration factor to be applied.

    @param sorting_func: optional parameter, a function that returns the values on which the collection is re-ordered after calibration. By default this will be the object's pt().

    @param sorting_reverse: optional parameter, a boolean whether or not the sorting should be reversed.
    '''

    def process(self, event):
        '''event must contain self.cfg_ana.src: collection of objects to be selected
        '''
        src_collection = getattr(event, self.cfg_ana.src)
        for obj in src_collection:
            calib = self.cfg_ana.calibrator_factor_func(obj)
            obj.scaleEnergy(calib)
        if hasattr(self.cfg_ana, 'sorting_func'):
            key = self.cfg_ana.sorting_func
            if hasattr(self.cfg_ana,'sorting_reverse'):
                reverse = self.cfg_ana.sorting_reverse
        else:
            key = lambda x : x.pt()
            reverse = True
        src_collection.sort(key = key, reverse = reverse)
        if not src_collection:
            src_collection = []
        setattr(event, self.cfg_ana.src, src_collection)
