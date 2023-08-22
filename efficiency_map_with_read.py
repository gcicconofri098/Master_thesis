import ROOT
import os
import numpy as np
from decimal import *

ROOT.EnableImplicitMT()

module_path = os.path.join(os.path.dirname(__file__), "utils.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')

getcontext().prec = 3

entries1 = {}

h2_2 = {}

integrated_luminosity = 59830
dataset_events = {}
pre_selection_signal = 0

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
    "signal": 0.01053 * integrated_luminosity,
}


histo_file = ROOT.TFile.Open("histograms_2d_discr_0_8_mass_window_no_discr_pres_no_veto_VBF_flashsim_corrected_n_events.root", "READ") #flashsim

#histo_file = ROOT.TFile.Open("signal_for_s_b_10_bins.root", "READ") #fullsim

h2_2["signal"] = histo_file.Get("h2_2_signal")


processes = list(h2_2.keys())

# print(h2_2['signal'].Integral())

for i in processes:
#     #* the value to normalize at the same integrated luminosity of the AN is 2.27

    h2_2[i].Scale(weights[i]*2.27)

print(h2_2['signal'].GetEntries())



#preselection_signal = 10.000867406513017*2.27 #flashsim
#preselection_signal = 10.22460045811286 *2.27 #flashsim no discriminator
#preselection_signal = 2.51770623 *2.27 #fullsim
#preselection_signal = 2.57837385 *2.27 #fullsim no discriminator

preselection_signal = 630 *2.27 #no preselection

print(preselection_signal)

hist_2 = h2_2['signal'].Clone()
hist_2.Reset()



for binx in reversed(range(1, 21)):
    for biny in reversed(range(1, 21)):
        if binx >= biny:
            stacked_sig = h2_2["signal"].Integral(binx, 20, biny, 20)
            print("stacked signal: ", stacked_sig)

            if stacked_sig > 0:
                new_bin_cont = Decimal(stacked_sig) / Decimal(preselection_signal)
                temp = Decimal(new_bin_cont)
                print(temp)
                hist_2.SetBinContent(binx, biny, temp)
            else:
                hist_2.SetBinContent(binx, biny, 0)

c1 = ROOT.TCanvas("c1", "plot", 4500, 3500)
c1.SetGrid()
h2_2['signal'].Draw("text COLZ")
h2_2['signal'].SetTitle("Distribution of signal for flashsim")
#h2_2['signal'].Scale(1/(h2_2['signal'].Integral()))


c2 = ROOT.TCanvas("c2", "Efficiency plot", 4500, 3500)
c2.SetGrid()
hist_2.Draw("text COLZ")
hist_2.SetTitle("Signal efficiency for flashsim")

c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/flashsim_discr_0_8_signal_2d_discr_mass_window_no_discr_pres_no_veto_VBF_corrected_n_events.png")


c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/flashsim_discr_0_8_efficiency_map_num_no_discr_pres_no_veto_VBF_corrected_n_events.png")

# output_file = ROOT.TFile.Open("efficiency_map_histo.root", "RECREATE")

# output_file.WriteObject(hist_2, "efficiency")