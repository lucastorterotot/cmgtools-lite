from CMGTools.H2TauTau.proto.analyzers.TriggerAnalyzer import TriggerFilterMatch

data_triggers = [
    # 'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v2', # up to run 274733
    # 'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v3', # up to run 276837
    # 'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v4', # up to run 278240
    # 'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v5', # up to run 280960
    # 'HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v2', # up to run 282544
    # 'HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v3', # up to run 284044

    # 'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v1', # runs 274748-276244
    # 'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v2', # runs 276271-278240
    # 'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v3', # runs 278270-280960
    # 'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v5', # runs 281010-284044
    'HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v*',
    'HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v*',
    'HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v*',
    ]

data_triggerfilters = [
    TriggerFilterMatch(trigtype='tt',
                       leg1_names=['hltDoublePFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsDz02Reg'],
                       leg2_names=['hltDoublePFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsDz02Reg'],
                       triggers=['HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v*']),
    TriggerFilterMatch(trigtype='tt',
                       leg1_names=['hltDoublePFTau40TrackPt1MediumChargedIsolationAndTightOOSCPhotonsDz02Reg'],
                       leg2_names=['hltDoublePFTau40TrackPt1MediumChargedIsolationAndTightOOSCPhotonsDz02Reg'],
                       triggers=['HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v*']),
    TriggerFilterMatch(trigtype='tt',
                       leg1_names=['hltDoublePFTau40TrackPt1TightChargedIsolationDz02Reg'],
                       leg2_names=['hltDoublePFTau40TrackPt1TightChargedIsolationDz02Reg'],
                       triggers=['HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v*']),
]

embedded_triggerfilters = [
    TriggerFilterMatch(trigtype='tt',
                       leg1_names=['hltDoubleL2IsoTau26eta2p2'],
                       leg2_names=['hltDoubleL2IsoTau26eta2p2'],
                       triggers=['HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v*']),
    TriggerFilterMatch(trigtype='tt',
                       leg1_names=['hltDoubleL2IsoTau26eta2p2'],
                       leg2_names=['hltDoubleL2IsoTau26eta2p2'],
                       triggers=['HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v*']),
    TriggerFilterMatch(trigtype='tt',
                       leg1_names=['hltDoubleL2IsoTau26eta2p2'],
                       leg2_names=['hltDoubleL2IsoTau26eta2p2'],
                       triggers=['HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v*']),
]

mc_triggers = [
    # 'HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v5',
    # 'HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v2',
    # # 'HLT_DoubleMediumCombinedIsoPFTau40_Trk1_eta2p1_Reg_v1', # higher threshold
    # 'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v5',
    # 'HLT_VLooseIsoPFTau120_Trk50_eta2p1_v5',
    # # 'HLT_PFTau140_eta2p1_v5' # prescaled
    'HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v*',
    'HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v*',
    'HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v*',
    ]

mc_triggerfilters = [
    TriggerFilterMatch(trigtype='tt',
                       leg1_names=['hltDoublePFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsDz02Reg'], 
                       leg2_names=['hltDoublePFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsDz02Reg'],
                       triggers=['HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v*']),
    TriggerFilterMatch(trigtype='tt',
                       leg1_names=['hltDoublePFTau40TrackPt1MediumChargedIsolationAndTightOOSCPhotonsDz02Reg'], 
                       leg2_names=['hltDoublePFTau40TrackPt1MediumChargedIsolationAndTightOOSCPhotonsDz02Reg'],
                       triggers=['HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v*']),
    TriggerFilterMatch(trigtype='tt',
                       leg1_names=['hltDoublePFTau40TrackPt1TightChargedIsolationDz02Reg'], 
                       leg2_names=['hltDoublePFTau40TrackPt1TightChargedIsolationDz02Reg'],
                       triggers=['HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v*']),
]

embed_triggers = [
    ]
