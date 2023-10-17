import ROOT
import os
import re

module_path = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils.h")
module_path2 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/nb.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_calibration.h")


#plt.rcParams['text.usetex'] = True

ROOT.gStyle.SetOptStat(1111)


ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path2}"')

files = {
    "QCD1_full": "/scratchnvme/cicco/QCD1/",
    "QCD2_full": "/scratchnvme/cicco/QCD2/",
    "QCD3_full": "/scratchnvme/cicco/QCD3/",
    "QCD4_full": "/scratchnvme/cicco/QCD4/",
    "QCD5_full": "/scratchnvme/cicco/QCD5/",
    "QCD6_full": "/scratchnvme/cicco/QCD6/",
    "QCD7_full": "/scratchnvme/cicco/QCD7/",
    "QCD8_full": "/scratchnvme/cicco/QCD8/",
#    "old_signal_full": "/scratchnvme/cicco/signal/",
    "signal_full": "/scratchnvme/cicco/signal_RunIISummer20UL16/",
    "QCD6_flash": "/scratchnvme/cicco/QCD6_good_flash/",
    "QCD7_flash": "/scratchnvme/cicco/QCD7_good_flash/",
    "QCD8_flash": "/scratchnvme/cicco/QCD8_good_flash/",
    "signal_flash": "/scratchnvme/cicco/signal_RunIISummer20UL16_flash/",
}

#processes = list(files.keys())
processes = ['signal_full', 'signal_flash']
integrated_luminosity = 59830


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

weights_keys = list(weights.keys())

n_events = {
    "QCD1": 79857456,
    "QCD2": 61542214,
    "QCD3": 56214199,
    "QCD4": 61097673,
    "QCD5": 47314826,
    "QCD6": 15230975,
    "QCD7": 11887406,
    "QCD8": 5710430,
    "signal": 540000,
}
entries1 = {}
events = {}
events_chain = {}
full_chain = {}
df = {}
histos = {}
histos_1d = {}
dataset_events = {}

for i in processes:
    f = os.listdir(files.get(i))
    num = len(f)
    entries1[i] = []
    events[i] = []
    if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 
        print("creating the TChains")
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
    
    else:
        df[i] = ROOT.RDataFrame("Events", entries1[i])
    print("added file to: {}".format(i))

    if str(i) == 'signal_full':

        df[i] = df[i].Define("Pt_leading_jet_pt", "FatJet_pt[0]").Define("Pt_subleading_jet_pt", "FatJet_pt[1]")

        df[i] = df[i].Define("Matched_gen_pt", "Take(GenJetAK8_pt, FatJet_genJetAK8Idx)").Define("resolution_full", "(Matched_gen_pt - FatJet_pt)/Matched_gen_pt").Define("ratio_full_post_calib", "FatJet_pt/Matched_gen_pt")

        df[i] = df[i].Define("Pre_calibration_pt", "(1-FatJet_rawFactor)*FatJet_pt").Define("resolution_pre_calib", "(Matched_gen_pt - Pre_calibration_pt)/Matched_gen_pt").Define("ratio_full_pre_calib", "Pre_calibration_pt/Matched_gen_pt")

        hist = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, 0, 1000), "Pt_leading_jet_pt").GetValue()
        hist2 = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, 0, 1000), "Pt_subleading_jet_pt").GetValue()
    
        df[i] = df[i].Filter("GenJetAK8_pt[0]>250 && GenJetAK8_pt[1]>250").Filter("FatJet_pt.size()>=2")

        hist3 = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, 0, 1000), "Pt_leading_jet_pt").GetValue()
        hist4 = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, 0, 1000), "Pt_subleading_jet_pt").GetValue()

        hist_res_full = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, -0.5, 0.5), "resolution_full").GetValue()


        df[i]= (df[i]
            .Define("new_discriminator", "FatJet_particleNetMD_Xbb/(1-FatJet_particleNetMD_Xcc - FatJet_particleNetMD_Xqq)")  
        )
        df[i] = (
            df[i]
            .Define(
            "sorted_FatJet_deepTagMD_HbbvsQCD",
            "Reverse(Argsort(new_discriminator))",)
            .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
            .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
            .Define("jet1_pt", "FatJet_pt[Jet1_index]")
            .Define("jet2_pt", "FatJet_pt[Jet2_index]")

        )

        hist_jet1_pt_full = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, 0, 1000), "jet1_pt").GetValue()

        hist_jet2_pt_full = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, 0, 1000), "jet2_pt").GetValue()

        hist_pre_calib_full = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, -1, 1), "resolution_pre_calib").GetValue()


        hist_pt_ratio_full_pre_calib = df[i].Histo1D((str(i), str(i) +";Pt; Events", 50, -1, 3), "ratio_full_pre_calib").GetValue()

        hist_pt_ratio_full_post_calib = df[i].Histo1D((str(i), str(i) +";Pt; Events", 50, -1, 3), "ratio_full_post_calib").GetValue()


    if str(i) == 'signal_flash':

        df[i] = df[i].Define("matching_index" , "lepton_matching_index(FatJet_eta, FatJet_phi, GenJetAK8_eta, GenJetAK8_phi)").Define("Matched_gen_pt", "Take(GenJetAK8_pt, matching_index)")

        df[i] = df[i].Define("pt_ratio_before_calib", "Matched_gen_pt/FatJet_pt").Define("resolution_pre_calib", "(Matched_gen_pt - FatJet_pt)/Matched_gen_pt")

        df[i] = df[i].Define("Post_calibration_pt", "calibrate_pt_double_n_bins(FatJet_eta, FatJet_pt)")


        df[i] = df[i].Define("ratio_flash_pre_calib", "FatJet_pt/Matched_gen_pt").Define("ratio_flash_post_calib", "Post_calibration_pt/Matched_gen_pt")


        df[i] = df[i].Define("pt_ratio_after_calib", "Matched_gen_pt/Post_calibration_pt")

        df[i] = df[i].Define("resolution_flash", "(Matched_gen_pt - Post_calibration_pt)/Matched_gen_pt")


        df[i] = df[i].Define("Pt_leading_jet_pt", "Post_calibration_pt[0]").Define("Pt_subleading_jet_pt", "Post_calibration_pt[1]")

        df[i] = (df[i]
                 .Define("Bad_res_events", "resolution_flash <-0.02")
                 .Define("Bad_reco_res_pt", "Post_calibration_pt[Bad_res_events]")
                 .Define("Bad_gen_res_pt", "Matched_gen_pt[Bad_res_events]")
                 #.Filter("matching_index[Bad_gen_res_pt[0]]!=-1 && matching_index[Bad_gen_res_pt[1]]!=-1")
        )

        hist_pre_calib_flash = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, -1, 1), "resolution_pre_calib").GetValue()
    

        hist3_flash = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, 0, 1000), "Pt_leading_jet_pt").GetValue()
        hist4_flash = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, 0, 1000), "Pt_subleading_jet_pt").GetValue()


        hist_res_flash = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, -0.5, 0.5), "resolution_flash").GetValue()


        hist_pt_ratio_pre = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, -5, 5), "pt_ratio_before_calib").GetValue()
        hist_pt_ration_after = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, -5, 5), "pt_ratio_after_calib").GetValue()

        hist_pt_ratio_flash_pre_calib = df[i].Histo1D((str(i), str(i) +";Pt; Events", 50, -1, 3), "ratio_flash_pre_calib").GetValue()

        hist_pt_ratio_flash_post_calib = df[i].Histo1D((str(i), str(i) +";Pt; Events", 50, -1, 3), "ratio_flash_post_calib").GetValue()



        df[i] = (df[i]
        .Define("HbbvsQCD_discriminator_lower_limited", "Where(FatJet_particleNetMD_XbbvsQCD>=0,  FatJet_particleNetMD_XbbvsQCD, 0)")
        .Define("HbbvsQCD_discriminator_limited", "Where(HbbvsQCD_discriminator_lower_limited<1, HbbvsQCD_discriminator_lower_limited, 0.9995) ")
        )

        df[i] = (
            df[i]
            .Define(
            "sorted_FatJet_deepTagMD_HbbvsQCD",
            "Reverse(Argsort(HbbvsQCD_discriminator_limited))",)
            .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
            .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")
            .Define("jet1_pt", "Post_calibration_pt[Jet1_index]")
            .Define("jet2_pt", "Post_calibration_pt[Jet2_index]")
        )

        hist_jet1_pt_flash = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, 0, 1000), "jet1_pt").GetValue()

        hist_jet2_pt_flash = df[i].Histo1D((str(i), str(i) +";Pt; Events", 100, 0, 1000), "jet2_pt").GetValue()

        hist_bad_reco_res_pt = df[i].Histo1D((str(i), str(i) +";Pt; Events", 80, 200, 1000), "Bad_reco_res_pt").GetValue()

        hist_bad_gen_res_pt = df[i].Histo1D((str(i), str(i) +";Pt; Events", 80, 200, 1000), "Bad_gen_res_pt").GetValue()

        print("entries bad reco", hist_bad_reco_res_pt.GetEntries())
        print("entries bad gen", hist_bad_gen_res_pt.GetEntries())



    # if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 

    #     df[i] = df[i].Define("Post_calibration_pt", "calibrate_pt(FatJet_eta, FatJet_pt)")

    #     df[i] = df[i].Define("Selection", "Post_calibration_pt >300 && abs(FatJet_eta) < 2.4").Define("Selected_softdrop", "FatJet_msoftdrop[Selection]").Define("Selected_discriminator", "FatJet_particleNetMD_XbbvsQCD[Selection]") 

    #     df[i] = (df[i]
    #         .Define("sorted_discriminator", "Reverse(Argsort(Selected_discriminator))")
    #         .Define("Jet1_index", "sorted_discriminator[0]")
    #         .Define("Jet2_index", "sorted_discriminator[1]")
    #         .Define("Jet1_discriminator", "Selected_discriminator[Jet1_index]")
    #         .Define("Jet2_discriminator", "Selected_discriminator[Jet2_index]")
    #         .Define("Jet1_softdrop", "Selected_softdrop[Jet1_index]")
    #         .Define("Jet2_softdrop", "Selected_softdrop[Jet2_index]")

    #        )
    #     df[i] = df[i].Filter("Selected_softdrop[Jet1_index]>50 && Selected_softdrop[Jet2_index]>50")

    # else:
    #     df[i] = df[i].Filter("GenJetAK8_pt[0]>= 250 && GenJetAK8_pt[1]>=250")
    #     df[i] = df[i].Define("Selection", "FatJet_pt > 300 && abs(FatJet_eta) < 2.4").Define("Selected_softdrop", "FatJet_msoftdrop[Selection]")

    #     df[i] = (df[i]
    #         .Define("discriminator", "FatJet_particleNetMD_Xbb/(1 - FatJet_particleNetMD_Xcc - FatJet_particleNetMD_Xqq)")
    #         .Define("sorted_discriminator", "Reverse(Argsort(discriminator))")
    #         .Define("Jet1_index", "sorted_discriminator[0]")
    #         .Define("Jet2_index", "sorted_discriminator[1]")
    #         .Define("Jet1_discriminator", "discriminator[Jet1_index]")
    #         .Define("Jet2_discriminator", "discriminator[Jet2_index]")
    #         .Define("Jet1_softdrop", "Selected_softdrop[Jet1_index]")
    #         .Define("Jet2_softdrop", "Selected_softdrop[Jet2_index]")
    # )

    #     df[i] = df[i].Filter("Selected_softdrop[Jet1_index]>50 && Selected_softdrop[Jet2_index]>50")


    # if str(i) == 'signal_flash' or str(i) == 'signal_full':
    #         df[i] = df[i].Filter("Jet1_softdrop>115 && Jet1_softdrop< 145 && Jet2_softdrop > 115 && Jet2_softdrop<145")


    # histos[i] = df[i].Histo2D(("Discriminator Jet1 vs Jet2", "Discriminator Jet1 vs Jet2; Jet1; Jet2", 10, 0.95, 1, 10, 0.95, 1),
    #      "Jet1_discriminator",
    #      "Jet2_discriminator").GetValue()

    # histos_1d[i] = df[i].Histo1D(("Softdrop_mass", "Softdrop mass Jet 1; Softdrop mass; Events", 25, 0, 500), "Jet1_softdrop").GetValue() 
    
# for key_full in processes:
#     key_nofull=key_full.split("_")[0]

#     print(f"weight for dataset {key_full} is: {weights[key_nofull]*2.27/n_events[key_nofull]}")

#     histos[key_full].Scale(weights[key_nofull]*2.27/n_events[key_nofull])
#     histos_1d[key_full].Scale(weights[key_nofull]*2.27/n_events[key_nofull])

# r_full = re.compile("QCD._full")
# r_flash = re.compile("QCD._flash")


# QCD_full_processes = list(filter(r_full.match, processes))
# QCD_flash_processes = list(filter(r_flash.match, processes))

# print("QCD fullsim processes:", QCD_full_processes)
# print("QCD flashsim processes:", QCD_flash_processes)


# QCD_full = histos_1d[str(QCD_full_processes[0])].Clone()
# QCD_flash = histos_1d[str(QCD_flash_processes[0])].Clone()

# for i in QCD_full_processes:
#     if str(i) == QCD_full_processes[0]:
#         continue
#     else:
#         QCD_full.Add(histos_1d[i])

# for i in QCD_flash_processes:
#     if str(i) == QCD_flash_processes[0]:
#         continue
#     else:
#         QCD_flash.Add(histos_1d[i])

# QCD_full.Scale(0.03810465040586403)
# QCD_flash.Scale(0.040677043832022024)

# #! SOFTDROP MASSES

# c15 = ROOT.TCanvas("c15", "Background distribution fullsim", 5000, 3500)

# legend15 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)

# QCD_full.Draw("HIST")
# QCD_full.SetTitle("Softdrop mass for Jet1, Run2 fullsim")
# QCD_full.SetLineWidth(2)
# QCD_full.SetFillColorAlpha(ROOT.kCyan - 10, 0.6)
# legend15.AddEntry(QCD_full, "Run2 fullsim, background", "f")



# histos_1d["signal_full"].Draw("SAME HIST")
# histos_1d["signal_full"].SetLineWidth(3)
# histos_1d["signal_full"].SetLineColor(ROOT.kRed +3)
# histos_1d["signal_full"].Scale(2000)
# legend15.AddEntry(histos_1d["signal_full"], "Run2 fullsim, signal x 2000", "l")

# legend15.Draw()

# c16 = ROOT.TCanvas("c16", "Background distribution fullsim", 5000, 3500)

# legend16 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)


# QCD_flash.SetTitle("Softdrop mass for Jet1, Run2 flashsim")
# QCD_flash.SetLineWidth(2)
# #QCD_flash.SetLineStyle(2)
# QCD_flash.Draw("HIST")
# QCD_flash.SetLineColor(ROOT.kGreen +2)
# QCD_flash.SetFillColorAlpha(ROOT.kGreen -10, 0.5)
# legend16.AddEntry(QCD_flash, "Run2 flashsim, background", "f")

# histos_1d["signal_flash"].Draw("SAME HIST")
# histos_1d["signal_flash"].SetLineWidth(3)
# #histos_1d["signal_flash"].SetLineStyle(2)

# histos_1d["signal_flash"].SetLineColor(ROOT.kBlack)
# histos_1d["signal_flash"].Scale(10000)
# legend16.AddEntry(histos_1d["signal_flash"], "Run2 flashsim, signal x 10000", "l")

# legend16.Draw()


# c19 = ROOT.TCanvas("c19", "Background distribution fullsim", 5000, 3500)

# c19.Divide(3,4)


# c19.cd(1)

# histos['QCD4_full'].Draw("COLZ")
# histos['QCD4_full'].SetTitle("QCD4 fullsim")

# c19.cd(2)

# histos['QCD5_full'].Draw("COLZ")
# histos['QCD5_full'].SetTitle("QCD5 fullsim")

# c19.cd(3)

# histos['QCD6_full'].Draw("COLZ")
# histos['QCD6_full'].SetTitle("QCD6 fullsim")

# c19.cd(4)

# histos['QCD7_full'].Draw("COLZ")
# histos['QCD7_full'].SetTitle("QCD7 fullsim")

# c19.cd(5)

# histos['QCD8_full'].Draw("COLZ")
# histos['QCD8_full'].SetTitle("QCD8 fullsim")

# c19.cd(6)

# histos['signal_full'].Draw("COLZ")
# histos['signal_full'].SetTitle("signal fullsim")

# c19.cd(7)

# histos['QCD6_flash'].Draw("COLZ")
# histos['QCD6_flash'].SetTitle("QCD6 flashsim")


# c19.cd(8)

# histos['QCD7_flash'].Draw("COLZ")
# histos['QCD7_flash'].SetTitle("QCD7 flashsim")

# c19.cd(9)

# histos['QCD8_flash'].Draw("COLZ")
# histos['QCD8_flash'].SetTitle("QCD8 flashsim")

# c19.cd(10)

# histos['signal_flash'].Draw("COLZ")
# histos['signal_flash'].SetTitle("signal flashsim")

jet_low_pt = hist.Integral(1, 25) #pt lower than 250
jet_high_pt = hist.Integral(26, 100) #pt higher than 250
print(f"number of jets with gen_pt lower than 250 is {jet_low_pt}")
print(f"number of jets with gen_pt higher than 250 is {jet_high_pt}")


c1 = ROOT.TCanvas("c1", "pt_leading jet pt", 4500, 3500)

hist.Draw("HIST")
hist.SetTitle("Pt distribution for pt-leading fatjet, fullsim, before flashsim preselection")
hist.SetLineWidth(2)

hist3.Draw("HIST SAME")
#hist3.SetTitle("Pt distribution for pt-leading fatjet, fullsim, after flashsim preselection")
hist3.SetLineWidth(2)

c1.SetLogy(1)

c2 = ROOT.TCanvas("c2", "pt_leading jet pt", 4500, 3500)

hist2.Draw("HIST")
hist2.SetTitle("Pt distribution for pt-subleading fatjet, fullsim, before flashsim preselection")
hist2.SetLineWidth(2)
c2.SetLogy(1)


c3 = ROOT.TCanvas("c3", "pt_leading jet pt", 4500, 3500)

legend1 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)


hist3.Draw("HIST")
hist3.SetTitle("Pt distribution for pt-leading fatjet after flashsim preselection")
hist3.SetLineWidth(2)
hist3.SetLineColor(ROOT.kTeal -6)
legend1.AddEntry(hist3, "Run2 fullsim", 'l')

hist3_flash.Draw("HIST SAME")
#hist3_flash.SetTitle("Pt distribution for pt-leading fatjet, flashsim, after flashsim preselection")
hist3_flash.SetLineWidth(2)
hist3_flash.SetLineColor(ROOT.kRed +2)
legend1.AddEntry(hist3_flash, "Run2 flashsim", 'l')

c3.SetLogy(1)
legend1.Draw()


c4 = ROOT.TCanvas("c4", "pt_leading jet pt", 4500, 3500)

legend2 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)

hist4.Draw("HIST")
hist4.SetTitle("Pt distribution for pt-subleading fatjet after flashsim preselection")
hist4.SetLineWidth(2)
hist4.SetLineColor(ROOT.kTeal -6)
legend2.AddEntry(hist4, "Run2 fullsim", 'l')

hist4_flash.Draw("HIST SAME")
hist4_flash.SetLineWidth(2)
hist4_flash.SetLineColor(ROOT.kRed +2)
legend2.AddEntry(hist4_flash, "Run2 flashsim", 'l')

legend2.Draw()

c4.SetLogy(1)


c5 = ROOT.TCanvas("c5", "pt_leading jet pt", 4500, 3500)

legend3 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)


hist_jet1_pt_full.Draw("HIST")
hist_jet1_pt_full.SetTitle("Pt distribution for Jet1 after flashsim preselection")
hist_jet1_pt_full.SetLineWidth(2)
hist_jet1_pt_full.SetLineColor(ROOT.kTeal -6)
legend3.AddEntry(hist_jet1_pt_full, "Run2 fullsim", 'l')

hist_jet1_pt_flash.Draw("HIST SAME")
#hist_jet1_pt_flash.SetTitle("Pt distribution for pt-leading fatjet, flashsim, after flashsim preselection")
hist_jet1_pt_flash.SetLineWidth(2)
hist_jet1_pt_flash.SetLineColor(ROOT.kRed +2)
legend3.AddEntry(hist_jet1_pt_flash, "Run2 flashsim", 'l')

c5.SetLogy(1)
legend3.Draw()


c6 = ROOT.TCanvas("c6", "pt_leading jet pt", 4500, 3500)

legend4 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)

hist_jet2_pt_full.Draw("HIST")
hist_jet2_pt_full.SetTitle("Pt distribution for Jet2 after flashsim preselection")
hist_jet2_pt_full.SetLineWidth(2)
hist_jet2_pt_full.SetLineColor(ROOT.kTeal -6)
legend4.AddEntry(hist_jet2_pt_full, "Run2 fullsim", 'l')

hist_jet2_pt_flash.Draw("HIST SAME")
hist_jet2_pt_flash.SetLineWidth(2)
hist_jet2_pt_flash.SetLineColor(ROOT.kRed +2)
legend4.AddEntry(hist_jet2_pt_flash, "Run2 flashsim", 'l')

legend4.Draw()

c6.SetLogy(1)


c7 = ROOT.TCanvas("c7", "pt_leading jet pt", 4500, 3500)


hist_res_full.Draw("HIST")
hist_res_full.SetTitle("Resolution fullsim after flashsim selection; (GEN-RECO)/GEN; Events")
hist_res_full.SetLineColor(ROOT.kTeal -6)
hist_res_full.SetLineWidth(2)

c8 = ROOT.TCanvas("c8", "pt_leading jet pt", 4500, 3500)


hist_res_flash.Draw("HIST")
hist_res_full.SetTitle("Resolution flashsim ; (GEN-RECO)/GEN; Events")
hist_res_flash.SetLineColor(ROOT.kRed+2)
hist_res_flash.SetLineWidth(2)



c9 = ROOT.TCanvas("c9", "bad res reco pt", 4500, 3500)

legend5 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)


hist_bad_reco_res_pt.Draw("HIST")
hist_bad_reco_res_pt.SetLineWidth(2)
hist_bad_reco_res_pt.SetTitle("Pt distribution for jets with resolution <-0.2, flashsim")
hist_bad_reco_res_pt.SetLineColor(ROOT.kTeal-6)
legend5.AddEntry(hist_bad_reco_res_pt, "RECO jets", 'l')
hist_bad_reco_res_pt.SetMaximum(750)


hist_bad_gen_res_pt.Draw("HIST SAME")
hist_bad_gen_res_pt.SetLineWidth(2)
hist_bad_gen_res_pt.SetLineColor(ROOT.kRed+2)
legend5.AddEntry(hist_bad_gen_res_pt, "GEN jets", 'l')


c10 = ROOT.TCanvas("c10", "Pt calibration", 4500, 3500)

legend6 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)

hist_pt_ratio_pre.Draw("HIST")
hist_pt_ratio_pre.SetLineWidth(2)
hist_pt_ratio_pre.SetTitle("Pt ratio")
hist_pt_ratio_pre.SetLineColor(ROOT.kTeal-6)
legend6.AddEntry(hist_pt_ratio_pre, "pre-calibration", 'l')


hist_pt_ration_after.Draw("HIST SAME")
hist_pt_ration_after.SetLineWidth(2)
hist_pt_ration_after.SetLineColor(ROOT.kRed+2)
legend6.AddEntry(hist_pt_ration_after, "post-calibration", 'l')

legend6.Draw()


c11 = ROOT.TCanvas("c11", "pt_leading jet pt", 4500, 3500)

legend11 = ROOT.TLegend(0.15,0.7, 0.4, 0.9)

hist_res_full.Draw("HIST")
hist_res_full.SetLineColor(ROOT.kTeal -6)
hist_res_full.SetLineWidth(2)
legend11.AddEntry(hist_res_full, "Run2 fullsim", 'l')
c11.GetPad(0).Update()
stats1 = hist_res_full.GetListOfFunctions().FindObject("stats").Clone("stats1")
stats1.SetY1NDC(.55)
stats1.SetY2NDC(.7)
c11.GetPad(0).Update()

hist_res_flash.Draw("HIST")
hist_res_flash.SetTitle("Resolution after new calibration; (GEN-RECO)/GEN; Events")
c11.GetPad(0).Update()
stats2 = hist_res_flash.GetListOfFunctions().FindObject("stats").Clone("stats2")
hist_res_flash.SetLineColor(ROOT.kRed+2)
hist_res_flash.SetLineWidth(2)
hist_res_flash.SetMaximum(4000)
legend11.AddEntry(hist_res_flash, "Run2 flashsim", 'l')
c11.GetPad(0).Update()
hist_res_full.Draw("SAME HIST")
stats1.Draw()
stats2.Draw()

legend11.Draw()

print(f"integral for pre-calibration res full is {hist_pre_calib_full.Integral()}")

print(f"integral for pre-calibration res flash is {hist_pre_calib_flash.Integral()}")

print(f"n_underflow res full is {hist_pre_calib_full.GetBinContent(0)}")
print(f"n_underflow res flash is {hist_pre_calib_flash.GetBinContent(0)}")

print(f"n_overflow res full is {hist_pre_calib_full.GetBinContent(101)}")
print(f"n_overflow res flash is {hist_pre_calib_flash.GetBinContent(101)}")


c12 = ROOT.TCanvas("c12", "pt_leading jet pt", 4500, 3500)

legend12 = ROOT.TLegend(0.15,0.7, 0.4, 0.9)

hist_pre_calib_full.Draw("HIST")
hist_pre_calib_full.SetLineColor(ROOT.kTeal -6)
hist_pre_calib_full.SetLineWidth(2)
legend12.AddEntry(hist_pre_calib_full, "Run2 fullsim", 'l')

c12.GetPad(0).Update()
stats1 = hist_pre_calib_full.GetListOfFunctions().FindObject("stats").Clone("stats1")
stats1.SetY1NDC(.55)
stats1.SetY2NDC(.7)
c12.GetPad(0).Update()

hist_pre_calib_flash.Draw("HIST")
hist_pre_calib_flash.SetTitle("Resolution before calibration; (GEN-RECO)/GEN; Events")
c12.GetPad(0).Update()
stats2 = hist_pre_calib_flash.GetListOfFunctions().FindObject("stats").Clone("stats2")
hist_pre_calib_flash.SetLineColor(ROOT.kRed+2)
hist_pre_calib_flash.SetLineWidth(2)
hist_pre_calib_flash.SetMaximum(7000)
legend12.AddEntry(hist_pre_calib_flash, "Run2 flashsim", 'l')
c12.GetPad(0).Update()
hist_pre_calib_full.Draw("SAME HIST")

stats1.Draw()
stats2.Draw()

legend12.Draw()



c13 = ROOT.TCanvas("c13", "pt_leading jet pt", 4500, 3500)

legend13 = ROOT.TLegend(0.15,0.7, 0.4, 0.9)

hist_pt_ratio_full_pre_calib.Draw("HIST")
hist_pt_ratio_full_pre_calib.SetLineColor(ROOT.kTeal -6)
hist_pt_ratio_full_pre_calib.SetLineWidth(2)
legend13.AddEntry(hist_pt_ratio_full_pre_calib, "Run2 fullsim", 'l')

c13.GetPad(0).Update()
stats1 = hist_pt_ratio_full_pre_calib.GetListOfFunctions().FindObject("stats").Clone("stats1")
stats1.SetY1NDC(.55)
stats1.SetY2NDC(.7)
c13.GetPad(0).Update()

hist_pt_ratio_flash_pre_calib.Draw("HIST")
hist_pt_ratio_flash_pre_calib.SetTitle("Pt ratio before calibration; RECO/GEN; Events")
c13.GetPad(0).Update()
stats2 = hist_pt_ratio_flash_pre_calib.GetListOfFunctions().FindObject("stats").Clone("stats2")
hist_pt_ratio_flash_pre_calib.SetLineColor(ROOT.kRed+2)
hist_pt_ratio_flash_pre_calib.SetLineWidth(2)
hist_pt_ratio_flash_pre_calib.SetMaximum(30000)
legend13.AddEntry(hist_pt_ratio_flash_pre_calib, "Run2 flashsim", 'l')
c13.GetPad(0).Update()
hist_pt_ratio_full_pre_calib.Draw("SAME HIST")

stats1.Draw()
stats2.Draw()

legend13.Draw()




c14 = ROOT.TCanvas("c14", "pt_leading jet pt", 4500, 3500)

legend14 = ROOT.TLegend(0.15,0.7, 0.4, 0.9)

hist_pt_ratio_full_post_calib.Draw("HIST")
hist_pt_ratio_full_post_calib.SetLineColor(ROOT.kTeal -6)
hist_pt_ratio_full_post_calib.SetLineWidth(2)
legend14.AddEntry(hist_pt_ratio_full_post_calib, "Run2 fullsim", 'l')

c14.GetPad(0).Update()
stats1 = hist_pt_ratio_full_post_calib.GetListOfFunctions().FindObject("stats").Clone("stats1")
stats1.SetY1NDC(.55)
stats1.SetY2NDC(.7)
c14.GetPad(0).Update()

hist_pt_ratio_flash_post_calib.Draw("HIST")
hist_pt_ratio_flash_post_calib.SetTitle("Pt ratio after new calibration; RECO/GEN; Events")
c14.GetPad(0).Update()
stats2 = hist_pt_ratio_flash_post_calib.GetListOfFunctions().FindObject("stats").Clone("stats2")
hist_pt_ratio_flash_post_calib.SetLineColor(ROOT.kRed+2)
hist_pt_ratio_flash_post_calib.SetLineWidth(2)
hist_pt_ratio_flash_post_calib.SetMaximum(30000)
legend14.AddEntry(hist_pt_ratio_flash_post_calib, "Run2 flashsim", 'l')
c14.GetPad(0).Update()
hist_pt_ratio_full_post_calib.Draw("SAME HIST")

stats1.Draw()
stats2.Draw()

legend14.Draw()





#c19.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/distr_discr_divided_pre_preselection.pdf")
# c15.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/softdrop_jet_no_discr_cut_full.pdf")
# c16.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/softdrop_jet_no_discr_cut_flash.pdf")
#c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_distr_pt_leading_fatjet_full.pdf")
#c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_distr_pt_subleading_fatjet_full.pdf")
# c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_distr_pt_leading_fatjet_gen_pres_full_flash.pdf")
# c4.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_distr_pt_subleading_fatjet_gen_pres_full_flash.pdf")
# c5.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_distr_jet1_gen_pres_full_flash.pdf")
# c6.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_distr_jet2_gen_pres_full_flash.pdf")
# c7.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/resolution_full_post_gen_pres.pdf")
# c8.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/resolution_flash.pdf")

# c9.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/bad_reco_pt_jets.pdf")
# c10.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_ratio_signal_calib.pdf")
c11.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/resolutions_full_flash_new_calib.pdf")
#c12.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/resolutions_full_flash_pre_calib.pdf")
#c13.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_ratio_flash_pre_calib.pdf")
c14.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_ratio_flash_post_new_calib.pdf")
