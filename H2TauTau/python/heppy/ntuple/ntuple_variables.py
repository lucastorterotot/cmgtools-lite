from tools import * 

default = Variable.default

event = Block(
    'event', lambda x: x,
    run = v(lambda x: x.run, int),
    lumi = v(lambda x: x.lumi, int),
    event = v(lambda x: x.eventId, int, 'l'),
    n_up = v(lambda x: getattr(x, 'NUP', default), int),
    n_pu = v(lambda x: x.nPU if x.nPU is not None else default),
    n_pv = v(lambda x: len(x.vertices), int),
    rho = v(lambda x: x.rho),
    is_data = v(lambda x: x.input.eventAuxiliary().isRealData(), int),
    )

#todo add top1_gen_pt and top2_gen_pt

generator = Block(
    'generator', lambda x: x,
    gen_boson_pt = v(lambda x: getattr(x, 'genPartonHT', default)),
    gen_boson_mass = v(lambda x : getattr(x, 'geninvmass', default)),
    )

flags = [
    'Flag_goodVertices',
    'Flag_globalTightHalo2016Filter',
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
    event_flags[flag] = v(lambda x: getattr(x,flag), int)

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
    # j1_rawf
    j2_pt = v(lambda x: x[1].pt() if len(x)>1 else default),
    j2_eta = v(lambda x: x[1].eta() if len(x)>1 else default),
    j2_phi = v(lambda x: x[1].phi() if len(x)>1 else default),
    j2_pumva = v(lambda x: x[1].puMva('pileupJetId:fullDiscriminant') if len(x)>1 else default ),
#    j2_puid = v(lambda x: x[1].pileUpJetId_htt() if len(x)>1 else default ),
    j2_flavour_parton = v(lambda x: x[1].partonFlavour() if len(x)>1 else default),
    j2_flavour_hadron = v(lambda x: x[1].hadronFlavour() if len(x)>1 else default),
    j2_rawf = v(lambda x: x[1].rawFactor() if len(x)>1 else default),

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
)


weights = Block(
    'weights', lambda x: x, 
    weight = v(lambda x : x.eventWeight),
    weight_pu = v(lambda x : x.puWeight),
    weight_dy = v(lambda x : getattr(x, 'dy_weight', 1.)),
    #todo weight_top
    weight_njet = v(lambda x : x.NJetWeight),
) 

triggers = Block(
    'triggers', lambda x: getattr(x.dileptons_sorted[0], 'matchedPaths', []),
    trg_doubletau = v(lambda x : any('DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v' in name for name in x)),
    trg_doubletau_lowpt = v(lambda x : any('DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v' in name for name in x)),
    trg_doubletau_lowpt_mediso = v(lambda x : any('DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v' in name for name in x)),
    trg_doubletau_mediso = v(lambda x : any('DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v' in name for name in x)),
    trg_electrontau = v(lambda x : any('Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v' in name for name in x)),
    trg_muonelectron_lowpte = v(lambda x : any('Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x)),
    trg_muonelectron_lowptmu = v(lambda x : any('Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in name for name in x)),
    trg_muontau_lowptmu = v(lambda x : any('IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v' in name for name in x)),
    trg_muontau_lowpttau = v(lambda x : any('IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1_v' in name for name in x)),
    trg_singleelectron = v(lambda x : any('Ele35_WPTight_Gsf_v' in name for name in x)),
    trg_singleelectron_lowpt = v(lambda x : any('Ele32_WPTight_Gsf_v' in name for name in x)),
    trg_singlemuon = v(lambda x : any('IsoMu27_v' in name for name in x)),
    trg_singlemuon_lowpt = v(lambda x : any('IsoMu24_v' in name for name in x)),
    trg_singletau_leading = v(lambda x : any('MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v' in name for name in x)),
    trg_singletau_trailing = v(lambda x : any('MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v' in name for name in x))
)

lepton_vars = dict(
    pt = v(lambda x: x.pt()),
    eta = v(lambda x: x.eta()),
    phi = v(lambda x: x.phi()),
    m = v(lambda x: x.mass()),
    q = v(lambda x: x.charge()),
    weight_idso = v(lambda x: getattr(x, 'weight_idiso', 1.)),
    weight_trig = v(lambda x: getattr(x, 'weight_trigger', 1.)),
    d0 = v(lambda x: x.dxy()),
    dz = v(lambda x: x.dz()),
    gen_match = v(lambda x: x.gen_match, int),
)

dilepton_vars = Block(
    'dileptons', lambda x: x.pfmet,
    met = v(lambda x: x.pt()),
    metphi = v(lambda x: x.phi()),
)

electron_vars = dict(
    id_e_mva_nt_loose = v(lambda x: x.mvaRun2('NonTrigSpring15MiniAOD')), 
    weight_tracking = v(lambda x: getattr(x, 'weight_tracking', 1. )),
    iso = v(lambda x: x.iso_htt()),
)

muon_vars = dict(
    weight_tracking = v(lambda x: getattr(x, 'weight_tracking', 1. )),
    iso = v(lambda x: x.iso_htt()),   
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
)

# necessary, or all lambdas will be the same! 
def make_func(tauid):
    return lambda x : x.tauID(tauid)
for tauid in tau_ids: 
    tau_vars[tauid] = v(make_func(tauid))


common = EventContent(
    [event, generator, weights, event_flags,
     triggers, jets20, jets30, bjets, vetoes,
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
