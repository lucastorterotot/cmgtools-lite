from ROOT import TChain

chain = TChain("tree")

files = ['DY1JetsToLL_M50_LO',
         'DY2JetsToLL_M50_LO',
         'DY3JetsToLL_M50_LO',
         'DY4JetsToLL_M50_LO',
         'DYJetsToLL_M10to50_LO',
         'DYJetsToLL_M50_LO_ext',
         'DYJetsToLL_M50_LO_ext2']
for n in files:
    chain.Add('/eos/user/g/gtouquet/Prod/MSSM_Samples_v2/'+n+'/H2TauTauTreeProducerTauTau/tree.root')

