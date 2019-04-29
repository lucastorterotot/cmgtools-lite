from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from CMGTools.H2TauTau.heppy.utils.tauid_weights import tauid_weights

class TauIDWeighter(Analyzer):
    """Adds the following hadronic tau weights to the event:
    - TauIDWeight
    - EToTauFakeWeight
    - MuToTauFakeWeight

    Example:
       tauidweighter = cfg.Analyzer(
          TauIDWeighter,
          'TauIDWeighter',
          taus = lambda event: return [event.dileptons_sorted[0].leg1(),event.dileptons_sorted[0].leg2()],
          WPs = {5:'Tight',4:'Loose',2:'Loose',3:'Tight',1:'Tight'}
       )

    @param taus: function to be called on event to retrieve the list of taus from which the weights are derived.

    @param WPs: dict of the form {<gen_match>:<working_point>,...} to choose which working point to use and apply to the event weight for each gen_match value.
    """

    gen_match_dict = {6:'JetToTau',
                      5:'TauID',
                      2:'MuToTaufake',
                      4:'MuToTaufake',
                      1:'EToTaufake',
                      3:'EToTaufake'}

    def getTauWeight(self, gen_match, pt, eta, decaymode, working_point):

        if self.gen_match_dict[gen_match] not in tauid_weights:
            return 1.

        aeta = abs(eta)
        weight = 1.

        wp_dict = tauid_weights[self.gen_match_dict[gen_match]]

        if working_point not in wp_dict:
            return 1.

        for etamax, value in wp_dict[working_point]:
            if aeta < etamax:
                weight = value
            else:
                break

        return weight

    def process(self, event):
        if self.cfg_comp.isData:
            return True

        if not hasattr(self.cfg_ana,'taus') or not self.cfg_ana.taus(event):
            return True

        taus = self.cfg_ana.taus(event)
        for tau in taus:
            if hasattr(self.cfg_ana,'WPs') and self.cfg_ana.WPs:
                weight = self.getTauWeight(tau.gen_match,
                                           tau.pt(),
                                           tau.eta(),
                                           tau.decayMode(),
                                           self.cfg_ana.WPs[self.gen_match_dict[tau.gen_match]])
                event.eventWeight *= weight
                setattr(tau,
                        'weight_idiso',
                        weight)
            else:
                for WP in ['VLoose','Loose','Medium','Tight','VTight']:
                    weight = self.getTauWeight(tau.gen_match,
                                               tau.pt(),
                                               tau.eta(),
                                               tau.decayMode(),
                                               WP)
                    setattr(tau,
                            'weight_{}_{}'.format(self.gen_match_dict[tau.gen_match],
                                                WP),
                            weight)
                
