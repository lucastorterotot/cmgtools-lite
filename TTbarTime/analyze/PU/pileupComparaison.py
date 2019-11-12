from ROOT import TCanvas, TFile, TH1D, TTree, TLegend
from ROOT import kRed, kBlue
from CMGTools.TTbarTime.proto.samples.fall17.ttbar import mc_signal
from CMGTools.TTbarTime.proto.samples.fall17.ttbar import mc_background

file_data = TFile("$CMSSW_BASE/src/CMGTools/H2TauTau/data/pudistributions_data_2017.root")
hist_data = file_data.Get("pileup")

file_sig = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/data/pileupSignal.root")
file_bkgd = TFile("$CMSSW_BASE/src/CMGTools/TTbarTime/data/pileupBackground.root")

hist_sig = []
hist_bkgd = []

c = TCanvas()

hist_data.Scale(1./hist_data.Integral())
hist_data.SetLineWidth(3)
hist_data.SetLineColor(kRed)



for i in range (2):
    hist_sig.append(file_sig.Get(mc_signal[i].dataset.replace('/','#')))
    hist_sig[i].Scale(1./hist_sig[i].Integral())
    hist_sig[i].SetLineWidth(3)
    hist_sig[i].SetLineColor(kBlue)
    hist_data.SetTitle("")
    hist_data.Draw()
    hist_sig[i].Draw("SAME")
    legend = TLegend(0.5,0.5,0.9,0.7)
    legend.AddEntry(hist_data, "data", "l")
    legend.AddEntry(hist_sig[i], "MC "+mc_signal[i].name, "l")
    legend.Draw()
    c.SaveAs("pu_comparaison/"+mc_signal[i].name+".png")
    c.Clear()
    
for i in range(7):
    hist_bkgd.append(file_bkgd.Get(mc_background[i].dataset.replace('/','#')))
    hist_bkgd[i].Scale(1./hist_bkgd[i].Integral())
    hist_bkgd[i].SetLineWidth(3)
    hist_bkgd[i].SetLineColor(kBlue)
    hist_data.SetTitle("")
    hist_data.Draw()
    hist_bkgd[i].Draw("SAME")
    legend = TLegend(0.5,0.5,0.9,0.7)
    legend.AddEntry(hist_data, "data", "l")
    legend.AddEntry(hist_bkgd[i], "MC "+mc_background[i].name, "l")
    legend.Draw()
    c.SaveAs("pu_comparaison/"+mc_background[i].name+".png")
    c.Clear()






