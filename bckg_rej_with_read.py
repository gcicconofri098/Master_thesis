import ROOT
from decimal import *

ROOT.EnableImplicitMT()

getcontext().prec = 5

entries1 = {}

ROOT.gStyle.SetOptStat(0)


df = {}
hist_2d = {}
h2_2 = {}

h2_2 = {}

integrated_luminosity = 59830
dataset_events = {}
#pre_sel_bckg = 54156.40533685765  #fullsim 

#pre_sel_bckg =  54321.15330935305 #fullsim prima

pre_sel_bckg = 17996.85547287977  #flashsim

binx_n = 1
biny_n = 1

hist = ROOT.TH2F(
    "hist", "Background rejection map for the discriminator; Value of Jet1 discriminator; Value of Jet2 discriminator", 10, 0.95, 1, 10, 0.95, 1
)


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

histo_file = ROOT.TFile.Open("histograms_flashshim_QCD_and_signal.root", "READ") #flashsim

#histo_file = ROOT.TFile.Open("histograms_2d_discr_mass_window_QCD_for_reshape_fullsim.root", "READ") #fullsim

#QCD_file = ROOT.TFile.Open("histograms_for_QCD_reshaping_2d_discr_0_86.root", "READ") #obsolete, all the histograms are together 


# h2_2["QCD1"] = histo_file.Get("h2_2_QCD1")
# h2_2["QCD2"] = histo_file.Get("h2_2_QCD2")
# h2_2["QCD3"] = histo_file.Get("h2_2_QCD3")
# h2_2["QCD4"] = histo_file.Get("h2_2_QCD4")
# h2_2["QCD5"] = histo_file.Get("h2_2_QCD5")
h2_2["QCD6"] = histo_file.Get("h2_2_QCD6")
h2_2["QCD7"] = histo_file.Get("h2_2_QCD7")
h2_2["QCD8"] = histo_file.Get("h2_2_QCD8")

# h2_2["WJets1"] = histo_file.Get("h2_2_WJets1")
# h2_2["WJets2"] = histo_file.Get("h2_2_WJets2")
# h2_2["WJets3"] = histo_file.Get("h2_2_WJets3")


# h2_2["ZJets1"] = histo_file.Get("h2_2_ZJets1")
# h2_2["ZJets2"] = histo_file.Get("h2_2_ZJets2")
# h2_2["ZJets3"] = histo_file.Get("h2_2_ZJets3")


# h2_2["TTHad"] = histo_file.Get("h2_2_TTHad")

# h2_2["TTSemilept"] = histo_file.Get("h2_2_TTSemilept")


# h2_2["ST_tw_antitop"] = histo_file.Get("h2_2_ST_tw_antitop")



# h2_2["ST_tw_top"] = histo_file.Get("h2_2_ST_tw_top")



# h2_2["GGH"] = histo_file.Get("h2_2_GGH")


# h2_2["VBFH"] = histo_file.Get("h2_2_VBFH")

# h2_2["ttH"] = histo_file.Get("h2_2_ttH")


# h2_2["WMinusH"] = histo_file.Get("h2_2_WMinusH")


# h2_2["WPlusH"] = histo_file.Get("h2_2_WPlusH")


# h2_2["ZH"] = histo_file.Get("h2_2_ZH")


# h2_2["ggZH"] = histo_file.Get("h2_2_ggZH")


# h2_2["WW"] = histo_file.Get("h2_2_WW")

# h2_2["WZ"] = histo_file.Get("h2_2_WZ")


# h2_2["ZZ"] = histo_file.Get("h2_2_ZZ")
processes = list(h2_2.keys())


for i in processes:
    #* the value to normalize at the same integrated luminosity of the AN is 2.27

    h2_2[i].Scale(weights[i]*2.27)

print("finished selection")

hist2d_bckg = h2_2["QCD6"].Clone()
# hist2d_bckg.Add(h2_2["QCD2"])
# hist2d_bckg.Add(h2_2["QCD3"])
# hist2d_bckg.Add(h2_2["QCD4"])
# hist2d_bckg.Add(h2_2["QCD5"])
# hist2d_bckg.Add(h2_2["QCD6"])
hist2d_bckg.Add(h2_2["QCD7"])
hist2d_bckg.Add(h2_2["QCD8"])

#hist2d_bckg.Scale(0.035) #fullsim

hist2d_bckg.Scale(0.04) #flashsim

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

for binx in reversed(range(1, 11)):
    for biny in reversed(range(1, 11)):
        if binx>=biny:
            new_bckg = hist2d_bckg.Integral(binx, 10, biny, 10)

            print("binx", binx)
            print("biny", biny)

            new_bin_cont = 1- (Decimal(pre_sel_bckg)- Decimal(new_bckg))/Decimal(pre_sel_bckg)
            temp = Decimal(new_bin_cont)
            #print(temp)

            hist.SetBinContent(binx, biny, temp)


c1 = ROOT.TCanvas("c1", "Efficiency plot", 1500, 1000)
c1.SetGrid()
hist.Draw("text COLZ")
hist.SetTitle("Background efficiency for flashsim")

c2 = ROOT.TCanvas("c2", "plot", 1500, 1000)
c2.SetGrid()
hist2d_bckg.SetTitle("Background distribution for flashsim")
hist2d_bckg.Draw("text COLZ")


c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/flashsim_bckg_rej_num_QCD_corrected.root.png")

c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/flashsim_bckg_cont_2d_QCD_corrected.root.png")


output_file = ROOT.TFile.Open("flashsim_bckg_map_histo_QCD_corrected.root", "RECREATE")

output_file.WriteObject(hist2d_bckg, "bckg_QCD_corrected")





