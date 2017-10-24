from CMGTools.H2TauTau.proto.analyzers.H2TauTauTreeProducerBase import H2TauTauTreeProducerBase

class H2TauTauTreeProducerTriggerRate(H2TauTauTreeProducerBase):

    def declareVariables(self, setup):
        self.var(self.tree, 'trigged')
        # self.var(self.tree, 'run')
        for pt1 in [30,32,34,36,38,40,42,44,46,48,50]:
            for pt2 in [25,27,29,31,33,35,37,39,41,43,45]:
                if pt2<pt1:
                    self.var(self.tree, 'passonline_{}_{}'.format(pt1,pt2))

    def process(self, event):
        self.tree.reset()
        self.fill(self.tree, 'trigged', event.trigged)
        # self.fill(self.tree, 'run', event.run)
        for pt1 in [30,32,34,36,38,40,42,44,46,48,50]:
            for pt2 in [25,27,29,31,33,35,37,39,41,43,45]:
                if pt2<pt1:
                    self.fill(self.tree,
                              'passonline_{}_{}'.format(pt1,pt2),
                              getattr(event,
                                      'trigpass{}_{}'.format(pt1,pt2),
                                      0)
                              )
        self.fillTree(event)
