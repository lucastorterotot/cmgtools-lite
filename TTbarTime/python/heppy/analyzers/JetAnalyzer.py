from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Jet import Jet

import os 

class JetAnalyzer(Analyzer):

    def beginLoop(self, setup):
        super(JetAnalyzer, self).beginLoop(setup)
        if self.cfg_ana.do_jec: 
            global_tag = self.cfg_ana.gt_mc 
            if not self.cfg_comp.isMC:
                global_tag = self.cfg_comp.dataGT

            do_residual = not self.cfg_comp.isMC
            from PhysicsTools.Heppy.physicsutils.JetReCalibrator import JetReCalibrator
            self.jet_calibrator = JetReCalibrator(
                global_tag, 'AK4PFchs', do_residual, 
                jecPath=os.path.expandvars(
                    "${CMSSW_BASE}/src/CMGTools/RootTools/data/jec"
                    ),
                calculateType1METCorrection=True
                )
        self.counters.addCounter('JetAnalyzer')
        count = self.counters.counter('JetAnalyzer')
        count.register('all events')
        count.register('at least 2 good jets')
        count.register('at least 2 clean jets')
 
    def declareHandles(self):
        super(JetAnalyzer, self).declareHandles()

        self.handles['jets'] = AutoHandle(
            self.cfg_ana.jets,
            'std::vector<pat::Jet>'
        )
        
    def process(self, event):
        self.readCollections(event.input)
        jets = self.handles['jets'].product()
        output_jets = []
        if self.cfg_ana.year == 2016 :
            for jet in jets:
                hjet = Jet(jet)
                output_jets.append(hjet)
        else:    
            for jet in jets:
                hjet = Jet(jet)
                if not hasattr(self.cfg_ana,'selection'):
                    continue
                elif self.cfg_ana.selection(hjet):
                    output_jets.append(hjet)

        if self.cfg_ana.do_jec:
            event.metShift = [0., 0.]
            event.type1METCorr = [0.,0.,0.]
            self.jet_calibrator.correctAll(output_jets, event.rho, delta=0.,
                                           addCorr=True, addShifts=True, 
                                           metShift=event.metShift,
                                           type1METCorr=event.type1METCorr)
        setattr(event, self.cfg_ana.output, output_jets)
        
        
        
        
        
        
        
