from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from CMGTools.TTbarTime.proto.physicsobjects.BTagSFARC import BTagSFARC

class BJetAnalyzerARC(Analyzer):
        
    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(BJetAnalyzerARC, self).__init__(cfg_ana, cfg_comp, looperName)
        self.btagSF = BTagSFARC(0, wp='loose')

    def process(self, event):
        '''Adds the is_btagged attribute to the jets of the
        given jets collection.
        '''
        
        sfb_weight = 1.
        jets = getattr(event, self.cfg_ana.jets)
        for jet in jets:
            jet.is_btagged = self.btagSF.isBTagged(jet, pt=jet.pt(),
                                                   eta=jet.eta(),
                                                   csv=jet.btag(
                    "pfCombinedInclusiveSecondaryVertexV2BJetTags"),
                                                   jetflavor=abs(jet.hadronFlavour()),
                                                   is_data=not self.cfg_comp.isMC,
                                                   csv_cut=0.5803 )
 
            if(jet.btagWeight > 0):
                sfb_weight *= jet.btagWeight
            
        setattr(event, 'sfbWeight', sfb_weight)
        event.eventWeight *= event.sfbWeight
            
                                                   

# CSVv2 "pfCombinedInclusiveSecondaryVertexV2BJetTags"  loose : 0.5803 
# DeepCSV "pfDeepCSVJetTags:probb + pfDeepCSVJetTags:probbb" loose : 0.1522  
