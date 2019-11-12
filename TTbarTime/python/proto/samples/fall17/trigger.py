from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerFilterMatch

############################################################################
# 2017
############################################################################

mc_triggers = [
    # electron
    'HLT_Ele35_WPTight_Gsf_v',
    'HLT_Ele38_WPTight_Gsf_v',
    'HLT_Ele40_WPTight_Gsf_v',
    'HLT_Ele32_WPTight_Gsf_L1DoubleEG_v',
    
    # muon
    'HLT_IsoMu24_eta2p1_v',      #Run A-D
    'HLT_IsoMu27_v',             #Run E-F
    
    # muon+electron
    'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v',
    'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v',
    'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL(_DZ)_v', #faire gaffe aux noms

    # double electron 
    'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL(_DZ)_v',
    
    # double muon 
    'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v'
]

data_triggers = [






    ]
