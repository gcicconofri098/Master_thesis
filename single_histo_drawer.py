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

histo_file = ROOT.TFile.Open("histograms_from_analysis_QCD_only_pt_pres.root", "READ")

h1["QCD1"] = histo_file.Get("h1_QCD1")
h1["QCD2"] = histo_file.Get("h1_QCD2")
h1["QCD3"] = histo_file.Get("h1_QCD3")
h1["QCD4"] = histo_file.Get("h1_QCD4")
h1["QCD5"] = histo_file.Get("h1_QCD5")
h1["QCD6"] = histo_file.Get("h1_QCD6")
h1["QCD7"] = histo_file.Get("h1_QCD7")
h1["QCD8"] = histo_file.Get("h1_QCD8")

# h1["WJets1"] = histo_file.Get("h2_2_WJets1")
# h1["WJets2"] = histo_file.Get("h2_2_WJets2")
# h1["WJets3"] = histo_file.Get("h2_2_WJets3")


# h1["ZJets1"] = histo_file.Get("h2_2_ZJets1")
# h1["ZJets2"] = histo_file.Get("h2_2_ZJets2")
# h1["ZJets3"] = histo_file.Get("h2_2_ZJets3")


# h1["TTHad"] = histo_file.Get("h2_2_TTHad")

# h1["TTSemilept"] = histo_file.Get("h2_2_TTSemilept")


# h1["ST_tw_antitop"] = histo_file.Get("h2_2_ST_tw_antitop")



# h1["ST_tw_top"] = histo_file.Get("h2_2_ST_tw_top")



# h1["GGH"] = histo_file.Get("h2_2_GGH")


# h1["VBFH"] = histo_file.Get("h2_2_VBFH")

# h1["ttH"] = histo_file.Get("h2_2_ttH")


# h1["WMinusH"] = histo_file.Get("h2_2_WMinusH")


# h1["WPlusH"] = histo_file.Get("h2_2_WPlusH")


# h1["ZH"] = histo_file.Get("h2_2_ZH")


# h1["ggZH"] = histo_file.Get("h2_2_ggZH")


# h1["WW"] = histo_file.Get("h2_2_WW")

# h1["WZ"] = histo_file.Get("h2_2_WZ")


# h1["ZZ"] = histo_file.Get("h2_2_ZZ")

#h1["signal"] = histo_file.Get("h2_signal")




processes = list(h1.keys())


for i in processes:
    #* the value to normalize at the same integrated luminosity of the AN is 2.27
    #print(type(h1[i]))
    h1[i].Scale(weights[i])

    #h1[i].Rebin(2)


    # h1[i].GetXaxis().SetRangeUser(40, 220)
    # h1[i].GetYaxis().SetRangeUser(40, 220)

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


# hist_VJets = h1["WJets1"].Clone()
# hist_VJets.Add(h1["WJets2"])
# hist_VJets.Add(h1["WJets3"])
# hist_VJets.Add(h1["ZJets1"])
# hist_VJets.Add(h1["ZJets2"])
# hist_VJets.Add(h1["ZJets3"])


# hist_TTBar_Had = h1["TTHad"].Clone()
# hist_TTBar_Semilep = h1["TTSemilept"].Clone()

# hist_ST = h1["ST_tw_antitop"].Clone()
# hist_ST.Add(h1["ST_tw_top"])

# hist_singleH = h1["GGH"].Clone()
# hist_singleH.Add(h1["VBFH"])
# hist_singleH.Add(h1["WMinusH"])
# hist_singleH.Add(h1["WPlusH"])
# hist_singleH.Add(h1["ZH"])
# hist_singleH.Add(h1["ggZH"])
# hist_singleH.Add(h1["ttH"])

# hist_VV = h1["WZ"].Clone()
# hist_VV.Add(h1["ZZ"])
# hist_VV.Add(h1["WW"])


#! Stacked histogram of Jet1 and jet2 for signal

# c11 = ROOT.TCanvas("c11", "Stacked Histograms", 800, 700)


# stacked = h1["signal"].Clone()
# stacked.Add(h2["signal"])
# stacked.Draw("HIST")


# TODO cat1

c1 = ROOT.TCanvas("c1", "Stacked Histograms after preselection", 800, 700)

# TODO Jet1 Histograms are stacked by type of background, but they are not printed on the same plot


legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


# c1.Divide(3, 3)


# c1.cd(7)

# temp7 = h1["signal"].Clone()
# temp7.SetNameTitle("temp7", "signal")

# temp7.Draw("HIST")
# temp7.SetLineColor(ROOT.kCyan + 4)
# temp7.SetFillColorAlpha(ROOT.kCyan - 6, 0.8)


# c1.cd(6)
# temp6 = h1["signal"].Clone()

# temp6.Add(hist_VJets)

# temp6.SetNameTitle("temp6", "Vjets")

# temp6.Draw("HIST")
# temp6.SetLineColor(ROOT.kGreen + 2)
# temp6.SetFillColorAlpha(ROOT.kGreen - 8, 0.8)


# c1.cd(5)

# temp5 = h1["signal"].Clone()
# temp5.Add(hist_VJets)
# temp5.Add(hist_TTBar_Had)

# # temp5.SetNameTitle("temp5", "Vjets + ttbar")

# temp5.Draw("HIST")
# temp5.SetLineColor(ROOT.kRed + 1)
# temp5.SetFillColorAlpha(ROOT.kRed - 8, 0.8)


# #temp8

# temp8 = h1["signal"].Clone()
# temp8.Add(hist_VJets)
# temp8.Add(hist_TTBar_Had)
# temp8.Add(hist_TTBar_Semilep)


# c1.cd(4)

# temp4 = h1["signal"].Clone()
# temp4.Add(hist_VJets)
# temp4.Add(hist_TTBar_Had)
# temp4.Add(hist_TTBar_Semilep)
# temp4.Add(hist_ST)

# # temp4.SetNameTitle("temp4", "Vjets + ttbar + ST")


# temp4.Draw("HIST")
# temp4.SetLineColor(ROOT.kBlue + 2)
# temp4.SetFillColorAlpha(ROOT.kBlue - 8, 0.8)


# c1.cd(3)

# temp3 = h1["signal"].Clone()
# temp3.Add(hist_VJets)
# temp3.Add(hist_TTBar_Had)
# temp3.Add(hist_TTBar_Semilep)
# temp3.Add(hist_ST)
# temp3.Add(hist_singleH)

# # temp3.SetNameTitle("temp3", "Vjets + ttbar + ST + single H")

# temp3.Draw("HIST")
# temp3.SetLineColor(ROOT.kGreen + 4)
# temp3.SetFillColorAlpha(ROOT.kGreen - 6, 0.8)


# c1.cd(2)

# temp2 = h1["signal"].Clone()
# temp2.Add(hist_VJets)
# temp2.Add(hist_TTBar_Had)
# temp2.Add(hist_TTBar_Semilep)
# temp2.Add(hist_ST)
# temp2.Add(hist_singleH)
# temp2.Add(hist_VV)

# # temp2.SetNameTitle("temp2", "Vjets + ttbar + ST + single H+ VV")


# temp2.Draw("HIST")
# temp2.SetLineColor(ROOT.kRed + 4)
# temp2.SetFillColorAlpha(ROOT.kRed + 1, 0.8)


# c1.cd(1)

# temp1 = h1["signal"].Clone()
# temp1.Add(hist_VJets)
# temp1.Add(hist_TTBar_Had)
# temp1.Add(hist_TTBar_Semilep)
# temp1.Add(hist_ST)
# temp1.Add(hist_singleH)
# temp1.Add(hist_VV)
# temp1.Add(hist_QCD)

# # temp1.SetNameTitle("temp1", "Vjets + ttbar + ST + single H+ VV + QCD")

# temp1.Draw("HIST")
# temp1.SetLineColor(ROOT.kBlue + 1)

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


#c2.Divide(3, 3)

#c2.cd(1)
hist_QCD.Draw("HIST")
hist_QCD.SetLineColor(ROOT.kBlue + 1)
hist_QCD.SetLineWidth(2)
#h1['signal'].SetFillColorAlpha(ROOT.kAzure + 6, 0.8)

#c2.SetGrid()

#c2.cd(2)
#hist_VJets.Draw("HIST")

#c2.cd(3)

#hist_TTBar_Had.Draw("HIST")

#c2.cd(4)

#hist_ST.Draw("HIST")

#c2.cd(5)

#hist_TTBar_Semilep.Draw("HIST")

#c2.cd(6)

#hist_singleH.Draw("HIST")


#c2.cd(7)

#hist_VV.Draw("HIST")


#c2.cd(8)

#hist_QCD.Draw("HIST")


c3 = ROOT.TCanvas("c3", "Stacked contributions for jet1 after preselection", 800, 700)


# TODO Stacked histograms for Jet1


# temp1.Draw("HIST")
# temp1.SetTitle("Distribution of Jet1 discriminator")
# # temp1.SetLineColor(ROOT.kBlue+1)
# temp1.SetFillColorAlpha(ROOT.kAzure + 6, 0.8)
# legend.AddEntry(temp1, "QCD", "f")


# temp1.ResetStats()
# jet1 = temp1.GetEntries()
# print("jet1 entries count", jet1)


# temp2.Draw("SAME HIST")
# # temp2.SetLineColor(ROOT.kRed+4)
# temp2.SetFillColorAlpha(ROOT.kRed + 1, 0.8)
# legend.AddEntry(temp2, "Double V events", "f")


# temp3.Draw("SAME HIST")
# # temp3.SetLineColor(ROOT.kGreen+4)
# temp3.SetFillColorAlpha(ROOT.kGreen - 6, 0.8)
# legend.AddEntry(temp3, "single Higgs", "f")


# temp4.Draw("SAME HIST")
# # temp4.SetLineColor(ROOT.kBlue+2)
# temp4.SetFillColorAlpha(ROOT.kBlue - 8, 0.8)
# legend.AddEntry(temp4, "single top", "f")


# temp8.Draw("SAME HIST")
# # temp8.SetLineColor(ROOT.kRed+1)
# temp8.SetFillColorAlpha(ROOT.kAzure - 4, 0.8)
# legend.AddEntry(temp8, "semileptonic t tbar events", "f")

# temp5.Draw("SAME HIST")
# # temp5.SetLineColor(ROOT.kRed+1)
# temp5.SetFillColorAlpha(ROOT.kRed - 8, 0.8)
# legend.AddEntry(temp5, "hadronic t tbar events", "f")


# temp6.Draw("SAME HIST")
# # temp6.SetLineColor(ROOT.kGreen+2)
# temp6.SetFillColorAlpha(ROOT.kGreen - 8, 0.8)
# legend.AddEntry(temp6, "V + jets", "f")

# h1["signal"].Draw("SAME HIST")
# h1["signal"].Scale(10)
# h1["signal"].SetLineColor(ROOT.kBlack)
# h1["signal"].SetLineWidth(2)

# legend.AddEntry(h1["signal"], "signal x 10", "l")


# legend.Draw()


c2.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/QCD_pt_jet1.pdf"
)
# c3.SaveAs(
#     "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/2d_discr_test.pdf"
# )

