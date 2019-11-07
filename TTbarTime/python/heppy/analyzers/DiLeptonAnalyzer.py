from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.utils.deltar import deltaR, deltaR2

import itertools
import math

class DiLepton(object):

    def __init__(self, l1, l2):
        if abs(l1.pdgId()) == abs(l2.pdgId()):
            # are of the same time 
            if l2.pt() > l1.pt():
                l1,l2=l2,l1
        self._l1 = l1 
        self._l2 = l2
        self._p4 = l1.p4()
        self._p4 += l2.p4() 

    def mTLeg1(self, met=None):
        if met:
            return self.mT(self.leg1(), met)
        else:
            return self.mT(self.leg1(), self.met)

    def mTLeg2(self, met=None):
        if met:
            return self.mT(self.leg2(), met)
        else:
            return self.mT(self.leg2(), self.met)

    def mtTotal(self, met=None):
        if met:
            mt2 = self.mTLeg1(met)**2 + self.mTLeg2(met)**2 + self.mT(self.leg1(), self.leg2())**2
        else:
            mt2 = self.mTLeg1()**2 + self.mTLeg2()**2 + self.mT(self.leg1(), self.leg2())**2
        return math.sqrt(mt2)

    def p4(self):
        return self._p4

    def leg1(self):
        return self._l1

    def leg2(self):
        return self._l2

    def pt_lead(self):
        if self._l1.pt() >= self._l2.pt() :
            return self._l1.pt()
        else:
            return self._l2.pt()
                        
    def pt_sublead(self):
        if self._l1.pt() <= self._l2.pt() :
            return self._l1.pt()
        else:
            return self._l2.pt()

    def mass(self):
        return self.p4().mass()

    def pt(self):
        return self.p4().pt()

    def sumPt(self):
        return self.leg1().pt() + self.leg2().pt()

    def pt_tt(self, met):
        px = self.leg1().px() + self.leg2().px() + met.px()
        py = self.leg1().py() + self.leg2().py() + met.py()
        return math.sqrt(px*px + py*py)

    @staticmethod
    def mT(cand1, cand2):
        pt = cand1.pt() + cand2.pt()
        px = cand1.px() + cand2.px()
        py = cand1.py() + cand2.py()
        try:
            return math.sqrt(pt*pt - px*px - py*py)
        except ValueError:
            print 'mT2 very close to 0 and negative due to rounding', pt, px, py
            print cand1.px(), cand1.py(), cand1.pt()
            print cand2.px(), cand2.py(), cand2.pt()
            return 0.

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
