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

ph2_flash_path = "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file1_flashim.root"

hist_nb0 = {}
hist_nb1 = {}
hist_nb2 = {}
hist_delta ={}

h_nb0 = {}
h_nb1 = {}
h_nb2 = {}
h_delta = {}

entries1 = {}

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
    "QCD_ph2": bckg_path,
    "sig_ph2": sig_path,
    "signal_flash": ph2_flash_path}

#processes = list(files.keys())
processes = ['signal_full', 'signal_flash', 'sig_ph2']
for i in processes:
    if str(i) != 'sig_ph2' and str(i)!= 'QCD_ph2' and str(i)!= 'signal_flash':
        f = os.listdir(files.get(i))
        num = len(f)
        entries1[i] = []

        for j in range(0, num):
            entries1[i].append(str(files.get(i)) + str(f[j]))

        df[i] = ROOT.RDataFrame("Events", entries1[i])

        print("added file to: {}".format(i))
    elif str(i)!= 'signal_flash':

        df[i]= ROOT.RDataFrame("MJets", str(files[i]))
    
    else:

        df[i]= ROOT.RDataFrame("Events", str(files[i]))



for i in processes:
    print("Begin selection: {}".format(i))


    if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' : 
        df[i] = (

            df[i].Define("Post_calibration_pt", "calibrate_pt(FatJet_eta, FatJet_pt)")
        )
        df[i] = (df[i]
        .Define("matching_index" , "lepton_matching_index(FatJet_eta, FatJet_phi, GenJetAK8_eta, GenJetAK8_phi)")
        .Define("Selection", "Post_calibration_pt> 300 && Post_calibration_pt< 500 && abs(FatJet_eta) < 2.5 && matching_index>=0")
        
        )
        df[i] = df[i].Filter("!matching_index.empty()")

    elif str(i) == 'QCD_ph2' or str(i) == 'sig_ph2':
        df[i] = df[i].Define("Post_calibration_pt", "calibrate_pt(Mfatjet_eta, MgenjetAK8_pt)")
        
        df[i] = df[i].Define("Selection","Post_calibration_pt> 300 && Post_calibration_pt< 500 && abs(Mfatjet_eta) < 2.5&& new_index>=0")
        df[i] = df[i].Filter("!new_index.empty()")

    elif  str(i) == 'signal_flash':

        df[i] = df[i].Define("Selection","FatJet_pt> 300 && FatJet_pt< 500 && abs(FatJet_eta) < 2.5")
        


    else: #fullsim

        df[i] = df[i].Define("Selection", "FatJet_pt> 300 && FatJet_pt< 500 && abs(FatJet_eta) < 2.5 && FatJet_genJetAK8Idx>=0")
        df[i] = df[i].Filter("!FatJet_genJetAK8Idx.empty()")


    if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' :
        df[i] = (
            df[i]
            .Define("new_discriminator", "FatJet_particleNetMD_XbbvsQCD[Selection]")
            .Define("FatJet_eta_sel", "FatJet_eta[Selection]")
            .Define("FatJet_phi_sel", "FatJet_phi[Selection]")
            .Define("GenJetAK8_eta_sel", "Take(GenJetAK8_eta, Selection)")
            .Define("GenJetAK8_phi_sel", "Take(GenJetAK8_phi, Selection)")
        )

    elif str(i) == 'signal_flash':
        df[i] = (
            df[i]
            .Define("new_discriminator", "FatJet_particleNetMD_XbbvsQCD[Selection]")
            .Define("FatJet_eta_sel", "FatJet_eta[Selection]")
            .Define("FatJet_phi_sel", "FatJet_phi[Selection]")
        )

    elif str(i) == 'QCD_ph2' or str(i) == 'sig_ph2': 

        df[i]= (df[i]
            .Define("new_discriminator", "Mfatjet_particleNetMD_XbbvsQCD[Selection]")
    )
        
    else: #*fullsim
            df[i] = (
            df[i]
            .Define("FatJet_eta_sel", "FatJet_eta[Selection]")
            .Define("FatJet_phi_sel", "FatJet_phi[Selection]")
            .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[Selection]")
            .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[Selection]")
            .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[Selection]")
            .Define("new_discriminator", "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)")
            )

    if str(i) !=  'sig_ph2' and str(i) != 'QCD_ph2' and str(i)!= 'signal_flash':

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

        #df[i] = df[i].Define("MgenjetAK8_nbFlavour", "count_nHadrons(GenPart_eta_good, GenPart_phi_good, GenJetAK8_eta, GenJetAK8_phi)").Define("Matching_nb_flavour", "Take(MgenjetAK8_nbFlavour, matching_index[Selection])")
        df[i] = df[i].Define("Matching_nb_flavour", "FatJet_nBhadrons[Selection]")

    elif str(i) == 'QCD_ph2' or str(i) == 'sig_ph2':

        df[i] = df[i].Define("Matching_nb_flavour", "Take(MgenjetAK8_nbFlavour, new_index[Selection])")



    else: #* fullsim
        df[i] = (df[i].Define("MgenjetAK8_nbFlavour_manual", "count_nHadrons(GenPart_eta_good, GenPart_phi_good, GenJetAK8_eta, GenJetAK8_phi)")
                 .Define("Matching_nb_flavour", "Take(MgenjetAK8_nbFlavour_manual, FatJet_genJetAK8Idx[Selection])")
                .Define("Delta", "Matching_nb_flavour - FatJet_nBHadrons[Selection]")
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
        (str(i), str(i) + "; Discriminator; Events", 50, -0.1, 1), "discriminator_nb_0"
    )

    hist_nb1[i] = df[i].Histo1D(
        (str(i), str(i) + "; Discriminator; Events", 50, -0.1, 1), "discriminator_nb_1"
    )

    hist_nb2[i] = df[i].Histo1D(
        (str(i), str(i) + "; Discriminator; Events", 50, -0.1, 1), "discriminator_nb_2"
    )

    # if str(i)=='QCD1_full' or str(i) == 'QCD2_full' or str(i) == 'QCD3_full' or str(i) == 'QCD4_full' or str(i) == 'QCD5_full' or str(i) == 'QCD6_full' or str(i) == 'QCD7_full' or str(i) == 'QCD8_full' or str(i) == 'signal_full':
    #     hist_delta[i] = df[i].Histo1D(
    #     (str(i), str(i) + "; Delta; Events", 6, -3, 3), "Delta"
    # )
    #     h_delta[i] = hist_delta[i].GetValue()

    h_nb0[i] = hist_nb0[i].GetValue()
    h_nb1[i] = hist_nb1[i].GetValue()
    h_nb2[i] = hist_nb2[i].GetValue()






# #! HISTOGRAMS FULLSIM

# hist_fullsim_nb0 = h_nb0['QCD1_full'].Clone()
# hist_fullsim_nb0.Add(h_nb0['QCD2_full'])
# hist_fullsim_nb0.Add(h_nb0['QCD3_full'])
# hist_fullsim_nb0.Add(h_nb0['QCD4_full'])
# hist_fullsim_nb0.Add(h_nb0['QCD5_full'])
# hist_fullsim_nb0.Add(h_nb0['QCD6_full'])
# hist_fullsim_nb0.Add(h_nb0['QCD7_full'])
# hist_fullsim_nb0.Add(h_nb0['QCD8_full'])
hist_fullsim_nb0 =(h_nb0['signal_full']).Clone()

hist_fullsim_nb0.ResetStats()

# hist_fullsim_nb1 = h_nb1['QCD1_full'].Clone()
# hist_fullsim_nb1.Add(h_nb1['QCD2_full'])
# hist_fullsim_nb1.Add(h_nb1['QCD3_full'])
# hist_fullsim_nb1.Add(h_nb1['QCD4_full'])
# hist_fullsim_nb1.Add(h_nb1['QCD5_full'])
# hist_fullsim_nb1.Add(h_nb1['QCD6_full'])
# hist_fullsim_nb1.Add(h_nb1['QCD7_full'])
# hist_fullsim_nb1.Add(h_nb1['QCD8_full'])
hist_fullsim_nb1 =(h_nb1['signal_full']).Clone()
print("nb=1 fullsim entries", hist_fullsim_nb1.GetEntries() )

hist_fullsim_nb1.ResetStats()

# hist_fullsim_nb2 = h_nb2['QCD1_full'].Clone()
# hist_fullsim_nb2.Add(h_nb2['QCD2_full'])
# hist_fullsim_nb2.Add(h_nb2['QCD3_full'])
# hist_fullsim_nb2.Add(h_nb2['QCD4_full'])
# hist_fullsim_nb2.Add(h_nb2['QCD5_full'])
# hist_fullsim_nb2.Add(h_nb2['QCD6_full'])
# hist_fullsim_nb2.Add(h_nb2['QCD7_full'])
# hist_fullsim_nb2.Add(h_nb2['QCD8_full'])
hist_fullsim_nb2 =(h_nb2['signal_full']).Clone()


hist_fullsim_nb2.ResetStats()

#! HISTOGRAMS FLASHSHIM 


# hist_flashsim_nb0 = h_nb0['QCD6_flash'].Clone()
# hist_flashsim_nb0.Add(h_nb0['QCD7_flash'])
# hist_flashsim_nb0.Add(h_nb0['QCD8_flash'])
hist_flashsim_nb0 =(h_nb0['signal_flash']).Clone()

hist_flashsim_nb0.ResetStats()

# hist_flashsim_nb1 = h_nb1['QCD6_flash'].Clone()
# hist_flashsim_nb1.Add(h_nb1['QCD7_flash'])
# hist_flashsim_nb1.Add(h_nb1['QCD8_flash'])
hist_flashsim_nb1 =(h_nb1['signal_flash']).Clone()
print("nb=1 flashsim entries", hist_flashsim_nb1.GetEntries() )


hist_flashsim_nb1.ResetStats()

# hist_flashsim_nb2 = h_nb2['QCD6_flash'].Clone()
# hist_flashsim_nb2.Add(h_nb2['QCD7_flash'])
# hist_flashsim_nb2.Add(h_nb2['QCD8_flash'])
hist_flashsim_nb2 =(h_nb2['signal_flash']).Clone()

hist_flashsim_nb2.ResetStats()

#! HISTOGRAMS PHASE2   

#hist_phase2_nb0 = h_nb0['QCD_ph2'].Clone()
hist_phase2_nb0 = h_nb0['sig_ph2'].Clone()


#hist_phase2_nb1 = h_nb1['QCD_ph2'].Clone()
hist_phase2_nb1 = h_nb1['sig_ph2'].Clone()
print("nb=1 phase2 entries", hist_phase2_nb1.GetEntries() )

#hist_phase2_nb2 = h_nb2['QCD_ph2'].Clone()
hist_phase2_nb2 = h_nb2['sig_ph2'].Clone()

full_nb0 = np.array([])
full_nb1 = np.array([])
full_nb2 = np.array([])

flash_nb0 = np.array([])
flash_nb1 = np.array([])
flash_nb2 = np.array([])

ph2_nb0 = np.array([])
ph2_nb1 = np.array([])
ph2_nb2 = np.array([])



fp_full_nb0 = np.array([])
fp_full_nb1 = np.array([])
fp_full_nb2 = np.array([])

fp_flash_nb0 = np.array([])
fp_flash_nb1 = np.array([])
fp_flash_nb2 = np.array([])

fp_ph2_nb0 = np.array([])
fp_ph2_nb1 = np.array([])
fp_ph2_nb2 = np.array([])

temp0_full = 0
temp1_full = 0
temp2_full = 0

temp0_flash = 0
temp1_flash = 0
temp2_flash = 0

temp0_ph2 = 0
temp1_ph2 = 0
temp2_ph2 = 0


for i in reversed(range(0, 101)):

    temp0_full = temp0_full + hist_fullsim_nb0.GetBinContent(i)

    full_nb0 = np.append(temp0_full, full_nb0)

    # full_nb0 = np.append(hist_fullsim_nb0.Integral(i, 200), full_nb0)

    # #fp_full_nb0 = np.append(hist_fullsim_nb0.Integral(i,200), fp_full_nb0)

    temp1_full = temp1_full + hist_fullsim_nb1.GetBinContent(i)

    full_nb1 = np.append(temp1_full, full_nb1)

    # full_nb1 = np.append(hist_fullsim_nb1.Integral(i, 200), full_nb1)

    # #fp_full_nb1 = np.append(hist_fullsim_nb1.Integral(i,200), fp_full_nb1)

    temp2_full = temp2_full + hist_fullsim_nb2.GetBinContent(i)

    full_nb2 = np.append(temp2_full, full_nb2)

    # full_nb2 = np.append(hist_fullsim_nb2.Integral(i, 200), full_nb2)

    # #fp_full_nb2 = np.append(hist_fullsim_nb2.Integral(i,200), fp_full_nb2)

    temp0_flash = temp0_flash + hist_flashsim_nb0.GetBinContent(i)

    flash_nb0 = np.append(temp0_flash, flash_nb0)


    # flash_nb0 = np.append(hist_flashsim_nb0.Integral(i, 200), flash_nb0)

    # #fp_flash_nb0 = np.append(hist_flashsim_nb0.Integral(i,200), fp_flash_nb0)

    temp1_flash = temp1_flash + hist_flashsim_nb1.GetBinContent(i)

    flash_nb1 = np.append(temp1_flash, flash_nb1)


    # flash_nb1 = np.append(hist_flashsim_nb1.Integral(i, 200), flash_nb1)

    # #fp_flash_nb1 = np.append(hist_flashsim_nb1.Integral(i,200), fp_flash_nb1)


    temp2_flash = temp2_flash + hist_flashsim_nb2.GetBinContent(i)

    flash_nb2 = np.append(temp2_flash, flash_nb2)

    # flash_nb2 = np.append(hist_flashsim_nb2.Integral(i, 200), flash_nb2)

    # #fp_flash_nb2 = np.append(hist_flashsim_nb2.Integral(i,200), fp_flash_nb2)

    temp0_ph2 = temp0_ph2 + hist_phase2_nb0.GetBinContent(i)

    ph2_nb0 = np.append(temp0_ph2, ph2_nb0)
    # ph2_nb0 = np.append(hist_phase2_nb0.Integral(i, 200), ph2_nb0)

    # #fp_ph2_nb0 = np.append(hist_phase2_nb0.Integral(i,200), fp_ph2_nb0)

    temp1_ph2 = temp1_ph2 + hist_phase2_nb1.GetBinContent(i)

    ph2_nb1 = np.append(temp1_ph2, ph2_nb1)

    # ph2_nb1 = np.append(hist_phase2_nb1.Integral(i, 200), ph2_nb1)

    # #fp_ph2_nb1 = np.append(hist_phase2_nb1.Integral(i,200), fp_ph2_nb1)

    temp2_ph2 = temp2_ph2 + hist_phase2_nb2.GetBinContent(i)

    ph2_nb2 = np.append(temp2_ph2, ph2_nb2)

    # ph2_nb2 = np.append(hist_phase2_nb2.Integral(i, 200), ph2_nb2)

    # #fp_ph2_nb2 = np.append(hist_phase2_nb2.Integral(i,200), fp_ph2_nb2)
    
    if float(hist_fullsim_nb2.GetBinLowEdge(i)) >= 0.75 and float(hist_fullsim_nb2.GetBinLowEdge(i))<= 0.9:
    
        print("bin {} with lower edge {}".format(i, hist_fullsim_nb2.GetBinLowEdge(i)))




total_full_nb0 = temp0_full
total_full_nb1 = temp1_full
total_full_nb2 = temp2_full

total_flash_nb0 = temp0_flash
total_flash_nb1 = temp1_flash
total_flash_nb2 = temp2_flash

total_ph2_nb0 = temp0_ph2
total_ph2_nb1 = temp1_ph2
total_ph2_nb2 = temp2_ph2

tp_per_full_nb0 = full_nb0/total_full_nb0
tp_per_full_nb1 = full_nb1/total_full_nb1
tp_per_full_nb2 = full_nb2/total_full_nb2

tp_per_flash_nb0 = flash_nb0/total_flash_nb0
tp_per_flash_nb1 = flash_nb1/total_flash_nb1
tp_per_flash_nb2 = flash_nb2/total_flash_nb2

tp_per_ph2_nb0 = ph2_nb0/total_ph2_nb0
tp_per_ph2_nb1 = ph2_nb1/total_ph2_nb1
tp_per_ph2_nb2 = ph2_nb2/total_ph2_nb2

#la percentuale di false positive è data dal numero di eventi di fondo che passa la selezione diviso la somma degli eventi che supera la selezione
#* y/ (y+x), dove y è il fondo e x il segnale
# fp_per_full_0_2 = fp_full_nb0/(fp_full_nb0 + full_nb2)
# fp_per_full_0_1 = fp_full_nb0/(fp_full_nb0 + full_nb1)
# fp_per_full_1_2 = fp_full_nb1/(fp_full_nb1 + full_nb2)

# fp_per_flash_0_2 = fp_flash_nb0/(fp_flash_nb0 + flash_nb2)
# fp_per_flash_0_1 = fp_flash_nb0/(fp_flash_nb0 + flash_nb1)
# fp_per_flash_1_2 = fp_flash_nb1/(fp_flash_nb1 + flash_nb2)

# fp_per_ph2_0_2 = fp_ph2_nb0/(fp_ph2_nb0 + ph2_nb2)
# fp_per_ph2_0_1 = fp_ph2_nb0/(fp_ph2_nb0 + ph2_nb1)
# fp_per_ph2_1_2 = fp_ph2_nb1/(fp_ph2_nb1 + ph2_nb2)


# c1 = ROOT.TCanvas("c1", "Fullsim distribution", 800, 700)


# legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

# hist_fullsim_nb0.Draw("HIST")
# hist_fullsim_nb0.SetTitle("Discriminator distribution for fullsim")
# hist_fullsim_nb0.SetLineWidth(2)
# hist_fullsim_nb0.SetLineColor(ROOT.kBlue +1)
# legend.AddEntry(hist_fullsim_nb0, " b = 0", "l")

# hist_fullsim_nb1.Draw("HIST SAME")
# hist_fullsim_nb1.SetLineWidth(2)
# hist_fullsim_nb1.SetLineColor(ROOT.kRed +1)
# legend.AddEntry(hist_fullsim_nb1, " b = 1", "l")

# hist_fullsim_nb2.Draw("HIST SAME")
# hist_fullsim_nb2.SetLineWidth(2)
# hist_fullsim_nb2.SetLineColor(ROOT.kBlack)
# legend.AddEntry(hist_fullsim_nb2, " b = 2", "l")
# c1.SetLogy()
# legend.Draw()

# c2 = ROOT.TCanvas("c2", "Flashsim distribution", 800, 700)


# legend2 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

# hist_flashsim_nb0.Draw("HIST")
# hist_flashsim_nb0.SetTitle("Discriminator distribution for flashsim")
# hist_flashsim_nb0.SetLineWidth(2)
# hist_flashsim_nb0.SetLineColor(ROOT.kBlue +1)
# legend2.AddEntry(hist_flashsim_nb0, " b = 0", "l")

# hist_flashsim_nb1.Draw("HIST SAME")
# hist_flashsim_nb1.SetLineWidth(2)
# hist_flashsim_nb1.SetLineColor(ROOT.kRed +1)
# legend2.AddEntry(hist_flashsim_nb1, " b = 1", "l")

# hist_flashsim_nb2.Draw("HIST SAME")
# hist_flashsim_nb2.SetLineWidth(2)
# hist_flashsim_nb2.SetLineColor(ROOT.kBlack)
# legend2.AddEntry(hist_flashsim_nb2, " b = 2", "l")
# c2.SetLogy()

# legend2.Draw()


# c3 = ROOT.TCanvas("c3", "Phase2 distribution", 800, 700)


# legend3 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

# hist_phase2_nb0.Draw("HIST")
# hist_phase2_nb0.SetTitle("Discriminator distribution for phase2")
# hist_phase2_nb0.SetLineWidth(2)
# hist_phase2_nb0.SetLineColor(ROOT.kBlue +1)
# legend3.AddEntry(hist_phase2_nb0, " b = 0", "lj")
# hist_phase2_nb1.Draw("HIST SAME")
# hist_phase2_nb1.SetLineWidth(2)
# hist_phase2_nb1.SetLineColor(ROOT.kRed +1)
# legend3.AddEntry(hist_phase2_nb1, " b = 1", "l")
# hist_phase2_nb2.Draw("HIST SAME")
# hist_phase2_nb2.SetLineWidth(2)
# hist_phase2_nb2.SetLineColor(ROOT.kBlack)
# legend3.AddEntry(hist_phase2_nb2, " b = 2", "l")
# c3.SetLogy()


# legend3.Draw()


#! ALL DISCRIMINATOR CASE PER CASE

c4 = ROOT.TCanvas("c4", "Flashsim distribution", 800, 700)


legend4 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

hist_fullsim_nb0.Draw("HIST")
hist_fullsim_nb0.SetTitle("Discriminator distribution for background, b = 0")
hist_fullsim_nb0.SetLineWidth(2)
hist_fullsim_nb0.SetLineColor(ROOT.kBlue +1)
hist_fullsim_nb0.SetMinimum(1)
hist_fullsim_nb0.Scale(1/hist_fullsim_nb0.Integral())
legend4.AddEntry(hist_fullsim_nb0, "fullsim", "l")
print("nb0 fullsim underflow", hist_fullsim_nb0.GetBinContent(0))


hist_flashsim_nb0.Draw("HIST SAME")
hist_flashsim_nb0.SetLineWidth(2)
hist_flashsim_nb0.SetLineColor(ROOT.kRed +1)
hist_flashsim_nb0.Scale(1/hist_flashsim_nb0.Integral())
print("nb0 flashsim underflow", hist_flashsim_nb0.GetBinContent(0))

legend4.AddEntry(hist_flashsim_nb0, " flashsim", "l")

hist_phase2_nb0.Draw("HIST SAME")
hist_phase2_nb0.SetLineWidth(2)
hist_phase2_nb0.SetLineColor(ROOT.kBlack)
hist_phase2_nb0.Scale(1/hist_phase2_nb0.Integral())

legend4.AddEntry(hist_phase2_nb0, " phase2 fullsim", "l")
c4.SetLogy()

legend4.Draw()
print("nb0 phase2 underflow", hist_phase2_nb0.GetBinContent(0))


c5 = ROOT.TCanvas("c5", "Flashsim distribution", 800, 700)


legend5 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

hist_fullsim_nb1.Draw("HIST")
hist_fullsim_nb1.SetTitle("Discriminator distribution for signal, b = 1")
hist_fullsim_nb1.SetLineWidth(2)
hist_fullsim_nb1.SetLineColor(ROOT.kBlue +1)
hist_fullsim_nb1.SetMinimum(1)
hist_fullsim_nb1.SetMaximum(10e4)
#hist_fullsim_nb1.Scale(1/hist_fullsim_nb1.Integral())

legend5.AddEntry(hist_fullsim_nb1, "fullsim", "l")
print("nb1 fullsim underflow", hist_fullsim_nb1.GetBinContent(0))


hist_flashsim_nb1.Draw("HIST SAME")
hist_flashsim_nb1.SetLineWidth(2)
hist_flashsim_nb1.SetLineColor(ROOT.kRed +1)
#hist_flashsim_nb1.Scale(1/hist_flashsim_nb1.Integral())

legend5.AddEntry(hist_flashsim_nb1, " flashsim", "l")
print("nb1 flashsim underflow", hist_flashsim_nb1.GetBinContent(0))


hist_phase2_nb1.Draw("HIST SAME")
hist_phase2_nb1.SetLineWidth(2)
hist_phase2_nb1.SetLineColor(ROOT.kBlack)
#hist_phase2_nb1.Scale(1/hist_phase2_nb1.Integral())

legend5.AddEntry(hist_phase2_nb1, " phase2 fullsim", "l")
c5.SetLogy()

legend5.Draw()
print("nb1 phase2 underflow", hist_phase2_nb1.GetBinContent(0))


c6 = ROOT.TCanvas("c6", "Flashsim distribution", 800, 700)


legend6 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

hist_fullsim_nb2.Draw("HIST")
hist_fullsim_nb2.SetTitle("Discriminator distribution for signal, b = 2")
hist_fullsim_nb2.SetLineWidth(2)
hist_fullsim_nb2.SetMinimum(1)
hist_fullsim_nb2.SetLineColor(ROOT.kBlue +1)
#hist_fullsim_nb2.Scale(1/hist_fullsim_nb2.Integral())

legend6.AddEntry(hist_fullsim_nb2, "fullsim", "l")

print("nb2 fullsim underflow", hist_fullsim_nb2.GetBinContent(0))


hist_flashsim_nb2.Draw("HIST SAME")
hist_flashsim_nb2.SetLineWidth(2)
hist_flashsim_nb2.SetLineColor(ROOT.kRed +1)
#hist_flashsim_nb2.Scale(1/hist_flashsim_nb2.Integral())

legend6.AddEntry(hist_flashsim_nb2, " flashsim", "l")

print("nb2 flashsim underflow", hist_flashsim_nb2.GetBinContent(0))


hist_phase2_nb2.Draw("HIST SAME")
hist_phase2_nb2.SetLineWidth(2)
hist_phase2_nb2.SetLineColor(ROOT.kBlack)
#hist_phase2_nb2.Scale(1/hist_phase2_nb2.Integral())

legend6.AddEntry(hist_phase2_nb2, " phase2 fullsim", "l")
c6.SetLogy()

legend6.Draw()



# c7 = ROOT.TCanvas("c7", "Flashsim distribution", 800, 700)


# h_delta['signal_full'].Draw("HIST")
# h_delta['signal_full'].SetTitle("Delta for fullsim")
# h_delta['signal_full'].SetLineWidth(2)
# h_delta['signal_full'].SetLineColor(ROOT.kBlue +1)
# h_delta['signal_full'].Draw()



# print("nb2 phase2 underflow", hist_phase2_nb2.GetBinContent(0))


# print("efficiency on signal fullsim", tp_per_full_nb2[87])
# print("efficiency on signal flashsim", tp_per_flash_nb2[87])
# print("efficiency on signal phase2", tp_per_ph2_nb2[87])


# #! 2b vs 0b

# tp_per_full_nb2_wo_underflow = tp_per_full_nb2[:-2]
# tp_per_flash_nb2_wo_underflow = tp_per_flash_nb2[:-2]
# tp_per_ph2_nb2_wo_underflow = tp_per_ph2_nb2[:-2]

# tp_per_full_nb1_wo_underflow = tp_per_full_nb1[:-2]
# tp_per_flash_nb1_wo_underflow = tp_per_flash_nb1[:-2]
# tp_per_ph2_nb1_wo_underflow = tp_per_ph2_nb1[:-2]

# tp_per_full_nb0_wo_underflow = tp_per_full_nb0[:-2]
# tp_per_flash_nb0_wo_underflow = tp_per_flash_nb0[:-2]
# tp_per_ph2_nb0_wo_underflow = tp_per_ph2_nb0[:-2]



# plt.plot(tp_per_full_nb2_wo_underflow, tp_per_full_nb0_wo_underflow, label = 'fullsim', color = 'seagreen', marker = '.', markersize=3 )
# plt.plot(tp_per_flash_nb2_wo_underflow, tp_per_flash_nb0_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
# plt.plot(tp_per_ph2_nb2_wo_underflow, tp_per_ph2_nb0_wo_underflow, label = 'phase2', color = 'lightcoral', marker = '.', markersize=3 )
# plt.plot(tp_per_full_nb2_wo_underflow[87],  tp_per_full_nb0_wo_underflow[87], label= 'fullsim @ $T>0.86$', marker= 'D', color = 'darkgreen')
# plt.plot(tp_per_flash_nb2_wo_underflow[87], tp_per_flash_nb0_wo_underflow[87], label = 'flashim @ $T>0.86$', marker = 'D', color = 'mediumblue')
# plt.plot(tp_per_ph2_nb2_wo_underflow[87], tp_per_ph2_nb0_wo_underflow[87], label = 'ph2 @ $T>0.86$', marker = 'D', color = 'crimson')

# plt.legend()

# plt.xlabel('Efficiency distribution of the discriminator for 2b')
# plt.ylabel('Efficiency distribution of the discriminator for 0b')

# plt.show()
# plt.yscale('log')
# plt.savefig('2b_sig_vs_0b_bckg_new_column.png')

# plt.close()



# #! 2b vs 1b

# plt.plot(tp_per_full_nb2, tp_per_full_nb1, label = 'fullsim', color = 'seagreen', marker = '.', markersize=3 )
# plt.plot(tp_per_flash_nb2, tp_per_flash_nb1, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
# plt.plot(tp_per_ph2_nb2, tp_per_ph2_nb1, label = 'phase2', color = 'lightcoral', marker = '.', markersize=3 )
# plt.plot(tp_per_full_nb2_wo_underflow[87],  tp_per_full_nb1_wo_underflow[87], label= 'fullsim @ $T>0.86$', marker= 'D', color = 'darkgreen')
# plt.plot(tp_per_flash_nb2_wo_underflow[87], tp_per_flash_nb1_wo_underflow[87], label = 'flashim @ $T>0.86$', marker = 'D', color = 'mediumblue')
# plt.plot(tp_per_ph2_nb2_wo_underflow[87], tp_per_ph2_nb1_wo_underflow[87], label = 'ph2 @ $T>0.86$', marker = 'D', color = 'crimson')



# plt.legend()

# plt.xlabel('Efficiency distribution of the discriminator for 2b')
# plt.ylabel('Efficiency distribution of the discriminator for 1b')

# plt.show()
# #plt.yscale('log')

# plt.savefig('2b_sig_vs_1b_sig_new_column.png')

# plt.close()


# #! 1b vs 0b

# plt.plot(tp_per_full_nb1, tp_per_full_nb0, label = 'fullsim', color = 'seagreen', marker = '.', markersize=3 )
# plt.plot(tp_per_flash_nb1, tp_per_flash_nb0, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
# plt.plot(tp_per_ph2_nb1, tp_per_ph2_nb0, label = 'phase2', color = 'lightcoral', marker = '.', markersize=3 )

# plt.legend()

# plt.xlabel('Efficiency distribution of the discriminator for 1b')
# plt.ylabel('Efficiency distribution of the discriminator for 0b')

# plt.show()
# plt.yscale('log')

# #plt.savefig('1b_sig_vs_0b_bckg.png')

# plt.close()




# c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/underflow_discr_distribution_fullsim.pdf")
# c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/underflow_discr_distribution_flashsim.pdf")
# c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/underflow_discr_distribution_phase2.pdf")

#c4.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/test_discr_distribution_nb_0_sig.pdf")
c5.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/test_ph2_w_flashsim_nb1_sig.pdf")
c6.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/test_ph2_w_flashsim_nb2_sig.pdf")


#c7.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/test_Delta.pdf")
