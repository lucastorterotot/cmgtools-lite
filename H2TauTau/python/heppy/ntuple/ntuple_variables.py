from tools import *
import math

default = Variable.default

event = Block(
    'event', lambda x: x,
    run = v(lambda x: x.run, int),
    lumi = v(lambda x: x.lumi, int),
    event = v(lambda x: x.eventId, int, 'l'),
    n_up = v(lambda x: getattr(x, 'NUP', default), int),
    n_pu = v(lambda x: getattr(x, 'nPU', default) if getattr(x, 'nPU', default) is not None else default, int),# to handle data and embedded samples
    n_pv = v(lambda x: len(x.vertices), int),
    rho = v(lambda x: x.rho),
    is_data = v(lambda x: x.input.eventAuxiliary().isRealData(), int),
    )

generator = Block(
    'generator', lambda x: x,
    gen_boson_pt = v(lambda x: getattr(x, 'genPartonHT', default)),
    gen_boson_mass = v(lambda x : getattr(x, 'geninvmass', default)),
    gen_top1_pt = v(lambda x : getattr(x, 'top1_pt', default)),
    gen_top2_pt = v(lambda x : getattr(x, 'top2_pt', default)),
    )

flags = [
    'Flag_goodVertices',
    'Flag_globalTightHalo2016Filter',
    'Flag_globalSuperTightHalo2016Filter',
    'Flag_HBHENoiseFilter',
    'Flag_HBHENoiseIsoFilter',
    'Flag_EcalDeadCellTriggerPrimitiveFilter',
    'Flag_BadPFMuonFilter',
    'Flag_BadChargedCandidateFilter',
    'Flag_eeBadScFilter',
    'Flag_ecalBadCalibFilter'
]
event_flags = Block('event_flags', lambda x: x)
for flag in flags: 
    event_flags[flag] = v(lambda x: getattr(x,flag,1), int) #flag default at 1 because no flag means event is good

vetoes = Block(
    'vetoes', lambda x: x,
    veto_dilepton = v(lambda x: not getattr(x,'veto_dilepton_passed',True), int),
    veto_extra_elec = v(lambda x: not x.veto_third_lepton_electrons_passed, int),
    veto_extra_muon = v(lambda x: not x.veto_third_lepton_muons_passed, int),
)

jets20 = Block(
    'jets20', lambda x: x.jets_20,
    n_jets_pt20 = v(lambda x: len(x), int),
    j1_pt = v(lambda x: x[0].pt() if len(x)>0 else default),
    j1_eta = v(lambda x: x[0].eta() if len(x)>0 else default),
    j1_phi = v(lambda x: x[0].phi() if len(x)>0 else default),
    # j1_bcsv = v(lambda x: x.bcsv()),
    j1_pumva = v(lambda x: x[0].puMva('pileupJetId:fullDiscriminant') if len(x)>0 else default),
#    j1_puid = v(lambda x: x[0].pileUpJetId_htt() if len(x)>0 else default),
    j1_flavour_parton = v(lambda x: x[0].partonFlavour() if len(x)>0 else default),
    j1_flavour_hadron = v(lambda x: x[0].hadronFlavour() if len(x)>0 else default),
    j1_rawf = v(lambda x: x[0].rawFactor() if len(x)>0 else default),
    j2_pt = v(lambda x: x[1].pt() if len(x)>1 else default),
    j2_eta = v(lambda x: x[1].eta() if len(x)>1 else default),
    j2_phi = v(lambda x: x[1].phi() if len(x)>1 else default),
    j2_pumva = v(lambda x: x[1].puMva('pileupJetId:fullDiscriminant') if len(x)>1 else default ),
#    j2_puid = v(lambda x: x[1].pileUpJetId_htt() if len(x)>1 else default ),
    j2_flavour_parton = v(lambda x: x[1].partonFlavour() if len(x)>1 else default),
    j2_flavour_hadron = v(lambda x: x[1].hadronFlavour() if len(x)>1 else default),
    j2_rawf = v(lambda x: x[1].rawFactor() if len(x)>1 else default),
    dijet_m = v(lambda x: (x[0].p4()+x[1].p4()).M() if len(x)>1 else default),
)

bjets = Block(
    'bjets', lambda x: x.bjets_20,
    n_bjets = v(lambda x: len(x), int),
)
for vname, variable in jets20.iteritems():
    if not vname.startswith('j'):
        continue
    newname = vname.replace('j1','b1',1)
    newname = newname.replace('j2','b2',1)
    bjets[newname] = variable

jets30 = Block(
    'jets30', lambda x: x.jets_30,
    n_jets_pt30 = v(lambda x: len(x), int),
    j1_pt_pt30 = v(lambda x: x[0].pt() if len(x)>0 else default),
    j1_eta_pt30 = v(lambda x: x[0].eta() if len(x)>0 else default),
    j1_phi_pt30 = v(lambda x: x[0].phi() if len(x)>0 else default),
    # j1_bcsv = v(lambda x: x.bcsv()),
    j1_pumva_pt30 = v(lambda x: x[0].puMva('pileupJetId:fullDiscriminant') if len(x)>0 else default),
#    j1_puid = v(lambda x: x[0].pileUpJetId_htt() if len(x)>0 else default),
    j1_flavour_parton_pt30 = v(lambda x: x[0].partonFlavour() if len(x)>0 else default),
    j1_flavour_hadron_pt30 = v(lambda x: x[0].hadronFlavour() if len(x)>0 else default),
    j1_rawf_pt30 = v(lambda x: x[0].rawFactor() if len(x)>0 else default),
    j2_pt_pt30 = v(lambda x: x[1].pt() if len(x)>1 else default),
    j2_eta_pt30 = v(lambda x: x[1].eta() if len(x)>1 else default),
    j2_phi_pt30 = v(lambda x: x[1].phi() if len(x)>1 else default),
    j2_pumva_pt30 = v(lambda x: x[1].puMva('pileupJetId:fullDiscriminant') if len(x)>1 else default ),
#    j2_puid = v(lambda x: x[1].pileUpJetId_htt() if len(x)>1 else default ),
    j2_flavour_parton_pt30 = v(lambda x: x[1].partonFlavour() if len(x)>1 else default),
    j2_flavour_hadron_pt30 = v(lambda x: x[1].hadronFlavour() if len(x)>1 else default),
    j2_rawf_pt30 = v(lambda x: x[1].rawFactor() if len(x)>1 else default),
    dijet_m_pt30 = v(lambda x: (x[0].p4()+x[1].p4()).M() if len(x)>1 else default),
)


weights = Block(
    'weights', lambda x: x, 
    weight = v(lambda x : x.eventWeight),
    weight_pu = v(lambda x : getattr(x, 'puWeight', 1.)),
    weight_dy = v(lambda x : getattr(x, 'dy_weight', 1.)),
    weight_top = v(lambda x : getattr(x, 'topweight', 1.)),
    weight_generator = v(lambda x : getattr(x, 'weight_gen', 1.)),
    weight_njet = v(lambda x : x.NJetWeight),
    ###weights embedding
    weight_embed_DoubleMuonHLT_eff = v(lambda x : getattr(x, 'weight_embed_DoubleMuonHLT_eff', 1.)),
    weight_embed_muonID_eff_l1 = v(lambda x : getattr(x, 'weight_embed_muonID_eff_l1', 1.)),
    weight_embed_muonID_eff_l2 = v(lambda x : getattr(x, 'weight_embed_muonID_eff_l2', 1.)),
    weight_embed_DoubleTauHLT_eff_l1 = v(lambda x : getattr(x, 'weight_embed_DoubleTauHLT_eff_l1', 1.)),
    weight_embed_DoubleTauHLT_eff_l2 = v(lambda x : getattr(x, 'weight_embed_DoubleTauHLT_eff_l2', 1.)),
    weight_embed_track_l1 = v(lambda x : getattr(x, 'weight_embed_track_l1', 1.)),
    weight_embed_track_l2 = v(lambda x : getattr(x, 'weight_embed_track_l2', 1.))
) 

triggers = Block(
    'triggers', lambda x: [getattr(x.dileptons_sorted[0], 'matchedPaths', []),x.dileptons_sorted[0]],
    trg_singletau1 = v(lambda x : any('MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v' in name for name in x[0]) and x[1].leg1().pt()>45. and abs(x[1].leg1().eta())<2.1),
    trg_singletau2 = v(lambda x : any('MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v' in name for name in x[0]) and x[1].leg2().pt()>45. and abs(x[1].leg2().eta())<2.1),
    trg_singletau  = v(lambda x : any('MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v' in name for name in x[0]) and any([tau.pt()>45. and abs(tau.eta()<2.1) for tau in [x[1].leg1(), x[1].leg2()]])),
    trg_singlemuon_24 = v(lambda x : any('IsoMu24_v' in name for name in x[0]) and x[1].leg1().pt()>25. and abs(x[1].leg1().eta())<2.1),
    trg_singlemuon_27 = v(lambda x : any('IsoMu27_v' in name for name in x[0]) and x[1].leg1().pt()>28. and abs(x[1].leg1().eta())<2.1),
    trg_singleelectron_27 = v(lambda x : any('Ele27_WPTight_Gsf_v' in name for name in x[0]) and x[1].leg1().pt()>28. and abs(x[1].leg1().eta())<2.1),
    trg_singleelectron_32 = v(lambda x : any('Ele32_WPTight_Gsf_v' in name for name in x[0]) and x[1].leg1().pt()>33. and abs(x[1].leg1().eta())<2.1),
    trg_singleelectron_35 = v(lambda x : any('Ele35_WPTight_Gsf_v' in name for name in x[0]) and x[1].leg1().pt()>36. and abs(x[1].leg1().eta())<2.1),
    trg_doubletau_35_mediso = v(lambda x : any('DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v' in name for name in x[0]) and all([tau.pt()>40. and abs(tau.eta()<2.1) for tau in [x[1].leg1(), x[1].leg2()]])),
    trg_doubletau_35_tightiso_tightid = v(lambda x : any('DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v' in name for name in x[0]) and all([tau.pt()>40. and abs(tau.eta()<2.1) for tau in [x[1].leg1(), x[1].leg2()]])),
    trg_doubletau_40_mediso_tightid = v(lambda x : any('DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v' in name for name in x[0]) and all([tau.pt()>45. and abs(tau.eta()<2.1) for tau in [x[1].leg1(), x[1].leg2()]])),
    trg_doubletau_40_tightiso = v(lambda x : any('DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v' in name for name in x[0]) and all([tau.pt()>45. and abs(tau.eta()<2.1) for tau in [x[1].leg1(), x[1].leg2()]])),
    trg_crossmuon_mu24tau20 = v(lambda x : any('IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1_v' in name for name in x[0]) and x[1].leg1().pt()>25. and abs(x[1].leg1().eta())<2.1 and x[1].leg2().pt()>21. and abs(x[1].leg2().eta())<2.1),
    trg_crossmuon_mu20tau27 = v(lambda x : any('IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v' in name for name in x[0]) and x[1].leg1().pt()>21. and abs(x[1].leg1().eta())<2.1 and x[1].leg2().pt()>32. and abs(x[1].leg2().eta())<2.1),
    trg_crossele_ele24tau30 = v(lambda x : any('Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v' in name for name in x[0]) and x[1].leg1().pt()>25. and abs(x[1].leg1().eta())<2.1 and x[1].leg2().pt()>35. and abs(x[1].leg2().eta())<2.1),
    trg_muonelectron_mu8ele23 = v(lambda x : any('Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x[0]) and x[1].leg1().pt()>24. and abs(x[1].leg1().eta())<2.5 and x[1].leg2().pt()>9. and abs(x[1].leg2().eta())<2.4),
    trg_muonelectron_mu12ele23 = v(lambda x : any('Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x[0]) and x[1].leg1().pt()>24.  and abs(x[1].leg1().eta())<2.5 and x[1].leg2().pt()>13.and abs(x[1].leg2().eta())<2.4),
    trg_muonelectron_mu23ele12 = v(lambda x : any('Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x[0]) and x[1].leg1().pt()>13.  and abs(x[1].leg1().eta())<2.5 and x[1].leg2().pt()>24.and abs(x[1].leg2().eta())<2.4)
)

triggers_matched = Block(
    'triggers_matched', lambda x: [getattr(x.dileptons_sorted[0], 'matchedPaths', []),x.dileptons_sorted[0]],
    trg_singletau_matched  = v(lambda x : any('MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v' in name for name in x[0])),
    trg_singlemuon_24_matched = v(lambda x : any('IsoMu24_v' in name for name in x[0])),
    trg_singlemuon_27_matched = v(lambda x : any('IsoMu27_v' in name for name in x[0])),
    trg_singleelectron_27_matched = v(lambda x : any('Ele27_WPTight_Gsf_v' in name for name in x[0])),
    trg_singleelectron_32_matched = v(lambda x : any('Ele32_WPTight_Gsf_v' in name for name in x[0])),
    trg_singleelectron_35_matched = v(lambda x : any('Ele35_WPTight_Gsf_v' in name for name in x[0])),
    trg_doubletau_35_mediso_matched = v(lambda x : any('DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v' in name for name in x[0])),
    trg_doubletau_35_tightiso_tightid_matched = v(lambda x : any('DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v' in name for name in x[0])),
    trg_doubletau_40_mediso_tightid_matched = v(lambda x : any('DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v' in name for name in x[0])),
    trg_doubletau_40_tightiso_matched = v(lambda x : any('DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v' in name for name in x[0])),
    trg_crossmuon_mu24tau20_matched = v(lambda x : any('IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1_v' in name for name in x[0])),
    trg_crossmuon_mu20tau27_matched = v(lambda x : any('IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v' in name for name in x[0])),
    trg_crossele_ele24tau30_matched = v(lambda x : any('Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v' in name for name in x[0])),
    trg_muonelectron_mu8ele23_matched = v(lambda x : any('Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x[0])),
    trg_muonelectron_mu12ele23_matched = v(lambda x : any('Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x[0])),
    trg_muonelectron_mu23ele12_matched = v(lambda x : any('Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x[0]))
)

triggers_fired = Block(
    'triggers_fired', lambda x: getattr(x, 'trigger_infos', []),
    trg_singletau_fired  = v(lambda x : any('MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v' in trg.name for trg in x if trg.fired)),
    trg_singlemuon_24_fired = v(lambda x : any('IsoMu24_v' in trg.name for trg in x if trg.fired)),
    trg_singlemuon_27_fired = v(lambda x : any('IsoMu27_v' in trg.name for trg in x if trg.fired)),
    trg_singleelectron_27_fired = v(lambda x : any('Ele27_WPTight_Gsf_v' in trg.name for trg in x if trg.fired)),
    trg_singleelectron_32_fired = v(lambda x : any('Ele32_WPTight_Gsf_v' in trg.name for trg in x if trg.fired)),
    trg_singleelectron_35_fired = v(lambda x : any('Ele35_WPTight_Gsf_v' in trg.name for trg in x if trg.fired)),
    trg_doubletau_35_mediso_fired = v(lambda x : any('DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v' in trg.name for trg in x if trg.fired)),
    trg_doubletau_35_tightiso_tightid_fired = v(lambda x : any('DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v' in trg.name for trg in x if trg.fired)),
    trg_doubletau_40_mediso_tightid_fired = v(lambda x : any('DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v' in trg.name for trg in x if trg.fired)),
    trg_doubletau_40_tightiso_fired = v(lambda x : any('DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v' in trg.name for trg in x if trg.fired)),
    trg_crossmuon_mu24tau20_fired = v(lambda x : any('IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1_v' in trg.name for trg in x if trg.fired)),
    trg_crossmuon_mu20tau27_fired = v(lambda x : any('IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v' in trg.name for trg in x if trg.fired)),
    trg_crossele_ele24tau30_fired = v(lambda x : any('Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v' in trg.name for trg in x if trg.fired)),
    trg_muonelectron_mu8ele23_fired = v(lambda x : any('Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in trg.name for trg in x if trg.fired)),
    trg_muonelectron_mu12ele23_fired = v(lambda x : any('Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in trg.name for trg in x if trg.fired)),
    trg_muonelectron_mu23ele12_fired = v(lambda x : any('Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v' in trg.name for trg in x if trg.fired))
)

lepton_vars = dict(
    pt = v(lambda x: x.pt()),
    eta = v(lambda x: x.eta()),
    phi = v(lambda x: x.phi()),
    m = v(lambda x: x.mass()),
    q = v(lambda x: x.charge()),
    weight_id = v(lambda x: getattr(x, 'weight_id', 1.)),
    weight_iso = v(lambda x: getattr(x, 'weight_iso', 1.)),
    weight_idiso = v(lambda x: getattr(x, 'weight_idiso', 1.)),
    gen_match = v(lambda x: getattr(x, 'gen_match', 0), int),
)

dilepton_vars = Block(
    'dilepton', lambda x: [x.dileptons_sorted[0],x.pfmet],
    m_vis = v(lambda x: x[0].mass()),
    mt_tot = v(lambda x: x[0].mtTotal(x[1])),
    l1_mt = v(lambda x: x[0].mTLeg1(x[1])),
    l2_mt = v(lambda x: x[0].mTLeg2(x[1])),
    pt_tt = v(lambda x: x[0].pt_tt(x[1]))
)

metvars = Block(
    'metvars', lambda x: x.pfmet,
    met = v(lambda x: x.pt()),
    metphi = v(lambda x: x.phi()),
)

electron_vars = dict(
    id_e_mva_nt_loose = v(lambda x: x.physObj.userFloat("ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values")), 
    weight_tracking = v(lambda x: getattr(x, 'weight_trk', 1. )),
    iso = v(lambda x: x.iso_htt()),
    d0 = v(lambda x: x.dxy()),
    dz = v(lambda x: x.dz()),
    weight_trig_e = v(lambda x: getattr(x, 'weight_trigger_e', 1.)),
    weight_trig_et = v(lambda x: getattr(x, 'weight_trigger_et', 1.)),
)

muon_vars = dict(
    weight_tracking = v(lambda x: getattr(x, 'weight_tracking', 1. )),
    iso = v(lambda x: x.iso_htt()), 
    d0 = v(lambda x: x.dxy()),
    dz = v(lambda x: x.dz()),  
    weight_trig_m = v(lambda x: getattr(x, 'weight_trigger_m', 1.)),
    weight_trig_mt = v(lambda x: getattr(x, 'weight_trigger_mt', 1.)),
)

tau_ids = [
    'decayModeFinding',
    'byIsolationMVArun2017v2DBoldDMwLTraw2017',
    'byVVLooseIsolationMVArun2017v2DBoldDMwLT2017',
    'byVLooseIsolationMVArun2017v2DBoldDMwLT2017',
    'byLooseIsolationMVArun2017v2DBoldDMwLT2017',
    'byMediumIsolationMVArun2017v2DBoldDMwLT2017',
    'byTightIsolationMVArun2017v2DBoldDMwLT2017',
    'byVTightIsolationMVArun2017v2DBoldDMwLT2017',
    'byVVTightIsolationMVArun2017v2DBoldDMwLT2017',
    'againstElectronVLooseMVA6',
    'againstElectronTightMVA6',
    'againstMuonTight3',
    'againstMuonLoose3',
    'chargedIsoPtSum',
    'neutralIsoPtSum',
    'puCorrPtSum',
    'footprintCorrection',
    'photonPtSumOutsideSignalCone'
]

tau_vars = dict(
    # weight_fakerate = v(lambda x: x),
    decay_mode = v(lambda x: x.decayMode(), int),
    d0 = v(lambda x: x.leadChargedHadrCand().dxy()),
    dz = v(lambda x: x.leadChargedHadrCand().dz()),
    weight_etotaufake_vloose = v(lambda x : getattr(x, 'weight_EToTaufake_VLoose', 1.)),
    weight_etotaufake_loose = v(lambda x : getattr(x, 'weight_EToTaufake_Loose', 1.)),
    weight_etotaufake_medium = v(lambda x : getattr(x, 'weight_EToTaufake_Medium', 1.)),
    weight_etotaufake_tight = v(lambda x : getattr(x, 'weight_EToTaufake_Tight', 1.)),
    weight_etotaufake_vtight = v(lambda x : getattr(x, 'weight_EToTaufake_VTight', 1.)),
    weight_mutotaufake_vloose = v(lambda x : getattr(x, 'weight_MuToTaufake_VLoose', 1.)),
    weight_mutotaufake_loose = v(lambda x : getattr(x, 'weight_MuToTaufake_Loose', 1.)),
    weight_mutotaufake_medium = v(lambda x : getattr(x, 'weight_MuToTaufake_Medium', 1.)),
    weight_mutotaufake_tight = v(lambda x : getattr(x, 'weight_MuToTaufake_Tight', 1.)),
    weight_mutotaufake_vtight = v(lambda x : getattr(x, 'weight_MuToTaufake_VTight', 1.)),
    weight_tauid_vloose = v(lambda x : getattr(x, 'weight_TauID_VLoose', 1.)),
    weight_tauid_loose = v(lambda x : getattr(x, 'weight_TauID_Loose', 1.)),
    weight_tauid_medium = v(lambda x : getattr(x, 'weight_TauID_Medium', 1.)),
    weight_tauid_tight = v(lambda x : getattr(x, 'weight_TauID_Tight', 1.)),
    weight_tauid_vtight = v(lambda x : getattr(x, 'weight_TauID_VTight', 1.)),
    weight_fakefactor_inclusive = v(lambda x : getattr(x, 'weight_fakefactor_inclusive', 1.)),
    weight_fakefactor_inclusive_up = v(lambda x : getattr(x, 'weight_fakefactor_inclusive_up', 1.)),
    weight_fakefactor_inclusive_down = v(lambda x : getattr(x, 'weight_fakefactor_inclusive_down', 1.)),
    weight_fakefactor_btag = v(lambda x : getattr(x, 'weight_fakefactor_btag', 1.)),
    weight_fakefactor_btag_up = v(lambda x : getattr(x, 'weight_fakefactor_btag_up', 1.)),
    weight_fakefactor_btag_down = v(lambda x : getattr(x, 'weight_fakefactor_btag_down', 1.)),
    weight_fakefactor_nobtag = v(lambda x : getattr(x, 'weight_fakefactor_nobtag', 1.)),
    weight_fakefactor_nobtag_up = v(lambda x : getattr(x, 'weight_fakefactor_nobtag_up', 1.)),
    weight_fakefactor_nobtag_down = v(lambda x : getattr(x, 'weight_fakefactor_nobtag_down', 1.)),
    weight_trig_t = v(lambda x: getattr(x, 'weight_trigger_t', 1.)),
    weight_trig_tt = v(lambda x: getattr(x, 'weight_trigger_tt', 1.)),
    weight_trig_et = v(lambda x: getattr(x, 'weight_trigger_et', 1.)),
    weight_trig_mt = v(lambda x: getattr(x, 'weight_trigger_mt', 1.)),
)

# necessary, or all lambdas will be the same! 
def make_func(tauid):
    return lambda x : x.tauID(tauid)
for tauid in tau_ids: 
    tau_vars[tauid] = v(make_func(tauid))


common = EventContent(
    [event, generator, weights, event_flags, metvars,
     triggers, triggers_matched, triggers_fired, jets20, jets30, bjets, vetoes,
     dilepton_vars,
     to_leg('l1_generic', lepton_vars, 'l1', 
            lambda x: x.dileptons_sorted[0].leg1()), 
     to_leg('l2_generic', lepton_vars, 'l2', 
            lambda x: x.dileptons_sorted[0].leg2()), 
     ]
)

mutau = copy.copy(common)
mutau.append(to_leg('l1_specific', muon_vars, 'l1', 
                    lambda x: x.dileptons_sorted[0].leg1()))
mutau.append(to_leg('l2_specific', tau_vars, 'l2', 
                    lambda x: x.dileptons_sorted[0].leg2()))


eletau = copy.copy(common)
eletau.append(to_leg('l1_specific', electron_vars, 'l1', 
                    lambda x: x.dileptons_sorted[0].leg1()))
eletau.append(to_leg('l2_specific', tau_vars, 'l2', 
                    lambda x: x.dileptons_sorted[0].leg2()))

tautau = copy.copy(common)
tautau.append(to_leg('l1_specific', tau_vars, 'l1',
                    lambda x: x.dileptons_sorted[0].leg1()))
tautau.append(to_leg('l2_specific', tau_vars, 'l2',
                    lambda x: x.dileptons_sorted[0].leg2()))
