### Hadronic taus energy scale factors

# Tables -----------------------------
# in the form IDweights[gen_match] gives
# a dict which keys are WP that gives then
# the form (etamax, value)

TauEnergyScales = {
    'JetToTau' : {
        '1prong0pi0' : 1.00 ,
        '1prong1pi0' : 1.00 ,
        '3prong0pi0' : 1.00 ,
        '3prong1pi0' : 1.00 ,
        },
    'HadronicTau' : {
        '1prong0pi0' : 1. + 0.7 / 100 ,
        '1prong1pi0' : 1. - 0.2 / 100 ,
        '3prong0pi0' : 1. + 0.1 / 100 ,
        '3prong1pi0' : 1. - 0.1 / 100 ,
        },
    'TauDecayedToMuon' : {
        '1prong0pi0' : 1.00 ,
        '1prong1pi0' : 1.00 ,
        '3prong0pi0' : 1.00 ,
        '3prong1pi0' : 1.00 ,
        },
    'TauDecayedToEle' : {
        '1prong0pi0' : 1. + 0.3 / 100 ,
        '1prong1pi0' : 1. + 3.6 / 100 ,
        '3prong0pi0' : 1.00 ,
        '3prong1pi0' : 1.00 ,
        },
    'promptMuon' : {
        '1prong0pi0' : 1.00 ,
        '1prong1pi0' : 1.00 ,
        '3prong0pi0' : 1.00 ,
        '3prong1pi0' : 1.00 ,
        },
    'promptEle' : {
        '1prong0pi0' : 1. + 0.3 / 100 ,
        '1prong1pi0' : 1. + 3.6 / 100 ,
        '3prong0pi0' : 1.00 ,
        '3prong1pi0' : 1.00 ,
        }}
