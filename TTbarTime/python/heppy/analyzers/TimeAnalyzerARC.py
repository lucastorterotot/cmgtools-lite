import os
from PhysicsTools.Heppy.analyzers.core.VertexHistograms import VertexHistograms
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.statistics.average import Average
from PhysicsTools.Heppy.physicsutils.EventAuxiliary import EventAuxiliary
import PhysicsTools.HeppyCore.framework.config as cfg



class TimeAnalyzerARC( Analyzer ):

    def declareHandles(self):
        super(PileUpAnalyzerARC, self).declareHandles()
        self.mchandles['time'] = AutoHandle(
            'std::vector<time>',
            fallbackLabel=""
            )
                                                                           
    def process(self, event):
        self.readCollections(event.input)
       
        if self.cfg_comp.isMC:
            event.time = map(EventAuxiliary,
                                                    self.mchandles['time'].product() )
            for t in event.time:
                event.time_unix = event.unixTime()
 
            if event.time is None:
                raise ValueError('time cannot be None!')


        print(event.time_unix)
        
        
