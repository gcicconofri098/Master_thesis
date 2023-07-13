import ROOT
import os
import numpy as np
from decimal import *

ROOT.EnableImplicitMT()

ROOT.gStyle.SetOptStat(0)

integrated_luminosity = 59830

getcontext().prec = 4

sig_file = ROOT.TFile.Open("histograms_flashshim_signal_10_bins.root", "READ")

signal = sig_file.Get("h2_2_signal")

signal.Scale(0.01053 * integrated_luminosity*2.27)

background_file = ROOT.TFile.Open("flashsim_bckg_map_histo_QCD_corrected.root", "READ")

background = background_file.Get("bckg_QCD_corrected")


hist = ROOT.TH2F(
    "hist", "S / #sqrt{B}; Value of Jet1 discriminator; Value of Jet2 discriminator", 10, 0.95, 1, 10, 0.95, 1
)

for binx in reversed(range(1, 11)):
    for biny in reversed(range(1, 11)):
        if binx >= biny:
            sig = ROOT.sqrt(signal.Integral(binx, 10, biny, 10))
            #sig= signal.GetBinContent(binx, biny)
            print("signal: ", sig)

            bckg = ROOT.sqrt(background.Integral(binx, 10, biny, 10))
            #bckg= background.GetBinContent(binx, biny)
            print("bckg: ", bckg)
            if bckg > 0:
                new_bin_cont = Decimal(sig) / Decimal(bckg)
                temp = Decimal(new_bin_cont)
                print(temp)
                hist.SetBinContent(binx, biny, temp)

c1 = ROOT.TCanvas("c1", "plot", 1500, 900)
c1.SetGrid()
hist.Draw("text COLZ")

c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/s_sqrt_b_flashsim_int.pdf")
