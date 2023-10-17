import ROOT
import os
import numpy as np
from decimal import *


getcontext().prec = 3

module_path_1 = os.path.join(os.path.dirname(__file__), "utils.h")
module_path_2 = os.path.join(os.path.dirname(__file__), "fatjets_utils.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_calibration.h")


ROOT.gInterpreter.ProcessLine(f'#include "{module_path_1}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_2}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')


ROOT.gStyle.SetOptStat(0)

ROOT.EnableImplicitMT(10)

files = {
    "QCD4": "/scratchnvme/cicco/QCD4_good_flash/",
    "QCD5": "/scratchnvme/cicco/QCD5_good_flash/",
    "QCD6": "/scratchnvme/cicco/QCD6_good_flash/",
    "QCD7": "/scratchnvme/cicco/QCD7_good_flash/",
    "QCD8": "/scratchnvme/cicco/QCD8_good_flash/",
    #"ph_2_full" : "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file_bckg.root",
    #"ph_2": "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file_bckg_flashsim.root"
    #"signal": "/scratchnvme/cicco/signal_RunIISummer20UL16_flash/",
    #"signal": "/scratchnvme/cicco/signal_RunIISummer20UL16/",

}

integrated_luminosity = 59830

weights = {
    "QCD4": 32100 * integrated_luminosity,
    "QCD5": 6831 * integrated_luminosity,
    "QCD6": 1207 * integrated_luminosity,
    "QCD7": 119.9 * integrated_luminosity,
    "QCD8": 25.24 * integrated_luminosity,
    "signal": 0.01053 * integrated_luminosity,

}

n_events = {
    "QCD4": 61097673,
    "QCD5": 47314826,
    "QCD6": 15230975,
    "QCD7": 11887406,
    "QCD8": 5710430,
    "signal": 540000,
}

entries1 = {}
events = {}
events_chain = {}
full_chain = {}
df = {}
histos = {}
histos_1d = {}
dataset_events = {}


processes = list(files.keys())
#processes = ['signal']
for i in processes:
    if str(i) != 'ph_2': 
        f = os.listdir(files.get(i))
        num = len(f)
        entries1[i] = []
        events[i] = []
        print("creating the TChains")
        events_chain[i] = ROOT.TChain("Events")
        full_chain[i] = ROOT.TChain("FullSim")

        for j in range(0, num):
            entries1[i].append(str(files.get(i)) + str(f[j]))

                
            #print("adding files to the TChains")
            events_chain[i].Add(str(files.get(i)) + str(f[j]))
            full_chain[i].Add(str(files.get(i)) + str(f[j]))
            events_chain[i].AddFriend(full_chain[i])

        df[i] = ROOT.RDataFrame(events_chain[i])

    else:
        df[i] = ROOT.RDataFrame("Events", files["ph_2"])
print("created the datframes")


histo_gen_pt = {}
histo_pt_ratio = {}
for i in processes: 
    if str(i)!= 'ph_2':
        df[i] = (df[i]
        .Define("matching_index" , "lepton_matching_index(FatJet_eta, FatJet_phi, GenJetAK8_eta, GenJetAK8_phi)")
        .Define("Post_calibration_pt", "calibrate_pt_double_n_bins(FatJet_eta, FatJet_pt)")
        .Define("Matched_gen_pt", "Take(GenJetAK8_pt, matching_index)")
        .Define("Ratio_RecoGen", "FatJet_pt/Matched_gen_pt")
        .Define("Abs_eta", "abs(FatJet_eta)")

        )

        histos[i] = df[i].Histo1D((str(i), str(i), 100, 0, 1000), "FatJet_pt").GetValue()
        histo_gen_pt[i] = df[i].Histo1D((str(i), str(i), 100, 0, 1000), "GenJetAK8_pt").GetValue()
        histo_pt_ratio[i] = df[i].Histo1D((str(i), str(i), 60, -0.5, 4), "Ratio_RecoGen").GetValue()
    else:
        df[i] = (df[i]
            .Define("Post_calibration_pt", "calibrate_pt_double_n_bins(Mfatjet_eta, Mfatjet_pt)")
                 
            .Define("Ratio_RecoGen", "Post_calibration_pt/MgenjetAK8_pt")
            .Define("Abs_eta", "abs(Mfatjet_eta)")
        )
        histos[i] = df[i].Histo1D((str(i), str(i), 100, 0, 1000), "Mfatjet_eta").GetValue()
        histo_gen_pt[i] = df[i].Histo1D((str(i), str(i), 100, 0, 1000), "MgenjetAK8_pt").GetValue()
        histo_pt_ratio[i] = df[i].Histo1D((str(i), str(i), 60, -0.5, 4), "Ratio_RecoGen").GetValue()





for i in processes:
    if str(i) != 'ph_2':
        histos[i].Scale(weights[i]*2.27/n_events[i])
        histo_gen_pt[i].Scale(weights[i]*2.27/n_events[i])
        


QCD_stacked = histos[str(processes[0])].Clone()
gen_pt_stacked = histo_gen_pt[str(processes[0])].Clone()
pt_ratio_stacked = histo_pt_ratio[str(processes[0])].Clone()
for i in processes:
    if str(i) == processes[0] or str(i) == 'ph_2':
        continue
    elif str(i)!= 'ph_2':
        QCD_stacked.Add(histos[i])
        gen_pt_stacked.Add(histo_gen_pt[i])
        pt_ratio_stacked.Add(histo_pt_ratio[i])



pt_bins = np.array([200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 3000], dtype="double")

new_pt_bins = np.array([200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 2000, 3000], dtype = 'double')


eta_bins = np.array([0, 0.8, 1.6, 2.4, 3.8, 5.0],  dtype="double")

new_eta_bins = np.array([0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 3.1, 3.8, 4.4, 5.0], dtype = 'double')

ratio_bins = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0], dtype="double")

print("About to create the 3D histogram")

for i in processes:

    histos[i] = df[i].Histo3D(
    ("flash", "flashsim sample", 24, new_pt_bins, 10, new_eta_bins, 20, ratio_bins), "Matched_gen_pt", "Abs_eta", "Ratio_RecoGen"
).GetValue()

    if str(i) != 'ph_2':
        histos[i].Scale(weights[i]*2.27/n_events[i])


QCD_stacked = histos[str(processes[0])].Clone()

for i in processes:
    if str(i) == processes[0] or str(i) == 'ph_2':
        continue
    elif str(i)!= 'ph_2':
        print(f"stacking {i}")
        QCD_stacked.Add(histos[i])


c1 = ROOT.TCanvas("c1", "Ratio in function of reco pt and eta", 800, 700)

QCD_stacked.Draw("LEGO2")

print("about to create the 2D histogram")

histo2d = df['QCD4'].Histo2D(
    ("flash", "flashsim sample", 24, new_pt_bins, 10, new_eta_bins), "Matched_gen_pt", "Abs_eta"
)
histo2d.Reset()

hist_test = df['QCD4'].Histo2D(
    ("flash", "flashsim sample", 24, 0, 1 , 10, 0, 1), "Matched_gen_pt", "Abs_eta"
)
hist_test.Reset()

hist_values = df['QCD4'].Histo2D(
    ("flash", "flashsim sample", 24, 0, 1 , 10, 0, 1), "Matched_gen_pt", "Abs_eta"
)
hist_values.Reset()

# Calculate mean ratio for each bin
mean_ratios = []

for i in range(1, len(new_pt_bins)):
    for j in range(1, len(new_eta_bins)):
        bin_contents_values = []
        entries = 0
        print(f"doing bin pt{i}, eta {j}")
        for k in range(1, len(ratio_bins)):
            bin_content = QCD_stacked.GetBinContent(i, j, k)* QCD_stacked.GetZaxis().GetBinCenter(k)
            entries += QCD_stacked.GetBinContent(i,j,k) 
            bin_contents_values.append(bin_content)
        if entries > 0:
            ratio = Decimal(sum(bin_contents_values))/Decimal(entries)
        else:
            ratio = 0
        histo2d.SetBinContent(i, j, ratio)
        hist_test.SetBinContent(i, j, ratio)
        if ratio !=0:
            hist_values.SetBinContent(i, j, 1/ratio)

        else:
            hist_values.SetBinContent(i, j, 0)


        mean_ratios.append(ratio)
mean_ratios = np.array(mean_ratios).reshape(len(new_pt_bins)-1, len(new_eta_bins)-1)


c2 = ROOT.TCanvas("c2", "Mean in function of reco pt and eta", 800, 700)

histo2d.Draw("COLZ text")


c3 = ROOT.TCanvas("c3", "Mean in function of reco pt and eta", 5500, 3500)

new_pt_bins.astype(int)

#new_pt_bins_int = int(new_pt_bins)

for i in range(1, len(new_pt_bins)):
    hist_test.GetXaxis().SetBinLabel(i, str(new_pt_bins[i]))
hist_test.LabelsOption("R")

for j in range(1, len(new_eta_bins)):
    hist_test.GetYaxis().SetBinLabel(j, str(new_eta_bins[j]))


for i in range(1, len(new_pt_bins)):
    hist_values.GetXaxis().SetBinLabel(i, str(new_pt_bins[i]))
hist_values.LabelsOption("R")

for j in range(1, len(new_eta_bins)):
    hist_values.GetYaxis().SetBinLabel(j, str(new_eta_bins[j]))




hist_test.Draw("COLZ text")
hist_test.SetTitle("Mean in function of gen pt and eta after calibration flashsim")
c3.Update()

c4 = ROOT.TCanvas("c4", "values for calibration", 5500, 3500)

hist_values.Draw("COLZ text")
hist_values.SetTitle("values for calibration")


for i in range(1, len(new_pt_bins)):
    hist_values.GetXaxis().SetBinLabel(i, str(new_pt_bins[i]))
hist_values.LabelsOption("R")

for j in range(1, len(new_eta_bins)):
    hist_values.GetYaxis().SetBinLabel(j, str(new_eta_bins[j]))

c4.Update()

# Print mean ratios
for i in range(0, len(new_pt_bins)-1): 
    for j in range(0, len(new_eta_bins)-1):
        print(f"Pt bin: {i}, Eta bin: {j}, Mean Ratio: {mean_ratios[i,j]}")

c2.SetLogy()
#dividere il reco per il rapporto per ogni bin in pt e eta 


# c5 = ROOT.TCanvas("c5", "gen_pt", 4500, 3500)

# legend = ROOT.TLegend(0.42, 0.72, 0.9, 0.9)

# gen_pt_stacked.Draw("HIST")
# gen_pt_stacked.SetTitle("GEN pt distributions")
# gen_pt_stacked.SetLineWidth(2)
# gen_pt_stacked.SetLineColor(ROOT.kTeal -6)
# legend.AddEntry(gen_pt_stacked, "Run2 flashsim", 'l')
# gen_pt_stacked.Scale(1/gen_pt_stacked.Integral())
# gen_pt_stacked.SetMaximum(1)

# histo_gen_pt['ph_2'].Draw('SAME HIST')
# histo_gen_pt["ph_2"].SetLineColor(ROOT.kRed+2)
# histo_gen_pt["ph_2"].SetLineWidth(2)
# legend.AddEntry(histo_gen_pt["ph_2"], 'Phase2 fullsim', 'l')
# histo_gen_pt["ph_2"].Scale(1/histo_gen_pt["ph_2"].Integral())

# legend.Draw()

# c5.SetLogy(1)



# c6 = ROOT.TCanvas("c6", "gen_pt", 4500, 3500)

# legend2 = ROOT.TLegend(0.62, 0.72, 0.9, 0.9)

# pt_ratio_stacked.Draw("HIST")
# pt_ratio_stacked.SetTitle("pt ratio")
# pt_ratio_stacked.SetLineWidth(2)
# pt_ratio_stacked.SetLineColor(ROOT.kTeal -6)
# legend2.AddEntry(pt_ratio_stacked, "Run2 flashsim", 'l')
# pt_ratio_stacked.Scale(1/pt_ratio_stacked.Integral())
# pt_ratio_stacked.SetMaximum(1)

# histo_pt_ratio['ph_2'].Draw('SAME HIST')
# histo_pt_ratio["ph_2"].SetLineColor(ROOT.kRed+2)
# histo_pt_ratio["ph_2"].SetLineWidth(2)
# legend2.AddEntry(histo_pt_ratio["ph_2"], 'Phase2 fullsim', 'l')
# histo_pt_ratio["ph_2"].Scale(1/histo_pt_ratio["ph_2"].Integral())

# legend2.Draw()

# c6.SetLogy(1)

c1.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/calibration/2x_bins_3d_ratio_for_calibration_post_calib_flash_all_QCD_GEN_on_axis.pdf"
)

# c2.SaveAs(
#     "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/calibration/2x_bins_mean_for_calibration_post_calib_flash_all_QCD_GEN_on_axis.pdf"
# )

c3.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/calibration/2x_bins_response_flash_all_QCD_GEN_on_axis.pdf"
)

# c4.SaveAs(
#     "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/calibration/2x_bins_values_for_calibration_regular_binning_post_calib_flash_all_QCD_GEN_on_axis.pdf"
# )

# c5.SaveAs(
#      "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/calibration/gen_pt_comparison.pdf"
#  )

# c6.SaveAs(
#      "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/calibration/pt_ratio_comparison.pdf"
#  )