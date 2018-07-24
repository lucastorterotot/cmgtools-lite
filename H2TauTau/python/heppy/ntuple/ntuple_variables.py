from tools import * 

default = Variable.default

event = Block(
    'event', lambda x: x,
    run = v(lambda x: x.run, int),
    lumi = v(lambda x: x.lumi, int),
    event = v(lambda x: x.eventId, int, 'l'),
    n_up = v(lambda x: getattr(x, 'NUP', default), int),
    n_pu = v(lambda x: x.nPU if x.nPU is not None else default, int),
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
    veto_dilepton = v(lambda x: not x.veto_dilepton_passed, int),
    veto_extra_elec = v(lambda x: not x.veto_third_lepton_electrons_passed, int),
    veto_extra_muon = v(lambda x: not x.veto_third_lepton_muons_passed, int),
)

# TODO add trigger flags
trigger = Block(
    'trigger', lambda x: x,
)

jets = Block(
    'jets', lambda x: x.jets_30,
    n_jets = v(lambda x: len(x), int),
)

jets20 = Block(
    'jets20', lambda x: x.jets_20,
    n_jets_pt20 = v(lambda x: len(x), int),
)

bjets = Block(
    'bjets', lambda x: x.bjets,
    n_bjets = v(lambda x: len(x), int),
)

weights = Block(
    'weights', lambda x: x, 
    weight = v(lambda x : x.eventWeight),
    weight_pu = v(lambda x : x.puWeight),
    weight_dy = v(lambda x : getattr(x, 'dy_weight', 1.)),
    #todo weight_top
    weight_njet = v(lambda x : x.NJetWeight),
) 


lepton_vars = dict(
    pt = v(lambda x: x.pt()),
    eta = v(lambda x: x.eta()),
    m = v(lambda x: x.mass()),
    q = v(lambda x: x.charge()),
    weight_idso = v(lambda x: getattr(x, 'weight_idiso', 1.)),
    weight_trig = v(lambda x: getattr(x, 'weight_trigger', 1.)),
    d0 = v(lambda x: x.dxy()),
    dz = v(lambda x: x.dz()),
    # todo : gen_match = v(lambda x: x.gen_match, int),
)

electron_vars = dict(
    id_e_mva_nt_loose = v(lambda x: x.mvaRun2('NonTrigSpring15MiniAOD')), 
    weight_tracking = v(lambda x: getattr(x, 'weight_tracking', 1. )),
    iso = v(lambda x: lep.iso_htt()),
)

muon_vars = dict(
    weight_tracking = v(lambda x: getattr(x, 'weight_tracking', 1. )),
    iso = v(lambda x: x.iso_htt()),   
)

tau_ids = [
    'decayModeFinding',
    # todo : put in Gael's wp system
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
     trigger, jets, jets20, 
     # bjets, 
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

