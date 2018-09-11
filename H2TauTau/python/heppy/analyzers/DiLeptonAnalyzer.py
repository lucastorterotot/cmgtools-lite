from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2

import itertools

class DiLepton(object):

    def __init__(self, l1, l2):
        if abs(l1.pdgId()) == abs(l2.pdgId()):
            # e.g. tau tau channel or any channel where the two legs 
            # are of the same time 
            if l2.pt() > l1.pt():
                l1,l2=l2,l1
        self._l1 = l1 
        self._l2 = l2
        self._p4 = l1.p4()
        self._p4 += l2.p4() 

    def p4(self):
        return self._p4

    def leg1(self):
        return self._l1

    def leg2(self):
        return self._l2

    def mass(self):
        return self.p4().mass()

    def pt(self):
        return self.p4().pt()

    def sumPt(self):
        return self.leg1().pt() + self.leg2().pt()

    def __repr__(self):
        header = '{cls}: mvis={mvis}, sumpT={sumpt}'.format(
            cls=self.__class__.__name__,
            mvis=self.mass(),
            sumpt=self.sumPt())
        return '\n'.join([header,
                          '\t'+str(self.leg1()),
                          '\t'+str(self.leg2())])


    

class DiLeptonAnalyzer(Analyzer):
        
    def process(self, event):
        l1s = getattr(event, self.cfg_ana.l1)
        l2s = getattr(event, self.cfg_ana.l2)
        pairs = []
        if l1s == l2s: 
            # same collection 
            for l1, l2 in itertools.combinations(l1s,2):
                pairs.append((l1,l2))
        else: 
            for l1 in l1s: 
                for l2 in l2s:
                    pairs.append((l1,l2))
        dileptons = []
        for l1, l2 in pairs: 
            dilepton = self.build_dilepton(l1,l2)
            if dilepton:
                dileptons.append(DiLepton(l1,l2))
        if not len(dileptons):
            return False
        else: 
            setattr(event, self.cfg_ana.output, dileptons)

    def build_dilepton(self, l1, l2):
        dr = deltaR(l1.eta(), l1.phi(), l2.eta(), l2.phi()) 
        if dr < self.cfg_ana.dr_min: 
            return None
        else:
            return DiLepton(l1,l2)
