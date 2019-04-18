### Hadronic taus IDs weight (including electron to tau fake weight and muon to tau fake weight)

# Tables -----------------------------
# in the form tauid_weights[gen_match] gives
# a dict which keys are WP that gives then
# the form (etamax, value)

tauid_weights = {
    'EToTau' : {
        'VLoose' : [ (99, 1.19),
                     (1.5, 1.09) ],
        'Loose' : [ (99, 1.25),
                    (1.5, 1.17) ],
        'Medium' : [ (99, 1.21),
                     (1.5, 1.40) ],
        'Tight' : [ (99, 1.53),
                    (1.5, 1.80) ],
        'VTight' : [ (99, 1.66),
                     (1.5, 1.96) ],
        },
    'MuToTau' : {
        'Loose' : [ (99, 1.),
                    (2.3, 1.94),
                    (1.7, 1.03),
                    (1.2, 1.10),
                    (0.8, 1.02),
                    (0.4, 1.06) ],
        'Tight' : [ (99, 1.),
                    (2.3, 1.61),
                    (1.7, 0.93),
                    (1.2, 1.14),
                    (0.8, 1.29),
                    (0.4, 1.17) ],
        },
    'TauID' : {
        'VLoose' : [ (99, 0.88) ],
        'Loose' : [ (99, 0.89) ],
        'Medium' : [ (99, 0.89) ],
        'Tight' : [ (99, 0.89) ],
        'VTight' : [ (99, 0.86) ],
        'VVTight' : [ (99, 0.84) ],
        }}
