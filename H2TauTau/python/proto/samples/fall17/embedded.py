import os
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

json = os.path.expandvars('$CMSSW_BASE/src/CMGTools/H2TauTau/data/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt')
lumi = 41529.

# Embedded2017B_tt = creator.makeDataComponent("Embedded2017B_tt", "/EmbeddingRun2017B/StoreResults-inputDoubleMu_94X_miniAOD-v1/USER", "CMS", ".*root")
Embedded2017B_tt = creator.makeDataComponent('Embedded2017B_tt', '/EmbeddingRun2017B/TauTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017C_tt = creator.makeDataComponent('Embedded2017C_tt', '/EmbeddingRun2017C/TauTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017D_tt = creator.makeDataComponent('Embedded2017D_tt', '/EmbeddingRun2017D/TauTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017E_tt = creator.makeDataComponent('Embedded2017E_tt', '/EmbeddingRun2017E/TauTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017F_tt = creator.makeDataComponent("Embedded2017F_tt", "/EmbeddingRun2017F/TauTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER", "CMS", ".*root")
# Embedded2017F_tt = creator.makeDataComponent('Embedded2017F_tt', '/EmbeddingRun2017F/TauTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')

embedded_tt = [Embedded2017B_tt,Embedded2017C_tt,Embedded2017D_tt,Embedded2017E_tt,Embedded2017F_tt]


Embedded2017B_mt = creator.makeDataComponent('Embedded2017B_mt', '/EmbeddingRun2017B/MuTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017C_mt = creator.makeDataComponent('Embedded2017C_mt', '/EmbeddingRun2017C/MuTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017D_mt = creator.makeDataComponent('Embedded2017D_mt', '/EmbeddingRun2017D/MuTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017E_mt = creator.makeDataComponent('Embedded2017E_mt', '/EmbeddingRun2017E/MuTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017F_mt = creator.makeDataComponent('Embedded2017F_mt', '/EmbeddingRun2017F/MuTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')

embedded_mt = [Embedded2017B_mt,Embedded2017C_mt,Embedded2017D_mt,Embedded2017E_mt,Embedded2017F_mt]


Embedded2017B_et = creator.makeDataComponent('Embedded2017B_et', '/EmbeddingRun2017B/ElTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017C_et = creator.makeDataComponent('Embedded2017C_et', '/EmbeddingRun2017C/ElTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017D_et = creator.makeDataComponent('Embedded2017D_et', '/EmbeddingRun2017D/ElTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017E_et = creator.makeDataComponent('Embedded2017E_et', '/EmbeddingRun2017E/ElTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017F_et = creator.makeDataComponent('Embedded2017F_et', '/EmbeddingRun2017F/ElTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')

embedded_et = [Embedded2017B_et,Embedded2017C_et,Embedded2017D_et,Embedded2017E_et,Embedded2017F_et]

for sample in embedded_tt+embedded_mt+embedded_et:
    sample.json = json
    sample.lumi = lumi
