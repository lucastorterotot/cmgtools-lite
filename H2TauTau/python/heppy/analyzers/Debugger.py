from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

class Debugger(Analyzer):
    '''Uses pdb debugger to stop at the end of an event.
    It is possible to make a conditionnal stop using the
    [condition] argument.

    Example::
         has_3_cleaned_muons_debugger = cfg.Analyzer(
           Debugger,
           'has_3_cleaned_muons_debugger',
           condition = lambda x : [getattr(x,'dileptons_sorted')[0].leg1(),
           getattr(x,'dileptons_sorted')[0].leg2()]
         )

    @param condition: conditionnal argument, function that takes 
        event as only parameter and returns a boolean. If returns
        True, pdb.set_trace() is called for this event.
    '''


    def process(self, event):
        if hasattr(self.cfg_ana, 'condition') and self.cfg_ana.condition:
            if self.cfg_ana.condition(event):
                import pdb;pdb.set_trace()
            else:
                return True
        else:
            # if condition is not set, or is None, do nothing
            return True
