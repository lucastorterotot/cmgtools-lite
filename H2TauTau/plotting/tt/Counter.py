from ROOT import TFile
import pickle

samples = ['VVTo2L2Nu',
           'VVTo2L2Nu_ext',
           'WWTo1L1Nu2Q',
           'WZTo2L2Q',
           'WZTo1L3Nu',
           'WZTo1L1Nu2Q',
           'WZJToLLLNu',
           'ZZTo4L',
           'ZZTo2L2Q']

# samples = ['T_tWch_ext']

# N_events = 0.

# for s in samples:
#     f = TFile('/eos/user/g/gtouquet/Prod/MSSM_Samples_v2/'+s+'/H2TauTauTreeProducerTauTau/tree.root')
#     t = f.Get('tree')
#     print s
#     for e in t:
#         N_events += e.weight

# print 'sumweight_events', N_events

N_events_pickle = 0.

for s in samples:
    pckobj = pickle.load(open('/eos/user/g/gtouquet/Prod/MSSM_Samples_v2/'+s+'/SkimAnalyzerCount/SkimReport.pck','r'))
    counters = dict(pckobj)
    print s, counters['Sum Weights']
    N_events_pickle += counters['Sum Weights']

print 'Nweight_events_pickle', N_events_pickle
