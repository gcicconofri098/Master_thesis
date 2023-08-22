import ROOT
import os
import numpy as np

module_path = os.path.join(os.path.dirname(__file__), "utils.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "utils_calibration.h")


ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')



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

qcd_post_sel_weighted = 0

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

#processes = list(files.keys())
processes = ['QCD6', 'QCD7', 'QCD8', 'signal']

#processes = ['signal']

#processes = ['QCD1', 'QCD2', 'QCD3', 'QCD4', 'QCD5', 'QCD6', 'QCD7', 'QCD8']

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

weighted_post_selection = 0

total_events = 0

total_events_post = 0

total_post_sel_weighted = 0

for i in processes:
    print("Begin selection: {}".format(i))
    dataset_events[i] = df[i].Count().GetValue()
    print("events in dataset {}: {}".format(i, dataset_events[i]))
    if str(i) != 'signal':
        total_events = total_events + dataset_events[i]
        print("total",total_events)
    #new_weights[i] = weights[i] / 540000
    #print("preselection events in dataset {}: {}".format(i, dataset_events[i]*new_weights[i]))
    #print(new_weights[i])

    df[i] = df[i].Filter("nFatJet>=2")

    df[i] = (
        df[i]
        .Define("Post_calibration_pt", "calibrate_pt(FatJet_eta, FatJet_pt)")

        .Define(
            # mu = 13, e = 11
            "FatJet_Selection",
            "Post_calibration_pt > 300 && abs(FatJet_eta) < 2.4 && fatjet_lepton_isolation(FatJet_eta, FatJet_phi, Electron_pt, Electron_eta, Electron_phi, Electron_pfRelIso03_all, 11)  && fatjet_lepton_isolation(FatJet_eta, FatJet_phi, Muon_pt, Muon_eta, Muon_phi, Muon_pfRelIso03_all, 13)",
        )
        .Define("Softdrop_sel_jets", "FatJet_msoftdrop[FatJet_Selection]")
        .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[FatJet_Selection]")
        .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[FatJet_Selection]")
        .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[FatJet_Selection]")
        .Define("new_discriminator", "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)")
        #.Define("new_discriminator", "FatJet_particleNetMD_XbbvsQCD[FatJet_Selection]")
        .Define("Eta_sel_jets", "FatJet_eta[FatJet_Selection]")
        .Define("Phi_sel_jets", "FatJet_phi[FatJet_Selection]")
        .Define("Pt_sel_jets", "Post_calibration_pt[FatJet_Selection]")
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
        .Define("Jet1_Selected_jets_pt", "Pt_sel_jets[Jet1_index]")
        .Define("Jet2_Selected_jets_pt", "Pt_sel_jets[Jet2_index]")

    )
    #print("count postpreselection, no veto, no MET: ",df[i].Count().GetValue())

    #df[i] = df[i].Filter("new_discriminator[Jet1_index]>0.86")
    df[i] = df[i].Filter("MET_pt <100")
    #print("count postpreselection, no veto: ",df[i].Count().GetValue())

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
        #df[i].Snapshot("pre_veto_Jets", "pre_veto.root", col_to_save)

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

    # df[i].Display("Delta_eta").Print()
    # df[i].Display("Jet_invariant_mass").Print()

    df[i] = (
        df[i]
        .Define(
            "VBF_events", "nJet >=2 && abs(Delta_eta) >4.0 && Jet_invariant_mass > 500"
        )
        #.Filter("!VBF_events")
    )
    #print("count postpreselection with veto: ",df[i].Count().GetValue())

    # if str(i) != "signal":
    #     pre_selection_background = (
    #         pre_selection_background + df[i].Count().GetValue() * new_weights[i]
    #     )
    #     print("pre preselection background: ", pre_selection_background)
    # else:
    #     pre_selection_signal = df[i].Count().GetValue() * new_weights[i]
    #     print("pre preselection signal: ", pre_selection_signal) 

    #df[i].Filter("Jet1_Selected_jets_discriminator >0.95 && Jet2_Selected_jets_discriminator > 0.95")


    if  (str(i) != 'QCD1') and (str(i) != 'QCD2') and (str(i) != 'QCD3') and (str(i) != 'QCD4') and (str(i) != 'QCD5') and (str(i) != 'QCD6') and (str(i) != 'QCD7') and (str(i) != 'QCD8'):
        #df[i] = df[i].Filter("new_discriminator[Jet1_index] > 0.996 && new_discriminator[Jet2_index] >0.98")
        df[i] = df[i].Filter("Jet1_Selected_jet_softdrop > 115 && Jet1_Selected_jet_softdrop < 145").Filter("Jet2_Selected_jet_softdrop > 115 && Jet2_Selected_jet_softdrop < 145")

    #print("count postpreselection with veto and mass window: ",df[i].Count().GetValue())


#     if str(i) != "signal":
#         post_selection_background = df[i].Count().GetValue()
        
#         print("post preselection background (non cumulative) for {}: {}".format(i, post_selection_background))
        
#         total_events_post = total_events_post + post_selection_background
#         print("total post selection",total_events_post)

#         percentage = post_selection_background/dataset_events[i]
#         print("percentage of {} that passes selection: {}".format(i, percentage))

#         weighted_post_selection = post_selection_background*new_weights[i]
#         print("total weighted post selection background:" , weighted_post_selection)

    
#     #print("finished jets selection for dataset: {}".format(i))
#     if  (str(i) != 'QCD1') and (str(i) != 'QCD2') and (str(i) != 'QCD3') and (str(i) != 'QCD4') and (str(i) != 'QCD5') and (str(i) != 'QCD6') and (str(i) != 'QCD7') and (str(i) != 'QCD8') and (str(i) != 'signal') :

#         total_post_sel_weighted = total_post_sel_weighted + df[i].Count().GetValue() * new_weights[i]

#     elif (str(i) == 'signal'):
#         post_selection_signal = df[i].Count().GetValue() * new_weights[i]
#         print("percentage: ", df[i].Count().GetValue()/dataset_events[i])
#         print("post preselection signal: ", post_selection_signal)

#     else:
#         qcd_post_sel_weighted = qcd_post_sel_weighted + df[i].Count().GetValue() * new_weights[i]

# qcd_post_sel_weighted = qcd_post_sel_weighted * 0.035 #0.04 #0.035 for fullsim

# total_weighted = total_post_sel_weighted + qcd_post_sel_weighted

# print("total background weighted with QCD corrected", total_weighted)
    


# #print("efficiency: ", post_selection_signal / pre_selection_signal)
# #bckg_eff = 1 - ((pre_selection_background- post_selection_background)/pre_selection_background)

# #print("bckg efficiency", bckg_eff)

# print("Finished selection")

# ROOT.gStyle.SetOptStat(0)

# hist1 = {}
# hist2 = {}
# histo2d = {}
# hist_tot = {}
# test1 = {}
# test2 = {}
# test2_2 = {}

# h1 = {}
# h2 = {}
# h2_2 = {}
# h_tot = {}


# no_weight = 0
# no_weight_2d = 0
# n_events = 0
# n_events_2d = 0
# jet1_bckg = 0
# jet2_bckg = 0
# for i in processes:
#     hist1[i] = df[i].Histo1D(
#         (str(i), str(i) + "; Pt; Events", 18, 40, 300), "Jet1_Selected_jet_softdrop"
#     )

#     hist2[i] = df[i].Histo1D(
#         (str(i), str(i) + "; Pt; Events", 18, 40, 300), "Jet2_Selected_jet_softdrop"
#     )

#     # hist_tot[i] = df[i].Histo1D(
#     #     (str(i), str(i) + "; Soft Drop mass; Events", 25, 0, 500), "Softdrop_sel_jets"
#     # )

#     histo2d[i] = df[i].Histo2D(
#         ("Jet1 vs Jet2", "Jet1 vs Jet2; Jet1; Jet2", 10, 0.8, 1, 10, 0.8, 1),
#         "Jet1_Selected_jets_discriminator",
#         "Jet2_Selected_jets_discriminator",
#     )

# #     histo2d[i] = df[i].Histo2D(
# #     ("Jet1 vs Jet2", "Jet1 vs Jet2; Jet1; Jet2", 18, 25, 295, 18, 25, 295),
# #     "Jet1_Selected_jet_softdrop",
# #     "Jet2_Selected_jet_softdrop",
# # )

#     print("created histograms for: {}".format(i))

#     # h1[i] = hist1[i].GetValue()

#     # #     if str(i) != "signal":
#     # #         jet1_bckg = jet1_bckg + h1[i].GetEntries() * new_weights[i]

#     # h1[i].Scale(1 / dataset_events[i])

#     # h2[i] = hist2[i].GetValue()
#     # h2[i].Scale(1 / dataset_events[i])

#     h2_2[i] = histo2d[i].GetValue()
#     h2_2[i].Scale(1 / 540000)

# #     # h_tot[i] = hist_tot[i].GetValue()
# #     # h_tot[i].Scale(1 / dataset_events[i])

#     print("got values for histograms of: {}".format(i))

#     print("weighted histograms for:{}".format(i))




# output_file = ROOT.TFile.Open("histograms_2d_discr_0_8_mass_window_no_discr_pres_no_veto_VBF_flashsim_corrected_n_events.root", "RECREATE")


# for i in processes:
#     # output_file.WriteObject(h1[i], "h1_" + str(i))
#     # output_file.WriteObject(h2[i], "h2_" + str(i))
#     # output_file.WriteObject(h_tot[i], "h_tot" + str(i))
#     output_file.WriteObject(h2_2[i], "h2_2_" + str(i))


# print("written on txt")
