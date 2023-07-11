import ROOT
import numpy as np
import matplotlib.pyplot as plt


ROOT.EnableImplicitMT()


integrated_luminosity = 59830

weights = {
    "QCD1": 27990000 * integrated_luminosity,
    "QCD2": 1712000 * integrated_luminosity,
    "QCD3": 347700 * integrated_luminosity,
    "QCD4": 32100 * integrated_luminosity,
    "QCD5": 6831 * integrated_luminosity,
    "QCD6": 1207 * integrated_luminosity,
    "QCD7": 119.9 * integrated_luminosity,
    "QCD8": 25.24 * integrated_luminosity,
    "WJets1": 315.2 * integrated_luminosity,
    "WJets2": 68.58 * integrated_luminosity,
    "WJets3": 34.69 * integrated_luminosity,
    "ZJets1": 145.3 * integrated_luminosity,
    "ZJets2": 34.29 * integrated_luminosity,
    "ZJets3": 18.57 * integrated_luminosity,
    "TTHad": 370.04 * integrated_luminosity,
    "TTSemilept": 369.49 * integrated_luminosity,
    "ST_tw_antitop": 35.85 * integrated_luminosity,
    "ST_tw_top": 35.85 * integrated_luminosity,
    "GGH": 9.60 * integrated_luminosity,
    "VBFH": 2.20 * integrated_luminosity,
    "ttH": 0.295 * integrated_luminosity,
    "WMinusH": 0.210 * integrated_luminosity,
    "WPlusH": 0.331 * integrated_luminosity,
    "ZH": 0.310 * integrated_luminosity,
    "ggZH": 0.050 * integrated_luminosity,
    "WW": 118.7 * integrated_luminosity,
    "WZ": 47.2 * integrated_luminosity,
    "ZZ": 16.52 * integrated_luminosity,
    "signal": 0.01053 * integrated_luminosity,
}

h2= {}
h2= {}
h_tot = {}
hist_sum = {}

histo_file = ROOT.TFile.Open("histograms_from_analysis_with_0_996_0_98_mass_met_and_softdrop_cut.root", "READ")


h2["WJets1"] = histo_file.Get("h2_WJets1")
h2["WJets2"] = histo_file.Get("h2_WJets2")
h2["WJets3"] = histo_file.Get("h2_WJets3")


h2["ZJets1"] = histo_file.Get("h2_ZJets1")
h2["ZJets2"] = histo_file.Get("h2_ZJets2")
h2["ZJets3"] = histo_file.Get("h2_ZJets3")


h2["TTHad"] = histo_file.Get("h2_TTHad")

h2["TTSemilept"] = histo_file.Get("h2_TTSemilept")


h2["ST_tw_antitop"] = histo_file.Get("h2_ST_tw_antitop")



h2["ST_tw_top"] = histo_file.Get("h2_ST_tw_top")



h2["GGH"] = histo_file.Get("h2_GGH")


h2["VBFH"] = histo_file.Get("h2_VBFH")

h2["ttH"] = histo_file.Get("h2_ttH")


h2["WMinusH"] = histo_file.Get("h2_WMinusH")


h2["WPlusH"] = histo_file.Get("h2_WPlusH")


h2["ZH"] = histo_file.Get("h2_ZH")


h2["ggZH"] = histo_file.Get("h2_ggZH")


h2["WW"] = histo_file.Get("h2_WW")

h2["WZ"] = histo_file.Get("h2_WZ")


h2["ZZ"] = histo_file.Get("h2_ZZ")

h2["signal"] = histo_file.Get("h2_signal")

QCD_file = ROOT.TFile.Open("histograms_from_analysis_QCD_0_86_MET_and_mass_cut.root", "READ")



h2["QCD1"] = QCD_file.Get("h2_QCD1")

num = h2["QCD1"].GetEntries()

h2["QCD2"] = QCD_file.Get("h2_QCD2")

num = num + h2["QCD2"].GetEntries()


h2["QCD3"] = QCD_file.Get("h2_QCD3")

num = num + h2["QCD3"].GetEntries()

h2["QCD4"] = QCD_file.Get("h2_QCD4")

num = num + h2["QCD4"].GetEntries()


h2["QCD5"] = QCD_file.Get("h2_QCD5")

num = num + h2["QCD5"].GetEntries()

h2["QCD6"] = QCD_file.Get("h2_QCD6")

num = num + h2["QCD6"].GetEntries()

h2["QCD7"] = QCD_file.Get("h2_QCD7")

num = num + h2["QCD7"].GetEntries()


h2["QCD8"] = QCD_file.Get("h2_QCD8")

num = num + h2["QCD8"].GetEntries()

print(num)


processes = list(h2.keys())


for i in processes:
    #* the value to normalize at the same integrated luminosity of the AN is 2.27
    #print(type(h2[i]))
    h2[i].Scale(weights[i]*2.27)

    #h2[i].Rebin(2)


    h2[i].GetXaxis().SetRangeUser(40, 220)
    #h2[i].GetXaxis().SetRangeUser(80., 150.)
    # h_tot[i].GetXaxis().SetRangeUser(40., 500.)
    #hist_sum[i].GetXaxis().SetRange(0, 500)

    # if str(i)== "QCD1" or str(i)== "QCD2" or str(i)== "QCD3" or str(i)== "QCD4" or str(i)== "QCD5" or str(i)== "QCD6" or str(i)== "QCD7" or str(i)== "QCD8":
    #     h2[i].Scale(30)
    #     h2[i].Scale(30)
    #     h_tot[i].Scale(30)
    #     #hist_sum[i].Scale(30)
    print("scaled: {}".format(str(i)))

hist_QCD = None
hist_VJets = None
hist_TTBar = None
hist_ST = None
hist_singleH = None


hist_QCD = h2["QCD1"].Clone()
hist_QCD.Add(h2["QCD2"])
hist_QCD.Add(h2["QCD3"])
hist_QCD.Add(h2["QCD4"])
hist_QCD.Add(h2["QCD5"])
hist_QCD.Add(h2["QCD6"])
hist_QCD.Add(h2["QCD7"])
hist_QCD.Add(h2["QCD8"])

hist_QCD.Scale(6.41295783938e-05)

hist_QCD.ResetStats()
print(hist_QCD.GetEntries())




hist_VJets = h2["WJets1"].Clone()
hist_VJets.Add(h2["WJets2"])
hist_VJets.Add(h2["WJets3"])
hist_VJets.Add(h2["ZJets1"])
hist_VJets.Add(h2["ZJets2"])
hist_VJets.Add(h2["ZJets3"])


hist_TTBar_Had = h2["TTHad"].Clone()
hist_TTBar_Semilep = h2["TTSemilept"].Clone()

hist_ST = h2["ST_tw_antitop"].Clone()
hist_ST.Add(h2["ST_tw_top"])

hist_GGH = h2["GGH"].Clone()

hist_VBFH = h2["VBFH"].Clone()

hist_VH = h2["WMinusH"].Clone()
hist_VH.Add(h2["WPlusH"])
hist_VH.Add(h2["ZH"])
hist_VH.Add(h2["ggZH"])

hist_ttH= h2["ttH"].Clone()

hist_VV = h2["WZ"].Clone()
hist_VV.Add(h2["ZZ"])
hist_VV.Add(h2["WW"])

hist1 = hist_ttH.Clone()
hist2 = hist_TTBar_Had.Clone()
hist2.Add(hist_TTBar_Semilep)

hist3 = hist_VH.Clone()

hist4 = hist_QCD.Clone()
hist4.Add(hist_GGH)
hist4.Add(hist_VBFH)

hist5 = hist_VJets.Clone()
hist5.Add(hist_VV)

hist6 = hist_ST.Clone()



#TODO cat1

c1 = ROOT.TCanvas("c1", "Stacked Histograms after preselection", 800, 700)

# TODO Jet1 Histograms are stacked by type of background, but they are not printed on the same plot


legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


# temp1=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH).Add(hist_VV).Add(hist_QCD)
# temp2=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH).Add(hist_VV)
# temp3=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH)
# temp4=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST)
# temp5=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar)
# temp6=h2["signal"].Clone().Add(hist_VJets)
# temp7=h2["signal"].Clone()


c2 = ROOT.TCanvas("c2", "Jet1 contributions after preselection", 800, 700)

# TODO Different contributions for the various type of background Jet1


c2.Divide(3, 3)

c2.cd(1)
h2["signal"].Draw("HIST")

c2.cd(2)
hist1.Draw("HIST")
hist1.SetTitle("TTH")

c2.cd(3)

hist2.Draw("HIST")
hist2.SetTitle("ttbar + jets")


c2.cd(4)

hist3.Draw("HIST")
hist3.SetTitle("VH")


c2.cd(5)

hist4.Draw("HIST")
hist4.SetTitle("QCD + ggH + VBFH")


c2.cd(6)

hist5.Draw("HIST")
hist5.SetTitle("V+jets + VV + ggZH")



c2.cd(7)

hist6.Draw("HIST")
hist6.SetTitle("ST")



c3 = ROOT.TCanvas("c3", "Stacked contributions for jet1 after preselection", 800, 700)


hist_tot1 = hist1.Clone()
hist_tot1.Add(hist2)
hist_tot1.Add(hist3)
hist_tot1.Add(hist4)
hist_tot1.Add(hist5)
hist_tot1.Add(hist6)

hist_tot2 = hist1.Clone()
hist_tot2.Add(hist2)
hist_tot2.Add(hist3)
hist_tot2.Add(hist4)
hist_tot2.Add(hist5)

hist_tot3 = hist1.Clone()
hist_tot3.Add(hist2)
hist_tot3.Add(hist3)
hist_tot3.Add(hist4)

hist_tot4 = hist1.Clone()
hist_tot4.Add(hist2)
hist_tot4.Add(hist3)

hist_tot5 = hist1.Clone()
hist_tot5.Add(hist2)

hist_tot6 = hist1.Clone()



hist_sig = h2["signal"].Clone()

# TODO Stacked histograms for Jet1


hist_tot1.Draw("HIST")
hist_tot1.SetTitle("Distribution of the softdrop mass for jet2")
# hist_tot1.SetLineColor(ROOT.kBlue+1)
hist_tot1.SetFillColorAlpha(ROOT.kAzure + 6, 0.8)
legend.AddEntry(hist_tot1, "ST ", "f")


hist_tot1.ResetStats()
jet1 = hist_tot1.GetEntries()
print("jet1 entries count", jet1)


hist_tot2.Draw("SAME HIST")
# hist_tot2.SetLineColor(ROOT.kRed+4)
hist_tot2.SetFillColorAlpha(ROOT.kAzure -5, 0.45)
legend.AddEntry(hist_tot2, "V jets + VV ", "f")


hist_tot3.Draw("SAME HIST")
# hist_tot3.SetLineColor(ROOT.kGreen+4)
hist_tot3.SetFillColorAlpha(ROOT.kGreen - 8, 0.9)
legend.AddEntry(hist_tot3, "QCD + ggH + VBFH + ggZH", "f")


hist_tot4.Draw("SAME HIST")
# hist_tot4.SetLineColor(ROOT.kBlue+2)
hist_tot4.SetFillColorAlpha(ROOT.kBlue - 8, 0.8)
legend.AddEntry(hist_tot4, "VH", "f")



hist_tot5.Draw("SAME HIST")
# hist_tot5.SetLineColor(ROOT.kRed+1)
hist_tot5.SetFillColorAlpha(ROOT.kTeal - 5, 0.7)
legend.AddEntry(hist_tot5, "t tbar + jets", "f")


hist_tot6.Draw("SAME HIST")
# hist_tot6.SetLineColor(ROOT.kGreen+2)
hist_tot6.SetFillColorAlpha(ROOT.kGreen - 8, 0.8)
legend.AddEntry(hist_tot6, "TTH", "f")

h2["signal"].Draw("SAME HIST")
h2["signal"].Scale(3.8)
h2["signal"].SetLineColor(ROOT.kBlack)
h2["signal"].SetLineWidth(2)

legend.AddEntry(h2["signal"], "signal x 3.8", "l")


legend.Draw()

c4 = ROOT.TCanvas("c4", "Signal to background ratio", 800, 700)

hist_tot1.ResetStats()

n = hist_tot1.GetNbinsX()
x = np.linspace(hist_tot1.GetXaxis().GetBinCenter(1),hist_tot1.GetXaxis().GetBinCenter(n),n,dtype=np.float64)

y= np.array([],dtype=np.float64)

for i in range(n):
    bckg = hist_tot1.GetBinContent(i)

    sig = hist_sig.GetBinContent(i)

    ratio = float(sig/(bckg+1e-10))

    y=np.append(y, ratio)


plt.plot(x, y, marker = 'o')
plt.xlabel("softdrop mass [GeV]")
plt.ylabel("S/B ratio")
plt.grid()


plt.savefig("ratio_plot.png")






c2.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/new_QCD_MET_and_cut_softdrop_jet2_contributions.pdf"
)
c3.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/new_QCD_MET_and_cut_softdrop_jet2_stacked.pdf"
)


