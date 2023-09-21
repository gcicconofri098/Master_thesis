import ROOT
#import CMS_lumi, tdrstyle
import os
import numpy as np
import matplotlib.pyplot as plt

ROOT.EnableImplicitMT()

#tdrstyle.SetTDRStyle()

module_path = os.path.join(os.path.dirname(__file__), "utils.h")
module_path2 = os.path.join(os.path.dirname(__file__), "nb.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "utils_calibration.h")

ROOT.gStyle.SetOptStat(0)


ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path2}"')


# #change the CMS_lumi variables (see CMS_lumi.py)
# #CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
# #CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
# CMS_lumi.writeExtraText = 1
# CMS_lumi.extraText = "Private Work"
# CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)





#! PHASE2 DATASETS

bckg_path = "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file_bckg.root"

sig_path = (
    "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file1.root"
)

dict_discr_hist1 = {}
dict_discr_hist2 = {}
dict_discr_hist_tot = {}

dict_softdrop_hist1 = {}
dict_softdrop_hist2 = {}
dict_softdrop_hist_tot = {}

entries1 = {}
events = {}
events_chain = {}
full_chain = {}
df = {}
dataset_events = {}


temp = 0
files = {
    "QCD1_full": "/scratchnvme/cicco/QCD1/",
    "QCD2_full": "/scratchnvme/cicco/QCD2/",
    "QCD3_full": "/scratchnvme/cicco/QCD3/",
    "QCD4_full": "/scratchnvme/cicco/QCD4/",
    "QCD5_full": "/scratchnvme/cicco/QCD5/",
    "QCD6_full": "/scratchnvme/cicco/QCD6/",
    "QCD7_full": "/scratchnvme/cicco/QCD7/",
    "QCD8_full": "/scratchnvme/cicco/QCD8/",
    "signal_full": "/scratchnvme/cicco/signal_RunIISummer20UL16/",
    "QCD6_flash": "/scratchnvme/cicco/QCD6_good_flash/",
    "QCD7_flash": "/scratchnvme/cicco/QCD7_good_flash/",
    "QCD8_flash": "/scratchnvme/cicco/QCD8_good_flash/",
    "signal_flash": "/scratchnvme/cicco/signal_RunIISummer20UL16_flash/",
    "QCD_ph2": bckg_path,
    "signal_ph2": sig_path
    }

processes = list(files.keys())
#processes = ['QCD6_flash','QCD7_flash','QCD8_flash','signal_flash']
#processes = ['signal_full', 'signal_flash', 'signal_ph2']
for i in processes:
    if str(i) != 'signal_ph2' and str(i)!= 'QCD_ph2':
        f = os.listdir(files.get(i))
        num = len(f)
        entries1[i] = []
        events[i] = []
        print("creating the TChains")
        if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 
            events_chain[i] = ROOT.TChain("Events")
            full_chain[i] = ROOT.TChain("FullSim")

        for j in range(0, num):
            entries1[i].append(str(files.get(i)) + str(f[j]))
            if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 
                
                print("adding files to the TChains")
                events_chain[i].Add(str(files.get(i)) + str(f[j]))
                full_chain[i].Add(str(files.get(i)) + str(f[j]))
        if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 
            events_chain[i].AddFriend(full_chain[i])

            df[i] = ROOT.RDataFrame(events_chain[i])
        
            #print(df[i].GetColumnNames())
        else:
            df[i] = ROOT.RDataFrame("Events", entries1[i])
        print("added file to: {}".format(i))
    else:
        df[i]= ROOT.RDataFrame("MJets", str(files[i]))
    

print("finished all trees")

for i in processes:
    print("Begin selection: {}".format(i))
    dict_discr_hist1[i] = {}
    dict_discr_hist2[i] = {}
    dict_discr_hist_tot[i] = {}

    dict_softdrop_hist1[i] = {}
    dict_softdrop_hist2[i] = {}
    dict_softdrop_hist_tot[i] = {}


    dataset_events[i] = df[i].Count().GetValue()
    
    print(f"number of events in dataset {i} is {dataset_events[i]}")


#* FLASHSIM DATASET

    if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 
        
        
        df[i] = (df[i]
        .Define("HbbvsQCD_discriminator_lower_limited", "Where(FatJet_particleNetMD_XbbvsQCD>=0,  FatJet_particleNetMD_XbbvsQCD, 0)")
        .Define("HbbvsQCD_discriminator_limited", "Where(HbbvsQCD_discriminator_lower_limited<1, HbbvsQCD_discriminator_lower_limited, 0.9995) ")
                
        )

        df[i] = (
            df[i]
            .Define(
            "sorted_HbbvsQCD_discriminator_limited",
            "Reverse(Argsort(HbbvsQCD_discriminator_limited))",
        )
            .Define("Jet1_index", "sorted_HbbvsQCD_discriminator_limited[0]")
            .Define("Jet2_index", "sorted_HbbvsQCD_discriminator_limited[1]")
        )
        df[i] = df[i].Define("Jet1_discriminator", "HbbvsQCD_discriminator_limited[Jet1_index]")
        df[i] = df[i].Define("Jet2_discriminator", "HbbvsQCD_discriminator_limited[Jet2_index]")

        df[i] = df[i].Define("Jet1_softdrop", "FatJet_msoftdrop[Jet1_index]")
        df[i] = df[i].Define("Jet2_softdrop", "FatJet_msoftdrop[Jet2_index]")

    #TODO NO_CUT        

        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 80, 0, 1), "HbbvsQCD_discriminator_limited")

  
        dict_discr_hist1[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 80, 0, 1), "Jet1_discriminator")


        dict_discr_hist2[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 100, 0, 400), "FatJet_msoftdrop")

        dict_softdrop_hist1[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 100, 0, 400), "Jet2_softdrop")

        df[i] = df[i].Filter("!FullSim.FatJet_eta.empty()")

  
    #TODO PT_WINDOW
        df[i] = (df[i]
        .Define("matching_index" , "lepton_matching_index(FatJet_eta, FatJet_phi, GenJetAK8_eta, GenJetAK8_phi)")
        .Define("Post_calibration_pt", "calibrate_pt(FatJet_eta, FatJet_pt)")

        .Define("Pt_Selection", "Post_calibration_pt> 300 && Post_calibration_pt< 500 ")# && matching_index>=0 
        
        .Define("pt_after_pt_sel", "Post_calibration_pt[Pt_Selection]")
        .Define("discr_after_pt_sel", "HbbvsQCD_discriminator_limited[Pt_Selection]")
        .Define("softdrop_after_pt_sel", "FatJet_msoftdrop[Pt_Selection]")
        .Define("eta_after_pt_sel", "FatJet_eta[Pt_Selection]")
        .Define("phi_after_pt_sel", "FatJet_phi[Pt_Selection]")
        )

        df[i] = df[i].Filter("discr_after_pt_sel.size()>=2")

        df[i] = df[i].Redefine("Jet1_discriminator", "discr_after_pt_sel[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_discriminator", "discr_after_pt_sel[Jet2_index]")

        df[i] = df[i].Redefine("Jet1_softdrop", "softdrop_after_pt_sel[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_softdrop", "softdrop_after_pt_sel[Jet2_index]")
        


        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 80, 0, 1), "discr_after_pt_sel")

        dict_discr_hist1[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 100, 0, 400), "softdrop_after_pt_sel")

        dict_softdrop_hist1[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 100, 0, 400), "Jet2_softdrop")


    #TODO ETA_CUT

        df[i] = (df[i].Define("Eta_Selection", "abs(eta_after_pt_sel) < 2.4 ")

        .Define("discr_after_eta_sel", "discr_after_pt_sel[Eta_Selection]")
        .Define("softdrop_after_eta_sel", "softdrop_after_pt_sel[Eta_Selection]")
        .Define("eta_after_eta_sel", "eta_after_pt_sel[Eta_Selection]")
        .Define("phi_after_eta_sel", "phi_after_pt_sel[Eta_Selection]")
        )

        df[i] = df[i].Filter("discr_after_eta_sel.size()>=2")

        df[i] = df[i].Redefine("Jet1_discriminator", "discr_after_eta_sel[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_discriminator", "discr_after_eta_sel[Jet2_index]")

        df[i] = df[i].Redefine("Jet1_softdrop", "softdrop_after_eta_sel[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_softdrop", "softdrop_after_eta_sel[Jet2_index]")



        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 80, 0, 1), "discr_after_eta_sel")

        dict_discr_hist1[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 100, 0, 400), "softdrop_after_eta_sel")

        dict_softdrop_hist1[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 100, 0, 400), "Jet2_softdrop")


    #TODO CLEANING

        df[i] = (df[i].Define("fatjets_cleaning", "fatjet_lepton_isolation(eta_after_eta_sel, phi_after_eta_sel, Electron_pt, Electron_eta, Electron_phi, Electron_pfRelIso03_all, 11)  && fatjet_lepton_isolation(eta_after_eta_sel, phi_after_eta_sel, Muon_pt, Muon_eta, Muon_phi, Muon_pfRelIso03_all, 13)")

        .Define("discr_after_cleaning", "discr_after_eta_sel[fatjets_cleaning]")
        .Define("softdrop_after_cleaning", "softdrop_after_eta_sel[fatjets_cleaning]")

        )

        df[i] = df[i].Filter("discr_after_cleaning.size()>=2")


        df[i] = df[i].Redefine("Jet1_discriminator", "discr_after_cleaning[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_discriminator", "discr_after_cleaning[Jet2_index]")

        df[i] = df[i].Redefine("Jet1_softdrop", "softdrop_after_cleaning[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_softdrop", "softdrop_after_cleaning[Jet2_index]")

    

        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['cleaning'] = df[i].Histo1D((str(i),str(i) + 'cleaning', 80, 0, 1), "discr_after_cleaning")

        dict_discr_hist1[i]['cleaning'] = df[i].Histo1D((str(i),str(i) + 'cleaning', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['cleaning'] = df[i].Histo1D((str(i),str(i) + 'cleaning', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['cleaning'] = df[i].Histo1D((str(i),str(i) + 'cleaning', 100, 0, 400), "softdrop_after_cleaning")

        dict_softdrop_hist1[i]['cleaning'] = df[i].Histo1D((str(i),str(i) + 'cleaning', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['cleaning'] = df[i].Histo1D((str(i),str(i) + 'cleaning', 100, 0, 400), "Jet2_softdrop")



        #df[i] = df[i].Filter("!matching_index.empty()")

        # hist2 = df[i].Histo1D((str(i),str(i), 100, 0,400), "Selected_jets")
        # h2 = hist2
        # h2.Draw()
        # print(f"events in dataset {i} after fatjet_pt window is {df[i].Count().GetValue()}")



    #TODO MASS REQUEST

        df[i] = df[i].Filter("softdrop_after_cleaning[Jet1_index] >=50 && softdrop_after_cleaning[Jet2_index] >=50")


        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 80, 0, 1), "discr_after_cleaning")

        dict_discr_hist1[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 100, 0, 400), "softdrop_after_cleaning")

        dict_softdrop_hist1[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 100, 0, 400), "Jet2_softdrop")





#* PHASE 2 DATASET


    elif str(i) == 'QCD_ph2' or str(i) == 'signal_ph2':

        print(f"number of events in dataset {i} is {df[i].Count().GetValue()}")

        df[i] = (
            df[i]
            .Define(
            "sorted_Mfatjet_particleNetMD_XbbvsQCD",
            "Reverse(Argsort(Mfatjet_particleNetMD_XbbvsQCD))",
        )
            .Define("Jet1_index", "sorted_Mfatjet_particleNetMD_XbbvsQCD[0]")
            .Define("Jet2_index", "sorted_Mfatjet_particleNetMD_XbbvsQCD[1]")
        )
        df[i] = df[i].Define("Jet1_discriminator", "Mfatjet_particleNetMD_XbbvsQCD[Jet1_index]")
        df[i] = df[i].Define("Jet2_discriminator", "Mfatjet_particleNetMD_XbbvsQCD[Jet2_index]")

        df[i] = df[i].Define("Jet1_softdrop", "Mfatjet_msoftdrop[Jet1_index]")
        df[i] = df[i].Define("Jet2_softdrop", "Mfatjet_msoftdrop[Jet2_index]")
        
    #TODO NO_CUT

        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 80, 0, 1), "Mfatjet_particleNetMD_XbbvsQCD")

        dict_discr_hist1[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 100, 0, 400), "Mfatjet_msoftdrop")

        dict_softdrop_hist1[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 100, 0, 400), "Jet2_softdrop")


    #TODO NFATJETS_REQUEST

        df[i] = df[i].Filter("Mfatjet_eta.size()>=2")


        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['nfatjets_request'] = df[i].Histo1D((str(i),str(i) + 'nfatjets_request', 80, 0, 1), "Mfatjet_particleNetMD_XbbvsQCD")

        dict_discr_hist1[i]['nfatjets_request'] = df[i].Histo1D((str(i),str(i) + 'nfatjets_request', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['nfatjets_request'] = df[i].Histo1D((str(i),str(i) + 'nfatjets_request', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['nfatjets_request'] = df[i].Histo1D((str(i),str(i) + 'nfatjets_request', 100, 0, 400), "Mfatjet_msoftdrop")

        dict_softdrop_hist1[i]['nfatjets_request'] = df[i].Histo1D((str(i),str(i) + 'nfatjets_request', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['nfatjets_request'] = df[i].Histo1D((str(i),str(i) + 'nfatjets_request', 100, 0, 400), "Jet2_softdrop")


        #print(f"Events after nfatjet request in dataset {i} is {df[i].Count().GetValue()}")

    #TODO GENJET_REQUEST

        df[i] = df[i].Filter("MgenjetAK8_pt[0]>=250 && MgenjetAK8_pt[1]>=250")
        

        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['genjet_request'] = df[i].Histo1D((str(i),str(i) + 'genjet_request', 80, 0, 1), "Mfatjet_particleNetMD_XbbvsQCD")

        dict_discr_hist1[i]['genjet_request'] = df[i].Histo1D((str(i),str(i) + 'genjet_request', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['genjet_request'] = df[i].Histo1D((str(i),str(i) + 'genjet_request', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['genjet_request'] = df[i].Histo1D((str(i),str(i) + 'genjet_request', 100, 0, 400), "Mfatjet_msoftdrop")

        dict_softdrop_hist1[i]['genjet_request'] = df[i].Histo1D((str(i),str(i) + 'genjet_request', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['genjet_request'] = df[i].Histo1D((str(i),str(i) + 'genjet_request', 100, 0, 400), "Jet2_softdrop")


        #print(f"events in dataset {i} after request on gen_pt is {df[i].Count().GetValue()}")


    #TODO PT_WINDOW

        df[i] = df[i].Define("Post_calibration_pt", "calibrate_pt(Mfatjet_eta, MgenjetAK8_pt)")
        

        df[i] = df[i].Define("Pt_Selection","Post_calibration_pt> 300 && Post_calibration_pt< 500")# && new_index>=0")

        df[i] = (df[i]
                .Define("pt_after_pt_sel", "Post_calibration_pt[Pt_Selection]")
                .Define("eta_after_pt_sel", "Mfatjet_eta[Pt_Selection]")
                .Define("discr_after_pt_sel", "Mfatjet_particleNetMD_XbbvsQCD[Pt_Selection]")
                .Define("softdrop_after_pt_sel", "Mfatjet_msoftdrop[Pt_Selection]")
        )


        df[i] = df[i].Redefine("Jet1_discriminator", "discr_after_pt_sel[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_discriminator", "discr_after_pt_sel[Jet2_index]")

        df[i] = df[i].Redefine("Jet1_softdrop", "softdrop_after_pt_sel[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_softdrop", "softdrop_after_pt_sel[Jet2_index]")
        

        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 80, 0, 1), "discr_after_pt_sel")

        dict_discr_hist1[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 100, 0, 400), "softdrop_after_pt_sel")

        dict_softdrop_hist1[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 100, 0, 400), "Jet2_softdrop")


    #TODO ETA_CUT

        df[i] = (df[i]
                .Define("Eta_Selection", "abs(eta_after_pt_sel) <2.4")
                .Define("discr_after_eta_sel", "discr_after_pt_sel[Eta_Selection]")
                .Define("softdrop_after_eta_sel", "softdrop_after_pt_sel[Eta_Selection]")    

        )

        df[i] = df[i].Filter("discr_after_eta_sel.size()>=2")


        df[i] = df[i].Redefine("Jet1_discriminator", "discr_after_eta_sel[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_discriminator", "discr_after_eta_sel[Jet2_index]")

        df[i] = df[i].Redefine("Jet1_softdrop", "softdrop_after_eta_sel[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_softdrop", "softdrop_after_eta_sel[Jet2_index]")
        

        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 80, 0, 1), "discr_after_eta_sel")

        dict_discr_hist1[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 100, 0, 400), "softdrop_after_eta_sel")

        dict_softdrop_hist1[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 100, 0, 400), "Jet2_softdrop")

    #TODO MASS REQUEST

        df[i] = df[i].Filter("softdrop_after_eta_sel[Jet1_index] >=50 && softdrop_after_eta_sel[Jet2_index] >=50")


        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 80, 0, 1), "discr_after_eta_sel")

        dict_discr_hist1[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 100, 0, 400), "softdrop_after_eta_sel")

        dict_softdrop_hist1[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 100, 0, 400), "Jet2_softdrop")



#* FULLSIM DATASETS

    else:
        #print(f"number of events in dataset {i} is {df[i].Count().GetValue()}")

        df[i] = (df[i]
            .Define("Fullsim_XbbvsQCD", "FatJet_particleNetMD_Xbb/(1-FatJet_particleNetMD_Xcc - FatJet_particleNetMD_Xqq)")
 
        )
        df[i] = (df[i]
            .Define(
            "sorted_Fullsim_XbbvsQCD",
            "Reverse(Argsort(Fullsim_XbbvsQCD))",
        )
            .Define("Jet1_index", "sorted_Fullsim_XbbvsQCD[0]")
            .Define("Jet2_index", "sorted_Fullsim_XbbvsQCD[1]")

        )

        df[i] = df[i].Define("Jet1_discriminator", "Fullsim_XbbvsQCD[Jet1_index]")
        df[i] = df[i].Define("Jet2_discriminator", "Fullsim_XbbvsQCD[Jet2_index]")

        df[i] = df[i].Define("Jet1_softdrop", "FatJet_msoftdrop[Jet1_index]")
        df[i] = df[i].Define("Jet2_softdrop", "FatJet_msoftdrop[Jet2_index]")

    #TODO NO_CUT


        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 80, 0, 1), "Fullsim_XbbvsQCD")

        dict_discr_hist1[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 100, 0, 400), "FatJet_msoftdrop")

        dict_softdrop_hist1[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['no_cut'] = df[i].Histo1D((str(i),str(i) + 'no_cut', 100, 0, 400), "Jet2_softdrop")

    #TODO NFATJETS_REQUEST

        df[i] = df[i].Filter("FatJet_pt.size()>=2")

        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['nfatjets_request'] = df[i].Histo1D((str(i),str(i) + 'nfatjets_request', 80, 0, 1), "Fullsim_XbbvsQCD")

        dict_discr_hist1[i]['nfatjets_request'] = df[i].Histo1D((str(i),str(i) + 'nfatjets_request', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['nfatjets_request'] = df[i].Histo1D((str(i),str(i) + 'nfatjets_request', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['nfatjets_request'] = df[i].Histo1D((str(i),str(i) + 'nfatjets_request', 100, 0, 400), "FatJet_msoftdrop")

        dict_softdrop_hist1[i]['nfatjets_request'] = df[i].Histo1D((str(i),str(i) + 'nfatjets_request', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['nfatjets_request'] = df[i].Histo1D((str(i),str(i) + 'nfatjets_request', 100, 0, 400), "Jet2_softdrop")


        #print(f"Events after nfatjet request in dataset {i} is {df[i].Count().GetValue}")

    #TODO GENJET_REQUEST

        df[i] = df[i].Filter("GenJetAK8_pt[0]>=250 && GenJetAK8_pt[1]>= 250")

        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['genjet_request'] = df[i].Histo1D((str(i),str(i) + 'genjet_request', 80, 0, 1), "Fullsim_XbbvsQCD")

        dict_discr_hist1[i]['genjet_request'] = df[i].Histo1D((str(i),str(i) + 'genjet_request', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['genjet_request'] = df[i].Histo1D((str(i),str(i) + 'genjet_request', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['genjet_request'] = df[i].Histo1D((str(i),str(i) + 'genjet_request', 100, 0, 400), "FatJet_msoftdrop")

        dict_softdrop_hist1[i]['genjet_request'] = df[i].Histo1D((str(i),str(i) + 'genjet_request', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['genjet_request'] = df[i].Histo1D((str(i),str(i) + 'genjet_request', 100, 0, 400), "Jet2_softdrop")

        #print(f"Events after gen_pt request in dataset {i} is {df[i].Count()}")


    #TODO PT_WINDOW



        df[i] = (df[i]
                .Define("Pt_Selection", "FatJet_pt> 300 && FatJet_pt< 500")
                .Define("pt_after_pt_sel", "FatJet_pt[Pt_Selection]")
                .Define("discr_after_pt_sel", "FatJet_particleNetMD_Xbb[Pt_Selection]/(1-FatJet_particleNetMD_Xcc[Pt_Selection] - FatJet_particleNetMD_Xqq[Pt_Selection])")
                .Define("softdrop_after_pt_sel", "FatJet_msoftdrop[Pt_Selection]")
                .Define("eta_after_pt_sel", "FatJet_eta[Pt_Selection]")
                .Define("phi_after_pt_sel", "FatJet_phi[Pt_Selection]")
        )

        df[i] = df[i].Filter("discr_after_pt_sel.size()>=2")

        df[i] = df[i].Redefine("Jet1_discriminator", "discr_after_pt_sel[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_discriminator", "discr_after_pt_sel[Jet2_index]")

        df[i] = df[i].Redefine("Jet1_softdrop", "softdrop_after_pt_sel[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_softdrop", "softdrop_after_pt_sel[Jet2_index]")
        

        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 80, 0, 1), "discr_after_pt_sel")

        dict_discr_hist1[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 100, 0, 400), "softdrop_after_pt_sel")

        dict_softdrop_hist1[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['pt_window'] = df[i].Histo1D((str(i),str(i) + 'pt_window', 100, 0, 400), "Jet2_softdrop")


        # hist4 = df[i].Histo1D((str(i),str(i), 100, 0,800), "Selected_jets")
        # h4 = hist4
        # h4.Draw()
        # print(f"events in dataset {i} after fatjet_pt window is {df[i].Count().GetValue()}")

    #TODO ETA_CUT

        df[i] = (df[i]
            .Define("Eta_Selection", "abs(eta_after_pt_sel) < 2.4")
            .Define("pt_after_eta_sel", "pt_after_pt_sel[Eta_Selection]")
            .Define("discr_after_eta_sel", "discr_after_pt_sel[Eta_Selection]")
            .Define("softdrop_after_eta_sel", "softdrop_after_pt_sel[Eta_Selection]")
            .Define("eta_after_eta_sel", "eta_after_pt_sel[Eta_Selection]")
            .Define("phi_after_eta_sel", "phi_after_pt_sel[Eta_Selection]")
    )

        df[i] = df[i].Redefine("Jet1_discriminator", "discr_after_eta_sel[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_discriminator", "discr_after_eta_sel[Jet2_index]")

        df[i] = df[i].Redefine("Jet1_softdrop", "softdrop_after_eta_sel[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_softdrop", "softdrop_after_eta_sel[Jet2_index]")




        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 80, 0, 1), "discr_after_eta_sel")

        dict_discr_hist1[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 100, 0, 400), "softdrop_after_eta_sel")

        dict_softdrop_hist1[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['eta_cut'] = df[i].Histo1D((str(i),str(i) + 'eta_cut', 100, 0, 400), "Jet2_softdrop")


    #TODO CLEANING

        df[i] = (df[i]
                .Define("fatjets_cleaning", "fatjet_lepton_isolation(eta_after_eta_sel, phi_after_eta_sel, Electron_pt, Electron_eta, Electron_phi, Electron_pfRelIso03_all, 11)  && fatjet_lepton_isolation(eta_after_eta_sel, phi_after_eta_sel, Muon_pt, Muon_eta, Muon_phi, Muon_pfRelIso03_all, 13)")
                .Define("discr_after_cleaning", "discr_after_eta_sel[fatjets_cleaning]")
                .Define("softdrop_after_cleaning", "softdrop_after_eta_sel[fatjets_cleaning]")
        )

        df[i] = df[i].Filter("discr_after_cleaning.size()>=2")

        df[i] = df[i].Redefine("Jet1_discriminator", "discr_after_cleaning[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_discriminator", "discr_after_cleaning[Jet2_index]")

        df[i] = df[i].Redefine("Jet1_softdrop", "softdrop_after_cleaning[Jet1_index]")
        df[i] = df[i].Redefine("Jet2_softdrop", "softdrop_after_cleaning[Jet2_index]")

    
        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['cleaning'] = df[i].Histo1D((str(i),str(i) + 'cleaning', 80, 0, 1), "discr_after_cleaning")

        dict_discr_hist1[i]['cleaning'] = df[i].Histo1D((str(i),str(i) + 'cleaning', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['cleaning'] = df[i].Histo1D((str(i),str(i) + 'cleaning', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['cleaning'] = df[i].Histo1D((str(i),str(i) + 'cleaning', 100, 0, 400), "softdrop_after_cleaning")

        dict_softdrop_hist1[i]['cleaning'] = df[i].Histo1D((str(i),str(i) + 'cleaning', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['cleaning'] = df[i].Histo1D((str(i),str(i) + 'cleaning', 100, 0, 400), "Jet2_softdrop")



    #TODO MASS REQUEST

        df[i] = df[i].Filter("softdrop_after_cleaning[Jet1_index] >=50 && softdrop_after_cleaning[Jet2_index] >=50")


        #! DISCRIMINATOR

        dict_discr_hist_tot[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 80, 0, 1), "discr_after_cleaning")

        dict_discr_hist1[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 80, 0, 1), "Jet1_discriminator")

        dict_discr_hist2[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 80, 0, 1), "Jet2_discriminator")


        #! SOFTDROP

        dict_softdrop_hist_tot[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 100, 0, 400), "softdrop_after_cleaning")

        dict_softdrop_hist1[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 100, 0, 400), "Jet1_softdrop")

        dict_softdrop_hist2[i]['softdrop_request'] = df[i].Histo1D((str(i),str(i) + 'softdrop_request', 100, 0, 400), "Jet2_softdrop")




selection_steps_full = list(dict_discr_hist1['signal_full'].keys())

selection_steps_flash = list(dict_discr_hist1['signal_flash'].keys())

selection_steps_ph2 = list(dict_discr_hist1['signal_ph2'])

print("selection steps fullsim", selection_steps_full)
print("selection steps flashsim", selection_steps_flash)
print("selection steps phase2", selection_steps_ph2)


#print("dict_discr_hist1", dict_discr_hist1)

stacked_full = {}

print("stacking the histograms")

# for j in selection_steps_full:
    
#     stacked_full[j] = {}

#     temp_full_tot = dict_discr_hist_tot['QCD1_full'][j].Clone()
#     temp_full_tot.Add(dict_discr_hist_tot['QCD2_full'][j])
#     temp_full_tot.Add(dict_discr_hist_tot['QCD3_full'][j])
#     temp_full_tot.Add(dict_discr_hist_tot['QCD4_full'][j])
#     temp_full_tot.Add(dict_discr_hist_tot['QCD5_full'][j])
#     temp_full_tot.Add(dict_discr_hist_tot['QCD6_full'][j])
#     temp_full_tot.Add(dict_discr_hist_tot['QCD7_full'][j])
#     temp_full_tot.Add(dict_discr_hist_tot['QCD8_full'][j])

#     stacked_full[j]['all_jets_discr'] = temp_full_tot


#     temp_full_hist1 = dict_discr_hist1['QCD1_full'][j].Clone()
#     temp_full_hist1.Add(dict_discr_hist1['QCD2_full'][j])
#     temp_full_hist1.Add(dict_discr_hist1['QCD3_full'][j])
#     temp_full_hist1.Add(dict_discr_hist1['QCD4_full'][j])
#     temp_full_hist1.Add(dict_discr_hist1['QCD5_full'][j])
#     temp_full_hist1.Add(dict_discr_hist1['QCD6_full'][j])
#     temp_full_hist1.Add(dict_discr_hist1['QCD7_full'][j])
#     temp_full_hist1.Add(dict_discr_hist1['QCD8_full'][j])

#     stacked_full[j]['jet1_discr'] = temp_full_hist1


#     temp_full_hist2 = dict_discr_hist2['QCD1_full'][j].Clone()
#     temp_full_hist2.Add(dict_discr_hist2['QCD2_full'][j])
#     temp_full_hist2.Add(dict_discr_hist2['QCD3_full'][j])
#     temp_full_hist2.Add(dict_discr_hist2['QCD4_full'][j])
#     temp_full_hist2.Add(dict_discr_hist2['QCD5_full'][j])
#     temp_full_hist2.Add(dict_discr_hist2['QCD6_full'][j])
#     temp_full_hist2.Add(dict_discr_hist2['QCD7_full'][j])
#     temp_full_hist2.Add(dict_discr_hist2['QCD8_full'][j])

#     stacked_full[j]['jet2_discr'] = temp_full_hist2




#     temp_full_tot = dict_softdrop_hist_tot['QCD1_full'][j].Clone()
#     temp_full_tot.Add(dict_softdrop_hist_tot['QCD2_full'][j])
#     temp_full_tot.Add(dict_softdrop_hist_tot['QCD3_full'][j])
#     temp_full_tot.Add(dict_softdrop_hist_tot['QCD4_full'][j])
#     temp_full_tot.Add(dict_softdrop_hist_tot['QCD5_full'][j])
#     temp_full_tot.Add(dict_softdrop_hist_tot['QCD6_full'][j])
#     temp_full_tot.Add(dict_softdrop_hist_tot['QCD7_full'][j])
#     temp_full_tot.Add(dict_softdrop_hist_tot['QCD8_full'][j])

#     stacked_full[j]['all_jets_softdrop'] = temp_full_tot


#     temp_full_hist1 = dict_softdrop_hist1['QCD1_full'][j].Clone()
#     temp_full_hist1.Add(dict_softdrop_hist1['QCD2_full'][j])
#     temp_full_hist1.Add(dict_softdrop_hist1['QCD3_full'][j])
#     temp_full_hist1.Add(dict_softdrop_hist1['QCD4_full'][j])
#     temp_full_hist1.Add(dict_softdrop_hist1['QCD5_full'][j])
#     temp_full_hist1.Add(dict_softdrop_hist1['QCD6_full'][j])
#     temp_full_hist1.Add(dict_softdrop_hist1['QCD7_full'][j])
#     temp_full_hist1.Add(dict_softdrop_hist1['QCD8_full'][j])

#     stacked_full[j]['jet1_softdrop'] = temp_full_hist1


#     temp_full_hist2 = dict_softdrop_hist2['QCD1_full'][j].Clone()
#     temp_full_hist2.Add(dict_softdrop_hist2['QCD2_full'][j])
#     temp_full_hist2.Add(dict_softdrop_hist2['QCD3_full'][j])
#     temp_full_hist2.Add(dict_softdrop_hist2['QCD4_full'][j])
#     temp_full_hist2.Add(dict_softdrop_hist2['QCD5_full'][j])
#     temp_full_hist2.Add(dict_softdrop_hist2['QCD6_full'][j])
#     temp_full_hist2.Add(dict_softdrop_hist2['QCD7_full'][j])
#     temp_full_hist2.Add(dict_softdrop_hist2['QCD8_full'][j])

#     stacked_full[j]['jet2_softdrop'] = temp_full_hist2




# stacked_flash = {}

# for j in selection_steps_flash:


#     stacked_flash[j] = {}

#     temp_flash_tot = dict_discr_hist_tot['QCD6_flash'][j].Clone()
#     temp_flash_tot.Add(dict_discr_hist_tot['QCD7_flash'][j])
#     temp_flash_tot.Add(dict_discr_hist_tot['QCD8_flash'][j])

#     stacked_flash[j]['all_jets_discr'] = temp_flash_tot


#     temp_flash_hist1 = dict_discr_hist1['QCD6_flash'][j].Clone()
#     temp_flash_hist1.Add(dict_discr_hist1['QCD7_flash'][j])
#     temp_flash_hist1.Add(dict_discr_hist1['QCD8_flash'][j])

#     stacked_flash[j]['jet1_discr'] = temp_flash_hist1


#     temp_flash_hist2 = dict_discr_hist2['QCD6_flash'][j].Clone()
#     temp_flash_hist2.Add(dict_discr_hist2['QCD7_flash'][j])
#     temp_flash_hist2.Add(dict_discr_hist2['QCD8_flash'][j])

#     stacked_flash[j]['jet2_discr'] = temp_flash_hist2


#     temp_flash_tot = dict_softdrop_hist_tot['QCD6_flash'][j].Clone()
#     temp_flash_tot.Add(dict_softdrop_hist_tot['QCD7_flash'][j])
#     temp_flash_tot.Add(dict_softdrop_hist_tot['QCD8_flash'][j])

#     stacked_flash[j]['all_jets_softdrop'] = temp_flash_tot


#     temp_flash_hist1 = dict_softdrop_hist1['QCD6_flash'][j].Clone()
#     temp_flash_hist1.Add(dict_softdrop_hist1['QCD7_flash'][j])
#     temp_flash_hist1.Add(dict_softdrop_hist1['QCD8_flash'][j])

#     stacked_flash[j]['jet1_softdrop'] = temp_flash_hist1


#     temp_flash_hist2 = dict_softdrop_hist2['QCD6_flash'][j].Clone()
#     temp_flash_hist2.Add(dict_softdrop_hist2['QCD7_flash'][j])
#     temp_flash_hist2.Add(dict_softdrop_hist2['QCD8_flash'][j])

#     stacked_flash[j]['jet2_softdrop'] = temp_flash_hist2


#TODO divide per fullsim, flashsim e ph2 separatamente, ogni taglio a parte

print("creating the histograms")

output_file = ROOT.TFile.Open("figures_analysis_complete/histograms_plus_softdrop_req.root", "RECREATE")

for i in processes:
    for j in selection_steps_full:



        if str(i) == 'QCD1_full'  or str(i) == 'QCD2_full' or str(i) == 'QCD3_full' or str(i) == 'QCD4_full'  or str(i) == 'QCD5_full'  or str(i) == 'QCD6_full' or str(i) == 'QCD7_full' or str(i) == 'QCD8_full' or str(i) == 'signal_full':
            
            dict_discr_hist_tot[i][j] = dict_discr_hist_tot[i][j].GetValue()
            dict_discr_hist1[i][j] = dict_discr_hist1[i][j].GetValue()
            dict_discr_hist2[i][j] = dict_discr_hist2[i][j].GetValue()
            dict_softdrop_hist_tot[i][j] = dict_softdrop_hist_tot[i][j].GetValue()
            dict_softdrop_hist1[i][j] = dict_softdrop_hist1[i][j].GetValue()
            dict_softdrop_hist2[i][j] = dict_softdrop_hist2[i][j].GetValue()
            
            
            output_file.WriteObject(dict_discr_hist_tot[i][j], "discr_histo_tot_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_discr_hist1[i][j], "discr_histo1_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_discr_hist2[i][j], "discr_histo2_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_softdrop_hist_tot[i][j], "soft_histo_tot_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_softdrop_hist1[i][j], "soft_histo1_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_softdrop_hist2[i][j], "soft_histo2_" + str(i)+ "_" + str(j))


    for j in selection_steps_flash:
        if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or  str(i) == 'QCD8_flash' or str(i) == 'signal_flash':
        
            dict_discr_hist_tot[i][j] = dict_discr_hist_tot[i][j].GetValue()
            dict_discr_hist1[i][j] = dict_discr_hist1[i][j].GetValue()
            dict_discr_hist2[i][j] = dict_discr_hist2[i][j].GetValue()
            dict_softdrop_hist_tot[i][j] = dict_softdrop_hist_tot[i][j].GetValue()
            dict_softdrop_hist1[i][j] = dict_softdrop_hist1[i][j].GetValue()
            dict_softdrop_hist2[i][j] = dict_softdrop_hist2[i][j].GetValue()


            output_file.WriteObject(dict_discr_hist_tot[i][j], "discr_histo_tot_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_discr_hist1[i][j], "discr_histo1_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_discr_hist2[i][j], "discr_histo2_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_softdrop_hist_tot[i][j], "soft_histo_tot_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_softdrop_hist1[i][j], "soft_histo1_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_softdrop_hist2[i][j], "soft_histo2_" + str(i)+ "_" + str(j))
            
    for j in selection_steps_ph2:
        if str(i) == 'QCD_ph2' or str(i) == 'signal_ph2':

            dict_discr_hist_tot[i][j] = dict_discr_hist_tot[i][j].GetValue()
            dict_discr_hist1[i][j] = dict_discr_hist1[i][j].GetValue()
            dict_discr_hist2[i][j] = dict_discr_hist2[i][j].GetValue()
            dict_softdrop_hist_tot[i][j] = dict_softdrop_hist_tot[i][j].GetValue()
            dict_softdrop_hist1[i][j] = dict_softdrop_hist1[i][j].GetValue()
            dict_softdrop_hist2[i][j] = dict_softdrop_hist2[i][j].GetValue()

            output_file.WriteObject(dict_discr_hist_tot[i][j], "discr_histo_tot_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_discr_hist1[i][j], "discr_histo1_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_discr_hist2[i][j], "discr_histo2_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_softdrop_hist_tot[i][j], "soft_histo_tot_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_softdrop_hist1[i][j], "soft_histo1_" + str(i)+ "_" + str(j))
            output_file.WriteObject(dict_softdrop_hist2[i][j], "soft_histo2_" + str(i)+ "_" + str(j))
            



# print("written on txt")


