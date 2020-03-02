from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

kreator = ComponentCreator()

### DY

DY1JetsToLL_M50_LO     = kreator.makeMCComponent("DY1JetsToLL_M50_LO",     "/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM",      "CMS", ".*root", 877.8)
DY1JetsToLL_M50_LO_ext = kreator.makeMCComponent("DY1JetsToLL_M50_LO_ext",     "/DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_v3_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM",      "CMS", ".*root", 877.8)
DY2JetsToLL_M50_LO     = kreator.makeMCComponent("DY2JetsToLL_M50_LO",     "/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM",      "CMS", ".*root", 304.4)
DY2JetsToLL_M50_LO_ext = kreator.makeMCComponent("DY2JetsToLL_M50_LO_ext",     "/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM",      "CMS", ".*root", 307)
DY3JetsToLL_M50_LO     = kreator.makeMCComponent("DY3JetsToLL_M50_LO",     "/DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM",      "CMS", ".*root", 111.5)
DY3JetsToLL_M50_LO_ext = kreator.makeMCComponent("DY3JetsToLL_M50_LO_ext",     "/DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM",      "CMS", ".*root", 111.5)
DY4JetsToLL_M50_LO     = kreator.makeMCComponent("DY4JetsToLL_M50_LO",     "/DY4JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_v2_94X_mc2017_realistic_v14-v2/MINIAODSIM",      "CMS", ".*root", 44.03)


DYJetsToLL_M50 = kreator.makeMCComponent("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 6225.42, fracNegWeights=0.16)
DYJetsToLL_M50_ext = kreator.makeMCComponent("DYJetsToLL_M50_ext", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM", "CMS", ".*root", 6225.42, fracNegWeights=0.16)
DYJetsToLL_M10to50_LO =  kreator.makeMCComponent("DYJetsToLL_M10to50_LO", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 21658.0) # /DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v2/MINIAODSIM

DYJets_to_stitch = [DY1JetsToLL_M50_LO,
                    DY2JetsToLL_M50_LO,
                    DY2JetsToLL_M50_LO_ext,
                    DY3JetsToLL_M50_LO,
                    DY4JetsToLL_M50_LO,
                    DYJetsToLL_M50,
                    DYJetsToLL_M50_ext]

dy_xsec = 5765.4


n_ev_dy_incl = 48099551.0 + 48744812.0
n_ev_dy_1jet = 32528702.0 + 34135231.0
n_ev_dy_2jet = 11611398.0 + 9691457.0
n_ev_dy_3jet = 4772102.0
n_ev_dy_4jet = 4327065.0


k_factor = dy_xsec/4954.0
dy_xsec_incl = 4954.0 * k_factor
dy_xsec_1jet = 878 * k_factor
dy_xsec_2jet = 307 * k_factor
dy_xsec_3jet = 112 * k_factor
dy_xsec_4jet = 44.2 * k_factor


dy_weight_dict = {
    0:dy_xsec_incl/n_ev_dy_incl,
    1:dy_xsec_1jet/(n_ev_dy_incl*dy_xsec_1jet/dy_xsec_incl + n_ev_dy_1jet),
    2:dy_xsec_2jet/(n_ev_dy_incl*dy_xsec_2jet/dy_xsec_incl  + n_ev_dy_2jet),
    3:dy_xsec_3jet/(n_ev_dy_incl*dy_xsec_3jet/dy_xsec_incl  + n_ev_dy_3jet),
    4:dy_xsec_4jet/(n_ev_dy_incl*dy_xsec_4jet/dy_xsec_incl  + n_ev_dy_4jet),
}

def getDYWeight(n_jets):
    return dy_weight_dict[n_jets]

for sample in DYJets_to_stitch:
    sample.weight_func = getDYWeight
    sample.xSection = dy_xsec



### single top

T_tch = kreator.makeMCComponent("T_tch", "/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM",           "CMS", ".*root", 136.02) # inclusive sample
TBar_tch = kreator.makeMCComponent("TBar_tch", "/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM", "CMS", ".*root", 80.95) # inclusive sample
TBar_tWch = kreator.makeMCComponent("TBar_tWch", "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM", "CMS", ".*root",35.85)
T_tWch= kreator.makeMCComponent("T_tWch", "/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM", "CMS", ".*root",35.85)

### ttbar

TTLep_pow  = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 88.29 )
TTHad_pow  = kreator.makeMCComponent("TTHad_pow", "/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM", "CMS", ".*root", 377.96 )
TTSemi_pow = kreator.makeMCComponent("TTSemi_pow", "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 365.35 )

### W + jets

WJetsToLNu_LO = kreator.makeMCComponent("WJetsToLNu_LO","/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM", "CMS", ".*root", 61526.7)
WJetsToLNu_LO_ext = kreator.makeMCComponent("WJetsToLNu_LO_ext","/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v2/MINIAODSIM", "CMS", ".*root", 61526.7)
W1JetsToLNu_LO = kreator.makeMCComponent("W1JetsToLNu_LO","/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/MINIAODSIM", "CMS", ".*root", 8104.0)
W2JetsToLNu_LO = kreator.makeMCComponent("W2JetsToLNu_LO","/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v4/MINIAODSIM", "CMS", ".*root", 2793.0)
W3JetsToLNu_LO = kreator.makeMCComponent("W3JetsToLNu_LO","/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 992.5)
W4JetsToLNu_LO = kreator.makeMCComponent("W4JetsToLNu_LO","/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 544.3)

Wjets_to_stitch = [WJetsToLNu_LO,
                   W1JetsToLNu_LO,
                   W2JetsToLNu_LO,
                   W3JetsToLNu_LO,
                   W4JetsToLNu_LO]

w_xsec = 61526.7
# From https://twiki.cern.ch/twiki/pub/CMS/HiggsToTauTauWorking2015/DYNjetWeights.xls r3
w_weight_dict = {
    0:1.304600668/w_xsec,
    1:0.216233816/w_xsec,
    2:0.115900663/w_xsec,
    3:0.058200264/w_xsec,
    4:0.06275589/w_xsec
}

def getWWeight(n_jets):
    return w_weight_dict[n_jets]

for sample in Wjets_to_stitch: 

    sample.weight_func = getWWeight
    # sample.xSection = w_xsec


### inclusive Di-Bosons

WW = kreator.makeMCComponent("WW", "/WW_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 75.88)
WZ = kreator.makeMCComponent("WZ", "/WZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 27.57)
ZZ = kreator.makeMCComponent("ZZ", "/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 12.14)

### Di-Bosons
VVTo2L2Nu = kreator.makeMCComponent("VVTo2L2Nu", "/VVTo2L2Nu_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 13.97)
WWTo2L2Nu = kreator.makeMCComponent("WWTo2L2Nu", "/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 11.08)
WWTo4Q = kreator.makeMCComponent("WWTo4Q", "/WWTo4Q_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 47.73)
WWToLNuQQ = kreator.makeMCComponent("WWToLNuQQ", "/WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 45.99)
WWToLNuQQ_ext = kreator.makeMCComponent("WWToLNuQQ_ext", "/WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM", "CMS", ".*root", 45.99)
WZTo2L2Q = kreator.makeMCComponent("WZTo2L2Q", "/WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 6.331)
WZTo1L3Nu = kreator.makeMCComponent("WZTo1L3Nu", "/WZTo1L3Nu_13TeV_amcatnloFXFX_madspin_pythia8_v2/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 3.293)
WZTo3LNu = kreator.makeMCComponent("WZTo3LNu", "/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 5.052)
WZTo1L1Nu2Q = kreator.makeMCComponent("WZTo1L1Nu2Q", "/WZTo1L1Nu2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM", "CMS", ".*root", 11.66)
ZZTo4L = kreator.makeMCComponent("ZZTo4L", "/ZZTo4L_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 1.325)
ZZTo4L_ext = kreator.makeMCComponent("ZZTo4L_ext", "/ZZTo4L_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM", "CMS", ".*root", 1.325)
ZZTo2L2Nu = kreator.makeMCComponent("ZZTo2L2Nu", "/ZZTo2L2Nu_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 0.6008)
ZZTo2L2Q = kreator.makeMCComponent("ZZTo2L2Q", "/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 3.688)

### Electroweak

WToLNu_M50_Plus2J = kreator.makeMCComponent("WToLNu_M50_Plus2J", "/EWKWMinus2Jets_WToLNu_M-50_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 29.59)
WToLNu_M50_Minus2J = kreator.makeMCComponent("WToLNu_M50_Minus2J", "/EWKWPlus2Jets_WToLNu_M-50_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 23.24)
ZToLL_M50 = kreator.makeMCComponent("ZToLL_M50", "/EWKZ2Jets_ZToLL_M-50_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 4.321)
ZToNuNu = kreator.makeMCComponent("ZToNuNu", "/EWKZ2Jets_ZToNuNu_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM", "CMS", ".*root", 10.66)

backgrounds = [DY1JetsToLL_M50_LO,
               DY1JetsToLL_M50_LO_ext,
               DY2JetsToLL_M50_LO,
               DY2JetsToLL_M50_LO_ext,
               DY3JetsToLL_M50_LO,
               DY3JetsToLL_M50_LO_ext,
               DY4JetsToLL_M50_LO,
               DYJetsToLL_M50,
               DYJetsToLL_M50_ext,
               DYJetsToLL_M10to50_LO,
               T_tch,
               TBar_tch,
               TBar_tWch,
               T_tWch,
               TTLep_pow,
               TTHad_pow,
               TTSemi_pow,
               WJetsToLNu_LO,
               WJetsToLNu_LO_ext,
               W1JetsToLNu_LO,
               W2JetsToLNu_LO,
               W3JetsToLNu_LO,
               W4JetsToLNu_LO,
               WW,
               WZ,
               ZZ,
               WToLNu_M50_Plus2J,
               WToLNu_M50_Minus2J,
               ZToLL_M50,
               ZToNuNu,
               VVTo2L2Nu,
               WWTo2L2Nu,
               WWTo4Q,
               WWToLNuQQ,
               WWToLNuQQ_ext,
               WZTo2L2Q,
               WZTo1L3Nu,
               WZTo3LNu,
               WZTo3LNu,
               WZTo1L1Nu2Q,
               ZZTo4L,
               ZZTo4L_ext,
               ZZTo2L2Nu,
               ZZTo2L2Q
               ]

DY = [DY1JetsToLL_M50_LO,
      DY1JetsToLL_M50_LO_ext,
      DY2JetsToLL_M50_LO,
      DY2JetsToLL_M50_LO_ext,
      DY3JetsToLL_M50_LO,
      DY3JetsToLL_M50_LO_ext,
      DY4JetsToLL_M50_LO,
      DYJetsToLL_M50,
      DYJetsToLL_M50_ext,
      DYJetsToLL_M10to50_LO]

TTbar = [TTLep_pow,
         TTHad_pow,
         TTSemi_pow]

generic_backgrounds = [comp for comp in backgrounds if comp not in DY+TTbar]
