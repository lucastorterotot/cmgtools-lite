from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from ROOT import TFile

class LeptonsWeighter(Analyzer):
    """Adds the following leptons weights to the event:
    - Ele iso
    - Ele ID
    - Muon iso
    - Muon ID

    Example:
       leptonsweighter = cfg.Analyzer(
          LeptonsWeighter,
          'LeptonsWeighter',
          workspace_path = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/htt_scalefactors_2017_v2.root',
          leptons = lambda event: return [event.dileptons_sorted[0].leg1()],
          leg1_vars_dict = ws_ele_vars_dict,
          leg1_func_dict = ws_ele_func_dict,
       )

    @param workspace_path: the rootfile containing the workspace

    @param lepton: function to be called on event to retrieve the list of leptons from which the weights are derived.
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
