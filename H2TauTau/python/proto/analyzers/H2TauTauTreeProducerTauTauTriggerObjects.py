from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase


class H2TauTauTreeProducerTrigger(H2TauTauTreeProducerBase):

    modlist=['hltDoubleL2IsoTau0eta2p2', 'hltDoubleL2Tau0eta2p2', 'hltL2TauIsoFilter', 'hltDoublePFTau35Reg', 'hltPFTauTrackReg', 'hltDoublePFTau35TrackPt1MediumChargedIsolationReg', 'hltDoublePFTau35TrackPt1Reg', 'hltDoubleL2IsoTau26eta2p2', 'hltDoubleL2Tau26eta2p2', 'hltL1sDoubleTauBigOR', 'hltDoublePFTau35TrackPt1MediumChargedIsolationL1HLTMatchedReg', 'hltDoublePFTau35TrackPt1MediumChargedIsolationDz02Reg']

    def declareVariables(self, setup):
        # for pt1 in [30,32,34,36,38,40,42,44,46,48,50]:
        #     for pt2 in [25,27,29,31,33,35,37,39,41,43,45]:
        #         if pt2<pt1:
        #             #self.var(self.tree, 'passoffline_{}_{}'.format(pt1,pt2))
        #             for mod in self.modlist:
        #                 self.var(self.tree, 'passonline_{}_{}'.format(pt1,pt2)+mod)
        pt1list = [30.,32.,34.,36.,38.,40.,42.,44.,46.,48.,50.]
        pt2list = [25.,27.,29.,31.,33.,35.,37.,39.,41.,43.,45.]
        for pt2 in pt2list:
            for pt1 in [pt for pt in pt1list if pt>pt2]:
                self.var(self.tree, 'trigger_'+str(int(pt2))+'_'+str(int(pt1)))
                self.var(self.tree, 'offline_'+str(int(pt2))+'_'+str(int(pt1)))
        self.var(self.tree, 'iEv')
        self.var(self.tree, 'lumi')
        self.var(self.tree, 'trigged')
        self.var(self.tree, 'Opentrigged')
        self.var(self.tree, 'passoff')
        # self.var(self.tree, 'counttrigged')
        # self.var(self.tree, 'notrigobj')

    def process(self, event):

        self.tree.reset()
        self.fill(self.tree, 'iEv', event.eventId)
        self.fill(self.tree, 'lumi', event.lumi)
        self.fill(self.tree, 'trigged', 
                  1 if getattr(event, 'trigged',False) else 0)
        self.fill(self.tree, 'Opentrigged',
                  1 if getattr(event,'Opentrigged',False) else 0)
        self.fill(self.tree, 'passoff', 
                  getattr(event,'passoff',0))
        pt1list = [30.,32.,34.,36.,38.,40.,42.,44.,46.,48.,50.]
        pt2list = [25.,27.,29.,31.,33.,35.,37.,39.,41.,43.,45.]
        for pt2 in pt2list:
            for pt1 in [pt for pt in pt1list if pt>pt2]:
                trigged = getattr(event, 'trigger_'+str(int(pt2))+'_'+str(int(pt1)),0)
                self.fill(self.tree, 'trigger_'+str(int(pt2))+'_'+str(int(pt1)), trigged)
                offline = getattr(event, 'offline_'+str(int(pt2))+'_'+str(int(pt1)),0)
                self.fill(self.tree, 'offline_'+str(int(pt2))+'_'+str(int(pt1)), offline)
        # # self.fill(self.tree, 'counttrigged', getattr(event,'counttrigged',0))
        # self.fill(self.tree, 'notrigobj', getattr(event,'notrigobj',0))

        # for pt1 in [30,32,34,36,38,40,42,44,46,48,50]:
        #     for pt2 in [25,27,29,31,33,35,37,39,41,43,45]:
        #         if pt2<pt1:
        #             #self.fill(self.tree, 
        #             #          'passoffline_{}_{}'.format(pt1,pt2),
        #             #          getattr(event,
        #             #                  'passoff',
        #             #                  0)
        #             #          )
        #             for mod in self.modlist:
        #                 self.fill(self.tree,
        #                           'passonline_{}_{}'.format(pt1,pt2)+mod,
        #                           getattr(event,
        #                                   'trigpass{}_{}'.format(pt1,pt2)+mod,
        #                                   0)
        #                           )
        

        self.fillTree(event)
