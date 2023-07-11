import ROOT
import os
import numpy as np

module_path = os.path.join(os.path.dirname(__file__), "utils.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')


ROOT.EnableImplicitMT(10)

entries1 = {}

df = {}
df_1 = {}
integrated_luminosity = 59830
dataset_events = {}
pre_selection_signal = 0
pre_selection_background = 0
post_selection_background = 0

efficiency = 0
post_selection_signal = 0
rejection = 0

temp = 0

weights = {
    "QCD1": 27990000 * integrated_luminosity,
    "QCD2": 1712000 * integrated_luminosity,
    "QCD3": 347700 * integrated_luminosity,
    "QCD4": 32100 * integrated_luminosity,
    "QCD5": 6831 * integrated_luminosity,
    "QCD6": 1207 * integrated_luminosity,
    "QCD7": 119.9 * integrated_luminosity,
    "QCD8": 25.24 * integrated_luminosity,
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

new_weights = {}


for i in processes:
    print("Begin selection: {}".format(i))
    dataset_events[i] = df[i].Count().GetValue()

    new_weights[i] = weights[i] / dataset_events[i]

    df[i] = df[i].Filter("nFatJet>=2")

    df[i] = (
        df[i]
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
    df[i] = df[i].Filter("new_discriminator.size()>=2")

    df[i] = (
        df[i]
        .Define(
            "sorted_FatJet_deepTagMD_HbbvsQCD",
            "Reverse(Argsort(new_discriminator))",
        )
        .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
        .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
    )
    df[i] = df[i].Filter(
        "Softdrop_sel_jets[Jet1_index]> 50 && Softdrop_sel_jets[Jet2_index]> 50"
    )
    df[i] = (
        df[i]
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

    df[i] = df[i].Filter("new_discriminator[Jet1_index]>0.86").Filter("MET_pt <100")

    #! VETO ON VBF

    df[i] = (
        df[i]
        .Define(
            "VBF_jet_preselection",
            "jet_isolation(Jet_eta, Jet_phi, Eta_sel_jets, Phi_sel_jets) && Jet_pt >25 && abs(Jet_eta) <4.7",
        )
        .Define("Candidate_jets_pt", "Jet_pt[VBF_jet_preselection]")
        .Define("Candidate_jets_mass", "Jet_mass[VBF_jet_preselection]")
        .Define("Candidate_jets_eta", "Jet_eta[VBF_jet_preselection]")
        .Define("Candidate_jets_phi", "Jet_phi[VBF_jet_preselection]")
    )

    df[i] = (
        df[i]
        .Define("Muon_preselection", "Muon_pt >5")
        .Define("Candidate_muon_pt", "Muon_pt[Muon_preselection]")
        .Define("Candidate_muon_eta", "Muon_eta[Muon_preselection]")
        .Define("Candidate_muon_phi", "Muon_phi[Muon_preselection]")
    )
    df[i] = (
        df[i]
        .Define("Electron_preselection", "Electron_pt >7")
        .Define("Candidate_el_pt", "Electron_pt[Electron_preselection]")
        .Define("Candidate_el_eta", "Electron_eta[Electron_preselection]")
        .Define("Candidate_el_phi", "Electron_phi[Electron_preselection]")
    )

    df[i] = (
        df[i]
        .Define(
            "Good_VBF_candidates",
            "part_isolation(Candidate_jets_eta, Candidate_jets_phi, Candidate_muon_eta, Candidate_muon_phi, Candidate_el_eta, Candidate_el_phi)",
        )
        .Define("Good_VBF_jets_eta", "Candidate_jets_eta[Good_VBF_candidates]")
        .Define("Good_VBF_jets_mass", "Candidate_jets_mass[Good_VBF_candidates]")
        .Define("Good_VBF_jets_pt", "Candidate_jets_pt[Good_VBF_candidates]")
        .Define("Good_VBF_jets_phi", "Candidate_jets_phi[Good_VBF_candidates]")
    )
    df[i] = (
        df[i]
        .Define("sorted_VBF_jets_pt", "Reverse(Argsort(Good_VBF_jets_pt))")
        .Define("VBF_Jet1_index", "sorted_VBF_jets_pt[0]")
        .Define("VBF_Jet2_index", "sorted_VBF_jets_pt[1]")
    )
    df[i] = (
        df[i]
        .Define("VBF_Jet1_eta", "Good_VBF_jets_eta[VBF_Jet1_index]")
        .Define("VBF_Jet2_eta", "Good_VBF_jets_eta[VBF_Jet2_index]")
        .Define("VBF_Jet1_mass", "Good_VBF_jets_mass[VBF_Jet1_index]")
        .Define("VBF_Jet2_mass", "Good_VBF_jets_mass[VBF_Jet2_index]")
        .Define("VBF_Jet1_pt", "Good_VBF_jets_pt[VBF_Jet1_index]")
        .Define("VBF_Jet2_pt", "Good_VBF_jets_pt[VBF_Jet2_index]")
        .Define("VBF_Jet1_phi", "Good_VBF_jets_phi[VBF_Jet1_index]")
        .Define("VBF_Jet2_phi", "Good_VBF_jets_phi[VBF_Jet2_index]")
    )

    df[i] = (
        df[i]
        .Define(
            "Delta_eta",
            "VBF_Jet1_eta - VBF_Jet2_eta",
        )
        .Define(
            "Jet_invariant_mass",
            "invariant_mass(VBF_Jet1_pt, VBF_Jet1_eta, VBF_Jet1_phi, VBF_Jet1_mass, VBF_Jet2_pt, VBF_Jet2_eta, VBF_Jet2_phi, VBF_Jet2_mass)",
        )
    )

    df[i] = (
        df[i]
        .Define(
            "VBF_events", "nJet >=2 && abs(Delta_eta) >4.0 && Jet_invariant_mass > 500"
        )
        .Filter("!VBF_events")
    )

    df[i] = df[i].Filter("Jet1_Selected_jet_softdrop > 80 && Jet1_Selected_jet_softdrop < 150")

    #df[i] = df[i].Filter("new_discriminator[Jet1_index] > 0.996 && new_discriminator[Jet2_index] >0.98")



    post_selection_background = (
            post_selection_background + df[i].Count().GetValue()
        )
        
    print("post preselection background: ", post_selection_background)


    print("finished jets selection for dataset: {}".format(i))


# print("efficiency: ", post_selection_signal / pre_selection_signal)
# bckg_eff = 1 - ((pre_selection_background- post_selection_background)/pre_selection_background)

# print("bckg efficiency", bckg_eff)

print("Finished selection")

ROOT.gStyle.SetOptStat(0)

hist1 = {}
hist2 = {}
histo2d = {}
hist_tot = {}
test1 = {}
test2 = {}
test2_2 = {}

h1 = {}
h2 = {}
h2_2 = {}
h_tot = {}


no_weight = 0
no_weight_2d = 0
n_events = 0
n_events_2d = 0
jet1_bckg = 0
jet2_bckg = 0
for i in processes:
    hist1[i] = df[i].Histo1D(
        (str(i), str(i) + "; Softdrop mass; Events", 17, 0, 155), "Jet1_Selected_jet_softdrop"
    )

    hist2[i] = df[i].Histo1D(
        (str(i), str(i) + "; Softdrop mass; Events", 17, 0, 220), "Jet2_Selected_jet_softdrop"
    )

    print("created histograms for: {}".format(i))

    h1[i] = hist1[i].GetValue()
    h1[i].Scale(1 / dataset_events[i])

    h2[i] = hist2[i].GetValue()
    h2[i].Scale(1 / dataset_events[i])


    print("got values for histograms of: {}".format(i))

    print("weighted histograms for:{}".format(i))


# post_selection_events = n_events + h1["signal"].GetEntries()*new_weights[i] +h2["signal"].GetEntries()*new_weights[i]
#! EFFICIENCY ESTIMATION AND BACKGROUND REJECTION

# rejection = (pre_selection_background -post_selection_background)/pre_selection_background

# print("Efficiency: ",efficiency)
# print("Background rejection: ",rejection)


output_file = ROOT.TFile.Open("histograms_from_analysis_QCD_0_86_MET_and_mass_cut.root", "RECREATE")


for i in processes:
    output_file.WriteObject(h1[i], "h1_" + str(i))
    output_file.WriteObject(h2[i], "h2_" + str(i))


print("written on txt")
