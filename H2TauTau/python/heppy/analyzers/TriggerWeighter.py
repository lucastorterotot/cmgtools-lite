from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from ROOT import TFile

class TriggerWeighter(Analyzer):
    '''Adds the trigger weight(s) to the given legs of the event.
    '''
    
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(TriggerWeighter, self).__init__(cfg_ana, cfg_comp, looperName)
        self.wsfile = TFile(self.cfg_ana.workspace_path)
        self.ws = self.wsfile.Get('w')

    def process(self, event):
        if self.cfg_comp.isData:
            return True
        
        try:
            legs = self.cfg_ana.legs(event)
        except AttributeError:
            print 'did not define what legs are to be used for trigger weights!'
            raise

        for index, leg in enumerate(legs):
            weight_trigger = 1
            num = index+1
            if hasattr(leg, 'trigtypes'):
                for triggertype in leg.trigtypes:
                    leg_vars_dict = getattr(self.cfg_ana,'leg'+str(num)+'_vars_dict')
                    leg_func_dict = getattr(self.cfg_ana,'leg'+str(num)+'_func_dict')
                    if triggertype in leg_func_dict.keys():
                        for name, func in leg_vars_dict.iteritems():
                            self.ws.var(name).setVal(func(leg))
                        val = self.ws.function(leg_func_dict[triggertype]).getVal()
                        weight_trigger *= val
                        setattr(leg, 'weight_trigger_'+str(triggertype), val)

            setattr(leg, 'weight_trigger', weight_trigger)
