from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerFilterMatch as TFM

data_triggers = [
    'HLT_Ele27_WPTight_Gsf_v*',
    'HLT_Ele32_WPTight_Gsf_v*',
    'HLT_Ele35_WPTight_Gsf_v*',
    'HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v*'
    ]

data_triggerfilters = [
    # Ele27
    TFM(trigtype='e',
        leg1_names=['hltEle27WPTightGsfTrackIsoFilter'], 
        leg2_names=[], 
        triggers=['HLT_Ele27_WPTight_Gsf_v*'],
        match_both_legs = False),
    # Ele32
    TFM(trigtype='e',
        leg1_names=['hltEle32WPTightGsfTrackIsoFilter'], 
        leg2_names=[], 
        triggers=['HLT_Ele32_WPTight_Gsf_v*'],
        match_both_legs = False),
    # Ele35
    TFM(trigtype='e',
        leg1_names=['hltEle35noerWPTightGsfTrackIsoFilter'], 
        leg2_names=[], 
        triggers=['HLT_Ele35_WPTight_Gsf_v*'],
        match_both_legs = False),
    # CrossTrigger
    TFM(trigtype='et',
        leg1_names=['hltEle24erWPTightGsfTrackIsoFilterForTau','hltOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30'], 
        leg2_names=['hltSelectedPFTau30LooseChargedIsolationL1HLTMatched','hltOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30'], 
        triggers=['HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v*'])
]

mc_triggers = [
    'HLT_Ele27_WPTight_Gsf_v*',
    'HLT_Ele32_WPTight_Gsf_v*',
    'HLT_Ele35_WPTight_Gsf_v*',
    'HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v*'
    ]

mc_triggerfilters = [
    # Ele27
    TFM(trigtype='e',
        leg1_names=['hltEle27WPTightGsfTrackIsoFilter'], 
        leg2_names=[], 
        triggers=['HLT_Ele27_WPTight_Gsf_v*'],
        match_both_legs = False),
    # Ele32
    TFM(trigtype='e',
        leg1_names=['hltEle32WPTightGsfTrackIsoFilter'], 
        leg2_names=[], 
        triggers=['HLT_Ele32_WPTight_Gsf_v*'],
        match_both_legs = False),
    # Ele35
    TFM(trigtype='e',
        leg1_names=['hltEle35noerWPTightGsfTrackIsoFilter'], 
        leg2_names=[], 
        triggers=['HLT_Ele35_WPTight_Gsf_v*'],
        match_both_legs = False),
    # CrossTrigger
    TFM(trigtype='et',
        leg1_names=['hltEle24erWPTightGsfTrackIsoFilterForTau','hltOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30'], 
        leg2_names=['hltSelectedPFTau30LooseChargedIsolationL1HLTMatched','hltOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30'], 
        triggers=['HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v*'])
]

embed_triggers = data_triggers

embed_triggerfilters = [
    # Ele27
    TFM(trigtype='e',
        leg1_names=['hltEle27WPTightGsfTrackIsoFilter'], 
        leg2_names=[], 
        triggers=['HLT_Ele27_WPTight_Gsf_v*'],
        match_both_legs = False),
    # Ele32
    TFM(trigtype='e',
        leg1_names=['hltEle32WPTightGsfTrackIsoFilter'], 
        leg2_names=[], 
        triggers=['HLT_Ele32_WPTight_Gsf_v*'],
        match_both_legs = False),
    # Ele35
    TFM(trigtype='e',
        leg1_names=['hltEle35noerWPTightGsfTrackIsoFilter'], 
        leg2_names=[], 
        triggers=['HLT_Ele35_WPTight_Gsf_v*'],
        match_both_legs = False),
    # CrossTrigger
    TFM(trigtype='et',
        leg1_names=['hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3'], 
        leg2_names=['hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3'], 
        triggers=['HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v*'])
]
