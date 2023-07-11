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
}

h1= {}
h2= {}
h_tot = {}
hist_sum = {}

histo_file = ROOT.TFile.Open("histograms_for_QCD_reshaping_2d_softdrop_0_86.root", "READ")

h1["QCD1"] = histo_file.Get("h2_2_QCD1")
h1["QCD2"] = histo_file.Get("h2_2_QCD2")
h1["QCD3"] = histo_file.Get("h2_2_QCD3")
h1["QCD4"] = histo_file.Get("h2_2_QCD4")
h1["QCD5"] = histo_file.Get("h2_2_QCD5")
h1["QCD6"] = histo_file.Get("h2_2_QCD6")
h1["QCD7"] = histo_file.Get("h2_2_QCD7")
h1["QCD8"] = histo_file.Get("h2_2_QCD8")

processes = list(h1.keys())


for i in processes:
    #* the value to normalize at the same integrated luminosity of the AN is 2.27
    h1[i].Scale(weights[i]*2.27)

hist_QCD = h1["QCD1"].Clone()
hist_QCD.Add(h1["QCD2"])
hist_QCD.Add(h1["QCD3"])
hist_QCD.Add(h1["QCD4"])
hist_QCD.Add(h1["QCD5"])
hist_QCD.Add(h1["QCD6"])
hist_QCD.Add(h1["QCD7"])
hist_QCD.Add(h1["QCD8"])

total = hist_QCD.Integral(1, 18, 1, 18)

mass_window = hist_QCD.Integral(7,8, 7,8)

ratio = mass_window/total

print(ratio)