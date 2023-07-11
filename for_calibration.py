import ROOT
import os
import numpy as np
from decimal import *


getcontext().prec = 3

module_path_1 = os.path.join(os.path.dirname(__file__), "utils.h")
module_path_2 = os.path.join(os.path.dirname(__file__), "fatjets_utils.h")


ROOT.gInterpreter.ProcessLine(f'#include "{module_path_1}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_2}"')


ROOT.gStyle.SetOptStat(0)

ROOT.EnableImplicitMT(10)


bckg_path = "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file_bckg.root"

sig_path = (
    "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file1.root"
)


df_bckg = ROOT.RDataFrame("MJets", bckg_path)

df_sig = ROOT.RDataFrame("MJets", sig_path)

df_bckg = (
    df_bckg
    .Define("Ratio_RecoGen", "Mfatjet_pt/MgenjetAK8_pt")
    .Define("Abs_eta", "abs(Mfatjet_eta)")
)



pt_bins = np.array([200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 3000], dtype="double")

eta_bins = np.array([0, 0.8, 1.6, 2.4, 3.8, 5.0],  dtype="double")

ratio_bins = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0], dtype="double")

print("About to create the 3D histogram")

histo = df_bckg.Histo3D(
    ("flash", "flashsim sample", 12, pt_bins, 5, eta_bins, 20, ratio_bins), "Mfatjet_pt", "Abs_eta", "Ratio_RecoGen"
)

c1 = ROOT.TCanvas("c1", "Ratio in function of reco pt and eta", 800, 700)

histo.Draw("LEGO2")

print("about to create the 2D histogram")

histo2d = df_bckg.Histo2D(
    ("flash", "flashsim sample", 12, pt_bins, 5, eta_bins), "Mfatjet_pt", "Mfatjet_eta"
)
histo2d.Reset()

hist_test = df_bckg.Histo2D(
    ("flash", "flashsim sample", 12, 0, 1 , 5, 0, 1), "Mfatjet_pt", "Mfatjet_eta"
)
hist_test.Reset()


# Calculate mean ratio for each bin
mean_ratios = []

for i in range(1, len(pt_bins)):
    for j in range(1, len(eta_bins)):
        bin_contents_values = []
        entries = 0
        print(f"doing bin pt{i}, eta {j}")
        for k in range(1, len(ratio_bins)):
            bin_content = histo.GetBinContent(i, j, k)* histo.GetZaxis().GetBinCenter(k)
            entries += histo.GetBinContent(i,j,k) 
            bin_contents_values.append(bin_content)
        if entries > 0:
            ratio = Decimal(sum(bin_contents_values))/Decimal(entries)
        else:
            ratio = 0
        histo2d.SetBinContent(i, j, ratio)
        hist_test.SetBinContent(i, j, ratio)

        mean_ratios.append(ratio)
mean_ratios = np.array(mean_ratios).reshape(len(pt_bins)-1, len(eta_bins)-1)


c2 = ROOT.TCanvas("c2", "Mean in function of reco pt and eta", 800, 700)

histo2d.Draw("COLZ text")


c3 = ROOT.TCanvas("c3", "Mean in function of reco pt and eta", 1000, 900)

pt_bins.astype(int)

#pt_bins_int = int(pt_bins)

for i in range(1, len(pt_bins)):
    hist_test.GetXaxis().SetBinLabel(i, str(pt_bins[i]))
hist_test.LabelsOption("R")

for j in range(1, len(eta_bins)):
    hist_test.GetYaxis().SetBinLabel(j, str(eta_bins[j]))


hist_test.Draw("COLZ text")
c3.Update()
# Print mean ratios
for i in range(0, len(pt_bins)-1): 
    for j in range(0, len(eta_bins)-1):
        print(f"Pt bin: {i}, Eta bin: {j}, Mean Ratio: {mean_ratios[i,j]}")

c2.SetLogy()
#dividere il reco per il rapporto per ogni bin in pt e eta 


c1.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/ratio_for_calibration.pdf"
)

c2.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/mean_for_calibration.pdf"
)

c3.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/scratch/test_mean_for_calibration.pdf"
)