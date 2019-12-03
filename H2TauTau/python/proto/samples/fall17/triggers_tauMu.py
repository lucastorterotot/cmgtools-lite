from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerFilterMatch as TFM

# 2016 data
data_triggers = [
    'HLT_IsoMu24_v*',
    'HLT_IsoMu27_v*',
    'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*'
    ]

data_triggerfilters = [
    # IsoMu24
    TFM(trigtype='m',
        leg1_names=['hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07'], 
        leg2_names=[], 
        triggers=['HLT_IsoMu24_v*'],
        match_both_legs = False),

    # IsoMu27
    TFM(trigtype='m',
        leg1_names=['hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07'], 
        leg2_names=[], 
        triggers=['HLT_IsoMu27_v*'],
        match_both_legs = False), 

    
    TFM(trigtype='mt',
        leg1_names=['hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'],
        leg2_names=['hltSelectedPFTau27LooseChargedIsolationAgainstMuonL1HLTMatched','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'],
        triggers=['HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*']),
]

mc_triggers = [
    'HLT_IsoMu24_v*',
    'HLT_IsoMu27_v*',
    'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*',
    ]

mc_triggerfilters = [
    # IsoMu24
    TFM(trigtype='m',
        leg1_names=['hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07'], 
        leg2_names=[], 
        triggers=['HLT_IsoMu24_v*'],
        match_both_legs = False),

    # IsoMu27
    TFM(trigtype='m',
        leg1_names=['hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07'], 
        leg2_names=[], 
        triggers=['HLT_IsoMu27_v*'],
        match_both_legs = False),  
    
    # IsoMu19_eta2p1_LooseIsoPFTau20
    TFM(trigtype='mt',
        leg1_names=['hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'],
        leg2_names=['hltSelectedPFTau27LooseChargedIsolationAgainstMuonL1HLTMatched','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'],
        triggers=['HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*']), 

]

embed_triggers = data_triggers

embed_triggerfilters = [
    # IsoMu24
    TFM(trigtype='m',
        leg1_names=['hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07'], 
        leg2_names=[], 
        triggers=['HLT_IsoMu24_v*'],
        match_both_legs = False),

    # IsoMu27
    TFM(trigtype='m',
        leg1_names=['hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07'], 
        leg2_names=[], 
        triggers=['HLT_IsoMu27_v*'],
        match_both_legs = False), 

    
    TFM(trigtype='mt',
        leg1_names=['hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07','hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded'],
        leg2_names=['hltL1sMu18erTau24erIorMu20erTau24er'],
        triggers=['HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v*']),

]
