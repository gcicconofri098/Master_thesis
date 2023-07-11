import ROOT
import os

ROOT.EnableImplicitMT()

entries1 ={}

df = {}
integrated_luminosity = 59830


weights = {
    "QCD1": 27990000* integrated_luminosity,
    "QCD2": 1712000 * integrated_luminosity, 
    "QCD3": 347700* integrated_luminosity, 
    "QCD4": 32100* integrated_luminosity, 
    "QCD5": 6831* integrated_luminosity, 
    "QCD6": 1207 * integrated_luminosity, 
    "QCD7": 119.9 * integrated_luminosity, 
    "QCD8": 25.24 * integrated_luminosity, 
    "WJets1": 315.2* integrated_luminosity, 
    "WJets2": 68.58 * integrated_luminosity, 
    "WJets3": 34.69 * integrated_luminosity, 
    "ZJets1": 145.3* integrated_luminosity, 
    "ZJets2": 34.29 * integrated_luminosity, 
    "ZJets3": 18.57 * integrated_luminosity, 
    "TTHad": 370.04 * integrated_luminosity, 
    "TTSemilept": 369.49* integrated_luminosity, 
    "ST_tw_antitop": 35.85 * integrated_luminosity, 
    "ST_tw_top": 35.85* integrated_luminosity, 
    "GGH": 9.60 * integrated_luminosity, 
    "VBFH": 2.20 * integrated_luminosity, 
    "ttH":  0.295 *integrated_luminosity,
    "WMinusH": 0.210 * integrated_luminosity, 
    "WPlusH": 0.331 * integrated_luminosity, 
    "ZH": 0.310 * integrated_luminosity, 
    "ggZH": 0.050 * integrated_luminosity, 
    "WW": 118.7* integrated_luminosity,
    "WZ": 47.2 * integrated_luminosity, 
    "ZZ": 16.52 * integrated_luminosity, 
    "signal": 0.01053 * integrated_luminosity
    }



files = {
        "QCD1": "/scratchnvme/cicco/QCD1/",
        "QCD2" : "/scratchnvme/cicco/QCD2/",
        "QCD3" : "/scratchnvme/cicco/QCD3/",
        "QCD4" : "/scratchnvme/cicco/QCD4/",
        "QCD5" : "/scratchnvme/cicco/QCD5/",
        "QCD6" : "/scratchnvme/cicco/QCD6/",
        "QCD7" : "/scratchnvme/cicco/QCD7/",
        "QCD8" : "/scratchnvme/cicco/QCD8/",
        "WJets1" : "/scratchnvme/cicco/WJets1/",
        "WJets2" : "/scratchnvme/cicco/WJets2/",
        "WJets3" : "/scratchnvme/cicco/WJets3/",
        "ZJets1" : "/scratchnvme/cicco/ZJets1/",
        "ZJets2" : "/scratchnvme/cicco/ZJets2/",
        "ZJets3" : "/scratchnvme/cicco/ZJets3/",
        "TTHad" : "/scratchnvme/cicco/TTHad/",
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
        "ZZ": "/scratchnvme/cicco/ZZ/",
        "signal": "/scratchnvme/cicco/signal/"
        }

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

    df[i] = df[i].Filter("HLT_PFJet500").Filter("HLT_PFHT1050").Filter("HLT_AK8PFJet360_TrimMass30").Filter("HLT_AK8PFJet380_TrimMass30").Filter("HLT_AK8PFJet400_TrimMass30").Filter("HLT_AK8PFHT800_TrimMass50").Filter("HLT_AK8PFHT750_TrimMass50")

    df[i] = df[i].Filter("nFatJet>=2")

    df[i] = df[i].Define("Events_Selection", "FatJet_pt > 300 && abs(FatJet_eta) < 2.4 && FatJet_msoftdrop > 50").Define("Final_selection", "Take(FatJet_msoftdrop, Events_Selection)")

    df[i] = df[i].Filter("Final_selection.size()>=2")



print("Finished selection")

ROOT.gStyle.SetOptStat(0)

hist_tot = {}

h_tot = {}


for i in processes:

    hist_tot[i] = df[i].Histo1D((str(i),str(i), 50, -100, 2000), "FatJet_msoftdrop")

    print("created histograms for: {}".format(i))

    h_tot[i] = hist_tot[i].GetValue()

    print("got values for histograms of: {}".format(i))


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
legend4 = ROOT.TLegend(0.59, 0.70, 0.71, 0.77)



total.SetFillColorAlpha(ROOT.kBlue -8, 0.8)
legend4.AddEntry(total, "background", "f")
total.Draw()


h_tot["signal"].SetLineColor(ROOT.kRed +2)
h_tot["signal"].SetLineWidth(2)
legend4.AddEntry(h_tot["signal"], "signal", "l")
h_tot["signal"].Draw("SAME")

c9.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/debug.pdf")
