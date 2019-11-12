from ROOT import kRed, kBlue, kGreen, kMagenta, kCyan, kOrange

luminosity2017 = 41.53
lumiRatio = 35.9/luminosity2017

cross_sec = [ #pb
    88.2,           #dilep
    365.3,         #semilep
    0.2043,       #TTW
    0.2529,       #TTZ
    3.36,           #STs
    136.02,       #STt
    80.95,         #STt~
    35.9,           #tW
    35.9            #tw~
]

eventsN0 = [
    69155808,                #dilep
    110014744*0.747,   #semilep
    4994543,                  #TTW
    7932650,                  #TTZ
    9914948,                  #STs
    5982064,                  #STt
    3675910*0.971,         #STt~
    7945242,                  #tW
    7745276                   #tw~
]

MC_sample = []
MC_sample.append("signal_MC_dilep")
MC_sample.append("signal_MC_semilep")
MC_sample.append("background_MC_TTW")
MC_sample.append("background_MC_TTZ")
MC_sample.append("background_MC_ST_s")
MC_sample.append("background_MC_ST_t_top")
MC_sample.append("background_MC_ST_t_antitop")
MC_sample.append("background_MC_tW_top")
MC_sample.append("background_MC_tW_antitop")

MC_name = []
MC_name.append("signal TT dilep")
MC_name.append("signal TT semilep")
MC_name.append("background TTW")
MC_name.append("background TTZ")
MC_name.append("background ST_s")
MC_name.append("background ST_t")
MC_name.append("background ST_t~")
MC_name.append("background ST_tW")
MC_name.append("background ST_tW~")

color = []
color.append(kRed)
color.append(kMagenta)
color.append(kGreen)
color.append(kBlue)
color.append(kMagenta+3)
color.append(kCyan)
color.append(kCyan+4)
color.append(kOrange)
color.append(kBlue+3)
