import ROOT

from copy        import deepcopy
from itertools   import combinations, product
from collections import OrderedDict

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.HeppyCore.utils.deltar import deltaR
from PhysicsTools.Heppy.physicsobjects.Tau import Tau
from PhysicsTools.Heppy.physicsobjects.PhysicsObject import PhysicsObject

class TauTauRateAnalyzer(Analyzer):

    def declareHandles(self):
        super(TauTauRateAnalyzer, self).declareHandles()
        self.handles['taus'] = AutoHandle('slimmedTaus', 'std::vector<pat::Tau>')

        self.handles['triggerresults'] = AutoHandle(
            ('TriggerResults', '', 'TEST'),
            'edm::TriggerResults'
        )
        
        self.handles['triggerevent'  ] = AutoHandle(
            ('hltTriggerSummaryAOD', '', 'TEST'),
            'trigger::TriggerEvent'
        )

    def process(self, event):
        super(TauTauRateAnalyzer, self).process(event)
        
        try:
            # Take the pre-sorted vertices from miniAOD
            event.goodVertices = event.vertices
        except:
            # pass if, for example, you're running on RAW only
            pass

        alltaus = []

        for discr in self.cfg_ana.discriminators:
            
            try:
                taus = getattr(event, discr)
            except:
                continue
            
            for ii in taus:
                tt = PhysicsObject(ii.tau)
                alreadyIn = False
                for jj in alltaus:
                    if deltaR(tt, jj) < 0.05:
                        alreadyIn = True
                        setattr(jj, discr, ii.discriminator)
                if not alreadyIn:
                    setattr(tt, discr, ii.discriminator)
                    alltaus.append(tt)

        alltaus.sort(key=lambda x: x.pt(), reverse=True)
        
        if hasattr(self.cfg_ana, 'ptcut'):
            alltaus = [tt for tt in alltaus if tt.pt()>self.cfg_ana.ptcut]

        filtersToMatch = self.readTriggerObject()
        for k, v in filtersToMatch.iteritems():
            for tau, to in product(alltaus, v):
                if deltaR(tau, to) < 0.05 and abs(to.pt() - tau.pt())<0.05:
                    setattr(tau, k, True)
        
        event.trigger_taus = alltaus

        if not self.cfg_ana.addOfflineTaus:
            return True
                    
        recotaus = self.handles['taus'].product()
        
        for tt in alltaus:
            dRmax = 0.5
            for rt in recotaus:        
                dR = deltaR(tt, rt)
                if dR < dRmax:
                     tt.recotau = rt
                     dRmax = dR
        
        return True

    def readTriggerObject(self):
        triggerResults = self.handles['triggerresults'].product()
        triggerEvent   = self.handles['triggerevent'  ].product()
        
        nFilters = triggerEvent.sizeFilters()

        import pdb; pdb.set_trace()
        
        if hasattr(self.cfg_ana, 'filtersToMatch'):
            filtersToMatch = OrderedDict()
            for ff in self.cfg_ana.filtersToMatch:
                filtersToMatch[ff] = []

        for iFilter in range(nFilters):
            filterTag      = triggerEvent.filterTag(iFilter).encode().split(':')[0]
            if filterTag not in filtersToMatch.keys():
                continue
            objectKeys     = triggerEvent.filterKeys(iFilter)
            triggerObjects = triggerEvent.getObjects()

            for iKey in range(objectKeys.size()):
                objKey     = objectKeys.at(iKey)
                triggerObj = triggerObjects[objKey]

                triggerObjCMG = PhysicsObject(triggerObj)
                triggerObjCMG.filterName = filterTag
                
                filtersToMatch[filterTag].append(triggerObjCMG)
        
        return filtersToMatch
        
        
        
        
