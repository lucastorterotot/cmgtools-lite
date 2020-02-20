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
    unix_time = v(lambda x: x.unixTime)
    )
   
jets30 = Block(
    'jets30', lambda x: x.jets_30,
    n_jets_pt30 = v(lambda x: len(x), int),
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

metvars = Block(
    'metvars', lambda x: x.pfmet,
    met = v(lambda x: x.pt()),
    metphi = v(lambda x: x.phi()),
)

weights = Block(
    'weights', lambda x: x, 
    weight = v(lambda x : x.eventWeight),
    weight_pu = v(lambda x : getattr(x, 'puWeight', 1.)),
    weight_sfb = v(lambda x : getattr(x, 'sfbWeight', 1.)),
    weight_sfe_id = v(lambda x : getattr(x, 'sfeIdWeight', 1.)),
    weight_sfe_reco = v(lambda x : getattr(x, 'sfeRecoWeight', 1.)),
    weight_sfm_id = v(lambda x : getattr(x, 'sfmIdWeight', 1.)),
    weight_sfm_iso = v(lambda x : getattr(x, 'sfmIsoWeight', 1.)),
    weight_sfm_trig_isomu27 = v(lambda x : getattr(x, 'sfmTrigIsoMu27Weight', 1.)),
    weight_sfm_trig_mu50 = v(lambda x : getattr(x, 'sfmTrigMu50Weight', 1.)),
#    weight_sf_ee_trig = v(lambda x : getattr(x, 'sfEETrigWeight', 1.)),
    weight_sf_em_trig = v(lambda x : getattr(x, 'sfEMTrigWeight', 1.)),
#    weight_sf_mm_trig = v(lambda x : getattr(x, 'sfMMTrigWeight', 1.)),
) 

triggers_fired = Block(
    'triggers_fired', lambda x: getattr(x, 'trigger_infos', []),
    # electron
    trg_electron_ele32doubleEG_fired       = v(lambda x : any('Ele32_WPTight_Gsf_L1DoubleEG_v' in trg.name for trg in x if trg.fired)),
    trg_electron_ele32_fired               = v(lambda x : any('Ele32_WPTight_Gsf_v' in trg.name for trg in x if trg.fired)),
    trg_electron_ele35_fired               = v(lambda x : any('Ele35_WPTight_Gsf_v' in trg.name for trg in x if trg.fired)),
    trg_electron_ele38_fired               = v(lambda x : any('Ele38_WPTight_Gsf_v' in trg.name for trg in x if trg.fired)), 
    trg_electron_ele40_fired               = v(lambda x : any('Ele40_WPTight_Gsf_v' in trg.name for trg in x if trg.fired)),
    # double electron
    trg_double_electron_ele23ele12DZ_fired = v(lambda x : any('Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v' in trg.name for trg in x if trg.fired)), 
    trg_double_electron_ele23ele12_fired   = v(lambda x : any('Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v' in trg.name for trg in x if trg.fired)),    
    # muon 
    trg_muon_mu24_fired                    = v(lambda x : any('IsoMu24_v' in trg.name for trg in x if trg.fired)),
    trg_muon_mu24tk_fired                  = v(lambda x : any('IsoTkMu24_v' in trg.name for trg in x if trg.fired)),
    trg_muon_mu24eta21_fired               = v(lambda x : any('IsoMu24_eta2p1_v' in trg.name for trg in x if trg.fired)), 
    trg_muon_mu27_fired                    = v(lambda x : any('IsoMu27_v' in trg.name for trg in x if trg.fired)),    
    # double muon
    trg_double_muon_mu17_fired             = v(lambda x : any('Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v' in trg.name for trg in x if trg.fired)),
    trg_double_muon_mu17m3_fired           = v(lambda x : any('Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v' in trg.name for trg in x if trg.fired)),
    trg_double_muon_mu17m8_fired           = v(lambda x : any('Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v' in trg.name for trg in x if trg.fired)), 
    # electron - muon
    trg_muon_electron_mu8ele23_fired       = v(lambda x : any('Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v' in trg.name for trg in x if trg.fired)),
    trg_muon_electron_mu12ele23_fired      = v(lambda x : any('Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v' in trg.name for trg in x if trg.fired)),
    trg_muon_electron_mu23ele12_fired      = v(lambda x : any('Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v' in trg.name for trg in x if trg.fired)),
    trg_muon_electron_mu8ele23DZ_fired     = v(lambda x : any('Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in trg.name for trg in x if trg.fired)),
    trg_muon_electron_mu12ele23DZ_fired    = v(lambda x : any('Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v' in trg.name for trg in x if trg.fired)),
    trg_muon_electron_mu23ele12DZ_fired    = v(lambda x : any('Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v' in trg.name for trg in x if trg.fired))
)

bjets = Block(
    'bjets', lambda x: x.bjets_30,
    n_bjets = v(lambda x: len(x), int),
)
for vname, variable in jets30.iteritems():
    if not vname.startswith('j'):
        continue
    newname = vname.replace('j1','b1',1)
    newname = newname.replace('j2','b2',1)
    bjets[newname] = variable

electron = Block(
    'electron', lambda x: x.select_electron[0],
    pt_elec    = v(lambda x: x.pt()),
    eta_elec   = v(lambda x: x.eta()),
    phi_elec   = v(lambda x: x.phi()),
    m_elec     = v(lambda x: x.mass()),
    q_elec     = v(lambda x: x.charge()),
    iso_elec   = v(lambda x: x.iso_htt()),
)

muon = Block(
    'muon', lambda x: x.select_muon[0],
    pt_muon    = v(lambda x: x.pt()),
    eta_muon   = v(lambda x: x.eta()),
    phi_muon   = v(lambda x: x.phi()),
    m_muon     = v(lambda x: x.mass()),
    q_muon     = v(lambda x: x.charge()),
    iso_muon   = v(lambda x: x.iso_htt()),
)

dilepton = Block(
    'dilepton', lambda x: x.dileptons_sorted[0],
    m_dilep = v(lambda x: x.mass()),
    pt_lead = v(lambda x: x.pt_lead()),
    pt_sublead = v(lambda x: x.pt_sublead()),
    eta_l1 = v(lambda x: x._l1.eta()),
    eta_l2 = v(lambda x: x._l2.eta())
)


common = EventContent(
    [event, weights, jets30, bjets, electron, muon, dilepton, metvars, triggers_fired]
)

################################################################################
#Weight Generator
################################################################################

nPU = Block(
    'pu', lambda x: x,
    pu = v(lambda x: x.nPU)
)

pileup = EventContent(
    [nPU]
)

