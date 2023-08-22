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
pre_selection_signal = 0
pre_selection_background = 0
post_selection_background = 0

efficiency = 0
post_selection_signal = 0
rejection = 0

qcd_post_sel_weighted = 0

temp = 0

weights = {

    "QCD6": 1207 * integrated_luminosity,
    "QCD7": 119.9 * integrated_luminosity,
    "QCD8": 25.24 * integrated_luminosity,
    "signal": 0.01053 * integrated_luminosity,
}

dataset_events ={
    "QCD6": 15230975,
    "QCD7": 11887406,
    "QCD8": 5710430,
    "signal": 540000}

files = {

    "QCD6": "/scratchnvme/cicco/QCD6_good_flash/",
    "QCD7": "/scratchnvme/cicco/QCD7_good_flash/",
    "QCD8": "/scratchnvme/cicco/QCD8_good_flash/",
    "signal": "/scratchnvme/cicco/signal_RunIISummer20UL16_flash/",
}

processes = list(files.keys())

#processes = ['signal']

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

    new_weights[i] = weights[i]/dataset_events[i]

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
        # .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[FatJet_Selection]")
        # .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[FatJet_Selection]")
        # .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[FatJet_Selection]")
        # .Define("new_discriminator", "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)")
        .Define("new_discriminator", "FatJet_particleNetMD_XbbvsQCD[FatJet_Selection]")
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

    df[i] = df[i].Filter("new_discriminator[Jet1_index]>0.83")
    df[i] = df[i].Filter("MET_pt <100")
    #print("count postpreselection, no veto: ",df[i].Count().GetValue())



    if  (str(i) != 'QCD1') and (str(i) != 'QCD2') and (str(i) != 'QCD3') and (str(i) != 'QCD4') and (str(i) != 'QCD5') and (str(i) != 'QCD6') and (str(i) != 'QCD7') and (str(i) != 'QCD8'):
        #df[i] = df[i].Filter("new_discriminator[Jet1_index] > 0.996 && new_discriminator[Jet2_index] >0.98")
        df[i] = df[i].Filter("Jet1_Selected_jet_softdrop > 115 && Jet1_Selected_jet_softdrop < 145").Filter("Jet2_Selected_jet_softdrop > 115 && Jet2_Selected_jet_softdrop < 145")

    print("count postpreselection with veto and mass window: ",df[i].Count().GetValue())


    if str(i) != "signal":
        post_selection_background = df[i].Count().GetValue()
        
        print("post preselection background (non cumulative) for {}: {}".format(i, post_selection_background))
        
        total_events_post = total_events_post + post_selection_background
        print("total post selection",total_events_post)

        percentage = post_selection_background/dataset_events[i]
        print("percentage of {} that passes selection: {}".format(i, percentage))

        weighted_post_selection = post_selection_background*new_weights[i]
        print("total weighted post selection background:" , weighted_post_selection)

    
    #print("finished jets selection for dataset: {}".format(i))
    if  (str(i) != 'QCD1') and (str(i) != 'QCD2') and (str(i) != 'QCD3') and (str(i) != 'QCD4') and (str(i) != 'QCD5') and (str(i) != 'QCD6') and (str(i) != 'QCD7') and (str(i) != 'QCD8') and (str(i) != 'signal') :

        total_post_sel_weighted = total_post_sel_weighted + df[i].Count().GetValue() * new_weights[i]

    elif (str(i) == 'signal'):
        post_selection_signal = df[i].Count().GetValue() * new_weights[i]
        print("percentage: ", df[i].Count().GetValue()/dataset_events[i])
        print("post preselection signal: ", post_selection_signal)

    else:
        qcd_post_sel_weighted = qcd_post_sel_weighted + df[i].Count().GetValue() * new_weights[i]

#* coefficienti per la QCD sono 0.4 per flashsim e 0.35 per fullsim

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
        (str(i), str(i) + "; Pt; Events", 18, 40, 300), "Jet1_Selected_jet_softdrop"
    )

    hist2[i] = df[i].Histo1D(
        (str(i), str(i) + "; Pt; Events", 18, 40, 300), "Jet2_Selected_jet_softdrop"
    )

    # hist_tot[i] = df[i].Histo1D(
    #     (str(i), str(i) + "; Soft Drop mass; Events", 25, 0, 500), "Softdrop_sel_jets"
    # )

    histo2d[i] = df[i].Histo2D(
        ("Jet1 vs Jet2", "Jet1 vs Jet2; Jet1; Jet2", 10, 0.8, 1, 10, 0.8, 1),
        "Jet1_Selected_jets_discriminator",
        "Jet2_Selected_jets_discriminator",
    )

#     histo2d[i] = df[i].Histo2D(
#     ("Jet1 vs Jet2", "Jet1 vs Jet2; Jet1; Jet2", 18, 25, 295, 18, 25, 295),
#     "Jet1_Selected_jet_softdrop",
#     "Jet2_Selected_jet_softdrop",
# )

    print("created histograms for: {}".format(i))

    # h1[i] = hist1[i].GetValue()

    # #     if str(i) != "signal":
    # #         jet1_bckg = jet1_bckg + h1[i].GetEntries() * new_weights[i]

    # h1[i].Scale(1 / dataset_events[i])

    # h2[i] = hist2[i].GetValue()
    # h2[i].Scale(1 / dataset_events[i])

    h2_2[i] = histo2d[i].GetValue()
    h2_2[i].Scale(1/dataset_events[i])


#     # h_tot[i] = hist_tot[i].GetValue()
#     # h_tot[i].Scale(1 / dataset_events[i])

    print("got values for histograms of: {}".format(i))

    print("weighted histograms for:{}".format(i))




output_file = ROOT.TFile.Open("histograms_for_analysis_flashsim_discr_pres_0_83.root", "RECREATE")


for i in processes:
    # output_file.WriteObject(h1[i], "h1_" + str(i))
    # output_file.WriteObject(h2[i], "h2_" + str(i))
    # output_file.WriteObject(h_tot[i], "h_tot" + str(i))
    output_file.WriteObject(h2_2[i], "h2_2_" + str(i))


print("written on txt")
