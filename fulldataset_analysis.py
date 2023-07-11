import ROOT
import os
import numpy as np

module_path = os.path.join(os.path.dirname(__file__), "utils.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')


#ROOT.EnableImplicitMT()

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
    "signal": "/scratchnvme/cicco/signal/",
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

    # df[i] = (
    #     df[i]
    #     .Filter("HLT_PFJet500")
    #     .Filter("HLT_PFHT1050")
    #     .Filter("HLT_AK8PFJet360_TrimMass30")
    #     .Filter("HLT_AK8PFJet380_TrimMass30")
    #     .Filter("HLT_AK8PFJet400_TrimMass30")
    #     .Filter("HLT_AK8PFHT800_TrimMass50")
    #     .Filter("HLT_AK8PFHT750_TrimMass50")
    #     .Filter("HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17")
    # )

    df[i] = df[i].Filter("nFatJet>=2")

    df[i] = (
        df[i]
        .Define(
            "Events_Selection",
            "FatJet_pt > 300 && abs(FatJet_eta) < 2.4"
        )
        .Define("Softdrop_sel_jets", "FatJet_msoftdrop[Events_Selection]")
        .Define("Discriminator_sel_jets", "FatJet_deepTagMD_HbbvsQCD[Events_Selection]")


    )

    df[i] = df[i].Filter("Discriminator_sel_jets.size()>=2")

    df[i] = (
        df[i]
        .Define(
            "sorted_FatJet_deepTagMD_HbbvsQCD",
            "Reverse(Argsort(Discriminator_sel_jets))",
        )
        .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
        .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
    )

    df[i] = df[i].Filter(
        "Softdrop_sel_jets[Jet1_index]> 50 && Softdrop_sel_jets[Jet2_index]> 50"
    )

    df[i] = (
        df[i]
        .Define("Jet1_Selected_jet", "Softdrop_sel_jets[Jet1_index]")
        .Define("Jet2_Selected_jet", "Softdrop_sel_jets[Jet2_index]")
        .Define("Jet1_Selected_jets_discriminator", "Discriminator_sel_jets[Jet1_index]")
        .Define("Jet2_Selected_jets_discriminator", "Discriminator_sel_jets[Jet2_index]")
        .Define("Sum_selected_jets", "Jet1_Selected_jet + Jet2_Selected_jet")
    )




    if str(i) != "signal":
        pre_selection_background = (
            pre_selection_background + df[i].Count().GetValue() * new_weights[i]
        )
        print("preselection background: ", pre_selection_background)
    else:
        pre_selection_signal = df[i].Count().GetValue() * new_weights[i]
        print("preselection signal: ", pre_selection_signal)

    df[i] = df[i].Filter("Discriminator_sel_jets[Jet1_index] > 0.5")

    if str(i) != "signal":
        post_selection_background = (
            post_selection_background + df[i].Count().GetValue() * new_weights[i]
        )
    else:
        post_selection_signal = df[i].Count().GetValue() * new_weights[i]
    
    print("post selection background : ", post_selection_background)

    print("finished jets selection for dataset: {}".format(i))


print("efficiency: ", post_selection_signal / pre_selection_signal)

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
        (str(i), str(i) + "; Soft Drop mass; Events", 25, 0, 500), "Jet1_Selected_jet"
    )

    hist2[i] = df[i].Histo1D(
        (str(i), str(i) + "; Soft Drop mass; Events", 25, 0, 500), "Jet2_Selected_jet"
    )

    hist_tot[i] = df[i].Histo1D(
        (str(i), str(i) + "; Soft Drop mass; Events", 25, 0, 500), "Softdrop_sel_jets"
    )


    histo2d[i] = df[i].Histo2D(
        ("Jet1 vs Jet2", "Jet1 vs Jet2; Jet1; Jet2", 20, 0,1, 20, 0,1),
        "Jet1_Selected_jets_discriminator",
        "Jet2_Selected_jets_discriminator",

    )

    print("created histograms for: {}".format(i))

    h1[i] = hist1[i].GetValue()

    #     if str(i) != "signal":
    #         jet1_bckg = jet1_bckg + h1[i].GetEntries() * new_weights[i]

    h1[i].Scale(1 / dataset_events[i])
    h2[i] = hist2[i].GetValue()

    if str(i) != "signal":
        jet2_bckg = jet2_bckg + h2[i].GetEntries() * new_weights[i]

    h2[i].Scale(1 / dataset_events[i])

    h2_2[i] = histo2d[i].GetValue()
    h2_2[i].Scale(1 / dataset_events[i])

    h_tot[i] = hist_tot[i].GetValue()
    h_tot[i].Scale(1 / dataset_events[i])

    print("got values for histograms of: {}".format(i))

    print("weighted histograms for:{}".format(i))


# post_selection_events = n_events + h1["signal"].GetEntries()*new_weights[i] +h2["signal"].GetEntries()*new_weights[i]
#! EFFICIENCY ESTIMATION AND BACKGROUND REJECTION

# rejection = (pre_selection_background -post_selection_background)/pre_selection_background

# print("Efficiency: ",efficiency)
# print("Background rejection: ",rejection)


output_file = ROOT.TFile.Open("histograms_from_analysis_with_0_86_no_veto.root", "RECREATE")


for i in processes:
    output_file.WriteObject(h1[i], "h1_" + str(i))
    output_file.WriteObject(h2[i], "h2_" + str(i))
    output_file.WriteObject(h_tot[i], "h_tot" + str(i))
    output_file.WriteObject(h2_2[i], "h2_2_" + str(i))


print("written on txt")
