import PhysicsTools.HeppyCore.framework.config as cfg

# import all analysers:
# Heppy analyzers
from PhysicsTools.Heppy.analyzers.core.JSONAnalyzer import JSONAnalyzer
from PhysicsTools.Heppy.analyzers.core.SkimAnalyzerCount import SkimAnalyzerCount
from PhysicsTools.Heppy.analyzers.core.EventSelector import EventSelector
from PhysicsTools.Heppy.analyzers.objects.VertexAnalyzer import VertexAnalyzer
from PhysicsTools.Heppy.analyzers.core.PileUpAnalyzer import PileUpAnalyzer
from PhysicsTools.Heppy.analyzers.gen.LHEWeightAnalyzer import LHEWeightAnalyzer
from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerAnalyzer

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

sequence_init = cfg.Sequence([
    lheweight,
    json,
    skim,
    trigger,  # First analyser that applies selections
    vertex,
    pileup
])
