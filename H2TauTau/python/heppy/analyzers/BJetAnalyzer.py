from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from CMGTools.H2TauTau.proto.physicsobjects.BTagSF import BTagSF

class BJetAnalyzer(Analyzer):
        
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(BJetAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        self.btagSF = BTagSF(0, wp='medium')

    def process(self, event):
        '''Adds the is_btagged attribute to the jets of the
        given jets collection.
        '''
        jets = getattr(event, self.cfg_ana.jets)
        for jet in jets:
            jet.is_btagged = self.btagSF.isBTagged(pt=jet.pt(),
                                                   eta=jet.eta(),
                                                   csv=jet.btag(
                    "pfDeepCSVDiscriminatorsJetTags:BvsAll"),
                                                   jetflavor=abs(jet.hadronFlavour()),
                                                   is_data=not self.cfg_comp.isMC,
                                                   csv_cut=0.4941)
                    
