import ROOT


#ROOT.EnableImplicitMT()

df = {}
weights = {
    "QCD1": 1.521e-7,
    "QCD2": 1.697e-5, 
    "QCD3": 1.462e-6, 
    "QCD4": 0.00031, 
    "QCD5": 0.0013, 
    "QCD6": 0.0051, 
    "QCD7": 0.0039, 
    "QCD8": 0.2363, 
    "WJets1": 0.00097, 
    "WJets2": 0.0022, 
    "WJets3": 0.0665, 
    "ZJets1": 0.00166, 
    "ZJets2": 0.0871, 
    "ZJets3": 0.0223, 
    "TTHad": 0.0596, 
    "TTSemilept": 0.0585, 
    "ST_tw_antitop": 0.0014, 
    "ST_tw_top": 0.06154, 
    "GGH": 0.0139, 
    "VBFH": 0.0076, 
    "WMinusH": 4.77, 
    "WPlusH": 0.202, 
    "ttH": 23.57,
    "ZH": 30.42, 
    "ggZH": 11.365, 
    "WW": 0.0067,
    "WZ": 0.321, 
    "ZZ": 1.261, 
    "signal": 0.5841}


df["QCD1"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/01CD88A2-878C-6446-9D9C-70BFF7D9E19C.root")

df["QCD2"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/01597A4E-6C68-B94C-90AA-45D8FAAB3E1E.root")

df["QCD3"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/0BADC302-9E0D-D04B-B1AC-537CC5540912.root")


df["QCD4"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/018FEA95-9E8E-214A-A020-7F55DC78B203.root")

df["QCD5"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/150F2AD2-0267-AE4F-90F9-D8191F29DC95.root")

df["QCD6"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/723E5B2D-0AF1-0D44-9D3F-3CE358680F9D.root")

df["QCD7"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/4BFB898A-D75F-424E-9796-39C2DB42F6F2.root")

df["QCD8"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/43A4A5EB-37B1-CA49-AF30-752C43FC828F.root")

df["WJets1"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/3233BD62-0A6C-1A4B-BB9B-14CC03C2AE1D.root")

df["WJets2"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/04CF847A-DA06-4849-82F3-34F4A86B4241.root")

df["WJets3"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/0760B6BD-F18E-084D-8E42-AD9F8A467F71.root")

df["ZJets1"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/B4FB8465-14B1-0449-9C14-DD2CD637D2DE.root")

df["ZJets2"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/22CD330D-3CD3-C642-923B-18EA67086FE3.root")

df["ZJets3"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/05B8CD6E-B303-A544-A285-5F2FFB47D5DC.root")

df["TTHad"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/0307C1DA-E49C-AB4B-9179-C70BE232321E.root")

df["TTSemilept"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/0520A050-AF68-EF43-AA5B-5AA77C74ED73.root")

df["ST_tw_antitop"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/6371B801-DE75-5B4B-A781-98523A058E30.root")

df["ST_tw_top"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/60FB6FDE-25EA-6C4E-80E5-96ED7EF8C294.root")

df["GGH"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/010C2B15-1748-D34C-AE93-66E0864A2E54.root")

df["VBFH"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/04A5B8B1-C004-9247-97F8-EE9274C7DB51.root")

df["WMinusH"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/7A64C23A-88F1-3948-8DBE-5CC68396199B.root")

df["WPlusH"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/16EFFFE4-67DB-364F-90DD-A082DCF9CC81.root")

df["ttH"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/19922B78-283B-CD48-8A3D-0308D48A824A.root")

df["ZH"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/FC08EB31-9A28-0842-A01F-F6E482777701.root")

df["ggZH"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/055A8936-10B9-D041-AD4C-4D8A3762F95E.root")

df["WW"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/A9859A3B-138E-0B45-A60E-A26B2E7CE4FD.root")

df["WZ"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/0D38D325-67C1-2748-8678-C0C48FD151C4.root")

df["ZZ"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/29E7B7EF-D0FD-7343-9437-5C4F253A7B49.root")

df["signal"] = ROOT.RDataFrame("Events", "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/4A33603E-8E8E-9C40-8086-C3345E752BE0.root")

processes = list(df.keys())

print(processes)

#df["signal"].Display("FatJet_pt").Print()

for i in processes:

    print("Begin selection: {}".format(i))

   
    df[i] = df[i].Filter("HLT_PFJet500").Filter("HLT_PFHT1050").Filter("HLT_AK8PFJet360_TrimMass30").Filter("HLT_AK8PFJet380_TrimMass30").Filter("HLT_AK8PFJet400_TrimMass30").Filter("HLT_AK8PFHT800_TrimMass50").Filter("HLT_AK8PFHT750_TrimMass50") #.Filter("HLT_AK8PFJet330_PFAK8BTagCSV_p17 || HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17")

    #df[i] = df[i].Define("First_sel", "nFatJet>=2 && FatJet_pt > 300").Define("Preselected_mass", "FatJet_msoftdrop[First_sel]")

    df[i] = df[i].Filter("nFatJet>=2")

    df[i] = df[i].Define("Events_Selection", "FatJet_pt > 300 && abs(FatJet_eta) < 2.4 && 80 < FatJet_msoftdrop && FatJet_msoftdrop < 170").Define("Selected_mass", "FatJet_deepTagMD_HbbvsQCD[Events_Selection]")



    df[i] = df[i].Filter("Selected_mass.size()>=2")
    df[i] = df[i].Define("sorted_FatJet_deepTagMD_HbbvsQCD", "Reverse(Argsort(Selected_mass))").Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]").Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
    
    df[i] = df[i].Filter("FatJet_deepTagMD_HbbvsQCD[Jet1_index]>0.95 && FatJet_deepTagMD_HbbvsQCD[Jet2_index]>0.85") #fat[0] is Jet1 and fat[1] is Jet2


    df[i] = df[i].Define("Jet1_selected_mass", "Selected_mass[Jet1_index]").Define("Jet2_selected_mass", "Selected_mass[Jet2_index]")



# c1 = ROOT.TCanvas("c1", "Histogram", 1000, 900)




# hs = ROOT.THStack()
# QCD_bckg = ROOT.THStack()
# VJets = ROOT.THStack()
# TTbar = ROOT.THStack()
# STop = ROOT.THStack()
# VV = ROOT.THStack()
# singleH = ROOT.THStack()
# signal = ROOT.THStack()

# legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)



#c1.Divide(6,5)






#legend.Draw()

#c2 = ROOT.TCanvas("c2", "Stacked Histograms", 800, 700)


#per fare simil thstack fare la somma degli hist dello stesso tipo e poi fare dei grafici temp printati assieme in cui 
#gli hist sono sommati ma con il secondo temp che contiene un grafico in meno in modo same, fino all'ultimo che ne contiene uno solo



# for i in processes:

#     print(str(i))
#     hist[i] = df[i].Histo1D(("","", 50, 0, 400), "Selected_mass")


    # if "QCD" in str(i):
        
    #     print("QCD dataset")

    #     hist[i].SetLineColor(ROOT.kRed+2)
    #     print("linecolor")
    #     #h1[i].SetLineWidth(3)
    #     hist[i].SetFillColor(ROOT.kRed-9)
    #     print("fillcolor")
    #     #h1[i].SetFillStyle(ROOT.kFDotted3)

    #     #h1[i] = hist[i].GetPtr()
    #     h1[i] = hist[i].GetValue()


    #     print("getvalue")
    #     QCD_bckg.Add(h1[i])
    #     print("add")
    #     legend.AddEntry(QCD_bckg, "QCD", "f")
    #     print("legend")
    #     print("completed hist")

    # elif "Jets" in str(i):
    #     print("V jet event")

    #     hist[i].SetLineColor(ROOT.kBlue+2)
    #     #h1[i].SetLineWidth(3)
    #     hist[i].SetFillColor(ROOT.kBlue-9)
    #     #h1[i].SetFillStyle(ROOT.kFDotted3)
    #     h1[i] = hist[i].GetValue()
    #     VJets.Add(h1[i])
    #     legend.AddEntry(VJets, "W+jets, Z +jets", "f")
        
    #     print("completed hist")


    # elif str(i)=="TTHad" or str(i) =="TTSemilept":

    #     print("ttbar event")
        
    #     hist[i].SetLineColor(ROOT.kGreen+2)
    #     #h1[i].SetLineWidth(3)
    #     hist[i].SetFillColor(ROOT.kGreen-9)
    #     #h1[i].SetFillStyle(ROOT.kFDotted3)
    #     h1[i] = hist[i].GetValue()
    #     TTbar.Add(h1[i])
    #     legend.AddEntry(TTbar, "T Tbar events", "f")

    #     print("completed hist")


    # elif "ST" in str(i):

    #     print("single top")

    #     hist[i].SetLineColor(ROOT.kCyan+2)
    #     #h1[i].SetLineWidth(3)
    #     hist[i].SetFillColor(ROOT.kCyan-9)
    #     #h1[i].SetFillStyle(ROOT.kFDotted3)
    #     h1[i] = hist[i].GetValue()
    #     STop.Add(h1[i])

    #     legend.AddEntry(STop, "Single top events", "f")

    #     print("completed hist")
    

    # elif str(i) == "ZZ" or str(i) == "WW" or str(i) == "WZ":

    #     print("VV")

        
    #     hist[i].SetLineColor(ROOT.kBlue+4)
    #     #h1[i].SetLineWidth(3)
    #     hist[i].SetFillColor(ROOT.kBlue-6)
    #     #h1[i].SetFillStyle(ROOT.kFDotted3)
    #     h1[i] = hist[i].GetValue()
    #     VV.Add(h1[i])
        
    #     legend.AddEntry(VV, "Double Vector boson", "f")
    

    #     print("completed hist")

    # elif (str(i) == "signal"):

    #     print("signal")

    #     hist[i].SetLineColor(ROOT.kRed+4)
    #     #h1[i].SetLineWidth(3)
    #     hist[i].SetFillColor(ROOT.kRed-6)
    #     #h1[i].SetFillStyle(ROOT.kFDotted3)
    #     h1[i] = hist[i].GetValue()
    #     signal.Add(h1[i])
        
    #     legend.AddEntry(signal, "signal", "f")
    

    #     print("completed hist")

    # else:

    #     print("single Higgs")

    #     hist[i].SetLineColor(ROOT.kGreen+4)
    #     #h1[i].SetLineWidth(3)
    #     hist[i].SetFillColor(ROOT.kGreen-6)
    #     #h1[i].SetFillStyle(ROOT.kFDotted3)
    #     h1[i] = hist[i].GetValue()
    #     singleH.Add(h1[i]) 

    #     legend.AddEntry(singleH, "sigle H", "f")

    #     print("completed hist")
    

ROOT.gStyle.SetOptStat(0)

hist1 = {}
hist2 = {}
histo2d = {}
hist_tot = {}

h1 = {}
h2 = {}
h2_2 = {}
h_tot = {}

n_events = 0

for i in processes:

    
    hist1[i] = df[i].Histo1D((str(i),str(i), 50, 0, 1.1), "Jet1_selected_mass")
    hist2[i] = df[i].Histo1D((str(i),str(i), 50, 0, 1.1), "Jet2_selected_mass")
    hist_tot[i] = df[i].Histo1D((str(i),str(i), 50, 0, 1.1), "Selected_mass")

    histo2d[i] = df[i].Histo2D(("Jet1 vs Jet2", "Jet1 vs Jet2; Jet1; Jet2", 30, 0, 1.02, 30, 0, 1.02), "Jet1_selected_mass", "Jet2_selected_mass")

    h1[i]= hist1[i].GetValue()
    h2[i]= hist2[i].GetValue()
    h2_2[i] =histo2d[i].GetValue()
    h_tot[i] = hist_tot[i].GetValue()

    if str(i) != "signal":

        n_events = n_events + h_tot[i].GetEntries()
    else:
        print("Number of signal events: {}".format(h_tot[i].GetEntries()))

    print("Number of background events: {}".format(n_events))

    h1[i].Scale(weights[i])
    h2[i].Scale(weights[i])
    histo2d[i].Scale(weights[i])
    h_tot[i].Scale(weights[i])


#! Jet1

hist_QCD=None
hist_VJets= None
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


hist_TTBar = h1["TTHad"].Clone()
hist_TTBar.Add(h1["TTSemilept"])

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



c1 = ROOT.TCanvas("c1", "Stacked Histograms", 800, 700)
legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


c1.Divide(3,3)



c1.cd(7)

temp7 = h1["signal"].Clone()

print(type(temp7))

temp7.Draw("HIST")
temp7.SetLineColor(ROOT.kCyan+4)
temp7.SetFillColorAlpha(ROOT.kCyan-6, 0.4)



c1.cd(6)

temp6 = h1["signal"].Clone()

print(type(temp6))
temp6.Add(hist_VJets)


temp6.Draw("HIST")
temp6.SetLineColor(ROOT.kGreen+2)
temp6.SetFillColorAlpha(ROOT.kGreen-8, 0.4)


print(type(temp6))


c1.cd(5)

temp5 = h1["signal"].Clone()
temp5.Add(hist_VJets)
temp5.Add(hist_TTBar)


temp5.Draw("HIST")
temp5.SetLineColor(ROOT.kRed+2)
temp5.SetFillColorAlpha(ROOT.kRed-8, 0.4)



c1.cd(4)

temp4 = h1["signal"].Clone()
temp4.Add(hist_VJets)
temp4.Add(hist_TTBar)
temp4.Add(hist_ST)



temp4.Draw("HIST")
temp4.SetLineColor(ROOT.kBlue+2)
temp4.SetFillColorAlpha(ROOT.kBlue-8, 0.4)




c1.cd(3)

temp3 = h1["signal"].Clone()
temp3.Add(hist_VJets)
temp3.Add(hist_TTBar)
temp3.Add(hist_ST)
temp3.Add(hist_singleH)


temp3.Draw("HIST")
temp3.SetLineColor(ROOT.kGreen+4)
temp3.SetFillColorAlpha(ROOT.kGreen-6, 0.4)





c1.cd(2)

temp2 = h1["signal"].Clone()
temp2.Add(hist_VJets)
temp2.Add(hist_TTBar)
temp2.Add(hist_ST)
temp2.Add(hist_singleH)
temp2.Add(hist_VV)



temp2.Draw("HIST")
temp2.SetLineColor(ROOT.kRed+4)
temp2.SetFillColorAlpha(ROOT.kRed-6, 0.4)



c1.cd(1)

temp1 = h1["signal"].Clone()
temp1.Add(hist_VJets)
temp1.Add(hist_TTBar)
temp1.Add(hist_ST)
temp1.Add(hist_singleH)
temp1.Add(hist_VV)
temp1.Add(hist_QCD)


temp1.Draw("HIST")
temp1.SetLineColor(ROOT.kBlue+4)
temp1.SetFillColorAlpha(ROOT.kBlue-6, 0.4)

# temp1=h1["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH).Add(hist_VV).Add(hist_QCD)
# temp2=h1["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH).Add(hist_VV)
# temp3=h1["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH)
# temp4=h1["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST)
# temp5=h1["signal"].Clone().Add(hist_VJets).Add(hist_TTBar)
# temp6=h1["signal"].Clone().Add(hist_VJets)
# temp7=h1["signal"].Clone()


c2 = ROOT.TCanvas("c2", "", 800, 700)


c2.Divide(3,3)

c2.cd(1)

h1["signal"].Draw("HIST")

c2.cd(2)

hist_VJets.Draw("HIST")

c2.cd(3)

hist_TTBar.Draw("HIST")

c2.cd(4)

hist_ST.Draw("HIST")

c2.cd(5)

hist_singleH.Draw("HIST")

c2.cd(6)

hist_VV.Draw("HIST")

c2.cd(7)

hist_QCD.Draw("HIST")




c3 = ROOT.TCanvas("c3", "", 800, 700)

temp1.Draw("HIST")
temp1.SetLineColor(ROOT.kBlue+4)
temp1.SetFillColorAlpha(ROOT.kBlue-6, 0.4)
legend.AddEntry(temp1,"QCD", "f")


temp2.Draw("SAME HIST")
temp2.SetLineColor(ROOT.kRed+4)
temp2.SetFillColorAlpha(ROOT.kRed-6, 0.4)
legend.AddEntry(temp2,"Double V events", "f")



temp3.Draw("SAME HIST")
temp3.SetLineColor(ROOT.kGreen+4)
temp3.SetFillColorAlpha(ROOT.kGreen-6, 0.4)
legend.AddEntry(temp3,"single Higgs", "f")


temp4.Draw("SAME HIST")
temp4.SetLineColor(ROOT.kBlue+2)
temp4.SetFillColorAlpha(ROOT.kBlue-8, 0.4)
legend.AddEntry(temp4,"single top", "f")


temp5.Draw("SAME HIST")
temp5.SetLineColor(ROOT.kRed+2)
temp5.SetFillColorAlpha(ROOT.kRed-8, 0.4)
legend.AddEntry(temp5,"t tbar events", "f")

temp6.Draw("SAME HIST")

temp6.SetLineColor(ROOT.kGreen+2)
temp6.SetFillColorAlpha(ROOT.kGreen-8, 0.4)
legend.AddEntry(temp6,"V + jets", "f")


temp7.Draw("SAME HIST")
temp7.SetLineColor(ROOT.kCyan+4)
temp7.SetFillColorAlpha(ROOT.kCyan-6, 0.4)
legend.AddEntry(temp7,"signal", "f")


legend.Draw()

#! Jet2


hist_QCD_2=None
hist_VJets_2= None
hist_TTBar_2 = None
hist_ST_2 = None
hist_singleH_2 = None
hist_VV = None


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


hist_TTBar_2 = h2["TTHad"].Clone()
hist_TTBar_2.Add(h2["TTSemilept"])

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



c4 = ROOT.TCanvas("c4", "Stacked Histograms", 800, 700)
legend2 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


c4.Divide(3,3)



c4.cd(7)

temp7_2 = h2["signal"].Clone()

print(type(temp7_2))

temp7_2.Draw("HIST")
temp7_2.SetLineColor(ROOT.kCyan+4)
temp7_2.SetFillColorAlpha(ROOT.kCyan-6, 0.4)



c4.cd(6)

temp6_2 = h2["signal"].Clone()

print(type(temp6_2))
temp6_2.Add(hist_VJets_2)


temp6_2.Draw("HIST")
temp6_2.SetLineColor(ROOT.kGreen+2)
temp6_2.SetFillColorAlpha(ROOT.kGreen-8, 0.4)


print(type(temp6_2))


c4.cd(5)

temp5_2 = h2["signal"].Clone()
temp5_2.Add(hist_VJets_2)
temp5_2.Add(hist_TTBar_2)


temp5_2.Draw("HIST")
temp5_2.SetLineColor(ROOT.kRed+2)
temp5_2.SetFillColorAlpha(ROOT.kRed-8, 0.4)



c4.cd(4)

temp4_2 = h2["signal"].Clone()
temp4_2.Add(hist_VJets_2)
temp4_2.Add(hist_TTBar_2)
temp4_2.Add(hist_ST_2)



temp4_2.Draw("HIST")
temp4_2.SetLineColor(ROOT.kBlue+2)
temp4_2.SetFillColorAlpha(ROOT.kBlue-8, 0.4)




c4.cd(3)

temp3_2 = h2["signal"].Clone()
temp3_2.Add(hist_VJets_2)
temp3_2.Add(hist_TTBar_2)
temp3_2.Add(hist_ST_2)
temp3_2.Add(hist_singleH_2)


temp3_2.Draw("HIST")
temp3_2.SetLineColor(ROOT.kGreen+4)
temp3_2.SetFillColorAlpha(ROOT.kGreen-6, 0.4)





c4.cd(2)

temp2_2 = h2["signal"].Clone()
temp2_2.Add(hist_VJets_2)
temp2_2.Add(hist_TTBar_2)
temp2_2.Add(hist_ST_2)
temp2_2.Add(hist_singleH_2)
temp2_2.Add(hist_VV_2)



temp2_2.Draw("HIST")
temp2_2.SetLineColor(ROOT.kRed+4)
temp2_2.SetFillColorAlpha(ROOT.kRed-6, 0.4)



c4.cd(1)

temp1_2 = h2["signal"].Clone()
temp1_2.Add(hist_VJets_2)
temp1_2.Add(hist_TTBar_2)
temp1_2.Add(hist_ST_2)
temp1_2.Add(hist_singleH_2)
temp1_2.Add(hist_VV_2)
temp1_2.Add(hist_QCD_2)


temp1_2.Draw("HIST")
temp1_2.SetLineColor(ROOT.kBlue+4)
temp1_2.SetFillColorAlpha(ROOT.kBlue-6, 0.4)

# temp1=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH).Add(hist_VV).Add(hist_QCD)
# temp2=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH).Add(hist_VV)
# temp3=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST).Add(hist_singleH)
# temp4=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar).Add(hist_ST)
# temp5=h2["signal"].Clone().Add(hist_VJets).Add(hist_TTBar)
# temp6=h2["signal"].Clone().Add(hist_VJets)
# temp7=h2["signal"].Clone()


c5 = ROOT.TCanvas("c5", "", 800, 700)


c5.Divide(3,3)

c5.cd(1)

h2["signal"].Draw("HIST")

c5.cd(2)

hist_VJets_2.Draw("HIST")

c5.cd(3)

hist_TTBar_2.Draw("HIST")

c5.cd(4)

hist_ST_2.Draw("HIST")

c5.cd(5)

hist_singleH_2.Draw("HIST")

c5.cd(6)

hist_VV_2.Draw("HIST")

c5.cd(7)

hist_QCD_2.Draw("HIST")




c6 = ROOT.TCanvas("c6", "", 800, 700)

temp1_2.Draw("HIST")
temp1_2.SetLineColor(ROOT.kBlue+4)
temp1_2.SetFillColorAlpha(ROOT.kBlue-6, 0.4)
legend2.AddEntry(temp1_2,"QCD", "f")


temp2_2.Draw("SAME HIST")
temp2_2.SetLineColor(ROOT.kRed+4)
temp2_2.SetFillColorAlpha(ROOT.kRed-6, 0.4)
legend2.AddEntry(temp2_2,"Double V events", "f")



temp3_2.Draw("SAME HIST")
temp3_2.SetLineColor(ROOT.kGreen+4)
temp3_2.SetFillColorAlpha(ROOT.kGreen-6, 0.4)
legend2.AddEntry(temp3_2,"single Higgs", "f")


temp4_2.Draw("SAME HIST")
temp4_2.SetLineColor(ROOT.kBlue+2)
temp4_2.SetFillColorAlpha(ROOT.kBlue-8, 0.4)
legend2.AddEntry(temp4_2,"single top", "f")


temp5_2.Draw("SAME HIST")
temp5_2.SetLineColor(ROOT.kRed+2)
temp5_2.SetFillColorAlpha(ROOT.kRed-8, 0.4)
legend2.AddEntry(temp5_2,"t tbar events", "f")

temp6_2.Draw("SAME HIST")

temp6_2.SetLineColor(ROOT.kGreen+2)
temp6_2.SetFillColorAlpha(ROOT.kGreen-8, 0.4)
legend2.AddEntry(temp6_2,"V + jets", "f")


temp7_2.Draw("SAME HIST")
temp7_2.SetLineColor(ROOT.kCyan+4)
temp7_2.SetFillColorAlpha(ROOT.kCyan-6, 0.4)
legend2.AddEntry(temp7_2,"signal", "f")


legend2.Draw()

c7 = ROOT.TCanvas("c7", "2d histo", 800, 700)

c7.Divide(2,2)

hist2d_bckg = h2_2["QCD1"].Clone()
hist2d_bckg.Add(h2_2["QCD2"])
hist2d_bckg.Add(h2_2["QCD3"])
hist2d_bckg.Add(h2_2["QCD4"])
hist2d_bckg.Add(h2_2["QCD5"])
hist2d_bckg.Add(h2_2["QCD6"])
hist2d_bckg.Add(h2_2["QCD7"])
hist2d_bckg.Add(h2_2["QCD8"])


hist2d_bckg.Add(h2_2["WJets1"])
hist2d_bckg.Add(h2_2["WJets2"])
hist2d_bckg.Add(h2_2["WJets3"])
hist2d_bckg.Add(h2_2["ZJets1"])
hist2d_bckg.Add(h2_2["ZJets2"])
hist2d_bckg.Add(h2_2["ZJets3"])


hist2d_bckg.Add(h2_2["TTHad"])
hist2d_bckg.Add(h2_2["TTSemilept"])

hist2d_bckg.Add(h2_2["ST_tw_antitop"])
hist2d_bckg.Add(h2_2["ST_tw_top"])

hist2d_bckg.Add(h2_2["GGH"])
hist2d_bckg.Add(h2_2["VBFH"])
hist2d_bckg.Add(h2_2["WMinusH"])
hist2d_bckg.Add(h2_2["WPlusH"])
hist2d_bckg.Add(h2_2["ZH"])
hist2d_bckg.Add(h2_2["ggZH"])

hist2d_bckg.Add(h2_2["WZ"])
hist2d_bckg.Add(h2_2["ZZ"])
hist2d_bckg.Add(h2_2["WW"])

c7.cd(1)
hist2d_bckg.Draw("COLZ")


c7.cd(4)
histo2d["signal"].Draw("COLZ")

c8 = ROOT.TCanvas("c8", "Jet1 vs Jet2", 800, 700)
#c8.SetLogy(1)
legend3 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


max = temp1_2.GetMaximum() + 50

temp1.Draw("HIST")
legend3.AddEntry(temp1, "Jet 1 bckg", "l")
temp1.SetLineColor(ROOT.kBlack)
temp1.SetLineWidth(3)
temp1.SetLineStyle(2)
temp1.SetMaximum(max)
temp1.ResetAttFill()


temp1_2.Draw("SAME HIST")
legend3.AddEntry(temp1_2, "Jet 2 bckg", "l")
temp1_2.SetLineColor(ROOT.kRed +2)
temp1_2.SetLineWidth(3)
temp1_2.SetLineStyle(2)
temp1_2.ResetAttFill()


h1["signal"].Draw("SAME HIST")
legend3.AddEntry(h1["signal"], "Jet 1 signal", "l")
h1["signal"].SetLineColor(ROOT.kBlack)
h1["signal"].SetLineWidth(2)
#h1["signal"].SetFillColorAlpha(0, 0)

h2["signal"].Draw("SAME HIST")
legend3.AddEntry(h2["signal"], "Jet 2 signal", "l")
h2["signal"].SetLineColor(ROOT.kRed +2)
h2["signal"].SetLineWidth(2)
#h2["signal"].SetFillColorAlpha(0, 0)

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

total.Add(h_tot["WJets1"])
total.Add(h_tot["WJets2"])
total.Add(h_tot["WJets3"])
total.Add(h_tot["ZJets1"])
total.Add(h_tot["ZJets2"])
total.Add(h_tot["ZJets3"])


total.Add(h_tot["TTHad"])
total.Add(h_tot["TTSemilept"])

total.Add(h_tot["ST_tw_antitop"])
total.Add(h_tot["ST_tw_top"])

total.Add(h_tot["GGH"])
total.Add(h_tot["VBFH"])
total.Add(h_tot["WMinusH"])
total.Add(h_tot["WPlusH"])
total.Add(h_tot["ZH"])
total.Add(h_tot["ggZH"])
total.Add(h_tot["ttH"])

total.Add(h_tot["WZ"])
total.Add(h_tot["ZZ"])
total.Add(h_tot["WW"])



c9 = ROOT.TCanvas("c9", "Signal to bckg", 900, 800)
#legend4 = ROOT.TLegend(0.59, 0.70, 0.71, 0.77)



total.SetFillColorAlpha(ROOT.kBlue -8, 0.4)
#legend4.AddEntry(total, "background", "f")


total.Draw("HIST AL*")

h_tot["signal"].SetLineColor(ROOT.kRed +2)
h_tot["signal"].SetLineWidth(2)
#legend4.AddEntry(h_tot["signal"], "signal", "l")
h_tot["signal"].SetTitle("Signal Jet1 vs Jet2 discriminator; Jet 1; Jet2")
h_tot["signal"].Draw("SAME HIST AL*")



#legend4.Draw()

#ROOT.gPad.SetLogy(1)

c2.SaveAs("processes_jet1.pdf")
c1.SaveAs("unstacked_jet1.pdf")
c3.SaveAs("stacked_jet1.pdf")
c7.SaveAs("jet1_vs_jet2_2d.pdf")
c8.SaveAs("jet1_vs_jet2.pdf")
c9.SaveAs("sig_to_bckg.pdf")