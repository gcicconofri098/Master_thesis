import ROOT
import os
import numpy as np
import matplotlib.pyplot as plt

ROOT.EnableImplicitMT()

module_path = os.path.join(os.path.dirname(__file__), "utils.h")
module_path2 = os.path.join(os.path.dirname(__file__), "nb.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "utils_calibration.h")

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
    "sig_ph2": sig_path
    }

#processes = list(files.keys())
#processes = ['QCD6_flash','QCD7_flash','QCD8_flash','signal_flash']
processes = ['signal_full', 'signal_flash', 'sig_ph2']
for i in processes:
    if str(i) != 'sig_ph2' and str(i)!= 'QCD_ph2':
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

    if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 
            
        print(f"number of events in dataset {i} is {df[i].Count().GetValue()}")

        df[i] = df[i].Filter("!FullSim.FatJet_eta.empty()")

        print("check if empty",df[i].Count().GetValue())
        df[i] = (df[i]
        .Define("matching_index" , "lepton_matching_index(FatJet_eta, FatJet_phi, GenJetAK8_eta, GenJetAK8_phi)")
        .Define("Post_calibration_pt", "calibrate_pt(FatJet_eta, FatJet_pt)")
        .Define("HbbvsQCD_discriminator_lower_limited", "Where(FatJet_particleNetMD_XbbvsQCD>=0,  FatJet_particleNetMD_XbbvsQCD, 0)")
        .Define("HbbvsQCD_discriminator_limited", "Where(HbbvsQCD_discriminator_lower_limited<1, HbbvsQCD_discriminator_lower_limited, 0.9995) ")



        .Define("Selection", "Post_calibration_pt> 300 && Post_calibration_pt< 500 && abs(FatJet_eta) < 2.4")# && matching_index>=0 && fatjet_lepton_isolation(FatJet_eta, FatJet_phi, Electron_pt, Electron_eta, Electron_phi, Electron_pfRelIso03_all, 11)  && fatjet_lepton_isolation(FatJet_eta, FatJet_phi, Muon_pt, Muon_eta, Muon_phi, Muon_pfRelIso03_all, 13)")
        .Define("Selected_jets", "Post_calibration_pt[Selection]")        
        )
        #df[i] = df[i].Filter("!matching_index.empty()")
        df[i] = df[i].Filter("Selected_jets.size()!=0")

        hist2 = df[i].Histo1D((str(i),str(i), 100, 0,800), "Selected_jets")
        h2 = hist2.GetValue()
        h2.Draw()
        print(f"events in dataset {i} after fatjet_pt window is {df[i].Count().GetValue()}")



    elif str(i) == 'QCD_ph2' or str(i) == 'sig_ph2':
        print(f"number of events in dataset {i} is {df[i].Count().GetValue()}")
        df[i] = df[i].Filter("Mfatjet_eta.size()>=2")

        print(f"Events after nfatjet request in dataset {i} is {df[i].Count().GetValue()}")

        #df[i] = df[i].Filter("MgenjetAK8_pt[0]>=250 && MgenjetAK8_pt[1]>=250")
        
        # df[i] = (df[i]
        #         .Define("fatjets_selection_gen", "gen_jet_pt_checker(Mfatjet_pt, MgenjetAK8_pt, new_index)")
        #         .Define("Selected_pt", "Mfatjet_pt[fatjets_selection_gen]")
        #         .Define("Selected_eta", "Mfatjet_eta[fatjets_selection_gen]")
        #         .Define("Selected_phi", "Mfatjet_phi[fatjets_selection_gen]")
        #         .Define("new_matching_index", "new_index[fatjets_selection_gen]")
        #         .Define("discriminator", "Mfatjet_particleNetMD_XbbvsQCD[fatjets_selection_gen]")
        # )
        # hist = df[i].Histo1D((str(i),str(i), 100, 0,800), "discriminator")
        # h = hist.GetValue()
        # h.Draw()
        print(f"events in dataset {i} after request on gen_pt is {df[i].Count().GetValue()}")

        df[i] = df[i].Define("Post_calibration_pt", "calibrate_pt(Mfatjet_eta, MgenjetAK8_pt)")
        
        df[i] = df[i].Define("Selection","Post_calibration_pt> 300 && Post_calibration_pt< 500 && abs(Mfatjet_eta) < 2.4")# && new_index>=0")
        #df[i] = df[i].Filter("!new_index.empty()")

    else: #*fullsim
        print(f"number of events in dataset {i} is {df[i].Count().GetValue()}")

        df[i] = df[i].Filter("FatJet_pt.size()>=2")

        print(f"Events after nfatjet request in dataset {i} is {df[i].Count().GetValue()}")

        #df[i] = df[i].Filter("GenJetAK8_pt[0]>=250 && GenJetAK8_pt[1]>= 250")

        print(f"Events after gen_pt request in dataset {i} is {df[i].Count().GetValue()}")

        df[i] = df[i].Define("Selection", "FatJet_pt> 300 && FatJet_pt< 500 && abs(FatJet_eta) < 2.4")# && FatJet_genJetAK8Idx>=0")# && fatjet_lepton_isolation(FatJet_eta, FatJet_phi, Electron_pt, Electron_eta, Electron_phi, Electron_pfRelIso03_all, 11)  && fatjet_lepton_isolation(FatJet_eta, FatJet_phi, Muon_pt, Muon_eta, Muon_phi, Muon_pfRelIso03_all, 13)")
        df[i] = df[i].Define("Selected_jets", "FatJet_pt[Selection]")
        df[i] = df[i].Filter("Selected_jets.size()!=0")

        #df[i] = df[i].Filter("!FatJet_genJetAK8Idx.empty()")


        # hist4 = df[i].Histo1D((str(i),str(i), 100, 0,800), "Selected_jets")
        # h4 = hist4.GetValue()
        # h4.Draw()
        # print(f"events in dataset {i} after fatjet_pt window is {df[i].Count().GetValue()}")





    if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash':
        df[i] = (
            df[i]
            .Define("new_discriminator", "HbbvsQCD_discriminator_limited[Selection]")
            .Define("FatJet_eta_sel", "FatJet_eta[Selection]")
            .Define("FatJet_phi_sel", "FatJet_phi[Selection]")
            .Define("Softdrop_sel_jets", "FatJet_msoftdrop[Selection]")

            .Define("GenJetAK8_eta_sel", "Take(GenJetAK8_eta, Selection)")
            .Define("GenJetAK8_phi_sel", "Take(GenJetAK8_phi, Selection)")
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
        "Softdrop_sel_jets[Jet1_index]> 40 && Softdrop_sel_jets[Jet2_index]> 40"
        )
        print("event after mass request", df[i].Count().GetValue())
        df[i] = df[i].Define("discr_jet1", "new_discriminator[Jet1_index]")
        df[i] = df[i].Define("discr_jet2", "new_discriminator[Jet2_index]")


    elif str(i) == 'QCD_ph2' or str(i) == 'sig_ph2': 

        df[i]= (df[i]
            .Define("new_discriminator", "Mfatjet_particleNetMD_XbbvsQCD[Selection]")
            .Define("Softdrop_sel_jets", "Mfatjet_msoftdrop[Selection]")
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
        "Softdrop_sel_jets[Jet1_index]> 40 && Softdrop_sel_jets[Jet2_index]> 40"
        )
        print("event after mass request", df[i].Count().GetValue())
        df[i] = df[i].Define("discr_jet1", "new_discriminator[Jet1_index]")
        df[i] = df[i].Define("discr_jet2", "new_discriminator[Jet2_index]")



        

        hist3 = df[i].Histo1D((str(i),str(i), 100, 0,800), "new_discriminator")
        h3 = hist3.GetValue()
        h3.Draw()
        print(f"events in dataset {i} after fatjet_pt window is {df[i].Count().GetValue()}")

        
    else: #*fullsim
        df[i] = (
            df[i]
            .Define("FatJet_eta_sel", "FatJet_eta[Selection]")
            .Define("FatJet_phi_sel", "FatJet_phi[Selection]")
            .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[Selection]")
            .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[Selection]")
            .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[Selection]")
            .Define("Softdrop_sel_jets", "FatJet_msoftdrop[Selection]")

            .Define("new_discriminator", "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)")
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
        "Softdrop_sel_jets[Jet1_index]> 40 && Softdrop_sel_jets[Jet2_index]> 40"
        )
        print("event after mass request", df[i].Count().GetValue())
        df[i] = df[i].Define("discr_jet1", "new_discriminator[Jet1_index]")
        df[i] = df[i].Define("discr_jet2", "new_discriminator[Jet2_index]")




#TODO FROM HERE ON, DEFINITION OF THE NB VARIABLES IS MADE

    if str(i) !=  'sig_ph2' and str(i) != 'QCD_ph2':

        df[i] = df[i].Define(
        "GenPart_IsLastB",
        "(abs(GenPart_pdgId) >=500 && abs(GenPart_pdgId) < 600) | (abs(GenPart_pdgId) >=5000 && abs(GenPart_pdgId) < 6000) && (GenPart_statusFlags &(1<<13))!=0",
    )

        df[i] = df[i].Define("GenPart_IsLastB_m", "Take(GenPart_IsLastB, GenPart_genPartIdxMother)")

        df[i] = df[i].Define(
            "GenPart_parent_IsNotLastB",
            "(GenPart_genPartIdxMother == -1 | GenPart_IsLastB_m ==0)",
        )

        df[i] = (df[i].Define(
            "GenPart_IsGoodB", "GenPart_IsLastB && GenPart_parent_IsNotLastB")
            .Define("GenPart_eta_good", "GenPart_eta[GenPart_IsGoodB]")
            .Define("GenPart_phi_good", "GenPart_phi[GenPart_IsGoodB]")
        )


    if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash':

        df[i] = df[i].Define("MgenjetAK8_nbFlavour", "count_nHadrons(GenPart_eta_good, GenPart_phi_good, GenJetAK8_eta, GenJetAK8_phi)").Define("Matching_nb_flavour", "Take(MgenjetAK8_nbFlavour, matching_index[Selection])")
        #df[i] = df[i].Define("Matching_nb_flavour", "FatJet_nBhadrons[Selection]")

    elif str(i) == 'QCD_ph2' or str(i) == 'sig_ph2':

        df[i] = df[i].Define("Matching_nb_flavour", "Take(MgenjetAK8_nbFlavour, new_index[Selection])")



    else: #* fullsim
        df[i] = (df[i].Define("MgenjetAK8_nbFlavour_manual", "count_nHadrons(GenPart_eta_good, GenPart_phi_good, GenJetAK8_eta, GenJetAK8_phi)")
                 .Define("Matching_nb_flavour", "Take(MgenjetAK8_nbFlavour_manual, FatJet_genJetAK8Idx[Selection])")
                #.Define("Delta", "Matching_nb_flavour - FatJet_nBHadrons[Selection]")
        )

    df[i] = (
            df[i]
            .Define("Matching_nb_0", "Matching_nb_flavour==0")
            .Define("Matching_nb_1", "Matching_nb_flavour == 1")
            .Define("Matching_nb_2", "Matching_nb_flavour == 2")
            .Define("discriminator_nb_0", "new_discriminator[Matching_nb_0]")
            .Define("discriminator_nb_1", "new_discriminator[Matching_nb_1]")
            .Define("discriminator_nb_2", "new_discriminator[Matching_nb_2]")   
            .Define("leading_jet_discriminator_nb_0", "discriminator_nb_0[0]")
            .Define("leading_jet_discriminator_nb_1", "discriminator_nb_1[0]")
            .Define("leading_jet_discriminator_nb_2", "discriminator_nb_2[0]")      
        )
    
    hist_nb0[i] = df[i].Histo1D(
        (str(i), str(i) + "; Discriminator; Events", 100, 0, 1), "discriminator_nb_0"
    )

    hist_nb1[i] = df[i].Histo1D(
        (str(i), str(i) + "; Discriminator; Events", 100, 0, 1), "discriminator_nb_1"
    )

    hist_nb2[i] = df[i].Histo1D(
        (str(i), str(i) + "; Discriminator; Events", 100, 0, 1), "discriminator_nb_2"
    )

    h_nb0[i] = hist_nb0[i].GetValue()
    h_nb1[i] = hist_nb1[i].GetValue()
    h_nb2[i] = hist_nb2[i].GetValue()

    if str(i) == 'signal_full' or str(i) == 'signal_flash' or str(i) == 'sig_ph2':
        hist_discr1[i] = df[i].Histo1D((str(i), str(i) + "; Discriminator; Events", 100, 0, 1), "discr_jet1")
        hist_discr2[i] = df[i].Histo1D((str(i), str(i) + "; Discriminator; Events", 100, 0, 1), "discr_jet2")
        hist_discr[i] =  df[i].Histo1D((str(i), str(i) + "; Discriminator; Events", 100, 0, 1), "new_discriminator")

        h_discr1[i] = hist_discr1[i].GetValue()
        h_discr2[i] = hist_discr2[i].GetValue()
        h_discr[i] = hist_discr[i].GetValue()

        h_clone_discr1[i] = h_discr1[i].Clone()
        h_clone_discr1[i].Add(h_discr2[i])

temp_full = 0
temp_flash = 0
temp_ph2 = 0
full = np.array([])
flash = np.array([])
ph2 = np.array([])


temp_full_jet1 = 0
temp_flash_jet1 = 0
temp_ph2_jet1 = 0
full_jet1 = np.array([])
flash_jet1 = np.array([])
ph2_jet1 = np.array([])



bin_lower = np.array([])

c1 = ROOT.TCanvas("c1", "Discriminator distribution", 800, 700)


legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

h_clone_discr1["signal_full"].Draw("HIST")
h_clone_discr1["signal_full"].SetTitle("Discriminator distribution for Jet1 and Jet2")
h_clone_discr1["signal_full"].SetLineWidth(2)
h_clone_discr1["signal_full"].SetLineColor(ROOT.kBlue +1)
legend.AddEntry(h_clone_discr1["signal_full"], " fullsim", "l")

h_clone_discr1["signal_flash"].Draw("HIST SAME")
h_clone_discr1["signal_flash"].SetLineWidth(2)
h_clone_discr1["signal_flash"].SetLineColor(ROOT.kRed +1)
legend.AddEntry(h_clone_discr1["signal_flash"], " flashsim", "l")

h_clone_discr1["sig_ph2"].Draw("HIST SAME")
h_clone_discr1["sig_ph2"].SetLineWidth(2)
h_clone_discr1["sig_ph2"].SetLineColor(ROOT.kBlack)
legend.AddEntry(h_clone_discr1["sig_ph2"], "phase2 fullsim", "l")
c1.SetLogy()

legend.Draw()

underflow_full = h_clone_discr1["signal_full"].GetBinContent(0)

print(f"the number of underflow events in fullsim is {underflow_full}")

underflow_flash = h_clone_discr1["signal_flash"].GetBinContent(0)

print(f"the number of underflow events in flashsim is {underflow_flash}")


underflow_ph2 = h_clone_discr1["sig_ph2"].GetBinContent(0)

print(f"the number of underflow events in phase 2 is {underflow_ph2}")




overflow_full = h_clone_discr1["signal_full"].GetBinContent(101)

print(f"the number of overflow events in fullsim is {overflow_full}")

overflow_flash = h_clone_discr1["signal_flash"].GetBinContent(101)

print(f"the number of overflow events in flashsim is {overflow_flash}")


overflow_ph2 = h_clone_discr1["sig_ph2"].GetBinContent(101)

print(f"the number of overflow events in phase 2 is {overflow_ph2}")




c2 = ROOT.TCanvas("c2", "Discriminator distribution", 800, 700)


legend2 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

h_discr1["signal_full"].Draw("HIST")
h_discr1["signal_full"].SetTitle("Discriminator distribution for Jet1 only")
h_discr1["signal_full"].SetLineWidth(2)
h_discr1["signal_full"].SetLineColor(ROOT.kBlue +1)
legend2.AddEntry(h_discr1["signal_full"], " fullsim", "l")

h_discr1["signal_flash"].Draw("HIST SAME")
h_discr1["signal_flash"].SetLineWidth(2)
h_discr1["signal_flash"].SetLineColor(ROOT.kRed +1)
legend2.AddEntry(h_discr1["signal_flash"], " flashsim", "l")

h_discr1["sig_ph2"].Draw("HIST SAME")
h_discr1["sig_ph2"].SetLineWidth(2)
h_discr1["sig_ph2"].SetLineColor(ROOT.kBlack)
legend2.AddEntry(h_discr1["sig_ph2"], "phase2 fullsim", "l")
c2.SetLogy()

legend2.Draw()



#TODO ALL JETS

c3 = ROOT.TCanvas("c3", "Discriminator distribution", 800, 700)


legend3 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

h_discr["signal_full"].Draw("HIST")
h_discr["signal_full"].SetTitle("Discriminator distribution for all jets")
h_discr["signal_full"].SetLineWidth(2)
h_discr["signal_full"].SetLineColor(ROOT.kBlue +1)
h_discr["signal_full"].SetMinimum(1)
legend3.AddEntry(h_discr["signal_full"], " fullsim", "l")

h_discr["signal_flash"].Draw("HIST SAME")
h_discr["signal_flash"].SetLineWidth(2)
h_discr["signal_flash"].SetLineColor(ROOT.kRed +1)
legend3.AddEntry(h_discr["signal_flash"], " flashsim", "l")

h_discr["sig_ph2"].Draw("HIST SAME")
h_discr["sig_ph2"].SetLineWidth(2)
h_discr["sig_ph2"].SetLineColor(ROOT.kBlack)
legend3.AddEntry(h_discr["sig_ph2"], "phase2 fullsim", "l")
c3.SetLogy()

legend3.Draw()





for i in reversed(range(0, 101)):

    temp_full = temp_full + h_clone_discr1['signal_full'].GetBinContent(i)

    full = np.append(temp_full, full)

    temp_flash = temp_flash + h_clone_discr1['signal_flash'].GetBinContent(i)

    flash = np.append(temp_flash, flash)

    temp_ph2 = temp_ph2 + h_clone_discr1['sig_ph2'].GetBinContent(i)

    ph2 = np.append(temp_ph2, ph2)



    temp_full_jet1 = temp_full_jet1 + h_discr1['signal_full'].GetBinContent(i)

    full_jet1 = np.append(temp_full_jet1, full_jet1)

    temp_flash_jet1 = temp_flash_jet1 + h_discr1['signal_flash'].GetBinContent(i)

    flash_jet1 = np.append(temp_flash_jet1, flash_jet1)

    temp_ph2_jet1 = temp_ph2_jet1 + h_discr1['sig_ph2'].GetBinContent(i)

    ph2_jet1 = np.append(temp_ph2_jet1, ph2_jet1)



    bin_lower = np.append(h_clone_discr1['signal_full'].GetBinLowEdge(i), bin_lower)

    
print(bin_lower)

#! JET1 + JET2
total_full = h_clone_discr1["signal_full"].GetEntries()
total_flash = h_clone_discr1['signal_flash'].GetEntries()
total_ph2 = h_clone_discr1["sig_ph2"].GetEntries()

efficiency_full = np.array([])
efficiency_flash = np.array([])
efficiency_ph2 = np.array([])

efficiency_full = full/total_full
efficiency_flash = flash/total_flash
efficiency_ph2 = ph2/total_ph2

bin_lower_wo_underflow = bin_lower[:-2]
efficiency_full_wo_underflow = efficiency_full[:-2]
efficiency_flash_wo_underflow = efficiency_flash[:-2]
efficiency_ph2_wo_underflow = efficiency_ph2[:-2]

#! JET1 ONLY

total_full_jet1 = h_discr1["signal_full"].GetEntries()
total_flash_jet1 = h_discr1['signal_flash'].GetEntries()
total_ph2_jet1 = h_discr1["sig_ph2"].GetEntries()

efficiency_full_jet1 = np.array([])
efficiency_flash_jet1 = np.array([])
efficiency_ph2_jet1 = np.array([])

efficiency_full_jet1 = full_jet1/total_full_jet1
efficiency_flash_jet1 = flash_jet1/total_flash_jet1
efficiency_ph2_jet1 = ph2_jet1/total_ph2_jet1


efficiency_full_wo_underflow_jet1 = efficiency_full_jet1[:-2]
efficiency_flash_wo_underflow_jet1 = efficiency_flash_jet1[:-2]
efficiency_ph2_wo_underflow_jet1 = efficiency_ph2_jet1[:-2]



#! JET1 + JET2


plt.plot(bin_lower_wo_underflow, efficiency_full_wo_underflow, label = 'run2 fullsim', color = 'seagreen', marker = '.', markersize=3 )
plt.plot(bin_lower_wo_underflow, efficiency_flash_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
plt.plot(bin_lower_wo_underflow, efficiency_ph2_wo_underflow, label = 'phase2 fullsim', color = 'lightcoral', marker = '.', markersize=3 )
plt.axhline(y = 0.85, color = 'r', linestyle = '-')
plt.grid(which ='both')

plt.legend()

plt.xlabel('Discriminator values')
plt.ylabel('Signal efficiency')

plt.show()
#plt.yscale('log')

#plt.savefig('cdf_no_nb_NO_gen_sel_cleaned_fats_no_cleaning_no_index_req_old_eta.png')

plt.close()



#! JET1 ONLY

plt.plot(bin_lower_wo_underflow, efficiency_full_wo_underflow_jet1, label = 'run2 fullsim', color = 'seagreen', marker = '.', markersize=3 )
plt.plot(bin_lower_wo_underflow, efficiency_flash_wo_underflow_jet1, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
plt.plot(bin_lower_wo_underflow, efficiency_ph2_wo_underflow_jet1, label = 'phase2 fullsim', color = 'lightcoral', marker = '.', markersize=3 )
plt.axhline(y = 0.86, color = 'r', linestyle = '-')
plt.axvline(x=0.85, color = 'blue', linestyle = '-')
plt.grid(which ='both')

plt.legend()

plt.xlabel('Discriminator values')
plt.ylabel('Signal efficiency')

plt.show()
#plt.yscale('log')

plt.savefig('cdf_no_nb_NO_gen_sel_cleaned_fats_jet1_only_no_cleaning_no_index_req_old_eta.png')

plt.close()




c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/discr_distribution_flashsim_limited_NO_gen_sel_cleaned_fats_jet1_and_jet2_no_cleaning_no_index_old_eta.pdf")
c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/discr_distribution_flashsim_limited_NO_gen_sel_cleaned_fats_jet1_only_no_cleaning_no_index_old_eta.pdf")
c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/discr_distribution_flashsim_limited_NO_gen_sel_cleaned_fats_all_jets_no_cleaning_no_index_old_eta.pdf")
