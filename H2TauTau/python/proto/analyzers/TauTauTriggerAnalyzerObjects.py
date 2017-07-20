from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar import deltaR, bestMatch
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from CMGTools.H2TauTau.proto.physicsobjects.DiObject import TauTau, DirectTauTau

from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import Tau, Muon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron

class TauTauTriggerAnalyzer(Analyzer):

    def declareHandles(self):
        super(TauTauTriggerAnalyzer, self).declareHandles()
        self.handles['taus'] = AutoHandle('slimmedTaus',
                                          'std::vector<pat::Tau>')

        myhandle = self.cfg_ana.triggerResultsHandle
        self.handles['triggerResultsHLT'] = AutoHandle(
            (myhandle[0], myhandle[1], myhandle[2]),
            'edm::TriggerResults')

        myhandle = self.cfg_ana.triggerObjectsHandle
        self.handles['triggerObjects'] = AutoHandle(
            (myhandle[0], myhandle[1], myhandle[2]),
            'std::vector<pat::TriggerObjectStandAlone>')

        self.handles['pfMET'] = AutoHandle(
            'slimmedMETs',
            'std::vector<pat::MET>'
        )
        self.handles['leptons'] = AutoHandle(
            'slimmedElectrons', 
            'std::vector<pat::Electron>'
        )
        
        self.handles['otherLeptons'] = AutoHandle(
            'slimmedMuons', 
            'std::vector<pat::Muon>'
        )

    def beginLoop(self, setup):
        super(TauTauTriggerAnalyzer, self).beginLoop(setup)
        self.modlist=[]# ['hltDoubleL2IsoTau26eta2p2', 'hltDoubleL2Tau26eta2p2', 'hltL2TauIsoFilter', 'hltL1sDoubleTauBigOR', 'hltDoublePFTau35Reg', 'hltPFTauTrackReg', 'hltDoublePFTau35TrackPt1Reg', 'hltDoublePFTau35TrackPt1MediumChargedIsolationReg', 'hltDoublePFTau35TrackPt1MediumChargedIsolationDz02Reg', 'hltDoublePFTau35TrackPt1MediumChargedIsolationL1HLTMatchedReg']#'hltDoubleL2IsoTau0eta2p2', 'hltDoubleL2Tau0eta2p2', 'hltL2TauIsoFilter', 'hltDoublePFTau35Reg', 'hltPFTauTrackReg', 'hltDoublePFTau35TrackPt1MediumChargedIsolationReg', 'hltDoublePFTau35TrackPt1Reg', 'hltDoubleL2IsoTau26eta2p2', 'hltDoubleL2Tau26eta2p2', 'hltL1sDoubleTauBigOR', 'hltDoublePFTau35TrackPt1MediumChargedIsolationL1HLTMatchedReg', 'hltDoublePFTau35TrackPt1MediumChargedIsolationDz02Reg']
        # self.counttrigged = 0
        # self.notrigobj = 0

    # def endLoop(self, setup):
    #     super(TauTauTriggerAnalyzer, self).endLoop(setup)
    #     import pdb; pdb.set_trace()

    def process(self, event):
        ### retreive trigger info
        self.readCollections(event.input)
        triggerBits = self.handles['triggerResultsHLT'].product()
        names = event.input.object().triggerNames(triggerBits)
        alltriggerObjects = self.handles['triggerObjects'].product()
        ###

        ### get a dict of all the trigger objects labels
        for to in alltriggerObjects:
            to.unpackPathNames(names)
            for fl in to.filterLabels():
                if fl not in self.modlist:
                    self.modlist.append(fl)
        ###

        ### use filter labels to order trigger objects
        triggerObjects = {}
        for mod in self.modlist:
            triggerObjects[mod] = sorted([to for to in alltriggerObjects if mod in to.filterLabels()],
                                key= lambda x: x.pt(),
                                reverse=True)
        ###
        
        # import pdb; pdb.set_trace()
        
        ### Study if no trig obj when trigg passes
        # if not triggerBits.accept(names.triggerIndex('HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v3')):
        #     return False
        # else:
        #     event.counttrigged=1

        # if not any([i for j,i in triggerObjects.iteritems()]):
        #     event.notrigobj=1
        #     return True
        # else:
        #     return True
        ###

        ### standard tautau
        event.goodVertices = event.vertices
        taus = self.handles['taus'].product()
        diLeps = self.buildDiLeptonsSingle(taus,event)
        seldilep = self.selectionSequence(event, 40., 40., diLeps)
        setattr(event,'passoff', 1 if len(seldilep)>=1 else 0)
        if (event.passoff==0):
            return False ### not interested if doesn't pass offline selection
        ###

        ### study how many events without trigobj when pass offline selection
        if not any([i for j,i in triggerObjects.iteritems()]):
            event.notrigobj=1
        #     return True
        # else:
        #     return True
        # ###

        # if not triggerBits.accept(names.triggerIndex('HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v3')):
        #     import pdb; pdb.set_trace()
        # else:
        #     return False

        # ### match best trigger object of every label to each leg
        # # TO DO: reorganise the matchTriggerObj to set the tags, to have one loop match+tagevent instead of one in there and one in here
        # self.matchTriggerObj(seldilep, event, triggerObjects)
        # ### test for trigger objects and their pt
        # # TO DO: maybe outer loop should be on leps and inner pt values?
        # for pt1 in [30,32,34,36,38,40,42,44,46,48,50]:
        #     for pt2 in [25,27,29,31,33,35,37,39,41,43,45]:
        #         if pt2<pt1:
        #             for dilep in seldilep:
        #                 for mod in self.modlist:
        #                     if hasattr(dilep.leg1(), 'trigobj'+mod) and \
        #                             hasattr(dilep.leg2(), 'trigobj'+mod):
        #                         if getattr(dilep.leg1(),'trigobj'+mod).pt()>pt1 and \
        #                                 getattr(dilep.leg2(),'trigobj'+mod).pt()>pt2:
        #                             if event.passoff==1:
        #                                 setattr(event,'trigpass{}_{}'.format(pt1,pt2)+mod, 1)
        # ###

        ### match best trigger object of every label to each leg
        for dilep in seldilep:
            for mod in self.modlist:
                for label, objects in triggerObjects.iteritems():
                    bm1, dr1 = bestMatch(dilep.leg1(), objects)
                    bm2, dr2 = bestMatch(dilep.leg2(), objects)
                    if dr1>0.5 or dr2>0.5:
                        continue
                    if bm1 and bm2:
                        if triggerBits.accept(names.triggerIndex('HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v3')):
                            for pt1 in [30,32,34,36,38,40,42,44,46,48,50]:
                                for pt2 in [25,27,29,31,33,35,37,39,41,43,45]:
                                    if pt2<pt1:
                                        if (bm1.pt()>pt1 and bm2.pt()>pt2) or (bm1.pt()>pt2 and bm2.pt()>pt1):
                                            setattr(event,'trigpass{}_{}'.format(pt1,pt2)+mod, 1)
        ###

        # if (event.passoff==1):# and hasattr(event, 'trigpass36_35hltDoublePFTau35TrackPt1MediumChargedIsolationDz02Reg')):
        #     for dilep in seldilep: print dilep
        #     for key, value in triggerObjects.iteritems(): print key, [v.pt() for v in value]
        #     import pdb;pdb.set_trace()

    def buildDiLeptonsSingle(self, leptons, event):
        di_objects = []
        met = self.handles['pfMET'].product()[0]
        taus = leptons

        for leg1 in taus:
            for leg2 in taus:
                if leg1 != leg2:
                    di_tau = DirectTauTau(Tau(leg1), Tau(leg2), met)
                    di_tau.leg2().associatedVertex = event.goodVertices[0]
                    di_tau.leg1().associatedVertex = event.goodVertices[0]
                    di_tau.mvaMetSig = None
                    di_objects.append(di_tau)
        return di_objects

    def selectionSequence(self, event, pt1, pt2, selDiLeptons):
        if self.thirdLeptonVeto(event):
            return []
        if self.otherLeptonVeto(event):
            return []
        diLeps = [diL for diL in selDiLeptons if ((deltaR(diL.leg1().eta(), diL.leg1().phi(), diL.leg2().eta(), diL.leg2().phi())) > 0.5)]
        diLeps = [diL for diL in diLeps if
                        self.testLeg(diL.leg1(), pt1)]
        diLeps = [diL for diL in diLeps if
                        self.testLeg(diL.leg2(), pt2)]
        diLeps = [diL for diL in diLeps if
                        diL.mass()>10.]
        return diLeps
        

    def testLeg(self, leg, pt):
        return (abs(leg.charge()) == 1 and
                abs(leg.leadChargedHadrCand().dz()) < 0.2 and
                leg.tauID('byVTightIsolationMVArun2v1DBoldDMwLT') > 0.5 and
                leg.tauID('againstElectronVLooseMVA6') and
                leg.tauID('againstMuonLoose3') and
                leg.pt() > pt and
                abs(leg.eta()) < 2.1 and
                leg.tauID('decayModeFinding') > 0.5)

    def thirdLeptonVeto(self,event):
        '''Build electrons for third lepton veto, associate best vertex.'''
        otherLeptons = []
        leptons = self.handles['leptons'].product()
        for index, lep in enumerate(leptons):
            pyl = Electron(lep)
            pyl.associatedVertex = event.goodVertices[0]
            pyl.rho = event.rho
            pyl.event = event
            if not pyl.mvaIDRun2('NonTrigSpring15MiniAOD', 'POG90'):
                continue
            if not pyl.relIsoR(R=0.3, dBetaFactor=0.5, allCharged=0) < 0.3:
                continue
            if not (pyl.pt()>10. and pyl.eta()<2.5):
                continue
            otherLeptons.append(pyl)
        return (len(otherLeptons)>0)

    def otherLeptonVeto(self,event):
        '''Build muons for veto, associate best vertex, select loose ID muons.
        The loose ID selection is done to ensure that the muon has an inner track.'''
        leptons = []
        leps = self.handles['otherLeptons'].product()
        for index, lep in enumerate(leps):
            pyl = Muon(lep)
            pyl.associatedVertex = event.goodVertices[0]
            if not pyl.muonID('POG_ID_Medium'):
                continue
            if not pyl.relIsoR(R=0.4, dBetaFactor=0.5, allCharged=0) < 0.3:
                continue
            if not (pyl.pt()>10. and pyl.eta()<2.4):
                continue
            leptons.append(pyl)
        return (len(leptons)>0)

    # def matchTriggerObj(self, seldilep, event, trigObjs):
    #     triggerBits = self.handles['triggerResultsHLT'].product()
    #     names = event.input.object().triggerNames(triggerBits)
    #     for lab, objs in trigObjs.iteritems():
    #         for dilep in seldilep:
    #             for leg in [dilep.leg1(), dilep.leg2()]:
    #                 bm, dr = bestMatch(leg,objs)
    #                 if dr >= 0.5:
    #                     continue
    #                 if triggerBits.accept(names.triggerIndex('HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v3')):
    #                     setattr(leg, 'trigobj'+lab, bm)
