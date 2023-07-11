import ROOT
import os
import numpy as np
from decimal import *

ROOT.EnableImplicitMT()

module_path = os.path.join(os.path.dirname(__file__), "utils.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')

getcontext().prec = 2

entries1 = {}

df = {}

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
    "ZZ": "/scratchnvme/cicco/ZZ/",
    "signal": "/scratchnvme/cicco/signal_RunIISummer20UL16/",
}

jet1_discr = np.linspace(0.95, 1, 20)
jet2_discr = np.linspace(0.95, 1, 20)
print("jet1 discr len", len(jet1_discr))
print("jet1 discr", jet1_discr)

print("jet2 discr len", len(jet2_discr))
print("jet2 discr", jet2_discr)

ROOT.gStyle.SetOptStat(0)


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

new_weights = {}
dataset_events["signal"] = df["signal"].Count().GetValue()

new_weights["signal"] = weights["signal"] / dataset_events["signal"]

# df["signal"] = (
#     df["signal"]
#     .Filter("HLT_PFJet500")
#     .Filter("HLT_PFHT1050")
#     .Filter("HLT_AK8PFJet360_TrimMass30")
#     .Filter("HLT_AK8PFJet380_TrimMass30")
#     .Filter("HLT_AK8PFJet400_TrimMass30")
#     .Filter("HLT_AK8PFHT800_TrimMass50")
#     .Filter("HLT_AK8PFHT750_TrimMass50")
# ) 

df["signal"] = df["signal"].Filter("nFatJet>=2")

df["signal"] = (
    df["signal"]
    .Define(
        # mu = 13, e = 11
        "FatJet_Selection",
        "FatJet_pt > 300 && abs(FatJet_eta) < 2.4 && fatjet_lepton_isolation(FatJet_electronIdx3SJ, Electron_pt, Electron_eta, Electron_pfRelIso03_all, 11)  && fatjet_lepton_isolation(FatJet_muonIdx3SJ, Muon_pt, Muon_eta, Muon_pfRelIso03_all, 13)",
    )
    .Define("Softdrop_sel_jets", "FatJet_msoftdrop[FatJet_Selection]")
    .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[FatJet_Selection]")
    .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[FatJet_Selection]")
    .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[FatJet_Selection]")
    .Define("new_discriminator", "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)")
    .Define("Eta_sel_jets", "FatJet_eta[FatJet_Selection]")
    .Define("Phi_sel_jets", "FatJet_phi[FatJet_Selection]")
)
df["signal"] = df["signal"].Filter("new_discriminator.size()>=2")

df["signal"] = (
    df["signal"]
    .Define(
        "sorted_FatJet_deepTagMD_HbbvsQCD",
        "Reverse(Argsort(new_discriminator))",
    )
    .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
    .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
)
df["signal"] = df["signal"].Filter(
    "Softdrop_sel_jets[Jet1_index]> 50 && Softdrop_sel_jets[Jet2_index]> 50"
)
df["signal"] = (
    df["signal"]
    .Define("Jet1_Selected_jet_softdrop", "Softdrop_sel_jets[Jet1_index]")
    .Define("Jet2_Selected_jet_softdrop", "Softdrop_sel_jets[Jet2_index]")
    .Define(
        "Jet1_Selected_jets_discriminator", "new_discriminator[Jet1_index]"
    )
    .Define(
        "Jet2_Selected_jets_discriminator", "new_discriminator[Jet2_index]"
    )
    .Define("Jet1_Selected_jets_eta", "Eta_sel_jets[Jet1_index]")
    .Define("Jet2_Selected_jets_eta", "Eta_sel_jets[Jet2_index]")
    .Define("Jet1_Selected_jets_phi", "Phi_sel_jets[Jet1_index]")
    .Define("Jet2_Selected_jets_phi", "Phi_sel_jets[Jet2_index]")
    .Define(
        "Sum_selected_jets",
        "Jet1_Selected_jet_softdrop + Jet2_Selected_jet_softdrop",
    )
)



hist_0 = df["signal"].Histo2D(
    (
        "hist",
        "Signal efficiency map for the discriminator; Value of Jet1 discriminator; Value of Jet2 discriminator",
        20,
        0.86,
        1,
        20,
        0.86,
        1,
    ),
    "Jet1_Selected_jets_discriminator",
    "Jet2_Selected_jets_discriminator",
)




# pre_selection_signal = df["signal"].Count().GetValue() * new_weights[i]
# print("pre preselection signal: ", pre_selection_signal)

#df["signal"] = df["signal"].Filter("new_discriminator[Jet1_index] > 0.985 && new_discriminator[Jet2_index] >0.98")



# if str(i) == "WJets1":
#     col_to_save = {
#         "Jet1_Selected_jets_eta",
#         "Jet2_Selected_jets_eta",
#         "Jet1_Selected_jets_phi",
#         "Jet2_Selected_jets_phi",
#         "Jet1_Selected_jet_softdrop",
#         "Jet2_Selected_jet_softdrop",
#         "Jet1_Selected_jets_discriminator",
#         "Jet2_Selected_jets_discriminator",
#     }
    #df["signal"].Snapshot("pre_veto_Jets", "pre_veto.root", col_to_save)

#! VETO ON VBF

df["signal"] = (
    df["signal"]
    .Define(
        "VBF_jet_preselection",
        "jet_isolation(Jet_eta, Jet_phi, Eta_sel_jets, Phi_sel_jets) && Jet_pt >25 && abs(Jet_eta) <4.7",
    )
    .Define("Candidate_jets_pt", "Jet_pt[VBF_jet_preselection]")
    .Define("Candidate_jets_mass", "Jet_mass[VBF_jet_preselection]")
    .Define("Candidate_jets_eta", "Jet_eta[VBF_jet_preselection]")
    .Define("Candidate_jets_phi", "Jet_phi[VBF_jet_preselection]")
)

df["signal"] = (
    df["signal"]
    .Define("Muon_preselection", "Muon_pt >5")
    .Define("Candidate_muon_pt", "Muon_pt[Muon_preselection]")
    .Define("Candidate_muon_eta", "Muon_eta[Muon_preselection]")
    .Define("Candidate_muon_phi", "Muon_phi[Muon_preselection]")
)
df["signal"] = (
    df["signal"]
    .Define("Electron_preselection", "Electron_pt >7")
    .Define("Candidate_el_pt", "Electron_pt[Electron_preselection]")
    .Define("Candidate_el_eta", "Electron_eta[Electron_preselection]")
    .Define("Candidate_el_phi", "Electron_phi[Electron_preselection]")
)

df["signal"] = (
    df["signal"]
    .Define(
        "Good_VBF_candidates",
        "part_isolation(Candidate_jets_eta, Candidate_jets_phi, Candidate_muon_eta, Candidate_muon_phi, Candidate_el_eta, Candidate_el_phi)",
    )
    .Define("Good_VBF_jets_eta", "Candidate_jets_eta[Good_VBF_candidates]")
    .Define("Good_VBF_jets_mass", "Candidate_jets_mass[Good_VBF_candidates]")
    .Define("Good_VBF_jets_pt", "Candidate_jets_pt[Good_VBF_candidates]")
    .Define("Good_VBF_jets_phi", "Candidate_jets_phi[Good_VBF_candidates]")
)
df["signal"] = (
    df["signal"]
    .Define("sorted_VBF_jets_pt", "Reverse(Argsort(Good_VBF_jets_pt))")
    .Define("VBF_Jet1_index", "sorted_VBF_jets_pt[0]")
    .Define("VBF_Jet2_index", "sorted_VBF_jets_pt[1]")
)
df["signal"] = (
    df["signal"]
    .Define("VBF_Jet1_eta", "Good_VBF_jets_eta[VBF_Jet1_index]")
    .Define("VBF_Jet2_eta", "Good_VBF_jets_eta[VBF_Jet2_index]")
    .Define("VBF_Jet1_mass", "Good_VBF_jets_mass[VBF_Jet1_index]")
    .Define("VBF_Jet2_mass", "Good_VBF_jets_mass[VBF_Jet2_index]")
    .Define("VBF_Jet1_pt", "Good_VBF_jets_pt[VBF_Jet1_index]")
    .Define("VBF_Jet2_pt", "Good_VBF_jets_pt[VBF_Jet2_index]")
    .Define("VBF_Jet1_phi", "Good_VBF_jets_phi[VBF_Jet1_index]")
    .Define("VBF_Jet2_phi", "Good_VBF_jets_phi[VBF_Jet2_index]")
)

df["signal"] = (
    df["signal"]
    .Define(
        "Delta_eta",
        "VBF_Jet1_eta - VBF_Jet2_eta",
    )
    .Define(
        "Jet_invariant_mass",
        "invariant_mass(VBF_Jet1_pt, VBF_Jet1_eta, VBF_Jet1_phi, VBF_Jet1_mass, VBF_Jet2_pt, VBF_Jet2_eta, VBF_Jet2_phi, VBF_Jet2_mass)",
    )
)

df["signal"] = (
    df["signal"]
    .Define(
        "VBF_events", "nJet >=2 && abs(Delta_eta) >4.0 && Jet_invariant_mass > 500"
    )
    .Filter("!VBF_events")
)

df["signal"] = df["signal"].Filter("new_discriminator[Jet1_index]>0.86")

event_number = 1


df_2 = {}


# for jet1 in range(len(jet1_discr)):
#     print("jet1: ", jet1)


#     for jet2 in range(len(jet2_discr)):
#         print("jet2: ", jet2)

#         print("pre creation of new column", df["signal"].Count().GetValue())
#         df_2[str(event_number)] = (
#             df["signal"]
#             .Define(
#                 "Discriminator_cut",
#                 "Selected_jets[Jet1_index]>="
#                 + str(jet1_discr[jet1])
#                 + " && Selected_jets[Jet2_index]>="
#                 + str(jet2_discr[jet2]),
#             )
#             .Filter("Discriminator_cut")
#         )
#         print("post creation of new column", df_2[str(event_number)].Count().GetValue())

#         df_2[str(event_number)] = df_2[str(event_number)].Filter("Selected_jets.size()>=2")

#         post_selection_signal = df_2[str(event_number)].Count().GetValue()

#         #efficiency = Decimal(post_selection_signal) / Decimal(pre_selection_signal)

#         efficiency = (post_selection_signal) / (pre_selection_signal)


#         print("efficiency for event {}: {}".format(event_number, efficiency))

#         hist.SetBinContent(jet1+1, jet2+1, efficiency)
#         event_number = event_number + 1

hist = df["signal"].Histo2D(
    (
        "hist",
        "Signal efficiency map for the discriminator; Value of Jet1 discriminator; Value of Jet2 discriminator",
        20,
        0.95,
        1,
        20,
        0.95,
        1,
    ),
    "Jet1_Selected_jets_discriminator",
    "Jet2_Selected_jets_discriminator",
)

hist_0 = df["signal"].Histo2D(
    (
        "hist",
        "Signal efficiency map for the discriminator; Value of Jet1 discriminator; Value of Jet2 discriminator",
        20,
        0.86,
        1,
        20,
        0.86,
        1,
    ),
    "Jet1_Selected_jets_discriminator",
    "Jet2_Selected_jets_discriminator",
)
preselection_signal = hist_0.GetEntries()
print(preselection_signal)

hist_2 = df["signal"].Histo2D(
    (
        "hist2",
        "Signal efficiency map for the discriminator; Value of Jet1 discriminator; Value of Jet2 discriminator",
        20,
        0.95,
        1,
        20,
        0.95,
        1,
    ),
    "Jet1_Selected_jets_discriminator",
    "Jet2_Selected_jets_discriminator",
)
hist_2.Reset()


for binx in reversed(range(1, 21)):
    for biny in reversed(range(1, 21)):
        if binx >= biny:
            stacked_sig = hist.Integral(binx, 20, biny, 20)
            print("stacked signal: ", stacked_sig)
            print("binx", binx)
            print("biny", biny)

            if stacked_sig > 0:
                new_bin_cont = Decimal(stacked_sig) / Decimal(preselection_signal)
                temp = Decimal(new_bin_cont)
                print(temp)
                hist_2.SetBinContent(binx, biny, temp)


c2 = ROOT.TCanvas("c2", "Efficiency plot", 4500, 3500)
c2.SetGrid()
#ROOT.gStyle.SetPaintTextFormat("1.1e")
hist_2.Draw("text COLZ")


c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/efficiency_map_num.pdf")

