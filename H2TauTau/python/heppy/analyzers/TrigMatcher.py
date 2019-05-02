from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Particle import Particle
from PhysicsTools.HeppyCore.utils.deltar import deltaR2, bestMatch
from ROOT import TLorentzVector

class TrigMatcher(Analyzer):
    '''Performs trigger matching on the first di-lepton 
    in the source collection.

    Example::
        leptons = cfg.Analyzer(
          TrigMatcher,
          src = 'dileptons',
          require_all_matched = False,
          )    

    @param src: the input di-lepton collection

    @param require_all_matched: if true, require trigger matching on both legs
    '''

    def beginLoop(self, setup):
        super(TrigMatcher, self).beginLoop(setup)
        self.counters.addCounter('TrigMatcher')
        count = self.counters.counter('TrigMatcher')
        count.register('all events')
        count.register('trig matched')
    
    def declareHandles(self):
        super(TrigMatcher, self).declareHandles()
        if self.cfg_comp.isMC and hasattr(self.cfg_comp, 'channel') and self.cfg_comp.channel in ['tt', 'mt', 'et']:
            self.handles['L1triggerObjects'] =  AutoHandle(
                ('caloStage2Digis','Tau','RECO'),
                'l1t::TauBxCollection'
                )

    def process(self, event):
        '''event must contain
        
        * self.cfg_ana.src: collection of di-leptons to be matched
        '''
        count = self.counters.counter('TrigMatcher')
        count.inc('all events')
        if self.cfg_comp.isMC and hasattr(self.cfg_comp, 'channel') and self.cfg_comp.channel in ['tt', 'mt', 'et']:
            ### for L1 matching
            self.readCollections(event.input)
            l1tobxvect = self.handles['L1triggerObjects'].product()
            self.l1tos = []
            l1to = l1tobxvect.begin(0)
            while l1to != l1tobxvect.end(0):
                self.l1tos.append(TLorentzVector(l1to.px(),l1to.py(),l1to.pz(),l1to.energy()))
                l1to += 1
            ###
        dileptons = getattr(event, self.cfg_ana.src) 
        if len(self.cfg_comp.triggers) > 0:
            # matching only the best di-lepton
            matched = self.trigMatched(event, dileptons[0],
                                       self.cfg_ana.require_all_matched)
            if matched: 
                count.inc('trig matched')


    def trigMatched(self, event, diL, 
                    require_all_matched=False, 
                    ptMin=None,  etaMax=None):
        '''Check that at least one trigger object is matched to the corresponding
        leg. If require_all_matched is True, 
        requires that each single trigger object has a match.'''
        matched = False
        diL.matchedPaths = set()
        if hasattr(self.cfg_ana, 'filtersToMatch'):
            filtersToMatch = self.cfg_ana.filtersToMatch[0]
            legs = [diL.leg1(), diL.leg2()]
            leg = legs[self.cfg_ana.filtersToMatch[1] - 1]
            triggerObjects = self.handles['triggerObjects'].product()
            for item in product(triggerObjects, filtersToMatch):
                to     = item[0]
                filter = item[1]
                print to.filterLabels()[-1], to.filterLabels()[-1] != filter
                if to.filterLabels()[-1] != filter:
                    continue
                if self.trigObjMatched(to, leg):
                    setattr(leg, filter, to)
                    
        if not self.cfg_comp.triggerobjects:
            if self.cfg_ana.verbose:
                print 'No trigger objects configured; auto-passing trigger matching'
            return True

        for info in event.trigger_infos:
            if (not info.fired) and not (hasattr(self.cfg_comp,'isEmbed') and self.cfg_comp.isEmbed):
                continue
            l1_matched = False
            l2_matched = False
            for to, to_names in zip(info.leg1_objs, info.leg1_names):
                if ptMin and to.pt() < ptMin:
                    continue
                if etaMax and abs(to.eta()) > etaMax:
                    continue
                if self.trigObjMatched(to, diL.leg1(), to_names):
                    l1_matched = True
                    if self.cfg_comp.isMC and hasattr(self.cfg_comp, 'channel') and self.cfg_comp.channel=='tt' and not self.matchL1TriggerObject(to):
                        l1_matched = False
            if l1_matched:
                if hasattr(diL.leg1(), 'trigtype'):
                    diL.leg1().trigtypes.update(info.trigtype)
                else :
                    diL.leg1().trigtypes = set([info.trigtype])
            if require_all_matched and l1_matched :
                required_triggernames = set()
                for match_info in info.match_infos :
                    for name in match_info.leg1_names :
                         required_triggernames.add(name)
                if not all(trgname in diL.leg1().triggernames for trgname in required_triggernames):
                    l1_matched = False

            for to, to_names in zip(info.leg2_objs, info.leg2_names):
                if ptMin and to.pt() < ptMin:
                    continue
                if etaMax and abs(to.eta()) > etaMax:
                    continue
                if self.trigObjMatched(to, diL.leg2(), to_names):
                    l2_matched = True
                    if self.cfg_comp.isMC and hasattr(self.cfg_comp, 'channel') and self.cfg_comp.channel in ['tt', 'mt', 'et'] and not self.matchL1TriggerObject(to):
                        l2_matched = False
            if l2_matched:
                if hasattr(diL.leg2(), 'trigtype'):
                    diL.leg2().trigtypes.update(info.trigtype)
                else :
                    diL.leg2().trigtypes = set([info.trigtype])
            if require_all_matched and l2_matched :
                required_triggernames = set()
                for match_info in info.match_infos :
                    for name in match_info.leg2_names :
                         required_triggernames.add(name)
                if not all(trgname in diL.leg2().triggernames for trgname in required_triggernames):
                    l2_matched = False

            if len(info.leg1_objs) == 0 and not (hasattr(self.cfg_comp,'isEmbed') and self.cfg_comp.isEmbed):
                l1_matched = True
            if len(info.leg2_objs) == 0 and not (hasattr(self.cfg_comp,'isEmbed') and self.cfg_comp.isEmbed):
                l2_matched = True
            path_matched = False
            if (l1_matched and l2_matched) or (not info.match_both and (l1_matched or l2_matched)):
                path_matched = True
            if path_matched:
                matched = True
                diL.matchedPaths.add(info.name)
        return matched


    def trigObjMatched(self, to, leg, names=None, dR2Max=0.25):  # dR2Max=0.089999
        '''Returns true if the trigger object is matched to one of the given
        legs'''
        eta = to.eta()
        phi = to.phi()
        to.matched = False
        if deltaR2(eta, phi, leg.eta(), leg.phi()) < dR2Max:
            to.matched = True
            if hasattr(leg, 'triggerobjects'):
                if to not in leg.triggerobjects:
                    leg.triggerobjects.append(to)
            else:
                leg.triggerobjects = [to]
            if names:
                if hasattr(leg, 'triggernames'):
                    leg.triggernames.update(names)
                else:
                    leg.triggernames = set(names)
        return to.matched

    def matchL1TriggerObject(self, to):
        l1to, dR2 = bestMatch(to, self.l1tos)
        if hasattr(self.cfg_comp, 'channel') and self.cfg_comp.channel  == 'tt' :
            ptcut = 31.9999
        else :
            ptcut = 0
        if dR2<0.25 and l1to.Pt() > ptcut:
            return True
        # for l1to in self.l1tos:
        #     if deltaR2(to.eta(),to.phi(),l1to.Eta(),l1to.Phi()) < 0.25 and l1to.Pt()>31.9999:# because some come with 31.999999999996 and are passed by KIT
        #         return True
        return False
