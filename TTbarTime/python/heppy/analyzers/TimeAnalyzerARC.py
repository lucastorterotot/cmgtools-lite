import os
from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.statistics.average import Average
import PhysicsTools.HeppyCore.framework.config as cfg



class TimeAnalyzerARC( Analyzer ):
                                                         
    def process(self, event):
        self.readCollections(event.input)
       
        time = event.input.eventAuxiliary().time()
        unix_time = time.unixTime()
#        unix_time = time.timeLow()

        setattr(event, 'unixTime', unix_time)

        if event.unixTime is None:
            raise ValueError('time cannot be None!')

        
        
