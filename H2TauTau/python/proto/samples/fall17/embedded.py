from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

# Embedded2017B_tt = creator.makeDataComponent("Embedded2017B_tt", "/EmbeddingRun2017B/StoreResults-inputDoubleMu_94X_miniAOD-v1/USER", "CMS", ".*root")
Embedded2017B_tt = creator.makeDataComponent('Embedded2017B_tt', '/EmbeddingRun2017B/TauTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017C_tt = creator.makeDataComponent('Embedded2017C_tt', '/EmbeddingRun2017C/TauTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017D_tt = creator.makeDataComponent('Embedded2017D_tt', '/EmbeddingRun2017D/TauTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017E_tt = creator.makeDataComponent('Embedded2017E_tt', '/EmbeddingRun2017E/TauTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root')
Embedded2017F_tt = creator.makeDataComponent("Embedded2017F_tt", "/EmbeddingRun2017F/TauTauFinalState-StoreResults_inputDoubleMu_94X_miniAOD-v2/USER", "CMS", ".*root")
# Embedded2017F_tt = creator.makeDataComponent('Embedded2017F_tt', '/EmbeddingRun2017F/TauTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')

embedded_tt = [Embedded2017B_tt,Embedded2017C_tt,Embedded2017D_tt,Embedded2017E_tt,Embedded2017F_tt]
