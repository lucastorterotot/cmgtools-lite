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

weights = Block(
    'weights', lambda x: x, 
    weight = v(lambda x : x.eventWeight),
    weight_pu = v(lambda x : getattr(x, 'puWeight', 1.)),
    weight_sfb = v(lambda x : getattr(x, 'sfbWeight', 1.)),
    weight_sfe = v(lambda x : getattr(x, 'sfeWeight', 1.)),
    weight_sfm_id = v(lambda x : getattr(x, 'sfmIdWeight', 1.)),
    weight_sfm_iso = v(lambda x : getattr(x, 'sfmIsoWeight', 1.)),
    weight_sfm_trig_isomu27 = v(lambda x : getattr(x, 'sfmTrigIsoMu27Weight', 1.)),
    weight_sfm_trig_mu50 = v(lambda x : getattr(x, 'sfmTrigMu50Weight', 1.)),
) 

triggers = Block(



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
    pt_elec = v(lambda x: x.pt()),
    m_elec = v(lambda x: x.mass()),
    q_elec =  v(lambda x: x.charge()),
    iso_elec = v(lambda x: x.iso_htt()),
    eta_elec = v(lambda x: x.eta()),
)

muon = Block(
    'muon', lambda x: x.select_muon[0],
    pt_muon = v(lambda x: x.pt()),
    m_muon = v(lambda x: x.mass()),
    q_muon =  v(lambda x: x.charge()),
    iso_muon = v(lambda x: x.iso_htt()),
    eta_muon = v(lambda x: x.eta()),
)

dilepton = Block(
    'dilepton', lambda x: x.dileptons_sorted[0],
    m_dilep = v(lambda x: x.mass()),
    pt_lead = v(lambda x: x.pt_lead()),
    pt_sublead = v(lambda x: x.pt_sublead()),
    l1_eta = v(lambda x: x._l1.eta()),
    l2_eta = v(lambda x: x._l2.eta())
)


common = EventContent(
    [event, weights, jets30, bjets, electron,muon,dilepton]
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

