from ROOT import TFile, TH2F, TLegend, TCanvas

f = TFile.Open('/afs/cern.ch/work/g/gtouquet/sync_Outdir/TriggerGGheff_multioffline/HiggsGGH125/H2TauTauTreeProducerTauTauTrigger/tree.root')

tree = f.Get('tree')

effdict = {}
for pt1 in [30,32,34,36,38,40,42,44,46,48,50]:
    for pt2 in [25,27,29,31,33,35,37,39,41,43,45]:
        if pt2<pt1:
            onsel = "offline_{pt2}_{pt1}==1 && Opentrigged == 1 && trigger_{pt2}_{pt1}==1"
            onsel = onsel.format(pt1=pt1,pt2=pt2)
            offsel = "offline_{pt2}_{pt1}==1".format(pt1=pt1,pt2=pt2)
            effdict['{}_{}_off'.format(pt1,pt2)]=tree.GetEntries(offsel)
            effdict['{}_{}_on'.format(pt1,pt2)]=tree.GetEntries(onsel)
        else:
            effdict['{}_{}_off'.format(pt1,pt2)]=0
            effdict['{}_{}_on'.format(pt1,pt2)]=0


th2 = TH2F("efficiencies","HLT Efficiencies",11,29.,51.,11,24.,46.)
th2.GetXaxis().SetTitle("leg_{1} P_{t} (GeV)")
th2.GetYaxis().SetTitle("leg_{2} P_{t} (GeV)")
th2.SetStats(0)

binx = 1
for pt1 in [30,32,34,36,38,40,42,44,46,48,50]:
    biny = 1
    for pt2 in [25,27,29,31,33,35,37,39,41,43,45]:
        if effdict['{}_{}_off'.format(pt1,pt2)] !=0:
            th2.SetBinContent(binx,biny,(float(effdict['{}_{}_on'.format(pt1,pt2)])/float(effdict['{}_{}_off'.format(pt1,pt2)])))
        else:
            th2.SetBinContent(binx,biny,-1)
        biny += 1
    binx += 1

# th2.SetMarkerSize(1.8)
th2.SetMarkerColor(2)
th2.SetMarkerStyle(21)
th2.SetBarOffset(0.2)

canva = TCanvas()
th2.SetTitle("Asymetric pt double Tau HLT Efficiencies and Rates")
th2.Draw("TEXT")

legend = TLegend(0.1,0.8,0.3,0.9)
legend.AddEntry(th2,"Efficiencies","P")
legend.Draw()

canva.SaveAs("Plot_eff_rate_HLT.pdf")
