import ROOT
import os
import numpy as np


ROOT.EnableImplicitMT()

entries1 = {}

df = {}
df_1 = {}
integrated_luminosity = 59830
dataset_events = {}
pre_selection_signal = 0
pre_selection_background = 0
post_selection_background = np.array([])

tagger = np.linspace(0.7, 1, 20)
print(tagger)
efficiency = np.array([])
post_selection_signal = np.array([])
rejection = np.array([])

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
    "signal": "/scratchnvme/cicco/signal/",
}


processes = list(files.keys())

for i in processes:
    f = os.listdir(files.get(i))
    num = len(f)
    entries1[i] = []

    for j in range(0, num):
        entries1[i].append(str(files.get(i)) + str(f[j]))

    df[i] = ROOT.RDataFrame("Events", entries1[i])

    print("added file to: {}".format(i))


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
            "FatJet_pt > 300 && abs(FatJet_eta) < 2.4",  # && 80 <FatJet_msoftdrop && FatJet_msoftdrop<170 ",
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
        "Softdrop_sel_jets[Jet1_index]>40 && Softdrop_sel_jets[Jet2_index]>40"
    )
    if str(i) != "signal":
        pre_selection_background = (
            pre_selection_background + df[i].Count().GetValue() * new_weights[i]
        )
        print("preselection background: ", pre_selection_background)
    else:
        pre_selection_signal = df[i].Count().GetValue() * new_weights[i]
        print("preselection signal: ", pre_selection_signal)


for j in range(len(tagger)):
    for i in processes:
        if str(i) != "signal":
            temp = temp + (
                df[i]
                .Filter("Discriminator_sel_jets[Jet1_index]>" + str(tagger[j]))
                .Count()
                .GetValue()
                * new_weights[i]
            )
        else:
            temp_sig = (
                df[i]
                .Filter("Discriminator_sel_jets[Jet1_index]>" + str(tagger[j]))
                .Count()
                .GetValue()
                * new_weights[i]
            )

    post_selection_signal = np.append(post_selection_signal, temp_sig)
    # print("postselection signal: ", temp_sig)

    post_selection_background = np.append(post_selection_background, temp)
    # print("postselection backgrond: ", temp)

    print("Finished value of the cut: {}".format(tagger[j]))

    efficiency = np.append(
        efficiency, (post_selection_signal[j] / pre_selection_signal)
    )

    print("efficiency", efficiency)

    rejection = np.append(
        rejection,
        (
            (pre_selection_background - post_selection_background[j])
            / pre_selection_background
        ),
    )
    print("background rejection", rejection)
    temp = 0
print("finished creating the arrays")

bg_efficiency = 1 - rejection

print("finished working on the macro")

np.savetxt("efficiency_test.txt", efficiency)
np.savetxt("rejection_test.txt", rejection)


print("written on txt")
