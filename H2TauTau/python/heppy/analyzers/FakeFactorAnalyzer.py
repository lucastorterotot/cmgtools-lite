from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from array import array
import ROOT


class FakeFactorAnalyzer(Analyzer):
    '''Stores the value of the fakefactor weight to apply to 
    data in the application region.
    !!! background fractions should be updated for the analysis!
    For nore information see :
    https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauJet2TauFakes
    '''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(FakeFactorAnalyzer, self).__init__(cfg_ana, cfg_comp, looperName)
        if self.cfg_comp.isData:
            self.btagfile = ROOT.TFile(self.cfg_ana.filepath.format(self.cfg_ana.channel,'btag'))
            self.nobtagfile = ROOT.TFile(self.cfg_ana.filepath.format(self.cfg_ana.channel,'nobtag'))
            self.inclfile = ROOT.TFile(self.cfg_ana.filepath.format(self.cfg_ana.channel,'inclusive'))
            self.btagff = self.btagfile.Get('ff_comb')
            self.nobtagff = self.nobtagfile.Get('ff_comb')
            self.inclff = self.inclfile.Get('ff_comb')
        

    def fake_factor_semileptonic(self, tau, njets, mvis, mt, lepton_iso, sys='', category='inclusive'):
        '''Interface function to retrieve the fake factors from
        the rootfile for the semileptonic channels.
        
        @param sys : if '' -> nominal value, else can be 'up' or 'down'
        '''
        inputs = [tau.pt(),
                  tau.decayMode(),
                  njets,
                  mvis,
                  mt,
                  lepton_iso,
                  self.frac_qcd,
                  self.frac_w,
                  self.frac_tt]
        if category == 'inclusive':
            ff = self.inclff
        elif category == 'btag':
            ff = self.btagff
        elif category == 'nobtag':
            ff = self.nobtagff
        else:
            raise ValueError('category must be in ["btag","nobtag","inclusive"]')
        if sys:
            return ff.value(len(inputs), array('d',inputs),sys)
        return ff.value(len(inputs), array('d',inputs))

    def fake_factor_fullyhadronic(self, tau1,tau2, njets, mvis, sys=''):
        '''Interface function to retrieve the fake factors from
        the rootfile for the fully hadronic channel.
        
        @param sys : if '' -> nominal value, else can be 'up' or 'down'
        '''
        inputs = [tau1.pt(),
                  tau2.pt(),
                  tau1.decayMode(),
                  njets,
                  mvis,
                  self.frac_qcd,
                  self.frac_w,
                  self.frac_tt,
                  self.frac_dy]
        if category == 'inclusive':
            ff = self.inclff
        elif category == 'btag':
            ff = self.btagff
        elif category == 'nobtag':
            ff = self.nobtagff
        else:
            raise ValueError('category must be in ["btag","nobtag","inclusive"]')
        if sys:
            return ff.value(len(inputs), array('d',inputs),sys)
        return ff.value(len(inputs), array('d',inputs))

    def set_ff_fullyhadronic(self, tau, tau2, njets, mvis):
        for cat in ["btag","nobtag","inclusive"]:
            setattr(tau, 
                    'weight_fakefactor_{}',
                    self.fake_factor_fullyhadronic(tau,tau2,njets,mvis))
            setattr(tau, 
                    'weight_fakefactor_{}_up',
                    self.fake_factor_fullyhadronic(tau,tau2,njets,mvis,'up'))
            setattr(tau, 
                    'weight_fakefactor_{}_down',
                    self.fake_factor_fullyhadronic(tau,tau2,njets,mvis,'down'))

    def set_ff_semileptonic(self, tau,  njets, mvis, mt, iso):
        for cat in ["btag","nobtag","inclusive"]:
            setattr(tau, 
                    'weight_fakefactor_{}',
                    self.fake_factor_semileptonic(tau,njets,mvis,mt,iso))
            setattr(tau, 
                    'weight_fakefactor_{}_up',
                    self.fake_factor_semileptonic(tau,njets,mvis,mt,iso,'up'))
            setattr(tau, 
                    'weight_fakefactor_{}_down',
                    self.fake_factor_semileptonic(tau,njets,mvis,mt,iso,'down'))

    def process(self, event):
        if not self.cfg_comp.isData:
            return True

        njets = len(event.jets30)
        mvis = event.dileptons_sorted[0].mass()

        if self.cfg_ana.channel == 'tt':
            tau1 = event.dileptons_sorted[0].leg1()
            tau2 = event.dileptons_sorted[0].leg2()
            self.set_ff_fullyhadronic(tau1, tau2, njets, mvis)
            self.set_ff_fullyhadronic(tau2, tau1, njets, mvis)

        elif self.cfg_ana.channel in ['mt','et']:
            mt = event.dileptons_sorted[0].mTLeg1(getattr(event,self.cfg_ana.met))
            tau = event.dileptons_sorted[0].leg2()
            lep = event.dileptons_sorted[0].leg1()
            self.set_ff_semileptonic(tau, njets, mvis, mt, lep.iso_htt())

        else:
            raise ValueError('Channel not or wrongly set')
