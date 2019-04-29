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

        leg1 = legs[0]
        for name, func in self.cfg_ana.leg1_vars_dict.iteritems():
            self.ws.var(name).setVal(func(leg1))
        val = self.ws.function(self.cfg_ana.leg1_func_name).getVal()
        setattr(leg1, 'weight_trigger', val)

        if len(legs)==2:
            leg2 = legs[1]
            for name, func in self.cfg_ana.leg2_vars_dict.iteritems():
                self.ws.var(name).setVal(func(leg2))
            val = self.ws.function(self.cfg_ana.leg2_func_name).getVal()
            setattr(leg2, 'weight_trigger', val)
