from MC_definitions import *
from ROOT import TCanvas, TFile, TH1F, TTree, TLegend, THStack

localisation = "$CMSSW_BASE/src/CMGTools/TTbarTime/analyze/MonteCarlo"

rootfile = []
for i in range(len(MC_sample)):
    rootfile.append(TFile(localisation+"/files_MC/"+MC_sample[i]+"/tree.root"))

##########################################################################
# Histo build part
##########################################################################

def histo_creation(lumi2017_param, variable_param, binHist_param, minHist_param, maxHist_param, titleX_param, titleY_param):

    histo = []
    legend = TLegend(0.5,0.5,0.9,0.9)
    canvas = TCanvas()
    
    if(lumi2017_param):
        legend.SetHeader("41.53 fb-1","C")
        canvas.SetName(variable_param+"2017")
    else:
        legend.SetHeader("35.9 fb-1","C")
        canvas.SetName(variable_param+"2016")
    
    for i in range(len(MC_sample)):
        foo = TH1F("essaie{}".format(i),"essaie{}".format(i),binHist_param,minHist_param,maxHist_param)
        rootfile[i].Get('events').Project("essaie{}".format(i),variable_param,"weight")
        histo.append(foo)
        histo[i].SetFillColor(color[i])
        histo[i].Scale(luminosity2017*1000*cross_sec[i]/eventsN0[i])
        if(not lumi2017_param):
            histo[i].Scale(lumiRatio)
        print(histo[i].GetEntries()*lumiRatio*luminosity2017*1000*cross_sec[i]/eventsN0[i])
        histo[i].Draw()
        legend.AddEntry(histo[i], MC_name[i], "f")
        
    stack = THStack(variable_param, "")
    for i in range(len(MC_sample)):
        stack.Add(histo[len(MC_sample)-(i+1)])
    stack.Draw("HIST")
    stack.GetXaxis().SetTitle(titleX_param)
    stack.GetYaxis().SetTitle(titleY_param)
    legend.Draw()
    
    if(lumi2017_param):
        canvas.SaveAs(localisation+"/results/MC_"+variable_param+"2017.png")
    else:
        canvas.SaveAs(localisation+"/results/MC_"+variable_param+"2016.png")
        
    canvas.Write()

##########################################################################
# File writing part
##########################################################################

newfile = TFile(localisation+"/results/MC_variables.root", "RECREATE")

#histo_creation(True, "pt_elec", 50, 0 ,250, "pT(e) GeV", "Events")
#histo_creation(True, "pt_muon", 50, 0 ,250, "pT(#mu) GeV", "Events")
#histo_creation(True, "lead_pt", 50, 0 ,250, "pT(lead) GeV", "Events")
#histo_creation(True, "sublead_pt", 50, 0 ,250, "pT(sublead) GeV", "Events")

histo_creation(False, "pt_elec", 50, 0 ,250, "pT(e-) GeV", "Events")
#histo_creation(False, "pt_muon", 50, 0 ,250, "pT(#mu) GeV", "Events")
#histo_creation(False, "lead_pt", 50, 0 ,250, "pT(lead) GeV", "Events")
#histo_creation(False, "sublead_pt", 50, 0 ,250, "pT(sublead) GeV", "Events")

#histo_creation(True, "n_bjets", 6, 0 ,6, "Jets b-tagged", "Events")
#histo_creation(False, "n_bjets", 6, 0 ,6, "Jets b-tagged", "Events")

newfile.Close()




