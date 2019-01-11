from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

Embedded2017B_tt = creator.makeDataComponent('Embedded2017B_tt', '/EmbeddingRun2017B/TauTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')
Embedded2017C_tt = creator.makeDataComponent('Embedded2017C_tt', '/EmbeddingRun2017C/TauTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')
Embedded2017D_tt = creator.makeDataComponent('Embedded2017D_tt', '/EmbeddingRun2017D/TauTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')
Embedded2017E_tt = creator.makeDataComponent('Embedded2017E_tt', '/EmbeddingRun2017E/TauTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')
Embedded2017F_tt = creator.makeDataComponent('Embedded2017F_tt', '/EmbeddingRun2017F/TauTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')

embedded_tt = [Embedded2017B_tt,Embedded2017C_tt,Embedded2017D_tt,Embedded2017E_tt,Embedded2017F_tt]


Embedded2017B_mt = creator.makeDataComponent('Embedded2017B_mt', '/EmbeddingRun2017B/MuTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')
Embedded2017C_mt = creator.makeDataComponent('Embedded2017C_mt', '/EmbeddingRun2017C/MuTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')
Embedded2017D_mt = creator.makeDataComponent('Embedded2017D_mt', '/EmbeddingRun2017D/MuTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')
Embedded2017E_mt = creator.makeDataComponent('Embedded2017E_mt', '/EmbeddingRun2017E/MuTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')
Embedded2017F_mt = creator.makeDataComponent('Embedded2017F_mt', '/EmbeddingRun2017F/MuTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')

embedded_mt = [Embedded2017B_mt,Embedded2017C_mt,Embedded2017D_mt,Embedded2017E_mt,Embedded2017F_mt]


Embedded2017B_et = creator.makeDataComponent('Embedded2017B_et', '/EmbeddingRun2017B/ElTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')
Embedded2017C_et = creator.makeDataComponent('Embedded2017C_et', '/EmbeddingRun2017C/ElTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')
Embedded2017D_et = creator.makeDataComponent('Embedded2017D_et', '/EmbeddingRun2017D/ElTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')
Embedded2017E_et = creator.makeDataComponent('Embedded2017E_et', '/EmbeddingRun2017E/ElTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')
Embedded2017F_et = creator.makeDataComponent('Embedded2017F_et', '/EmbeddingRun2017F/ElTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER', 'CMS', '.*root',dbsInstance='phys03')

embedded_et = [Embedded2017B_et,Embedded2017C_et,Embedded2017D_et,Embedded2017E_et,Embedded2017F_et]
