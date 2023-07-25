import ROOT
import os
import numpy as np
import matplotlib.pyplot as plt

ROOT.EnableImplicitMT()

module_path = os.path.join(os.path.dirname(__file__), "utils.h")
module_path2 = os.path.join(os.path.dirname(__file__), "nb.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "utils_calibration.h")



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


h_nb0 = {}
h_nb1 = {}
h_nb2 = {}


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
    "QCD6_flash": "/scratchnvme/cicco/QCD6_good_flash/",
    "QCD7_flash": "/scratchnvme/cicco/QCD7_good_flash/",
    "QCD8_flash": "/scratchnvme/cicco/QCD8_good_flash/",
    "signal_flash": "/scratchnvme/cicco/signal_RunIISummer20UL16_flash/",
    "QCD_ph2": bckg_path,
    "sig_ph2": sig_path}

processes = list(files.keys())

for i in processes:
    if str(i) != 'sig_ph2' and str(i)!= 'QCD_ph2':
        f = os.listdir(files.get(i))
        num = len(f)
        entries1[i] = []

        for j in range(0, num):
            entries1[i].append(str(files.get(i)) + str(f[j]))

        df[i] = ROOT.RDataFrame("Events", entries1[i])

        print("added file to: {}".format(i))
    else:
        df[i]= ROOT.RDataFrame("MJets", str(files[i]))


for i in processes:
    print("Begin selection: {}".format(i))
    if str(i) == 'QCD_ph2' or str(i) == 'sig_ph2': 
        df[i] = df[i].Filter("Mfatjet_pt.size()>=2")
    else:
        df[i] = df[i].Filter("nFatJet>=2")

    if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash': 
        df[i] = df[i].Define("Post_calibration_pt", "calibrate_pt(FatJet_eta, FatJet_pt)")

        df[i] = df[i].Define("Selection","Post_calibration_pt> 300 && Post_calibration_pt< 500 && abs(FatJet_eta) < 2.5")
    elif str(i) == 'QCD_ph2' or str(i) == 'sig_ph2':
        df[i] = df[i].Define("Post_calibration_pt", "calibrate_pt(Mfatjet_eta, MgenjetAK8_pt)")

        df[i] = df[i].Define("Selection","Post_calibration_pt> 300 && Post_calibration_pt< 500 && abs(Mfatjet_eta) < 2.5")

    else:

        df[i] = df[i].Define("Selection", "FatJet_pt> 300 && FatJet_pt< 500 && abs(FatJet_eta) < 2.5")


    if str(i) == 'QCD6_flash' or str(i) == 'QCD7_flash' or str(i) == 'QCD8_flash' or str(i) == 'signal_flash':
        df[i] = (
            df[i]
            .Define("new_discriminator", "FatJet_particleNetMD_XbbvsQCD[Selection]")
            .Define("FatJet_eta_sel", "FatJet_eta[Selection]")
            .Define("FatJet_phi_sel", "FatJet_phi[Selection]")
            .Define("GenJetAK8_eta_sel", "Take(GenJetAK8_eta, Selection)")
            .Define("GenJetAK8_phi_sel", "Take(GenJetAK8_phi, Selection)")
            .Define("matching_index" , "lepton_matching_index(FatJet_eta_sel, FatJet_phi_sel, GenJetAK8_eta_sel, GenJetAK8_phi_sel)")

        )

    elif str(i) == 'QCD_ph2' or str(i) == 'sig_ph2': 

        df[i]= (df[i]
            .Define("new_discriminator", "Mfatjet_particleNetMD_XbbvsQCD[Selection]")
    )
        
    else:
            df[i] = (
            df[i]
            .Define("FatJet_eta_sel", "FatJet_eta[Selection]")
            .Define("FatJet_phi_sel", "FatJet_phi[Selection]")
            .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[Selection]")
            .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[Selection]")
            .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[Selection]")
            .Define("new_discriminator", "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)")
            )

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

        df[i] = df[i].Define("MgenjetAK8_nbFlavour", "count_nHadrons(GenPart_eta_good, GenPart_phi_good, FatJet_eta_sel, FatJet_phi_sel)").Define("Matching_nb_flavour", "Take(MgenjetAK8_nbFlavour, matching_index)")


    elif str(i) == 'QCD_ph2' or str(i) == 'sig_ph2':

        df[i] = df[i].Define("Matching_nb_flavour", "Take(MgenjetAK8_nbFlavour, new_index)")
    
    else: #* fullsim
        df[i] = (df[i].Define("MgenjetAK8_nbFlavour", "count_nHadrons(GenPart_eta_good, GenPart_phi_good, FatJet_eta_sel, FatJet_phi_sel)")
                 .Define("Matching_nb_flavour", "Take(MgenjetAK8_nbFlavour, FatJet_genJetAK8Idx)"))

    df[i] = (
            df[i]
            .Define("Matching_nb_0", "Matching_nb_flavour==0")
            .Define("Matching_nb_1", "Matching_nb_flavour == 1")
            .Define("Matching_nb_2", "Matching_nb_flavour == 2")
            .Define("discriminator_nb_0", "Take(new_discriminator, Matching_nb_0)")
            .Define("discriminator_nb_1", "Take(new_discriminator, Matching_nb_1)")
            .Define("discriminator_nb_2", "Take(new_discriminator, Matching_nb_2)")      
        )
    hist_nb0[i] = df[i].Histo1D(
        (str(i), str(i) + "; Discriminator; Events", 200, 0, 1), "discriminator_nb_0"
    )

    hist_nb1[i] = df[i].Histo1D(
        (str(i), str(i) + "; Discriminator; Events", 200, 0, 1), "discriminator_nb_1"
    )

    hist_nb2[i] = df[i].Histo1D(
        (str(i), str(i) + "; Discriminator; Events", 200, 0, 1), "discriminator_nb_2"
    )

    h_nb0[i] = hist_nb0[i].GetValue()
    h_nb1[i] = hist_nb1[i].GetValue()
    h_nb2[i] = hist_nb2[i].GetValue()




#! HISTOGRAMS FULLSIM

hist_fullsim_nb0 = h_nb0['QCD1_full'].Clone()
hist_fullsim_nb0.Add(h_nb0['QCD2_full'])
hist_fullsim_nb0.Add(h_nb0['QCD3_full'])
hist_fullsim_nb0.Add(h_nb0['QCD4_full'])
hist_fullsim_nb0.Add(h_nb0['QCD5_full'])
hist_fullsim_nb0.Add(h_nb0['QCD6_full'])
hist_fullsim_nb0.Add(h_nb0['QCD7_full'])
hist_fullsim_nb0.Add(h_nb0['QCD8_full'])
#hist_fullsim_nb0.Add(h_nb0['signal_full'])

hist_fullsim_nb1 = h_nb1['QCD1_full'].Clone()
hist_fullsim_nb1.Add(h_nb1['QCD2_full'])
hist_fullsim_nb1.Add(h_nb1['QCD3_full'])
hist_fullsim_nb1.Add(h_nb1['QCD4_full'])
hist_fullsim_nb1.Add(h_nb1['QCD5_full'])
hist_fullsim_nb1.Add(h_nb1['QCD6_full'])
hist_fullsim_nb1.Add(h_nb1['QCD7_full'])
hist_fullsim_nb1.Add(h_nb1['QCD8_full'])
#hist_fullsim_nb1.Add(h_nb1['signal_full'])

hist_fullsim_nb2 = h_nb2['QCD1_full'].Clone()
hist_fullsim_nb2.Add(h_nb2['QCD2_full'])
hist_fullsim_nb2.Add(h_nb2['QCD3_full'])
hist_fullsim_nb2.Add(h_nb2['QCD4_full'])
hist_fullsim_nb2.Add(h_nb2['QCD5_full'])
hist_fullsim_nb2.Add(h_nb2['QCD6_full'])
hist_fullsim_nb2.Add(h_nb2['QCD7_full'])
hist_fullsim_nb2.Add(h_nb2['QCD8_full'])
#hist_fullsim_nb2.Add(h_nb2['signal_full'])

#! HISTOGRAMS FLASHSHIM 


hist_flashsim_nb0 = h_nb0['QCD6_flash'].Clone()
hist_flashsim_nb0.Add(h_nb0['QCD7_flash'])
hist_flashsim_nb0.Add(h_nb0['QCD8_flash'])
#hist_flashsim_nb0.Add(h_nb0['signal_flash'])

hist_flashsim_nb1 = h_nb1['QCD6_flash'].Clone()
hist_flashsim_nb1.Add(h_nb1['QCD7_flash'])
hist_flashsim_nb1.Add(h_nb1['QCD8_flash'])
#hist_flashsim_nb1.Add(h_nb1['signal_flash'])

hist_flashsim_nb2 = h_nb2['QCD6_flash'].Clone()
hist_flashsim_nb2.Add(h_nb2['QCD7_flash'])
hist_flashsim_nb2.Add(h_nb2['QCD8_flash'])
#hist_flashsim_nb2.Add(h_nb2['signal_flash'])

#! HISTOGRAMS PHASE2   

hist_phase2_nb0 = h_nb0['QCD_ph2'].Clone()
#hist_phase2_nb0.Add(h_nb0['sig_ph2'])

hist_phase2_nb1 = h_nb1['QCD_ph2'].Clone()
#hist_phase2_nb1.Add(h_nb1['sig_ph2'])

hist_phase2_nb2 = h_nb2['QCD_ph2'].Clone()
#hist_phase2_nb2.Add(h_nb2['sig_ph2'])

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



for i in range(1, 201):

    full_nb0 = np.append(hist_fullsim_nb0.Integral(i, 200), full_nb0)

    #fp_full_nb0 = np.append(hist_fullsim_nb0.Integral(i,200), fp_full_nb0)


    full_nb1 = np.append(hist_fullsim_nb1.Integral(i, 200), full_nb1)

    #fp_full_nb1 = np.append(hist_fullsim_nb1.Integral(i,200), fp_full_nb1)


    full_nb2 = np.append(hist_fullsim_nb2.Integral(i, 200), full_nb2)

    #fp_full_nb2 = np.append(hist_fullsim_nb2.Integral(i,200), fp_full_nb2)



    flash_nb0 = np.append(hist_flashsim_nb0.Integral(i, 200), flash_nb0)

    #fp_flash_nb0 = np.append(hist_flashsim_nb0.Integral(i,200), fp_flash_nb0)


    flash_nb1 = np.append(hist_flashsim_nb1.Integral(i, 200), flash_nb1)

    #fp_flash_nb1 = np.append(hist_flashsim_nb1.Integral(i,200), fp_flash_nb1)


    flash_nb2 = np.append(hist_flashsim_nb2.Integral(i, 200), flash_nb2)

    #fp_flash_nb2 = np.append(hist_flashsim_nb2.Integral(i,200), fp_flash_nb2)


    ph2_nb0 = np.append(hist_phase2_nb0.Integral(i, 200), ph2_nb0)

    #fp_ph2_nb0 = np.append(hist_phase2_nb0.Integral(i,200), fp_ph2_nb0)


    ph2_nb1 = np.append(hist_phase2_nb1.Integral(i, 200), ph2_nb1)

    #fp_ph2_nb1 = np.append(hist_phase2_nb1.Integral(i,200), fp_ph2_nb1)


    ph2_nb2 = np.append(hist_phase2_nb2.Integral(i, 200), ph2_nb2)

    #fp_ph2_nb2 = np.append(hist_phase2_nb2.Integral(i,200), fp_ph2_nb2)




total_full_nb0 = hist_fullsim_nb0.Integral(1,200)
total_full_nb1 = hist_fullsim_nb1.Integral(1,200)
total_full_nb2 = hist_fullsim_nb2.Integral(1,200)

total_flash_nb0 = hist_flashsim_nb0.Integral(1,200)
total_flash_nb1 = hist_flashsim_nb1.Integral(1,200)
total_flash_nb2 = hist_flashsim_nb2.Integral(1,200)

total_ph2_nb0 = hist_phase2_nb0.Integral(1,200)
total_ph2_nb1 = hist_phase2_nb1.Integral(1,200)
total_ph2_nb2 = hist_phase2_nb2.Integral(1,200)

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


c1 = ROOT.TCanvas("c1", "Fullsim distribution", 800, 700)


legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

hist_fullsim_nb0.Draw("HIST")
hist_fullsim_nb0.SetTitle("Discriminator distribution for fullsim")
hist_fullsim_nb0.SetLineWidth(2)
hist_fullsim_nb0.SetLineColor(ROOT.kBlue +1)
legend.AddEntry(hist_fullsim_nb0, " b = 0", "l")

hist_fullsim_nb1.Draw("HIST SAME")
hist_fullsim_nb1.SetLineWidth(2)
hist_fullsim_nb1.SetLineColor(ROOT.kRed +1)
legend.AddEntry(hist_fullsim_nb1, " b = 1", "l")

hist_fullsim_nb2.Draw("HIST SAME")
hist_fullsim_nb2.SetLineWidth(2)
hist_fullsim_nb2.SetLineColor(ROOT.kBlack)
legend.AddEntry(hist_fullsim_nb2, " b = 2", "l")

legend.Draw()

c2 = ROOT.TCanvas("c2", "Flashsim distribution", 800, 700)


legend2 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

hist_flashsim_nb0.Draw("HIST")
hist_flashsim_nb0.SetTitle("Discriminator distribution for flashsim")
hist_flashsim_nb0.SetLineWidth(2)
hist_flashsim_nb0.SetLineColor(ROOT.kBlue +1)
legend2.AddEntry(hist_flashsim_nb0, " b = 0", "l")

hist_flashsim_nb1.Draw("HIST SAME")
hist_flashsim_nb1.SetLineWidth(2)
hist_flashsim_nb1.SetLineColor(ROOT.kRed +1)
legend2.AddEntry(hist_flashsim_nb1, " b = 1", "l")

hist_flashsim_nb2.Draw("HIST SAME")
hist_flashsim_nb2.SetLineWidth(2)
hist_flashsim_nb2.SetLineColor(ROOT.kBlack)
legend2.AddEntry(hist_flashsim_nb2, " b = 2", "l")

legend2.Draw()


c3 = ROOT.TCanvas("c3", "Phase2 distribution", 800, 700)


legend3 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

hist_phase2_nb0.Draw("HIST")
hist_phase2_nb0.SetTitle("Discriminator distribution for phase2")
hist_phase2_nb0.SetLineWidth(2)
hist_phase2_nb0.SetLineColor(ROOT.kBlue +1)
legend3.AddEntry(hist_phase2_nb0, " b = 0", "l")
hist_phase2_nb1.Draw("HIST SAME")
hist_phase2_nb1.SetLineWidth(2)
hist_phase2_nb1.SetLineColor(ROOT.kRed +1)
legend3.AddEntry(hist_phase2_nb1, " b = 1", "l")
hist_phase2_nb2.Draw("HIST SAME")
hist_phase2_nb2.SetLineWidth(2)
hist_phase2_nb2.SetLineColor(ROOT.kBlack)
legend3.AddEntry(hist_phase2_nb2, " b = 2", "l")

legend3.Draw()




#! 2b vs 0b

plt.plot(tp_per_full_nb2, tp_per_full_nb0, label = 'fullsim', color = 'seagreen', marker = '.', markersize=3 )
plt.plot(tp_per_flash_nb2, tp_per_flash_nb0, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
plt.plot(tp_per_ph2_nb2, tp_per_ph2_nb0, label = 'phase2', color = 'lightcoral', marker = '.', markersize=3 )

plt.legend()

plt.xlabel('Efficiency distribution of the discriminator for 2b')
plt.ylabel('Efficiency distribution of the discriminator for 0b')

plt.show()

plt.savefig('2b_vs_0b.png')

plt.close()


#! 2b vs 1b

plt.plot(tp_per_full_nb2, tp_per_full_nb1, label = 'fullsim', color = 'seagreen', marker = '.', markersize=3 )
plt.plot(tp_per_flash_nb2, tp_per_flash_nb1, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
plt.plot(tp_per_ph2_nb2, tp_per_ph2_nb1, label = 'phase2', color = 'lightcoral', marker = '.', markersize=3 )

plt.legend()

plt.xlabel('Efficiency distribution of the discriminator for 2b')
plt.ylabel('Efficiency distribution of the discriminator for 1b')

plt.show()

plt.savefig('2b_vs_1b.png')

plt.close()


#! 1b vs 0b

plt.plot(tp_per_full_nb1, tp_per_full_nb0, label = 'fullsim', color = 'seagreen', marker = '.', markersize=3 )
plt.plot(tp_per_flash_nb1, tp_per_flash_nb0, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
plt.plot(tp_per_ph2_nb1, tp_per_ph2_nb0, label = 'phase2', color = 'lightcoral', marker = '.', markersize=3 )

plt.legend()

plt.xlabel('Efficiency distribution of the discriminator for 1b')
plt.ylabel('Efficiency distribution of the discriminator for 0b')

plt.show()

plt.savefig('1b_vs_0b.png')

plt.close()


c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/discr_distribution_fullsim.pdf")
c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/discr_distribution_flashsim.pdf")
c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/discr_distribution_phase2.pdf")
