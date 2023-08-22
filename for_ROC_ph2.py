import ROOT
import os
import numpy as np


ROOT.EnableImplicitMT()

module_path = os.path.join(os.path.dirname(__file__), "utils.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "utils_calibration.h")
    

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')

#! PHASE2 DATASETS

bckg_path = "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file_bckg.root"

sig_path = "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file1.root"




entries1 = {}

df = {}
df_1 = {}
integrated_luminosity = 59830
dataset_events = {}
pre_selection_signal = 0
pre_selection_background = 0
post_selection_background = np.array([])

tagger = np.linspace(0.7, 1, 15)
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
    "signal": "/scratchnvme/cicco/signal_RunIISummer20UL16/",
}

files_ph2 = {'QCD_ph2': bckg_path,
         'sig_ph2': sig_path}

#processes = ['QCD_ph2']

processes = list(files_ph2.keys())

# for i in processes:
#     f = os.listdir(files.get(i))
#     num = len(f)
#     entries1[i] = []

#     for j in range(0, num):
#         entries1[i].append(str(files.get(i)) + str(f[j]))

#     df[i] = ROOT.RDataFrame("Events", entries1[i])

#     print("added file to: {}".format(i))
for i in processes:

    df[i]= ROOT.RDataFrame("MJets", str(files_ph2[i]))
    print(files_ph2[i])


new_weights = {}

for i in processes:
    print("Begin selection: {}".format(i))
    dataset_events[i] = df[i].Count().GetValue()

    #new_weights[i] = weights[i] / dataset_events[i]

    df[i] = df[i].Filter("Mfatjet_pt.size()>=2")

    df[i] = df[i].Define("Post_calibration_pt", "calibrate_pt(Mfatjet_eta, Mfatjet_pt)")


    df[i] = (
        df[i]
        .Define(
            # mu = 13, e = 11
            "FatJet_Selection",
        "Mfatjet_pt > 300 && abs(Mfatjet_eta) < 2.4 ",
        )
        .Define("Softdrop_sel_jets", "Mfatjet_msoftdrop[FatJet_Selection]")
        .Define("Pt_sel_jets", "Mfatjet_pt[FatJet_Selection]")

        # .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[FatJet_Selection]")
        # .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[FatJet_Selection]")
        # .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[FatJet_Selection]")
        # .Define("new_discriminator", "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)")
        .Define("new_discriminator", "Mfatjet_particleNetMD_XbbvsQCD[FatJet_Selection]")
    )
    df[i] = df[i].Filter("new_discriminator.size()>=2")

    df[i] = (
        df[i]
        .Define(
            "sorted_FatJet_particleNet_HbbvsQCD",
            "Reverse(Argsort(new_discriminator))",
        )
        .Define("Jet1_index", "sorted_FatJet_particleNet_HbbvsQCD[0]")
        .Define("Jet2_index", "sorted_FatJet_particleNet_HbbvsQCD[1]")
    )
    df[i] = (df[i].Filter(
        "Softdrop_sel_jets[Jet1_index]> 40 && Softdrop_sel_jets[Jet2_index]> 40"
    )
    .Filter("Pt_sel_jets[Jet1_index]> 300 && Pt_sel_jets[Jet1_index]<500 && Pt_sel_jets[Jet2_index]> 300 && Pt_sel_jets[Jet2_index]<500")
    )
    if str(i) != "sig_ph2":
        pre_selection_background = (
            pre_selection_background + df[i].Count().GetValue() #* new_weights[i]
        )
        print("preselection background: ", pre_selection_background)
    else:
        pre_selection_signal = df[i].Count().GetValue() #* new_weights[i]
        print("preselection signal: ", pre_selection_signal)


for j in range(len(tagger)):
    for i in processes:
        if str(i) != "sig_ph2":
            temp = temp + (
                df[i]
                .Filter("new_discriminator[Jet1_index]>" + str(tagger[j]))
                .Count()
                .GetValue()
                #* new_weights[i]
            )
        else:
            temp_sig = (
                df[i]
                .Filter("new_discriminator[Jet1_index]>" + str(tagger[j]))
                .Count()
                .GetValue()
                #* new_weights[i]
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

np.savetxt("tagger_values_phase2_QCD.txt", tagger)
np.savetxt("efficiency_phase2_QCD.txt", efficiency)
np.savetxt("rejection_phase2_QCD.txt", rejection)


print("written on txt")
