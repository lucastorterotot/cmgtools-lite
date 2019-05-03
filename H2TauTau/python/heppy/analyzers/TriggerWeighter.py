from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from ROOT import TFile

class TriggerWeighter(Analyzer):
    '''Adds the trigger weight(s) to the given legs of the event.

    Example:
    ws_tau_vars_dict = {'t_pt':lambda tau:tau.pt(),
                        't_eta':lambda tau:tau.eta(),
                        't_phi':lambda tau:tau.phi()}
    ws_tau_func_dict = {'tt':'t_trg_tight_tt_ratio'}
    from CMGTools.H2TauTau.heppy.analyzers.TriggerWeighter import TriggerWeighter
    triggerweighter = cfg.Analyzer(
        TriggerWeighter,
        'TriggerWeighter',
        workspace_path = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_2017_v2.root',
        legs = lambda event: [event.dileptons_sorted[0].leg1(),event.dileptons_sorted[0].leg2()],
        leg1_vars_dict = ws_tau_vars_dict,
        leg2_vars_dict = ws_tau_vars_dict,
        leg1_func_dict = ws_tau_func_dict,
        leg2_func_dict = ws_tau_func_dict
    )

    @param legs: the legs of the event

    @param workspace_path: the rootfile containing the workspace

    @param legX_vars_dict: the variables used in the workspace function

    @param legX_func_dict: the function for each trigger type to be used to
    compute the weight

    the trigger types matched by the leg are important as one weight is applied
    for each trigger type.
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
