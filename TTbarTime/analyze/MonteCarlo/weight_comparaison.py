from MC_definitions import *
from ROOT import TCanvas, TFile, TH1F, TTree, TLegend, THStack
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("variable", help="choose variable of TTree")
args = parser.parse_args()

##########################################################################
# Variables def
##########################################################################

is2016 = True

variable = args.variable
binHist = 45
minHist = 0
maxHist = 250
titleX = variable
titleY = "Events"

localisation = "$CMSSW_BASE/src/CMGTools/TTbarTime/analyze/MonteCarlo"

rootfile = TFile(localisation+"/files_MC/"+MC_sample[0]+"/tree.root")

##########################################################################
# Histo build part
##########################################################################

legend = TLegend(0.5,0.5,0.9,0.9)
canvas = TCanvas()

legend.SetHeader(MC_name[0]+" 41.53 fb-1","C")
if(is2016):
    legend.SetHeader(MC_name[0]+" 35.9 fb-1","C")
canvas.SetName(variable+"2017")

histoU = TH1F("unweight","",binHist,minHist,maxHist)
rootfile.Get('events').Project("unweight",variable)
histoU.Scale(luminosity2017*1000*cross_sec[0]/eventsN0[0])
if(is2016):
    histoU.Scale(lumiRatio)
histoU.SetLineColor(color[3])
histoU.SetLineWidth(2)
histoU.SetStats(0)
histoU.GetXaxis().SetTitle(titleX)
histoU.GetYaxis().SetTitle(titleY)
legend.AddEntry(histoU, "unweighted", "f")

histoP = TH1F("weightP","",binHist,minHist,maxHist)
rootfile.Get('events').Project("weightP",variable,"weight_pu")
histoP.Scale(luminosity2017*1000*cross_sec[0]/eventsN0[0])
if(is2016):
    histoP.Scale(lumiRatio)
histoP.SetLineColor(color[1])
histoP.SetLineWidth(2)
legend.AddEntry(histoP, "weighted PU", "f")

histoB = TH1F("weightB","",binHist,minHist,maxHist)
rootfile.Get('events').Project("weightB",variable,"weight_sfb")
histoB.Scale(luminosity2017*1000*cross_sec[0]/eventsN0[0])
if(is2016):
    histoB.Scale(lumiRatio)
histoB.SetLineColor(color[2])
histoB.SetLineWidth(2)
legend.AddEntry(histoB, "weighted SF:b", "f")

histoE = TH1F("weightE","",binHist,minHist,maxHist)
rootfile.Get('events').Project("weightE",variable,"weight_sfe")
histoE.Scale(luminosity2017*1000*cross_sec[0]/eventsN0[0])
if(is2016):
    histoE.Scale(lumiRatio)
histoE.SetLineColor(color[4])
histoE.SetLineWidth(2)
legend.AddEntry(histoE, "weighted SF:e", "f")

histoMid = TH1F("weightMid","",binHist,minHist,maxHist)
rootfile.Get('events').Project("weightMid",variable,"weight_sfm_id")
histoMid.Scale(luminosity2017*1000*cross_sec[0]/eventsN0[0])
if(is2016):
    histoMid.Scale(lumiRatio)
histoMid.SetLineColor(color[5])
histoMid.SetLineWidth(2)
legend.AddEntry(histoMid, "weighted SF:m ID", "f")

histoMiso = TH1F("weightMiso","",binHist,minHist,maxHist)
rootfile.Get('events').Project("weightMiso",variable,"weight_sfm_iso")
histoMiso.Scale(luminosity2017*1000*cross_sec[0]/eventsN0[0])
if(is2016):
    histoMiso.Scale(lumiRatio)
histoMiso.SetLineColor(color[6])
histoMiso.SetLineWidth(2)
legend.AddEntry(histoMiso, "weighted SF:m Iso", "f")

histoW = TH1F("weight","",binHist,minHist,maxHist)
rootfile.Get('events').Project("weight",variable,"weight")
histoW.Scale(luminosity2017*1000*cross_sec[0]/eventsN0[0])
if(is2016):
    histoW.Scale(lumiRatio)
histoW.SetLineColor(color[0])
histoW.SetLineWidth(2)
legend.AddEntry(histoW, "weighted", "f")

print(histoW.GetEntries()*lumiRatio*luminosity2017*1000*cross_sec[0]/eventsN0[0])

histoU.Draw()
histoP.Draw("SAME")
histoB.Draw("SAME")
histoE.Draw("SAME")
histoMid.Draw("SAME")
histoMiso.Draw("SAME")
histoW.Draw("SAME")
legend.Draw()

canvas.SaveAs(localisation+"/results/weighted_comparaison_"+variable+".png")
        
