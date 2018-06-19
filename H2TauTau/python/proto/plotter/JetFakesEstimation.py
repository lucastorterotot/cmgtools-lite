import copy
import os

from CMGTools.H2TauTau.proto.plotter.Variables import dict_all_vars
from CMGTools.H2TauTau.proto.plotter.HistCreator import createHistogram
from CMGTools.H2TauTau.proto.plotter.PlotConfigs import HistogramCfg
from ROOT import gSystem, gROOT

if "/sFakeFactor_cc.so" not in gSystem.GetLibraries(): 
    gROOT.ProcessLine(".L %s/src/CMGTools/H2TauTau/python/proto/plotter/FakeFactor.cc+" % os.environ['CMSSW_BASE']);
    from ROOT import getFFWeight

def jetFakesEstimation(all_samples, cut, int_lumi, total_weight):

    norm_var = dict_all_vars['_norm_']

    to_substract = copy.deepcopy([s for s in all_samples if (not s.is_signal) and (not s.is_data)])
    
    # for sample in to_substract:

    scale = 1.

    for sample in to_substract:
        sample.scale = scale if sample.name == 'data_obs' else -scale

    jet_fakes_expr_tosubstract = '(((l1_byIsolationMVArun2v1DBoldDMwLT>0.5 && l1_byIsolationMVArun2v1DBoldDMwLT<2.5 && l2_byIsolationMVArun2v1DBoldDMwLT>2.5)*(0.5*getFFWeight(l1_pt,l2_pt,l1_decayMode,n_jets,mvis,mt_total))*(l1_gen_match<6)) + ((l2_byIsolationMVArun2v1DBoldDMwLT>0.5 && l2_byIsolationMVArun2v1DBoldDMwLT<2.5 && l1_byIsolationMVArun2v1DBoldDMwLT>2.5)*(0.5*getFFWeight(l2_pt,l1_pt,l2_decayMode,n_jets,mvis,mt_total))*(l2_gen_match<6)))'

    # for sample in all_samples:
    #     if (not sample.is_signal) and (not sample.is_data):
    #         if sample.weight_expr==None:
    #             sample.weight_expr='1'
    #         sample.weight_expr = '('+sample.weight_expr+')'
    
    # not_jet_fakes_cut = '*(l1_gen_match<6 || l2_gen_match<6)'
    # for sample in to_substract:
    #     if (not sample.is_signal) and (not sample.is_data):
    #         if sample.weight_expr==None:
    #             sample.weight_expr='1'
    #         sample.weight_expr = '('+sample.weight_expr+')'+not_jet_fakes_cut
    #         sample.scale = -1.

    # to_substract_expr = '(!(l1_gen_match == 5 && l2_gen_match == 5))*0.5*( l1_gen_match < 6 || l2_gen_match < 6 )'

    JetFakes_samples = copy.deepcopy([s for s in all_samples if s.name == 'data_obs'])#not s.is_signal])

    # for sample in JetFakes_samples:
    #     sample.scale = scale if sample.name == 'data_obs' else -scale
    # import pdb;pdb.set_trace()
    jet_fakes_expr = '(((l1_byIsolationMVArun2v1DBoldDMwLT>0.5 && l1_byIsolationMVArun2v1DBoldDMwLT<2.5 && l2_byIsolationMVArun2v1DBoldDMwLT>2.5)*(0.5*getFFWeight(l1_pt,l2_pt,l1_decayMode,n_jets,mvis,mt_total))) + ((l2_byIsolationMVArun2v1DBoldDMwLT>0.5 && l2_byIsolationMVArun2v1DBoldDMwLT<2.5 && l1_byIsolationMVArun2v1DBoldDMwLT>2.5)*(0.5*getFFWeight(l2_pt,l1_pt,l2_decayMode,n_jets,mvis,mt_total))))'
    # # jet_fakes_expr = '('+str(cut)+')*'+jet_fakes_expr
    # for s in JetFakes_samples:
    #     if sample.weight_expr==None:
    #         sample.weight_expr='1'
    #     sample.weight_expr = '('+sample.weight_expr+')'+jet_fakes_expr

    JetFakes = HistogramCfg(name='jetFakes_direct', var=None, cfgs=JetFakes_samples, cut=str(cut), lumi=int_lumi, weight=jet_fakes_expr)

    to_substract_expr = jet_fakes_expr

    JetFakes_tosubstract = HistogramCfg(name='jetFakes_tosubstract', var=None, cfgs=to_substract, cut=str(cut), lumi=int_lumi, weight=jet_fakes_expr_tosubstract)

    # all_samples = [x for x in all_samples if x.name in ['data_obs']]
    all_samples.append(JetFakes)
    # all_samples = [JetFakes, to_substract_expr]
    return all_samples
