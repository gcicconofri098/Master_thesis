import ROOT
import os
import numpy as np
from decimal import *
import re

ROOT.EnableImplicitMT()

module_path = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils.h")
module_path2 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/nb.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_calibration.h")
module_path_4 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_higgs_within_nbd.h")


ROOT.gStyle.SetOptStat(0)


ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path2}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_4}"')

ROOT.gStyle.SetPaintTextFormat("1.f")


hist_nb0 = {}
hist_nb1 = {}
hist_nb2 = {}
hist_delta ={}
hist_discr1 = {}
hist_discr2 = {}
hist_discr = {}


h_discr1 = {}
h_discr2 = {}
h_discr = {}


h_nb0 = {}
h_nb1 = {}
h_nb2 = {}
h_delta = {}

entries1 = {}
events = {}
events_chain = {}
full_chain = {}
df = {}
dataset_events = {}

h_clone_discr1 = {}

h_pt_leading_jet = {}


integrated_luminosity = 59830

histos = {}


temp = 0
files = {
    # "QCD1_full": "/scratchnvme/cicco/QCD1/",
    # "QCD2_full": "/scratchnvme/cicco/QCD2/",
    # "QCD3_full": "/scratchnvme/cicco/QCD3/",
    # "QCD4_full": "/scratchnvme/cicco/QCD4/",
    # "QCD5_full": "/scratchnvme/cicco/QCD5/",
    # "QCD6_full": "/scratchnvme/cicco/QCD6/",
    # "QCD7_full": "/scratchnvme/cicco/QCD7/",
    # "QCD8_full": "/scratchnvme/cicco/QCD8/",
#    "old_signal_full": "/scratchnvme/cicco/signal/",
#    "signal_full": "/scratchnvme/cicco/signal_RunIISummer20UL16/",
    "QCD4_flash": "/scratchnvme/cicco/QCD4_flash_new_training/",
    "QCD5_flash": "/scratchnvme/cicco/QCD5_flash_new_training/",
    "QCD6_flash": "/scratchnvme/cicco/QCD6_flash_new_training/",
    "QCD7_flash": "/scratchnvme/cicco/QCD7_flash_new_training/",
    "QCD8_flash": "/scratchnvme/cicco/QCD8_flash_new_training/",
    #"signal_flash": "/scratchnvme/cicco/signal_RunIISummer20UL16_flash/",
    # "QCD_ph2": bckg_path,
    # "signal_ph2": sig_path
    }
weights={
    "QCD1_full": 27990000 * integrated_luminosity,
    "QCD2_full": 1712000 * integrated_luminosity,
    "QCD3_full": 347700 * integrated_luminosity,
    "QCD4_full": 32100 * integrated_luminosity,
    "QCD5_full": 6831 * integrated_luminosity,
    "QCD6_full": 1207 * integrated_luminosity,
    "QCD7_full": 119.9 * integrated_luminosity,
    "QCD8_full": 25.24 * integrated_luminosity,
    "signal_full": 0.01053 * integrated_luminosity,
    "QCD4_flash": 32100 * integrated_luminosity,
    "QCD5_flash": 6831 * integrated_luminosity,
    "QCD6_flash": 1207 * integrated_luminosity,
    "QCD7_flash": 119.9 * integrated_luminosity,
    "QCD8_flash": 25.24 * integrated_luminosity,
    "signal_flash": 0.01053 * integrated_luminosity,
}


n_events = {
    "QCD1_full": 79857456,
    "QCD2_full": 61542214,
    "QCD3_full": 56214199,
    "QCD4_full": 61097673,
    "QCD5_full": 47314826,
    "QCD6_full": 15230975,
    "QCD7_full": 11887406,
    "QCD8_full": 5710430,
    "signal_full": 540000,
    "QCD4_flash": 61097673,
    "QCD5_flash": 47314826,
    "QCD6_flash": 15230975,
    "QCD7_flash": 11887406,
    "QCD8_flash": 5710430,
    "signal_flash": 540000,
}



#processes = list(files.keys())
processes = ['QCD4_flash', 'QCD5_flash', 'QCD6_flash','QCD7_flash','QCD8_flash']#,'signal_flash']
#processes = ['signal_full', 'signal_flash']# 'signal_ph2']
for i in processes:
    if str(i) != 'signal_ph2' and str(i)!= 'QCD_ph2':
        f = os.listdir(files.get(i))
        num = len(f)
        entries1[i] = []
        events[i] = []
        if str(i) == 'QCD4_flash' or str(i) == 'QCD5_flash' or str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 
            print("creating the TChains")
            events_chain[i] = ROOT.TChain("Events")
            full_chain[i] = ROOT.TChain("FullSim")

        for j in range(0, num):
            entries1[i].append(str(files.get(i)) + str(f[j]))

            if str(i) == 'QCD4_flash' or str(i) == 'QCD5_flash' or str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 
                
                print("adding files to the TChains")
                events_chain[i].Add(str(files.get(i)) + str(f[j]))
                full_chain[i].Add(str(files.get(i)) + str(f[j]))
        if str(i) == 'QCD4_flash' or str(i) == 'QCD5_flash' or str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 
            events_chain[i].AddFriend(full_chain[i])

            df[i] = ROOT.RDataFrame(events_chain[i])
        
        else:
            df[i] = ROOT.RDataFrame("Events", entries1[i])
        print("added file to: {}".format(i))
    else:
        df[i]= ROOT.RDataFrame("MJets", str(files[i]))

print("finished all trees")

for i in processes:
    histos[i] = {}
    df[i] = df[i].Define("higgs_flag", "has_H_within_0_8(GenPart_eta, GenPart_phi, GenPart_pdgId, GenJetAK8_eta, GenJetAK8_phi)")

    histos[i]['1d_higgs_flag'] = df[i].Histo1D(("Higgs flag", "Higgs flag; Flag Value; Events", 4, -1, 2), "higgs_flag").GetValue()


QCD_higgs_flag =  histos[str(processes[0])]['1d_higgs_flag'].Clone()

for i in processes:
    if str(i) == str(processes[0]):
        continue
    else:
        QCD_higgs_flag.Add(histos[i]['1d_higgs_flag'])



c1 = ROOT.TCanvas("c1", "flashsim higgs flag", 5000, 3500)

QCD_higgs_flag.Draw("HIST")
QCD_higgs_flag.SetTitle("Higgs flag on QCD; Flag values; Events")
QCD_higgs_flag.SetLineWidth(2)

c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training/flashsim_higgs_flag.pdf")
