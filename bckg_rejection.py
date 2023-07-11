import ROOT
import os
import numpy as np
from decimal import *

ROOT.EnableImplicitMT()

getcontext().prec = 4

entries1 = {}

df = {}
hist_2d = {}
h2_2 = {}

integrated_luminosity = 59830
dataset_events = {}
pre_sel_bckg = 0

binx_n = 1
biny_n = 1

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
}


files = {
    "QCD1": "/scratchnvme/cicco/QCD1/",
    "QCD2": "/scratchnvme/cicco/QCD2/",
    "QCD3": "/scratchnvme/cicco/QCD3/",
    "QCD4": "/scratchnvme/cicco/QCD4/",
    "QCD5": "/scratchnvme/cicco/QCD5/",
    "QCD6": "/scratchnvme/cicco/QCD6/",
    "QCD7": "/scratchnvme/cicco/QCD7/",
    "QCD8": "/scratchnvme/cicco/QCD8/",
    "WJets1": "/scratchnvme/cicco/WJets1/",
    "WJets2": "/scratchnvme/cicco/WJets2/",
    "WJets3": "/scratchnvme/cicco/WJets3/",
    "ZJets1": "/scratchnvme/cicco/ZJets1/",
    "ZJets2": "/scratchnvme/cicco/ZJets2/",
    "ZJets3": "/scratchnvme/cicco/ZJets3/",
    "TTHad": "/scratchnvme/cicco/TTHad/",
    "TTSemilept": "/scratchnvme/cicco/TTSemilept/",
    "ST_tw_antitop": "/scratchnvme/cicco/ST_tw_antitop/",
    "ST_tw_top": "/scratchnvme/cicco/ST_tw_top/",
    "GGH": "/scratchnvme/cicco/GGH/",
    "VBFH": "/scratchnvme/cicco/VBFH/",
    "ttH": "/scratchnvme/cicco/ttH/",
    "WMinusH": "/scratchnvme/cicco/WMinusH/",
    "WPlusH": "/scratchnvme/cicco/WPlusH/",
    "ZH": "/scratchnvme/cicco/ZH/",
    "ggZH": "/scratchnvme/cicco/ggZH/",
    "WW": "/scratchnvme/cicco/WW/",
    "WZ": "/scratchnvme/cicco/WZ/",
    "ZZ": "/scratchnvme/cicco/ZZ/"
}

ROOT.gStyle.SetOptStat(0)

hist = ROOT.TH2F(
    "hist", "Background rejection map for the discriminator; Value of Jet1 discriminator; Value of Jet2 discriminator", 20, 0, 1, 20, 0, 1
)

processes = list(files.keys())

for i in processes:
    f = os.listdir(files.get(i))
    num = len(f)
    print(num)
    entries1[i] = []

    for j in range(0, num):
        entries1[i].append(str(files.get(i)) + str(f[j]))

    df[i] = ROOT.RDataFrame("Events", entries1[i])

    print("added file to: {}".format(i))


print(processes)


for i in processes:

    print("Begin selection: {}".format(i))
    dataset_events[i] = df[i].Count().GetValue()

    weights[i] = weights[i] / dataset_events[i]

    df[i] = (
        df[i]
        .Filter("HLT_PFJet500")
        .Filter("HLT_PFHT1050")
        .Filter("HLT_AK8PFJet360_TrimMass30")
        .Filter("HLT_AK8PFJet380_TrimMass30")
        .Filter("HLT_AK8PFJet400_TrimMass30")
        .Filter("HLT_AK8PFHT800_TrimMass50")
        .Filter("HLT_AK8PFHT750_TrimMass50")
    )  # .Filter("HLT_AK8PFJet330_PFAK8BTagCSV_p17 || HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17")

    df[i] = df[i].Filter("nFatJet>=2")

    df[i] = (
        df[i]
        .Define(
            "Events_Selection",
            "FatJet_pt > 300 && abs(FatJet_eta) < 2.4",
        )
        .Define("Selected_jets", "FatJet_deepTagMD_HbbvsQCD[Events_Selection]")
        .Define("Softdrop_sel_jets", "FatJet_msoftdrop[Events_Selection]")

    )

    df[i] = df[i].Filter("Selected_jets.size()>=2")

    pre_sel_bckg = pre_sel_bckg +  df[i].Count().GetValue()*weights[i]

    df[i] = (
        df[i]
        .Define("sorted_FatJet_deepTagMD_HbbvsQCD", "Reverse(Argsort(Selected_jets))")
        .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
        .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
        .Define("Jet1_selected", "Selected_jets[Jet1_index]")
        .Define("Jet2_selected", "Selected_jets[Jet2_index]")
    )

    df[i] = df[i].Filter("Softdrop_sel_jets[Jet1_index]>50 && Softdrop_sel_jets[Jet2_index]>50")

    hist_2d[i] = df[i].Histo2D(
        ("Jet1 vs Jet2", "Jet1 vs Jet2; Jet1; Jet2", 20, 0, 1, 20, 0, 1),
        "Jet1_selected",
        "Jet2_selected",
    )

    h2_2[i] = hist_2d[i].GetValue()

    h2_2[i].Scale(weights[i])

print("finished selection")

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

for binx in reversed(range(1, 21)):
    for biny in reversed(range(1, 21)):
        if binx>=biny:
            new_bckg = hist2d_bckg.Integral(binx, 20, biny, 20)

            print("binx", binx)
            print("biny", biny)

            if new_bckg>0:
                new_bin_cont = (Decimal(pre_sel_bckg)- Decimal(new_bckg))/Decimal(pre_sel_bckg)
                print(new_bin_cont)
                hist.SetBinContent(binx, biny, new_bin_cont)






c1 = ROOT.TCanvas("c1", "Efficiency plot", 800, 700)
c1.SetGrid()
hist.Draw("text COLZ")

c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/bckg_rej_num.pdf")
