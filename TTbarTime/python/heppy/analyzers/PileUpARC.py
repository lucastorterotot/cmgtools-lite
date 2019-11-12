import os
from PhysicsTools.Heppy.analyzers.core.VertexHistograms import VertexHistograms
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.statistics.average import Average
from PhysicsTools.Heppy.physicsutils.PileUpSummaryInfo import PileUpSummaryInfo
import PhysicsTools.HeppyCore.framework.config as cfg



class PileUpAnalyzerARC( Analyzer ):

    def declareHandles(self):
        super(PileUpAnalyzerARC, self).declareHandles()
        self.mchandles['pusi'] = AutoHandle(
            'slimmedAddPileupInfo',
            'std::vector<PileupSummaryInfo>',
            fallbackLabel="addPileupInfo"
            )
                                                                           
    def process(self, event):
        self.readCollections(event.input)
       
        if self.cfg_comp.isMC:
            event.pileUpInfo = map(PileUpSummaryInfo,
                                                    self.mchandles['pusi'].product() )
            for puInfo in event.pileUpInfo:
                if puInfo.getBunchCrossing()==0:
                    event.nPU = puInfo.nTrueInteractions()
 
            if event.nPU is None:
                raise ValueError('nPU cannot be None! means that no pu info \
                                             has been found for bunch crossing 0.')


        print(event.nPU)
        
        
