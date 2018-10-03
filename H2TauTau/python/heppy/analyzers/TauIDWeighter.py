from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer

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
                      2:'MuToTau',
                      4:'MuToTau',
                      1:'EToTau',
                      3:'EToTau'}

    def getTauIDWeight(self, pt, eta, decaymode, working_point):
        if working_point == 'VLoose':
            return 0.99
        elif working_point == 'Loose':
            return 0.99
        elif working_point == 'Medium':
            return 0.97
        elif working_point == 'Tight':
            return 0.95
        elif working_point == 'VTight':
            return 0.93
        else:
            return 1.

    def getMuToTauWeight(self, pt, eta, decaymode, working_point):
        aeta = abs(eta)
        if working_point == 'Loose':
            if aeta < 0.4:
                return 1.22
            if aeta < 0.8:
                return 1.12
            if aeta < 1.2:
                return 1.26
            if aeta < 1.7:
                return 1.22
            if aeta < 2.3:
                return 2.39
        elif working_point == 'Tight':
            if aeta < 0.4:
                return 1.47
            if aeta < 0.8:
                return 1.55
            if aeta < 1.2:
                return 1.33
            if aeta < 1.7:
                return 1.72
            if aeta < 2.3:
                return 2.50
        else:
            return 1.

    def getEToTauWeight(self, pt, eta, decaymode, working_point):
        aeta = abs(eta)
        if working_point == 'VLoose':
            if aeta < 1.5:
                return 1.21
            else:
                return 1.38
        elif working_point == 'Loose':
            if aeta < 1.5:
                return 1.32
            else:
                return 1.38
        elif working_point == 'Medium':
            if aeta < 1.5:
                return 1.32
            else:
                return 1.53
        elif working_point == 'Tight':
            if aeta < 1.5:
                return 1.40
            else:
                return 1.90
        elif working_point == 'VTight':
            if aeta < 1.5:
                return 1.21
            else:
                return 1.97
        else:
            return 1.

    def getTauWeight(self, gen_match, pt, eta, decaymode, working_point):
        if gen_match == 5:
            return self.getTauIDWeight(pt, eta, decaymode, working_point)
        elif gen_match in [2,4]:
            return self.getMuToTauWeight(pt, eta, decaymode, working_point)
        elif gen_match in [1,3]:
            return self.getEToTauWeight(pt, eta, decaymode, working_point)
        else:
            return 1.

    def process(self, event):

        if not hasattr(self.cfg_ana,'taus') or not self.cfg_ana.taus(event):
            return True

        taus = self.cfg_ana.taus(event)
        for tau in taus:
            if hasattr(self.cfg_ana,'WPs') and self.cfg_ana.WPs:
                weight = self.getTauWeight(tau.gen_match,
                                           tau.pt(),
                                           tau.eta(),
                                           tau.decayMode(),
                                           self.cfg_ana.WPs[tau.gen_match])
                event.eventWeight *= weight
                setattr(tau,
                        '{}{}Weight'.format(self.gen_match_dict[tau.gen_match],
                                            self.cfg_ana.WP),
                        weight)
            else:
                for WP in ['VLoose','Loose','Medium','Tight','VTight']:
                    weight = self.getTauWeight(tau.gen_match,
                                               tau.pt(),
                                               tau.eta(),
                                               tau.decayMode(),
                                               WP)
                    setattr(tau,
                            '{}{}Weight'.format(self.gen_match_dict[tau.gen_match],
                                                WP),
                            weight)
                
