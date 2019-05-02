from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from ROOT import TFile

class LeptonsWeighter(Analyzer):
    """Adds the following leptons weights to the event:
    - Ele iso
    - Ele ID
    - Muon iso
    - Muon ID

    Example:
    ws_ele_idiso_vars_dict = {'e_pt':lambda ele:ele.pt(),
                          'e_eta':lambda ele:ele.eta()}
    ws_ele_idiso_func_dict = {'id':'e_id90_kit_ratio',
                          'iso':'e_iso_kit_ratio'}
    from CMGTools.H2TauTau.heppy.analyzers.LeptonsWeighter import LeptonsWeighter
    eleidisoweighter = cfg.Analyzer(
        LeptonsWeighter,
        'EleIDisoWeighter',
        workspace_path = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_2017_v2.root',
        legs = lambda event: [event.dileptons_sorted[0].leg1()],
        leg1_vars_dict = ws_ele_idiso_vars_dict,
        leg1_func_dict = ws_ele_idiso_func_dict
    )

    @param legs: function to be called on event to retrieve the list of the legs (leptons of the event) from which the weights are derived.

    @param workspace_path: the rootfile containing the workspace

    @param legX_vars_dict: the variables used in the workspace function

    @param legX_func_dict: the function for each weight type to be used to
    compute the weight

    the trigger types matched by the leg are important as one weight is applied
    for each trigger type.
    """
    
    pdgID_to_str = {11 : 'e', 13 : 'm'}

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(LeptonsWeighter, self).__init__(cfg_ana, cfg_comp, looperName)
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
            num = index+1
            leg_vars_dict = getattr(self.cfg_ana,'leg'+str(num)+'_vars_dict')
            leg_func_dict = getattr(self.cfg_ana,'leg'+str(num)+'_func_dict')
            for weight_type in leg_func_dict.keys():
                for name, func in leg_vars_dict.iteritems():
                    self.ws.var(name).setVal(func(leg))
                val = self.ws.function(leg_func_dict[weight_type]).getVal()
                setattr(leg, 'weight_'+str(weight_type), val)
            weight_id = getattr(leg, 'weight_id', 1)
            weight_iso= getattr(leg, 'weight_iso',1)
            setattr(leg, 'weight_idiso', weight_id*weight_iso)
