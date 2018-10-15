from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Tau import Tau

class TauAnalyzer(Analyzer):

    def declareHandles(self):
        super(TauAnalyzer, self).declareHandles()

        self.handles['taus'] = AutoHandle(
            self.cfg_ana.taus,
            'std::vector<pat::Tau>'
        )
        
    def process(self, event):
        self.readCollections(event.input)
        taus = self.handles['taus'].product()
        htaus = []
        for tau in taus:
            htau = Tau(tau)
            htau.associatedVertex = event.vertices[0]
            self.attach_tau_gen_match(tau)
            self.correct_energy(tau)
            htaus.append(htau)
        setattr(event, self.cfg_ana.output, htaus)
 
    def correct_energy(self, tau):
        if hasattr(tau, 'gen_match') :
            if tau.gen_match == 5 :
                if tau.decayMode == 0 : # h
                    tau.scaleEnergy(0.97)
                elif tau.decayMode == 1 : # h p0
                    tau.scaleEnergy(0.98)
                elif tau.decayMode == 10 : # hhh
                    tau.scaleEnergy(0.99)
                # elif tau.decayMode == 11 ? : # hhh p0
        else:
            print 'No gen match for tau lepton!'

    def attach_tau_gen_match(self, tau):
        flag = 6

        gen_p = tau.genLepton() if hasattr(tau, 'genLepton') else None
        if gen_p:
            pdg_id = abs(gen_p.pdgId())
            if pdg_id == 15:
                if gen_p.pt() > 15.:
                    flag = 5
            elif gen_p.pt() > 8.:
                if pdg_id == 11:
                    flag = 1
                elif pdg_id == 13:
                    flag = 2
                if flag in [1, 2]:
                    if gen_p.statusFlags().isDirectPromptTauDecayProduct():
                        flag += 2
                    elif not gen_p.statusFlags().isPrompt():
                        flag = 6

        tau.gen_match = flag

            
