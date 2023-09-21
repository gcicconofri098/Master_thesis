import ROOT

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

h1= {}
h2= {}
h_tot = {}
hist_sum = {}

histo_file = ROOT.TFile.Open("histograms_from_analysis_with_0_996_0_98_mass_met_and_softdrop_cut.root", "READ")

h1["QCD1"] = histo_file.Get("h1_QCD1")
h1["QCD2"] = histo_file.Get("h1_QCD2")
h1["QCD3"] = histo_file.Get("h1_QCD3")
h1["QCD4"] = histo_file.Get("h1_QCD4")
h1["QCD5"] = histo_file.Get("h1_QCD5")
h1["QCD6"] = histo_file.Get("h1_QCD6")
h1["QCD7"] = histo_file.Get("h1_QCD7")
h1["QCD8"] = histo_file.Get("h1_QCD8")

h2["QCD1"] = histo_file.Get("h2_QCD1")
h2["QCD2"] = histo_file.Get("h2_QCD2")
h2["QCD3"] = histo_file.Get("h2_QCD3")
h2["QCD4"] = histo_file.Get("h2_QCD4")
h2["QCD5"] = histo_file.Get("h2_QCD5")
h2["QCD6"] = histo_file.Get("h2_QCD6")
h2["QCD7"] = histo_file.Get("h2_QCD7")
h2["QCD8"] = histo_file.Get("h2_QCD8")

h_tot["QCD1"] = histo_file.Get("h_totQCD1")
h_tot["QCD2"] = histo_file.Get("h_totQCD2")
h_tot["QCD3"] = histo_file.Get("h_totQCD3")
h_tot["QCD4"] = histo_file.Get("h_totQCD4")
h_tot["QCD5"] = histo_file.Get("h_totQCD5")
h_tot["QCD6"] = histo_file.Get("h_totQCD6")
h_tot["QCD7"] = histo_file.Get("h_totQCD7")
h_tot["QCD8"] = histo_file.Get("h_totQCD8")

# hist_sum["QCD1"] = histo_file.Get("hist_sum_QCD1")
# hist_sum["QCD2"] = histo_file.Get("hist_sum_QCD2")
# hist_sum["QCD3"] = histo_file.Get("hist_sum_QCD3")
# hist_sum["QCD4"] = histo_file.Get("hist_sum_QCD4")
# hist_sum["QCD5"] = histo_file.Get("hist_sum_QCD5")
# hist_sum["QCD6"] = histo_file.Get("hist_sum_QCD6")
# hist_sum["QCD7"] = histo_file.Get("hist_sum_QCD7")
# hist_sum["QCD8"] = histo_file.Get("hist_sum_QCD8")


h1["WJets1"] = histo_file.Get("h1_WJets1")
h1["WJets2"] = histo_file.Get("h1_WJets2")
h1["WJets3"] = histo_file.Get("h1_WJets3")

h2["WJets1"] = histo_file.Get("h2_WJets1")
h2["WJets2"] = histo_file.Get("h2_WJets2")
h2["WJets3"] = histo_file.Get("h2_WJets3")

h_tot["WJets1"] = histo_file.Get("h_totWJets1")
h_tot["WJets2"] = histo_file.Get("h_totWJets2")
h_tot["WJets3"] = histo_file.Get("h_totWJets3")


# hist_sum["WJets1"] = histo_file.Get("hist_sum_WJets1")
# hist_sum["WJets2"] = histo_file.Get("hist_sum_WJets2")
# hist_sum["WJets3"] = histo_file.Get("hist_sum_WJets3")


h1["ZJets1"] = histo_file.Get("h1_ZJets1")
h1["ZJets2"] = histo_file.Get("h1_ZJets2")
h1["ZJets3"] = histo_file.Get("h1_ZJets3")

h2["ZJets1"] = histo_file.Get("h2_ZJets1")
h2["ZJets2"] = histo_file.Get("h2_ZJets2")
h2["ZJets3"] = histo_file.Get("h2_ZJets3")

h_tot["ZJets1"] = histo_file.Get("h_totZJets1")
h_tot["ZJets2"] = histo_file.Get("h_totZJets2")
h_tot["ZJets3"] = histo_file.Get("h_totZJets3")


# hist_sum["ZJets1"] = histo_file.Get("hist_sum_ZJets1")
# hist_sum["ZJets2"] = histo_file.Get("hist_sum_ZJets2")
# hist_sum["ZJets3"] = histo_file.Get("hist_sum_ZJets3")


h1["TTHad"] = histo_file.Get("h1_TTHad")

h2["TTHad"] = histo_file.Get("h2_TTHad")

h_tot["TTHad"] = histo_file.Get("h_totTTHad")

# hist_sum["TTHad"] = histo_file.Get("hist_sum_TTHad")


h1["TTSemilept"] = histo_file.Get("h1_TTSemilept")

h2["TTSemilept"] = histo_file.Get("h2_TTSemilept")

h_tot["TTSemilept"] = histo_file.Get("h_totTTSemilept")

# hist_sum["TTSemilept"] = histo_file.Get("hist_sum_TTSemilept")


h1["ST_tw_antitop"] = histo_file.Get("h1_ST_tw_antitop")

h2["ST_tw_antitop"] = histo_file.Get("h2_ST_tw_antitop")

h_tot["ST_tw_antitop"] = histo_file.Get("h_totST_tw_antitop")

# hist_sum["ST_tw_antitop"] = histo_file.Get("hist_sum_ST_tw_antitop")


h1["ST_tw_top"] = histo_file.Get("h1_ST_tw_top")

h2["ST_tw_top"] = histo_file.Get("h2_ST_tw_top")

h_tot["ST_tw_top"] = histo_file.Get("h_totST_tw_top")

# hist_sum["ST_tw_top"] = histo_file.Get("hist_sum_ST_tw_top")


h1["GGH"] = histo_file.Get("h1_GGH")

h2["GGH"] = histo_file.Get("h2_GGH")

h_tot["GGH"] = histo_file.Get("h_totGGH")

# hist_sum["GGH"] = histo_file.Get("hist_sum_GGH")


h1["VBFH"] = histo_file.Get("h1_VBFH")

h2["VBFH"] = histo_file.Get("h2_VBFH")

h_tot["VBFH"] = histo_file.Get("h_totVBFH")

# hist_sum["VBFH"] = histo_file.Get("hist_sum_VBFH")


h1["ttH"] = histo_file.Get("h1_ttH")

h2["ttH"] = histo_file.Get("h2_ttH")

h_tot["ttH"] = histo_file.Get("h_totttH")

# hist_sum["ttH"] = histo_file.Get("hist_sum_ttH")


h1["WMinusH"] = histo_file.Get("h1_WMinusH")

h2["WMinusH"] = histo_file.Get("h2_WMinusH")

h_tot["WMinusH"] = histo_file.Get("h_totWMinusH")

#hist_sum["WMinusH"] = histo_file.Get("hist_sum_WMinusH")


h1["WPlusH"] = histo_file.Get("h1_WPlusH")

h2["WPlusH"] = histo_file.Get("h2_WPlusH")

h_tot["WPlusH"] = histo_file.Get("h_totWPlusH")

#hist_sum["WPlusH"] = histo_file.Get("hist_sum_WPlusH")


h1["ZH"] = histo_file.Get("h1_ZH")

h2["ZH"] = histo_file.Get("h2_ZH")

h_tot["ZH"] = histo_file.Get("h_totZH")

#hist_sum["ZH"] = histo_file.Get("hist_sum_ZH")


h1["ggZH"] = histo_file.Get("h1_ggZH")

h2["ggZH"] = histo_file.Get("h2_ggZH")

h_tot["ggZH"] = histo_file.Get("h_totggZH")

#hist_sum["ggZH"] = histo_file.Get("hist_sum_ggZH")


h1["WW"] = histo_file.Get("h1_WW")

h2["WW"] = histo_file.Get("h2_WW")

h_tot["WW"] = histo_file.Get("h_totWW")

#hist_sum["WW"] = histo_file.Get("hist_sum_WW")


h1["WZ"] = histo_file.Get("h1_WZ")

h2["WZ"] = histo_file.Get("h2_WZ")

h_tot["WZ"] = histo_file.Get("h_totWZ")

#hist_sum["WZ"] = histo_file.Get("hist_sum_WZ")


h1["ZZ"] = histo_file.Get("h1_ZZ")

h2["ZZ"] = histo_file.Get("h2_ZZ")

h_tot["ZZ"] = histo_file.Get("h_totZZ")

#hist_sum["ZZ"] = histo_file.Get("hist_sum_ZZ")


h1["signal"] = histo_file.Get("h1_signal")

h2["signal"] = histo_file.Get("h2_signal")

h_tot["signal"] = histo_file.Get("h_totsignal")

#hist_sum["signal"] = histo_file.Get("hist_sum_signal")



processes = list(h1.keys())


for i in processes:
    #* the value to normalize at the same integrated luminosity of the AN is 2.27
    #print(type(h1[i]))
    h1[i].Scale(weights[i])
    h2[i].Scale(weights[i])
    h_tot[i].Scale(weights[i])
    #hist_sum[i].Scale(weights[i])


    # h1[i].Rebin(2)
    # h2[i].Rebin(2)
    # h_tot[i].Rebin(30)
    #hist_sum[i].Rebin(25)

    #h1[i].GetXaxis().SetRangeUser(80, 150)
    #h2[i].GetXaxis().SetRangeUser(80., 150.)
    # h_tot[i].GetXaxis().SetRangeUser(40., 500.)
    #hist_sum[i].GetXaxis().SetRange(0, 500)

    # if str(i)== "QCD1" or str(i)== "QCD2" or str(i)== "QCD3" or str(i)== "QCD4" or str(i)== "QCD5" or str(i)== "QCD6" or str(i)== "QCD7" or str(i)== "QCD8":
    #     h1[i].Scale(30)
    #     h2[i].Scale(30)
    #     h_tot[i].Scale(30)
    #     #hist_sum[i].Scale(30)
    print("scaled: {}".format(str(i)))

hist_QCD = None
hist_VJets = None
hist_TTBar = None
hist_ST = None
hist_singleH = None



hist_QCD = h1["QCD1"].Clone()
hist_QCD.Add(h1["QCD2"])
hist_QCD.Add(h1["QCD3"])
hist_QCD.Add(h1["QCD4"])
hist_QCD.Add(h1["QCD5"])
hist_QCD.Add(h1["QCD6"])
hist_QCD.Add(h1["QCD7"])
hist_QCD.Add(h1["QCD8"])


hist_VJets = h1["WJets1"].Clone()
hist_VJets.Add(h1["WJets2"])
hist_VJets.Add(h1["WJets3"])
hist_VJets.Add(h1["ZJets1"])
hist_VJets.Add(h1["ZJets2"])
hist_VJets.Add(h1["ZJets3"])


hist_TTBar_Had = h1["TTHad"].Clone()
hist_TTBar_Semilep = h1["TTSemilept"].Clone()

hist_ST = h1["ST_tw_antitop"].Clone()
hist_ST.Add(h1["ST_tw_top"])

hist_singleH = h1["GGH"].Clone()
hist_singleH.Add(h1["VBFH"])
hist_singleH.Add(h1["WMinusH"])
hist_singleH.Add(h1["WPlusH"])
hist_singleH.Add(h1["ZH"])
hist_singleH.Add(h1["ggZH"])
hist_singleH.Add(h1["ttH"])

hist_VV = h1["WZ"].Clone()
hist_VV.Add(h1["ZZ"])
hist_VV.Add(h1["WW"])


#! Stacked histogram of Jet1 and jet2 for signal

# c11 = ROOT.TCanvas("c11", "Stacked Histograms", 800, 700)


# stacked = h1["signal"].Clone()
# stacked.Add(h2["signal"])
# stacked.Draw("HIST")


# TODO cat1

c1 = ROOT.TCanvas("c1", "Stacked Histograms after preselection", 800, 700)

# TODO Jet1 Histograms are stacked by type of background, but they are not printed on the same plot


legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


c1.Divide(3, 3)


c1.cd(7)

temp7 = h1["signal"].Clone()
temp7.SetNameTitle("temp7", "signal")

temp7.Draw("HIST")
temp7.SetLineColor(ROOT.kCyan + 4)
temp7.SetFillColorAlpha(ROOT.kCyan - 6, 0.8)


c1.cd(6)
temp6 = h1["signal"].Clone()

temp6.Add(hist_VJets)

temp6.SetNameTitle("temp6", "Vjets")

temp6.Draw("HIST")
temp6.SetLineColor(ROOT.kGreen + 2)
temp6.SetFillColorAlpha(ROOT.kGreen - 8, 0.8)


c1.cd(5)

temp5 = h1["signal"].Clone()
temp5.Add(hist_VJets)
temp5.Add(hist_TTBar_Had)

# temp5.SetNameTitle("temp5", "Vjets + ttbar")

temp5.Draw("HIST")
temp5.SetLineColor(ROOT.kRed + 1)
temp5.SetFillColorAlpha(ROOT.kRed - 8, 0.8)


#temp8

temp8 = h1["signal"].Clone()
temp8.Add(hist_VJets)
temp8.Add(hist_TTBar_Had)
temp8.Add(hist_TTBar_Semilep)


c1.cd(4)

temp4 = h1["signal"].Clone()
temp4.Add(hist_VJets)
temp4.Add(hist_TTBar_Had)
temp4.Add(hist_TTBar_Semilep)
temp4.Add(hist_ST)

# temp4.SetNameTitle("temp4", "Vjets + ttbar + ST")


temp4.Draw("HIST")
temp4.SetLineColor(ROOT.kBlue + 2)
temp4.SetFillColorAlpha(ROOT.kBlue - 8, 0.8)


c1.cd(3)

temp3 = h1["signal"].Clone()
temp3.Add(hist_VJets)
temp3.Add(hist_TTBar_Had)
temp3.Add(hist_TTBar_Semilep)
temp3.Add(hist_ST)
temp3.Add(hist_singleH)

# temp3.SetNameTitle("temp3", "Vjets + ttbar + ST + single H")

temp3.Draw("HIST")
temp3.SetLineColor(ROOT.kGreen + 4)
temp3.SetFillColorAlpha(ROOT.kGreen - 6, 0.8)


c1.cd(2)

temp2 = h1["signal"].Clone()
temp2.Add(hist_VJets)
temp2.Add(hist_TTBar_Had)
temp2.Add(hist_TTBar_Semilep)
temp2.Add(hist_ST)
temp2.Add(hist_singleH)
temp2.Add(hist_VV)

# temp2.SetNameTitle("temp2", "Vjets + ttbar + ST + single H+ VV")


temp2.Draw("HIST")
temp2.SetLineColor(ROOT.kRed + 4)
temp2.SetFillColorAlpha(ROOT.kRed + 1, 0.8)


c1.cd(1)

temp1 = h1["signal"].Clone()
temp1.Add(hist_VJets)
temp1.Add(hist_TTBar_Had)
temp1.Add(hist_TTBar_Semilep)
temp1.Add(hist_ST)
temp1.Add(hist_singleH)
temp1.Add(hist_VV)
temp1.Add(hist_QCD)

# temp1.SetNameTitle("temp1", "Vjets + ttbar + ST + single H+ VV + QCD")

temp1.Draw("HIST")
temp1.SetLineColor(ROOT.kBlue + 1)
# temp1.SetFillColorAlpha(ROOT.kBlue - 6, 0.8)

# temp1=h1["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH).Add(hist_VV).Add(hist_QCD)
# temp2=h1["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH).Add(hist_VV)
# temp3=h1["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH)
# temp4=h1["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST)
# temp5=h1["signal"].Clone().Add(hist_VJets).Add(hist_TTBar)
# temp6=h1["signal"].Clone().Add(hist_VJets)
# temp7=h1["signal"].Clone()


c2 = ROOT.TCanvas("c2", "Jet1 contributions after preselection", 800, 700)

# TODO Different contributions for the various type of background Jet1


c2.Divide(3, 3)

c2.cd(1)
h1["signal"].Draw("HIST")

c2.cd(2)
hist_VJets.Draw("HIST")

c2.cd(3)

hist_TTBar_Had.Draw("HIST")

c2.cd(4)

hist_ST.Draw("HIST")

c2.cd(5)

hist_TTBar_Semilep.Draw("HIST")

c2.cd(6)

hist_singleH.Draw("HIST")


c2.cd(7)

hist_VV.Draw("HIST")


c2.cd(8)

hist_QCD.Draw("HIST")


c3 = ROOT.TCanvas("c3", "Stacked contributions for jet1 after preselection", 800, 700)


# TODO Stacked histograms for Jet1


temp1.Draw("HIST")
temp1.SetTitle("Distribution of Jet1 discriminator")
# temp1.SetLineColor(ROOT.kBlue+1)
temp1.SetFillColorAlpha(ROOT.kAzure + 6, 0.8)
legend.AddEntry(temp1, "QCD", "f")


temp1.ResetStats()
jet1 = temp1.GetEntries()
print("jet1 entries count", jet1)


temp2.Draw("SAME HIST")
# temp2.SetLineColor(ROOT.kRed+4)
temp2.SetFillColorAlpha(ROOT.kRed + 1, 0.8)
legend.AddEntry(temp2, "Double V events", "f")


temp3.Draw("SAME HIST")
# temp3.SetLineColor(ROOT.kGreen+4)
temp3.SetFillColorAlpha(ROOT.kGreen - 6, 0.8)
legend.AddEntry(temp3, "single Higgs", "f")


temp4.Draw("SAME HIST")
# temp4.SetLineColor(ROOT.kBlue+2)
temp4.SetFillColorAlpha(ROOT.kBlue - 8, 0.8)
legend.AddEntry(temp4, "single top", "f")


temp8.Draw("SAME HIST")
# temp8.SetLineColor(ROOT.kRed+1)
temp8.SetFillColorAlpha(ROOT.kAzure - 4, 0.8)
legend.AddEntry(temp8, "semileptonic t tbar events", "f")

temp5.Draw("SAME HIST")
# temp5.SetLineColor(ROOT.kRed+1)
temp5.SetFillColorAlpha(ROOT.kRed - 8, 0.8)
legend.AddEntry(temp5, "hadronic t tbar events", "f")


temp6.Draw("SAME HIST")
# temp6.SetLineColor(ROOT.kGreen+2)
temp6.SetFillColorAlpha(ROOT.kGreen - 8, 0.8)
legend.AddEntry(temp6, "V + jets", "f")

h1["signal"].Draw("SAME HIST")
h1["signal"].Scale(10)
h1["signal"].SetLineColor(ROOT.kBlack)
h1["signal"].SetLineWidth(2)

legend.AddEntry(h1["signal"], "signal x 10", "l")


legend.Draw()


#! Jet2


hist_QCD_2 = None
hist_VJets_2 = None
hist_TTBar_2 = None
hist_ST_2 = None
hist_singleH_2 = None
hist_VV_2 = None


hist_QCD_2 = h2["QCD1"].Clone()
hist_QCD_2.Add(h2["QCD2"])
hist_QCD_2.Add(h2["QCD3"])
hist_QCD_2.Add(h2["QCD4"])
hist_QCD_2.Add(h2["QCD5"])
hist_QCD_2.Add(h2["QCD6"])
hist_QCD_2.Add(h2["QCD7"])
hist_QCD_2.Add(h2["QCD8"])

hist_VJets_2 = h2["WJets1"].Clone()
hist_VJets_2.Add(h2["WJets2"])
hist_VJets_2.Add(h2["WJets3"])
hist_VJets_2.Add(h2["ZJets1"])
hist_VJets_2.Add(h2["ZJets2"])
hist_VJets_2.Add(h2["ZJets3"])


hist_TTBar_Had_2 = h2["TTHad"].Clone()
hist_TTBar_Semi_2= h2["TTSemilept"].Clone()

hist_ST_2 = h2["ST_tw_antitop"].Clone()
hist_ST_2.Add(h2["ST_tw_top"])

hist_singleH_2 = h2["GGH"].Clone()
hist_singleH_2.Add(h2["VBFH"])
hist_singleH_2.Add(h2["WMinusH"])
hist_singleH_2.Add(h2["WPlusH"])
hist_singleH_2.Add(h2["ZH"])
hist_singleH_2.Add(h2["ggZH"])
hist_singleH_2.Add(h2["ttH"])

hist_VV_2 = h2["WZ"].Clone()
hist_VV_2.Add(h2["ZZ"])
hist_VV_2.Add(h2["WW"])


c4 = ROOT.TCanvas("c4", "Stacked Histograms Jet2 after preselection", 800, 700)

# TODO Jet2 Histograms are stacked by contributions, but printed on different plots

legend2 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


c4.Divide(3, 3)


c4.cd(7)

temp7_2 = h2["signal"].Clone()

print(type(temp7_2))

temp7_2.Draw("HIST")
# temp7_2.SetLineColor(ROOT.kCyan+4)
temp7_2.SetFillColorAlpha(ROOT.kCyan - 6, 0.8)


c4.cd(6)

temp6_2 = h2["signal"].Clone()

print(type(temp6_2))
temp6_2.Add(hist_VJets_2)


temp6_2.Draw("HIST")
# temp6_2.SetLineColor(ROOT.kGreen+2)
temp6_2.SetFillColorAlpha(ROOT.kGreen - 8, 0.8)


c4.cd(5)

temp5_2 = h2["signal"].Clone()
temp5_2.Add(hist_VJets_2)
temp5_2.Add(hist_TTBar_Had_2)

temp5_2.Draw("HIST")
# temp5_2.SetLineColor(ROOT.kRed+1)
temp5_2.SetFillColorAlpha(ROOT.kRed - 8, 0.8)


print(type(temp6_2))


temp8_2 = h2["signal"].Clone()
temp8_2.Add(hist_VJets_2)
temp8_2.Add(hist_TTBar_Had_2)
temp8_2.Add(hist_TTBar_Semi_2)

temp8_2.Draw("HIST")
# temp8_2.SetLineColor(ROOT.kRed+1)
temp8_2.SetFillColorAlpha(ROOT.kRed - 8, 0.8)




c4.cd(4)

temp4_2 = h2["signal"].Clone()
temp4_2.Add(hist_VJets_2)
temp4_2.Add(hist_TTBar_Had_2)
temp4_2.Add(hist_TTBar_Semi_2)
temp4_2.Add(hist_ST_2)


temp4_2.Draw("HIST")
# temp4_2.SetLineColor(ROOT.kBlue+2)
temp4_2.SetFillColorAlpha(ROOT.kBlue - 8, 0.8)


c4.cd(3)

temp3_2 = h2["signal"].Clone()
temp3_2.Add(hist_VJets_2)
temp3_2.Add(hist_TTBar_Had_2)
temp3_2.Add(hist_TTBar_Semi_2)
temp3_2.Add(hist_ST_2)
temp3_2.Add(hist_singleH_2)


temp3_2.Draw("HIST")
# temp3_2.SetLineColor(ROOT.kGreen+4)
temp3_2.SetFillColorAlpha(ROOT.kGreen - 6, 0.8)


c4.cd(2)

temp2_2 = h2["signal"].Clone()
temp2_2.Add(hist_VJets_2)
temp2_2.Add(hist_TTBar_Had_2)
temp2_2.Add(hist_TTBar_Semi_2)
temp2_2.Add(hist_ST_2)
temp2_2.Add(hist_singleH_2)
temp2_2.Add(hist_VV_2)


temp2_2.Draw("HIST")
# temp2_2.SetLineColor(ROOT.kRed+4)
temp2_2.SetFillColorAlpha(ROOT.kRed + 1, 0.8)


c4.cd(1)

temp1_2 = h2["signal"].Clone()
temp1_2.Add(hist_VJets_2)
temp1_2.Add(hist_TTBar_Had_2)
temp1_2.Add(hist_TTBar_Semi_2)
temp1_2.Add(hist_ST_2)
temp1_2.Add(hist_singleH_2)
temp1_2.Add(hist_VV_2)
temp1_2.Add(hist_QCD_2)


temp1_2.Draw("HIST")
# temp1_2.SetLineColor(ROOT.kBlue+1)
temp1_2.SetFillColorAlpha(ROOT.kBlue - 6, 0.8)

# temp1=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH).Add(hist_VV).Add(hist_QCD)
# temp2=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH).Add(hist_VV)
# temp3=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH)
# temp4=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST)
# temp5=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar)
# temp6=h2["signal"].Clone().Add(hist_VJets)
# temp7=h2["signal"].Clone()


c5 = ROOT.TCanvas("c5", "Contributions for jet 2 after preselection", 800, 700)

# TODO Histograms for jet 2 are divided by type of contribution

c5.Divide(3, 3)

c5.cd(1)

signal_2 = h2["signal"].Draw("HIST")

c5.cd(2)

hist_VJets_2.Draw("HIST")


c5.cd(3)

#hist_TTBar_2.Draw("HIST")


c5.cd(4)

hist_ST_2.Draw("HIST")


c5.cd(5)

hist_singleH_2.Draw("HIST")


c5.cd(6)

hist_VV_2.Draw("HIST")


c5.cd(7)

hist_QCD_2.Draw("HIST")


c6 = ROOT.TCanvas("c6", "Stacked contributions for jet2 after preselection", 800, 700)

# TODO Stacked contributions for jet 2

temp1_2.Draw("HIST")
# temp1_2.SetLineColor(ROOT.kBlue+1)
temp1_2.SetFillColorAlpha(ROOT.kAzure + 6, 0.8)
legend2.AddEntry(temp1_2, "QCD", "f")
temp1_2.SetTitle("Contributions for Jet2 softfdrop mass")

temp1_2.ResetStats()
jet2 = temp1_2.GetEntries()
print("jet1 entries count", jet2)


temp2_2.Draw("SAME HIST")
# temp2_2.SetLineColor(ROOT.kRed+4)
temp2_2.SetFillColorAlpha(ROOT.kRed + 1, 0.8)
legend2.AddEntry(temp2_2, "Double V events", "f")


temp3_2.Draw("SAME HIST")
# temp3_2.SetLineColor(ROOT.kGreen+4)
temp3_2.SetFillColorAlpha(ROOT.kGreen - 6, 0.8)
legend2.AddEntry(temp3_2, "single Higgs", "f")


temp4_2.Draw("SAME HIST")
# temp4_2.SetLineColor(ROOT.kBlue+2)
temp4_2.SetFillColorAlpha(ROOT.kBlue - 8, 0.8)
legend2.AddEntry(temp4_2, "single top", "f")


temp8_2.Draw("SAME HIST")
# temp8_2.SetLineColor(ROOT.kRed+1)
temp8_2.SetFillColorAlpha(ROOT.kRed - 8, 0.8)
legend2.AddEntry(temp8_2, "semileptonic t tbar events", "f")


temp5_2.Draw("SAME HIST")
# temp5_2.SetLineColor(ROOT.kRed+1)
temp5_2.SetFillColorAlpha(ROOT.kAzure +4, 0.8)
legend2.AddEntry(temp5_2, "hadronic t tbar events", "f")

temp6_2.Draw("SAME HIST")

# temp6_2.SetLineColor(ROOT.kGreen+2)
temp6_2.SetFillColorAlpha(ROOT.kGreen - 8, 0.8)
legend2.AddEntry(temp6_2, "V + jets", "f")

print(h2["signal"].GetEntries())

#temp0 = h2["signal"].Clone()

#temp0.ResetAttLine()

h2["signal"].Draw("SAME HIST")
h2["signal"].Scale(10)
h2["signal"].SetLineWidth(2)
h2["signal"].SetLineColor(ROOT.kBlack)
legend2.AddEntry(h2["signal"], "signal x 10", "l")


legend2.Draw()

# c7 = ROOT.TCanvas("c7", "Jet1 vs Jet2 2d background after preselection", 800, 700)

# # TODO 2d lego for background, Jet1 vs Jet2


# hist2d_bckg = h2_2["QCD1"].Clone()
# hist2d_bckg.Add(h2_2["QCD2"])
# hist2d_bckg.Add(h2_2["QCD3"])
# hist2d_bckg.Add(h2_2["QCD4"])
# hist2d_bckg.Add(h2_2["QCD5"])
# hist2d_bckg.Add(h2_2["QCD6"])
# hist2d_bckg.Add(h2_2["QCD7"])
# hist2d_bckg.Add(h2_2["QCD8"])


# hist2d_bckg.Add(h2_2["WJets1"])
# hist2d_bckg.Add(h2_2["WJets2"])
# hist2d_bckg.Add(h2_2["WJets3"])
# hist2d_bckg.Add(h2_2["ZJets1"])
# hist2d_bckg.Add(h2_2["ZJets2"])
# hist2d_bckg.Add(h2_2["ZJets3"])


# hist2d_bckg.Add(h2_2["TTHad"])
# hist2d_bckg.Add(h2_2["TTSemilept"])

# hist2d_bckg.Add(h2_2["ST_tw_antitop"])
# hist2d_bckg.Add(h2_2["ST_tw_top"])

# hist2d_bckg.Add(h2_2["GGH"])
# hist2d_bckg.Add(h2_2["VBFH"])
# hist2d_bckg.Add(h2_2["WMinusH"])
# hist2d_bckg.Add(h2_2["WPlusH"])
# hist2d_bckg.Add(h2_2["ZH"])
# hist2d_bckg.Add(h2_2["ggZH"])

# hist2d_bckg.Add(h2_2["WZ"])
# hist2d_bckg.Add(h2_2["ZZ"])
# hist2d_bckg.Add(h2_2["WW"])


# hist2d_bckg.Draw("COLZ")
# hist2d_bckg.SetTitle("Lego plot for background")

# print()


# c10 = ROOT.TCanvas("c10", "Jet1 vs Jet2 2d signal", 800, 700)

# # TODO 2d lego for signal, Jet1 vs Jet2


# histo2d["signal"].Draw("COLZ")

# histo2d["signal"].SetTitle("Lego plot for signal")


c8 = ROOT.TCanvas("c8", "Jet1 vs Jet2 after preselection", 800, 700)

# TODO 1D plots for Jet1 and Jet2

legend3 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


# max = temp1_2.GetMaximum() + 50

# temp1.Draw("HIST")
# legend3.AddEntry(temp1, "Jet 1 bckg", "l")
# temp1.SetLineColor(ROOT.kBlack)
# temp1.SetLineWidth(3)
# temp1.SetLineStyle(2)
# temp1.SetMaximum(max)
# #temp1.ResetAttFill()


# temp1_2.Draw("SAME HIST")
# legend3.AddEntry(temp1_2, "Jet 2 bckg", "l")
# temp1_2.SetLineColor(ROOT.kRed +2)
# temp1_2.SetLineWidth(3)
# temp1_2.SetLineStyle(2)
# #temp1_2.ResetAttFill()


h1["signal"].Draw("HIST")
legend3.AddEntry(h1["signal"], "Jet 1 signal", "l")
h1["signal"].SetLineColor(ROOT.kBlack)
h1["signal"].SetLineWidth(2)
# h1["signal"].SetFillColorAlpha(0, 0)

h2["signal"].Draw("SAME HIST")
legend3.AddEntry(h2["signal"], "Jet 2 signal", "l")
h2["signal"].SetLineColor(ROOT.kRed + 2)
h2["signal"].SetLineWidth(2)
# h2["signal"].SetFillColorAlpha(0, 0)

legend3.Draw()

#! All jets


total = h_tot["QCD1"].Clone()
total.Add(h_tot["QCD2"])
total.Add(h_tot["QCD3"])
total.Add(h_tot["QCD4"])
total.Add(h_tot["QCD5"])
total.Add(h_tot["QCD6"])
total.Add(h_tot["QCD7"])
total.Add(h_tot["QCD8"])

# total.Add(h_tot["WJets1"])
# total.Add(h_tot["WJets2"])
# total.Add(h_tot["WJets3"])
# total.Add(h_tot["ZJets1"])
# total.Add(h_tot["ZJets2"])
# total.Add(h_tot["ZJets3"])


# total.Add(h_tot["TTHad"])
# total.Add(h_tot["TTSemilept"])

# total.Add(h_tot["ST_tw_antitop"])
# total.Add(h_tot["ST_tw_top"])

# total.Add(h_tot["GGH"])
# total.Add(h_tot["VBFH"])
# total.Add(h_tot["WMinusH"])
# total.Add(h_tot["WPlusH"])
# total.Add(h_tot["ZH"])
# total.Add(h_tot["ggZH"])
# total.Add(h_tot["ttH"])

# total.Add(h_tot["WZ"])
# total.Add(h_tot["ZZ"])
# total.Add(h_tot["WW"])


c9 = ROOT.TCanvas("c9", "Signal to bckg", 900, 800)
legend4 = ROOT.TLegend(0.62, 0.70, 0.82, 0.85)
ROOT.gPad.SetLogy(1)

total.SetLineColor(ROOT.kBlue + 2)
total.SetLineWidth(2)
legend4.AddEntry(total, "QCD background", "l")
total.Draw("HIST")
total.Scale(1 / total.Integral())
total.SetTitle("Tagger distribution for signal and QCD background; FatJet_deepTagMD_HbbvsQCD; Fraction of events")

h_tot["signal"].SetLineColor(ROOT.kRed + 2)
h_tot["signal"].SetLineWidth(2)
scale = h_tot["signal"].Integral()
h_tot["signal"].Scale(1 / scale)
legend4.AddEntry(h_tot["signal"], "signal", "l")
# h_tot["signal"].SetTitle("Signal Jet1 vs Jet2 discriminator; Jet 1; Jet2")
h_tot["signal"].Draw("SAME HIST")
legend4.Draw()


#! INVARIANT MASS OF THE PAIR OF JETS

# sum_hist_QCD = None
# sum_hist_VJets = None
# sum_hist_TTBar = None
# sum_hist_ST = None
# sum_hist_singleH = None
# sum_hist_VV = None

# sum_hist_QCD = hist_sum["QCD1"].Clone()
# sum_hist_QCD.Add(hist_sum["QCD2"])
# sum_hist_QCD.Add(hist_sum["QCD3"])
# sum_hist_QCD.Add(hist_sum["QCD4"])
# sum_hist_QCD.Add(hist_sum["QCD5"])
# sum_hist_QCD.Add(hist_sum["QCD6"])
# sum_hist_QCD.Add(hist_sum["QCD7"])
# sum_hist_QCD.Add(hist_sum["QCD8"])

# sum_hist_VJets = hist_sum["WJets1"].Clone()
# sum_hist_VJets.Add(hist_sum["WJets2"])
# sum_hist_VJets.Add(hist_sum["WJets3"])
# sum_hist_VJets.Add(hist_sum["ZJets1"])
# sum_hist_VJets.Add(hist_sum["ZJets2"])
# sum_hist_VJets.Add(hist_sum["ZJets3"])


# sum_hist_TTBar = hist_sum["TTHad"].Clone()
# sum_hist_TTBar.Add(hist_sum["TTSemilept"])

# sum_hist_ST = hist_sum["ST_tw_antitop"].Clone()
# sum_hist_ST.Add(hist_sum["ST_tw_top"])

# sum_hist_singleH = hist_sum["GGH"].Clone()
# sum_hist_singleH.Add(hist_sum["VBFH"])
# sum_hist_singleH.Add(hist_sum["WMinusH"])
# sum_hist_singleH.Add(hist_sum["WPlusH"])
# sum_hist_singleH.Add(hist_sum["ZH"])
# sum_hist_singleH.Add(hist_sum["ggZH"])
# sum_hist_singleH.Add(hist_sum["ttH"])

# sum_hist_VV = hist_sum["WZ"].Clone()
# sum_hist_VV.Add(hist_sum["ZZ"])
# sum_hist_VV.Add(hist_sum["WW"])


# c12 = ROOT.TCanvas("c12", "Invariant mass of the two jets", 900, 800)

# legend5 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


# temp1_3 = hist_sum["signal"].Clone()
# temp1_3.Add(sum_hist_VJets)
# temp1_3.Add(sum_hist_TTBar)
# temp1_3.Add(sum_hist_ST)
# temp1_3.Add(sum_hist_singleH)
# temp1_3.Add(sum_hist_VV)
# temp1_3.Add(sum_hist_QCD)

# temp1_3.Draw("HIST")
# temp1_3.SetNameTitle("temp1_3", "Invariant mass of the two jets")
# legend5.AddEntry(temp1_3, "QCD", "f")
# temp1_3.SetFillColorAlpha(ROOT.kAzure + 6, 0.8)


# temp2_3 = hist_sum["signal"].Clone()
# temp2_3.Add(sum_hist_VJets)
# temp2_3.Add(sum_hist_TTBar)
# temp2_3.Add(sum_hist_ST)
# temp2_3.Add(sum_hist_singleH)
# temp2_3.Add(sum_hist_VV)
# temp2_3.Draw("HIST SAME")
# temp2_3.SetFillColorAlpha(ROOT.kRed + 1, 0.8)
# legend5.AddEntry(temp2_3, "VV events", "f")


# temp3_3 = hist_sum["signal"].Clone()
# temp3_3.Add(sum_hist_VJets)
# temp3_3.Add(sum_hist_TTBar)
# temp3_3.Add(sum_hist_ST)
# temp3_3.Add(sum_hist_singleH)
# temp3_3.Draw("SAME HIST")
# temp3_3.SetFillColorAlpha(ROOT.kGreen - 6, 0.8)
# legend5.AddEntry(temp3_3, "single H events", "f")


# temp4_3 = hist_sum["signal"].Clone()
# temp4_3.Add(sum_hist_VJets)
# temp4_3.Add(sum_hist_TTBar)
# temp4_3.Add(sum_hist_ST)
# temp4_3.Draw("SAME HIST")
# temp4_3.SetFillColorAlpha(ROOT.kBlue - 8, 0.8)
# legend5.AddEntry(temp4_3, "single T events", "f")


# temp5_3 = hist_sum["signal"].Clone()
# temp5_3.Add(sum_hist_VJets)
# temp5_3.Add(sum_hist_TTBar)
# temp5_3.Draw("SAME HIST")
# temp5_3.SetFillColorAlpha(ROOT.kRed - 8, 0.8)
# legend5.AddEntry(temp5_3, "TTbar events", "f")


# temp6_3 = hist_sum["signal"].Clone()

# temp6_3.Add(sum_hist_VJets)
# temp6_3.Draw("SAME HIST")
# temp6_3.SetFillColorAlpha(ROOT.kGreen - 8, 0.8)
# legend5.AddEntry(temp6_3, "V+ jets", "f")


# temp7_3 = hist_sum["signal"].Clone()
# temp7_3.Draw("SAME HIST")
# temp7_3.Scale(4500)
# temp7_3.SetLineColor(ROOT.kRed + 2)
# legend5.AddEntry(temp7_3, "signal x 4500", "l")


# legend5.Draw()

# ROOT.gPad.SetLogy(1)

c2.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/contributions_jet1_0_996_0_98_with_MET_and_mass_cut.pdf"
)
c3.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/stacked_jet1_0_996_0_98_with_MET_and_mass_cut.pdf"
)
# c5.SaveAs(
#     "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/contributions_jet2_nocut.pdf"
# )
c6.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/stacked_jet2_0_996_0_98_with_MET_and_mass_cut.pdf"
)


# # c7.SaveAs(
# #     "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/jet1_vs_jet2_2d_bckg_nocut.pdf"
# # )
# # c10.SaveAs(
# #     "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/jet1_vs_jet2_2d_sig_nocut.pdf"
# # )

# c8.SaveAs(
#     "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/jet1_vs_jet2_nocut.pdf"
# )

# c9.SaveAs(
#     "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/tagger_nocut.pdf"
# )

# c11.SaveAs(
#     "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/alljets_stacked_nocut.pdf"
# )

# c12.SaveAs(
#     "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/inv_mass_QCDscaled.pdf"
# )
