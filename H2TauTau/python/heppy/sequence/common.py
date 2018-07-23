import PhysicsTools.HeppyCore.framework.config as cfg

import ROOT 

# import all analysers:
# Heppy analyzers
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount import SkimAnalyzerCount
from PhysicsTools.Heppy.analyzers.core.EventSelector import EventSelector
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer import PileUpAnalyzer
from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer import LHEWeightAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerAnalyzer

from CMGTools.H2TauTau.heppy.analyzers.Selector import Selector
from CMGTools.H2TauTau.heppy.analyzers.EventFilter import EventFilter



puFileMC = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/pudistributions_mc_2017_artur_Jul9.root'
puFileData = '$CMSSW_BASE/src/CMGTools/H2TauTau/data/pudistributions_data_2017.root'

lheweight = cfg.Analyzer(
    LHEWeightAnalyzer, name="LHEWeightAnalyzer",
    useLumiInfo=False
)

json = cfg.Analyzer(
    JSONAnalyzer,
    name='JSONAnalyzer',
)

skim = cfg.Analyzer(
    SkimAnalyzerCount,
    name='SkimAnalyzerCount'
)


trigger = cfg.Analyzer(
    TriggerAnalyzer,
    name='TriggerAnalyzer',
    addTriggerObjects=True,
    requireTrigger=True,
    usePrescaled=False
)

vertex = cfg.Analyzer(
    VertexAnalyzer,
    name='VertexAnalyzer',
    fixedWeight=1,
    keepFailingEvents=True,
    verbose=False
)

pileup = cfg.Analyzer(
    PileUpAnalyzer,
    name='PileUpAnalyzer',
    true=True,
    autoPU=False
)


from CMGTools.H2TauTau.heppy.analyzers.TauAnalyzer import TauAnalyzer
taus = cfg.Analyzer(
    TauAnalyzer,
    output = 'taus',
    taus = 'slimmedTaus'
)


from CMGTools.H2TauTau.heppy.analyzers.MuonAnalyzer import MuonAnalyzer
muons = cfg.Analyzer(
    MuonAnalyzer,
    output = 'muons',
    muons = 'slimmedMuons',
)

from CMGTools.H2TauTau.heppy.analyzers.ElectronAnalyzer import ElectronAnalyzer
electrons = cfg.Analyzer(
    ElectronAnalyzer,
    output = 'electrons',
    electrons = 'slimmedElectrons',
)

# third lepton veto ==============================================================                                
def select_muon_third_lepton_veto(muon):
    return muon.pt() > 10             and \
        abs(muon.eta()) < 2.4         and \
        muon.muonID('POG_ID_Medium')  and \
        abs(muon.dxy()) < 0.045       and \
        abs(muon.dz())  < 0.2         and \
        muon.relIso(0.4, 'dbeta', dbeta_factor=0.5, all_charged=False) < 0.3
sel_muons_third_lepton_veto = cfg.Analyzer(
    Selector,
    '3lepv_muons',
    output = 'sel_muons_third_lepton_veto',
    src = 'muons',
    filter_func = select_muon_third_lepton_veto
)

def select_electron_third_lepton_veto(electron):
    return electron.pt() > 10             and \
        abs(electron.eta()) < 2.5         and \
        electron.mvaIDRun2("Fall17noIso","wp90")  and \
        abs(electron.dxy()) < 0.045       and \
        abs(electron.dz())  < 0.2         and \
        electron.passConversionVeto()     and \
        electron.gsfTrack().hitPattern().numberOfLostHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) <= 1 and \
        electron.relIso(0.3, "EA", area='03', all_charged=False) < 0.3
sel_electrons_third_lepton_veto = cfg.Analyzer(
    Selector,
    '3lepv_electrons',
    output = 'sel_electrons_third_lepton_veto',
    src = 'electrons',
    filter_func = select_electron_third_lepton_veto
)

# TODO this is for mu tau, change filter func in cfg for other channels
third_lepton_veto_muons = cfg.Analyzer(
    EventFilter,
    '3lepv_muons',
    src = 'sel_muons_third_lepton_veto',
    filter_func = lambda x : len(x) <= 1,
    output = 'veto_third_lepton_muons_passed'
)

third_lepton_veto_electrons = cfg.Analyzer(
    EventFilter,
    '3lepv_electrons',
    src = 'sel_electrons_third_lepton_veto',
    filter_func = lambda x : len(x) == 0,
    output = 'veto_third_lepton_electrons_passed'
)

sequence_third_lepton_veto = cfg.Sequence([
        sel_muons_third_lepton_veto,
        sel_electrons_third_lepton_veto,
        third_lepton_veto_muons,
        third_lepton_veto_electrons
])



sequence_beforedil = cfg.Sequence([
        json,
        skim,
        vertex,
        taus, 
        muons, 
        electrons,
])

sequence_beforedil.extend(sequence_third_lepton_veto)

sequence_afterdil = cfg.Sequence([
        trigger, 
        lheweight,
        pileup, 
]) 
