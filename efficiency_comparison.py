import ROOT
import os
import numpy as np
import matplotlib.pyplot as plt

ROOT.EnableImplicitMT()

module_path = os.path.join(os.path.dirname(__file__), "utils.h")
module_path2 = os.path.join(os.path.dirname(__file__), "nb.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "utils_calibration.h")


#plt.rcParams['text.usetex'] = True

ROOT.gStyle.SetOptStat(0)


ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path2}"')

#! PHASE2 DATASETS

bckg_path = "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file_bckg.root"

sig_path = (
    "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file1.root"
)

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
    # "QCD4_flash": "/scratchnvme/cicco/QCD4_good_flash/",
    # "QCD5_flash": "/scratchnvme/cicco/QCD5_good_flash/",
    # "QCD6_flash": "/scratchnvme/cicco/QCD6_good_flash/",
    # "QCD7_flash": "/scratchnvme/cicco/QCD7_good_flash/",
    # "QCD8_flash": "/scratchnvme/cicco/QCD8_good_flash/",
    "signal_flash": "/scratchnvme/cicco/signal_RunIISummer20UL16_flash/",
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



processes = list(files.keys())
#processes = ['QCD6_flash','QCD7_flash','QCD8_flash','signal_flash']
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

remaining_events = {}

for i in processes:
    print(f"weight for sample {i} is: {weights[i]/n_events[i]} without 2.27 luminosity factor")

for i in processes:
    print("Begin selection: {}".format(i))


    if str(i) == 'QCD4_flash' or str(i) == 'QCD5_flash' or str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 
        
        print(f"number of events in dataset {i} is {df[i].Count().GetValue()}")
        df[i] = df[i].Filter("FatJet_pt.size()!=0", "number of events that enter the selection (already nfat>2, gen_pt req)")

        df[i] = df[i].Filter("!FullSim.FatJet_eta.empty()")

        df[i] = (df[i]
        .Define("matching_index" , "lepton_matching_index(FatJet_eta, FatJet_phi, GenJetAK8_eta, GenJetAK8_phi)")
        .Define("Post_calibration_pt", "calibrate_pt_double_n_bins(FatJet_eta, FatJet_pt)")
        .Define("Post_calibration_softdrop", "calibrate_pt_double_n_bins_softdrop(FatJet_eta, FatJet_pt, FatJet_msoftdrop)")

        .Define("HbbvsQCD_discriminator_lower_limited", "Where(FatJet_particleNetMD_XbbvsQCD>=0,  FatJet_particleNetMD_XbbvsQCD, 0)")
        .Define("HbbvsQCD_discriminator_limited", "Where(HbbvsQCD_discriminator_lower_limited<1, HbbvsQCD_discriminator_lower_limited, 0.9995) ")
        )
        df[i] = (df[i]
        .Define("Selection_pt", "Post_calibration_pt> 300")
        
        .Define("new_discriminator", "HbbvsQCD_discriminator_limited[Selection_pt]")
        .Define("FatJet_eta_sel", "FatJet_eta[Selection_pt]")
        .Define("FatJet_phi_sel", "FatJet_phi[Selection_pt]")
        .Define("Softdrop_sel_jets", "Post_calibration_softdrop[Selection_pt]")
        .Define("Selected_pt", "Post_calibration_pt[Selection_pt]")
        )

        df[i] = df[i].Filter("Selected_pt.size()>=2", "events after request on fat_pt")

        df[i] = df[i].Define("Second_selection", "abs(FatJet_eta_sel) < 2.4")

        df[i] = df[i].Define("Second_selection_eta", "FatJet_eta_sel[Second_selection]")
        df[i] = df[i].Define("Second_selection_discriminator", "new_discriminator[Second_selection]")
        df[i] = df[i].Define("Second_selection_mass", "Softdrop_sel_jets[Second_selection]")
        df[i] = df[i].Define("Second_selection_pt", "Selected_pt[Second_selection]")
        df[i] = df[i].Define("Second_selection_phi", "FatJet_phi_sel[Second_selection]")

        
        df[i] = df[i].Filter("Second_selection_mass.size()>=2", "events after request on fat eta")

        df[i] = (
            df[i]
            .Define(
            "sorted_FatJet_deepTagMD_HbbvsQCD",
            "Reverse(Argsort(Second_selection_discriminator))",
        )
            .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
            .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
        )
        df[i] = df[i].Filter(
        "Second_selection_mass[Jet1_index]> 40 && Second_selection_mass[Jet2_index]> 40", "events after mass req"
        )

        df[i] = (df[i]
                .Define("jet1_discr", "Second_selection_discriminator[Jet1_index]")
                .Define("jet1_softdrop", "Second_selection_mass[Jet1_index]")
                .Define("jet2_discr", "Second_selection_discriminator[Jet2_index]")
                .Define("jet2_softdrop", "Second_selection_mass[Jet2_index]")

        )
        df[i] = df[i].Filter("jet1_softdrop>105 && jet1_softdrop<135 && jet2_softdrop >105 && jet2_softdrop <135", "events after mass window")

       

    else: #*fullsim
        print(f"number of events in dataset {i} is {df[i].Count().GetValue()}")

        df[i] = df[i].Filter("GenJetAK8_pt[0]>250 && GenJetAK8_pt[1]>250", "number of events after gen_pt")

        df[i] = df[i].Filter("FatJet_pt.size()>=2", "number of events after nfatjets>=2")

        df[i] = df[i].Define("Selection_pt", "FatJet_pt> 300")

        df[i] = (df[i]
            .Define("Selected_pt", "FatJet_pt[Selection_pt]")
            .Define("Selected_mass", "FatJet_msoftdrop[Selection_pt]")
            .Define("Selected_eta", "FatJet_eta[Selection_pt]")
            .Define("Selected_phi", "FatJet_phi[Selection_pt]")
            .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[Selection_pt]")
            .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[Selection_pt]")
            .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[Selection_pt]")
            .Define("new_discriminator", "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)")        

        )
        df[i] = df[i].Filter("Selected_pt.size()>=2", "number of events after pt selection")
        
        df[i] = df[i].Define("Second_selection", "abs(Selected_eta)<2.4")

        df[i] = (df[i]
            .Define("Second_selection_discriminator", "new_discriminator[Second_selection]")
            .Define("Second_selection_mass", "Selected_mass[Second_selection]")
            .Define("Second_selection_pt", "Selected_pt[Second_selection]")
            .Define("Second_selection_phi", "Selected_phi[Second_selection]")
            .Define("Second_selection_eta", "Selected_eta[Second_selection]")
        )

        df[i] = df[i].Filter("Second_selection_discriminator.size()>=2", "events after request on fat_eta")

        df[i] = (
            df[i]
            .Define(
            "sorted_FatJet_deepTagMD_HbbvsQCD",
            "Reverse(Argsort(Second_selection_discriminator))")
        )

        df[i] = (df[i]
            .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
            .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
        )
        df[i] = df[i].Filter(
        "Second_selection_mass[Jet1_index]> 40 && Second_selection_mass[Jet2_index]> 40",  "events after mass req"
        )           
        df[i] = (df[i]
        .Define("jet1_discr", "Second_selection_discriminator[Jet1_index]")
        .Define("jet2_discr", "Second_selection_discriminator[Jet2_index]")

        .Define("jet1_softdrop", "Second_selection_mass[Jet1_index]")
        .Define("jet2_softdrop", "Second_selection_mass[Jet2_index]")
        )

        #df[i] = df[i].Filter("jet1_softdrop>115 && jet1_softdrop<145 && jet2_softdrop >115 && jet2_softdrop <145", "events after mass window")






#TODO FROM HERE ON, DEFINITION OF THE NB VARIABLES IS MADE

    # if str(i) !=  'signal_ph2' and str(i) != 'QCD_ph2':

    #     df[i] = df[i].Define(
    #     "GenPart_IsLastB",
    #     "(abs(GenPart_pdgId) >=500 && abs(GenPart_pdgId) < 600) | (abs(GenPart_pdgId) >=5000 && abs(GenPart_pdgId) < 6000) && (GenPart_statusFlags &(1<<13))!=0",
    # )

    #     df[i] = df[i].Define("GenPart_IsLastB_m", "Take(GenPart_IsLastB, GenPart_genPartIdxMother)")

    #     df[i] = df[i].Define(
    #         "GenPart_parent_IsNotLastB",
    #         "(GenPart_genPartIdxMother == -1 | GenPart_IsLastB_m ==0)",
    #     )

    #     df[i] = (df[i].Define(
    #         "GenPart_IsGoodB", "GenPart_IsLastB && GenPart_parent_IsNotLastB")
    #         .Define("GenPart_eta_good", "GenPart_eta[GenPart_IsGoodB]")
    #         .Define("GenPart_phi_good", "GenPart_phi[GenPart_IsGoodB]")
    #     )


    # if str(i) == 'QCD4_flash' or str(i) == 'QCD5_flash' or str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash':

    #     df[i] = df[i].Define("MgenjetAK8_nbFlavour", "count_nHadrons(GenPart_eta_good, GenPart_phi_good, GenJetAK8_eta, GenJetAK8_phi)").Define("Matching_nb_flavour", "Take(MgenjetAK8_nbFlavour, matching_index[Selection])")
    #     #df[i] = df[i].Define("Matching_nb_flavour", "FatJet_nBhadrons[Selection]")

    # elif str(i) == 'QCD_ph2' or str(i) == 'signal_ph2':

    #     df[i] = df[i].Define("Matching_nb_flavour", "Take(MgenjetAK8_nbFlavour, new_index[Selection])")



    # else: #* fullsim
    #     df[i] = (df[i].Define("MgenjetAK8_nbFlavour_manual", "count_nHadrons(GenPart_eta_good, GenPart_phi_good, GenJetAK8_eta, GenJetAK8_phi)")
    #              .Define("Matching_nb_flavour", "Take(MgenjetAK8_nbFlavour_manual, FatJet_genJetAK8Idx[Selection])")
    #             #.Define("Delta", "Matching_nb_flavour - FatJet_nBHadrons[Selection]")
    #     )

    # df[i] = (
    #         df[i]
    #         .Define("Matching_nb_0", "Matching_nb_flavour==0")
    #         .Define("Matching_nb_1", "Matching_nb_flavour == 1")
    #         .Define("Matching_nb_2", "Matching_nb_flavour == 2")
    #         .Define("discriminator_nb_0", "new_discriminator[Matching_nb_0]")
    #         .Define("discriminator_nb_1", "new_discriminator[Matching_nb_1]")
    #         .Define("discriminator_nb_2", "new_discriminator[Matching_nb_2]")   
    #         .Define("leading_jet_discriminator_nb_0", "discriminator_nb_0[0]")
    #         .Define("leading_jet_discriminator_nb_1", "discriminator_nb_1[0]")
    #         .Define("leading_jet_discriminator_nb_2", "discriminator_nb_2[0]")      
    #     )

for i in processes:

    #if str(i) == 'signal_full' or str(i) == 'signal_flash':

    df[i].Report().Print()

    remaining_events[i] = df[i].Count().GetValue()

    # if remaining_events[i]!=0:
    #     if str(i) == 'QCD4_flash' or str(i) == 'QCD5_flash' or str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 

    #         df[i].Snapshot("Events", "snapshots_no_nb/" + str(i) + "_no_pt_window_calibrated_mass_no_nb.root", {
    #                                 #"leading_jet_discriminator_nb_0", 
    #                                 #"leading_jet_discriminator_nb_1", 
    #                                 #"leading_jet_discriminator_nb_2",
    #                                 #"discriminator_nb_0",
    #                                 #"discriminator_nb_1",
    #                                 #"discriminator_nb_2",
    #                                 #"Matching_nb_flavour", 
    #                                 "Second_selection_pt",
    #                                 "MET_pt",
    #                                 "jet1_discr",
    #                                 "jet2_discr", 
    #                                 "Second_selection_discriminator", 
    #                                 "jet1_softdrop",
    #                                 "jet2_softdrop", 
    #                                 "Second_selection_mass", 
    #                                 "Second_selection_eta", 
    #                                 "Second_selection_phi",
    #                                 #"Matching_hadron_flavour",
    #                                 #"Matching_parton_flavour"
    #                                 })
            
    #     else:

    #         df[i].Snapshot("Events", "snapshots_no_nb/" + str(i) + "_no_pt_window_no_nb.root", {
    #                                 #"leading_jet_discriminator_nb_0", 
    #                                 #"leading_jet_discriminator_nb_1", 
    #                                 #"leading_jet_discriminator_nb_2",
    #                                 #"discriminator_nb_0",
    #                                 #"discriminator_nb_1",
    #                                 #"discriminator_nb_2",
    #                                 #"Matching_nb_flavour", 
    #                                 "Second_selection_pt",
    #                                 "MET_pt",
    #                                 "jet1_discr",
    #                                 "jet2_discr", 
    #                                 "Second_selection_discriminator", 
    #                                 "jet1_softdrop",
    #                                 "jet2_softdrop", 
    #                                 "Second_selection_mass", 
    #                                 "Second_selection_eta", 
    #                                 "Second_selection_phi",
    #                                 #"Matching_hadron_flavour",
    #                                 #"Matching_parton_flavour"
    #                                 })
            
        

    print(f"snapshotted dataset {i}")

