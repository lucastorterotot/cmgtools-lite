import copy
import os

from CMGTools.H2TauTau.proto.plotter.Variables import dict_all_vars
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from ROOT import gSystem, gROOT

if "/sFakeFactor_cc.so" not in gSystem.GetLibraries(): 
    gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/FakeFactor.cc+" % os.environ['CMSSW_BASE']);
    from ROOT import getFFWeight

def jetFakesEstimation(all_samples):

    not_jet_fakes_cut = '*(!(l1_gen_match==6 || l2_gen_match==6))'
    for sample in all_samples:
        if (not sample.is_signal) and (not sample.is_data):
            if sample.weight_expr==None:
                sample.weight_expr='1'
            sample.weight_expr = '('+sample.weight_expr+')'+not_jet_fakes_cut

    JetFakes = copy.deepcopy([s for s in all_samples if s.name == 'data_obs'])

    jet_fakes_expr = '*(((l1_byIsolationMVArun2v1DBoldDMwLT>0.5 && l1_byIsolationMVArun2v1DBoldDMwLT<2.5)*(0.5*getFFWeight(l1_pt,l2_pt,l1_decayMode,n_jets,mvis,mt_total))) || ((l2_byIsolationMVArun2v1DBoldDMwLT>0.5 && l2_byIsolationMVArun2v1DBoldDMwLT<2.5)*(0.5*getFFWeight(l2_pt,l1_pt,l2_decayMode,n_jets,mvis,mt_total))))'
    i = 0
    for s in JetFakes:
        s.is_data = False
        i += 1
        s.name = 'JetFakes'+str(i)
        if sample.weight_expr==None:
            sample.weight_expr='1'
        s.weight_expr = '('+sample.weight_expr+')'+jet_fakes_expr

    all_samples.extend(JetFakes)
    return all_samples
