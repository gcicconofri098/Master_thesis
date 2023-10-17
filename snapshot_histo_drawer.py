import ROOT
import os
import CMS_lumi, tdrstyle
import matplotlib.pyplot as plt
import numpy as np
import re

ROOT.EnableImplicitMT()



df_files = {
    "QCD1_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD1_full.root",
    "QCD2_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD2_full.root",
    "QCD3_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD3_full.root",
    "QCD4_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD4_full.root",
    "QCD5_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD5_full.root",
    "QCD6_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD6_full.root",
    "QCD7_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD7_full.root",
    "QCD8_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD8_full.root",
    "signal_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/signal_full.root",
    "QCD6_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD6_flash.root",
    "QCD7_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD7_flash.root",
    "QCD8_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD8_flash.root",
    "signal_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/signal_flash.root",
    "QCD_ph2": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD_ph2.root",
    "signal_ph2": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/signal_ph2.root"
}

processes = list(df_files.keys())

ROOT.gStyle.SetOptStat(0)

#tdrstyle.setTDRStyle()

#writeExtraText = True


# #change the CMS_lumi variables (see CMS_lumi.py)
# #CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
# #CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
# CMS_lumi.writeExtraText = 1
# CMS_lumi.extraText = "Private Work"
# CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)




df = {}

existing_files = {}

for i in processes:
    try:
        if os.path.getsize(df_files[i])==0:
            print("file is empty")
    except OSError:
        continue
    else:
        existing_files[i] = df_files[i]

existing_processes = list(existing_files.keys())
print(f"existing processes are: {existing_processes}")

h_distributions = {}

for i in existing_processes:

    df[i] = ROOT.RDataFrame("Events", existing_files[i])

    df[i] = df[i].Define("lower_edge_pt", "Selected_pt > 300 && Selected_pt <350")
    df[i] = df[i].Define("upper_edge_pt", "Selected_pt > 450 && Selected_pt <500")

    df[i] = (df[i]
        .Define("lower_edge_pt_discriminator", "new_discriminator[lower_edge_pt]")
        .Define("upper_edge_pt_discriminator", "new_discriminator[upper_edge_pt]")
    )

    df[i] = df[i].Define("discr_hadron_0", "new_discriminator[Matching_hadron_flavour ==0]")

    print("created the dataframes")


for i in existing_processes:
    
    h_distributions[i] = {}

    h_distributions[i]['jet1_discr'] = df[i].Histo1D((str(i), str(i) + "; Discriminator; Events", 100, 0, 1), "jet1_discr").GetValue()
    h_distributions[i]['jet1_softdrop'] = df[i].Histo1D((str(i), str(i) + "; Softdrop mass; Events", 100, 30, 500), "jet1_softdrop").GetValue()
    h_distributions[i]['alljets_discr'] =  df[i].Histo1D((str(i), str(i) + "; Discriminator; Events", 100, 0, 1), "new_discriminator").GetValue()
    h_distributions[i]['alljets_softdrop'] = df[i].Histo1D((str(i), str(i) + "; Softdrop mass; Events", 100, 30, 500), "Softdrop_sel_jets").GetValue()
    h_distributions[i]['matching_nb'] = df[i].Histo1D((str(i), str(i) + "; Number of b; Events",5, 0, 5), "Matching_nb_flavour").GetValue()
    h_distributions[i]['lower_edge_discr'] = df[i].Histo1D((str(i), str(i) + "; Discriminator; Events", 30, 0, 1), "lower_edge_pt_discriminator").GetValue()
    h_distributions[i]['upper_edge_discr'] = df[i].Histo1D((str(i), str(i) + "; Discriminator; Events", 30, 0, 1), "upper_edge_pt_discriminator").GetValue()
    h_distributions[i]['parton_flavour'] = df[i].Histo1D((str(i), str(i) + "; Discriminator; Events", 27, -5, 22), "Matching_parton_flavour").GetValue()
    h_distributions[i]['hadron_flavour'] = df[i].Histo1D((str(i), str(i) + "; Discriminator; Events", 20, 0, 7), "Matching_hadron_flavour").GetValue()

    h_distributions[i]['discr_hadron_0'] = df[i].Histo1D((str(i), str(i) + "; Discriminator; Events", 100, 0, 1), "discr_hadron_0").GetValue()

    
    if str(i) == 'signal_full' or str(i) == 'signal_flash' or str(i) == 'signal_ph2': 
        
        h_distributions[i]['nb_0'] = df[i].Histo1D((str(i), str(i) + "nb 0; Discriminator; Events", 30, 0, 1), "leading_jet_discriminator_nb_0").GetValue()
        h_distributions[i]['nb_1'] = df[i].Histo1D((str(i), str(i) + "nb 1; Discriminator; Events", 30, 0, 1), "leading_jet_discriminator_nb_1").GetValue()
        h_distributions[i]['nb_2'] = df[i].Histo1D((str(i), str(i) + "nb 2; Discriminator; Events", 30, 0, 1), "leading_jet_discriminator_nb_2").GetValue()
    
    else:
        
        h_distributions[i]['nb_0'] = df[i].Histo1D((str(i), str(i) + "nb 0; Discriminator; Events", 30, 0, 1), "leading_jet_discriminator_nb_0").GetValue()
        h_distributions[i]['nb_1'] = df[i].Histo1D((str(i), str(i) + "nb 1; Discriminator; Events", 30, 0, 1), "leading_jet_discriminator_nb_1").GetValue()
        h_distributions[i]['nb_2'] = df[i].Histo1D((str(i), str(i) + "nb 2; Discriminator; Events", 30, 0, 1), "leading_jet_discriminator_nb_2").GetValue()

    #h_distributions[i]['alljets_eta'] = df[i].Histo1D((str(i), str(i) + "; Eta; Events", 100, -2.5, 2.5), "FatJet_eta_sel").GetValue()
    #h_distributions[i]['alljets_phi'] = df[i].Histo1D((str(i), str(i) + "; Phi; Events", 100, -3, 3), "FatJet_phi_sel").GetValue()


r_full = re.compile("QCD._full")
r_flash = re.compile("QCD._flash")


QCD_full_processes = list(filter(r_full.match, existing_processes))
QCD_flash_processes = list(filter(r_flash.match, existing_processes))

print("QCD fullsim processes:", QCD_full_processes)
print("QCD flashsim processes:", QCD_flash_processes)


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

#! QCD FULLSIM STACKING

print("starting to stack histos")

QCD_full_nb0 = h_distributions[str(QCD_full_processes[0])]['nb_0'].Clone()
QCD_full_nb1 = h_distributions[str(QCD_full_processes[0])]['nb_1'].Clone()
QCD_full_nb2 = h_distributions[str(QCD_full_processes[0])]['nb_2'].Clone()
QCD_full_jet1 = h_distributions[str(QCD_full_processes[0])]['jet1_discr'].Clone()
QCD_full = h_distributions[str(QCD_full_processes[0])]['alljets_discr'].Clone()
QCD_full_nb_distr = h_distributions[str(QCD_full_processes[0])]['matching_nb'].Clone() 
QCD_full_lower_edge_discr = h_distributions[str(QCD_full_processes[0])]['lower_edge_discr'].Clone()
QCD_full_upper_edge_discr = h_distributions[str(QCD_full_processes[0])]['upper_edge_discr'].Clone()
QCD_full_parton_flavour = h_distributions[str(QCD_full_processes[0])]['parton_flavour'].Clone()
QCD_full_hadron_flavour = h_distributions[str(QCD_full_processes[0])]['hadron_flavour'].Clone()

QCD_full_discr_had_flav_0 = h_distributions[str(QCD_full_processes[0])]['discr_hadron_0'].Clone()

for i in QCD_full_processes:
    if str(i) == QCD_full_processes[0]:
        continue
    else:
        QCD_full_nb0.Add(h_distributions[i]['nb_0'])
        QCD_full_nb1.Add(h_distributions[i]['nb_1'])
        QCD_full_nb2.Add(h_distributions[i]['nb_2'])
        QCD_full_jet1.Add(h_distributions[i]['jet1_discr'])
        QCD_full.Add(h_distributions[i]['alljets_discr'])
        QCD_full_nb_distr.Add(h_distributions[i]['matching_nb'])
        QCD_full_lower_edge_discr.Add(h_distributions[i]['lower_edge_discr'])
        QCD_full_upper_edge_discr.Add(h_distributions[i]['upper_edge_discr'])
        QCD_full_hadron_flavour.Add(h_distributions[i]['hadron_flavour'])
        QCD_full_parton_flavour.Add(h_distributions[i]['parton_flavour'])

        QCD_full_discr_had_flav_0.Add(h_distributions[i]['discr_hadron_0'])

        print(f"adding histo for {i}")

QCD_full_nb0_entries = (QCD_full_nb0.GetEntries())
QCD_full_nb1_entries = (QCD_full_nb1.GetEntries())
QCD_full_nb2_entries = (QCD_full_nb2.GetEntries())
print("entries fullsim QCD from QCD_full:", QCD_full.GetEntries())

#! QCD FLASHSIM STACKING

QCD_flash_nb0 = h_distributions[str(QCD_flash_processes[0])]['nb_0'].Clone()
QCD_flash_nb1 = h_distributions[str(QCD_flash_processes[0])]['nb_1'].Clone()
QCD_flash_nb2 = h_distributions[str(QCD_flash_processes[0])]['nb_2'].Clone()
QCD_flash_jet1 = h_distributions[str(QCD_flash_processes[0])]['jet1_discr'].Clone()
QCD_flash = h_distributions[str(QCD_flash_processes[0])]['alljets_discr'].Clone()
QCD_flash_nb_distr = h_distributions[str(QCD_flash_processes[0])]['matching_nb'].Clone()

QCD_flash_lower_edge_discr = h_distributions[str(QCD_flash_processes[0])]['lower_edge_discr'].Clone()
QCD_flash_upper_edge_discr = h_distributions[str(QCD_flash_processes[0])]['upper_edge_discr'].Clone()
QCD_flash_parton_flavour = h_distributions[str(QCD_flash_processes[0])]['parton_flavour'].Clone()
QCD_flash_hadron_flavour = h_distributions[str(QCD_flash_processes[0])]['hadron_flavour'].Clone()

QCD_flash_discr_had_flav_0 = h_distributions[str(QCD_flash_processes[0])]['discr_hadron_0'].Clone()

for i in QCD_flash_processes:
    if str(i) == QCD_flash_processes[0]:
        continue
    else:
        QCD_flash_nb0.Add(h_distributions[i]['nb_0'])
        QCD_flash_nb1.Add(h_distributions[i]['nb_1'])
        QCD_flash_nb2.Add(h_distributions[i]['nb_2'])
        QCD_flash_jet1.Add(h_distributions[i]['jet1_discr'])
        QCD_flash.Add(h_distributions[i]['alljets_discr'])
        QCD_flash_nb_distr.Add(h_distributions[i]['matching_nb'])

        QCD_flash_lower_edge_discr.Add(h_distributions[i]['lower_edge_discr'])
        QCD_flash_upper_edge_discr.Add(h_distributions[i]['upper_edge_discr'])
        QCD_flash_hadron_flavour.Add(h_distributions[i]['hadron_flavour'])
        QCD_flash_parton_flavour.Add(h_distributions[i]['parton_flavour'])

        QCD_flash_discr_had_flav_0.Add(h_distributions[i]['discr_hadron_0'])

        print(f"adding histo for {i}")

QCD_flash_nb0_entries = (QCD_flash_nb0.GetEntries())
QCD_flash_nb1_entries = (QCD_flash_nb1.GetEntries())
QCD_flash_nb2_entries = (QCD_flash_nb2.GetEntries())

#! entries phase2

#QCD_entries_ph2_jet1 = h_discr1['QCD_ph2'].GetEntries()

QCD_ph2_nb0_entries = h_distributions['QCD_ph2']['nb_0'].GetEntries()
QCD_ph2_nb1_entries = h_distributions['QCD_ph2']['nb_1'].GetEntries()
QCD_ph2_nb2_entries = h_distributions['QCD_ph2']['nb_2'].GetEntries()



bin_lower = np.array([])

for i in range(1, 30):
    print(f"lower bin edge: {QCD_full_parton_flavour.GetBinLowEdge(i)}, and QCD full has {QCD_full_parton_flavour.GetBinContent(i)} events" )
    print(f"lower bin edge: {QCD_full_parton_flavour.GetBinLowEdge(i)}, and signal full has {h_distributions['signal_full']['parton_flavour'].GetBinContent(i)} events" )
    
    print(f"lower bin edge: {QCD_full_parton_flavour.GetBinLowEdge(i)}, and QCD flash has {QCD_flash_parton_flavour.GetBinContent(i)} events" )
    print(f"lower bin edge: {QCD_full_parton_flavour.GetBinLowEdge(i)}, and signal flash has {h_distributions['signal_flash']['parton_flavour'].GetBinContent(i)} events" )
    
    print(f"lower bin edge: {QCD_full_parton_flavour.GetBinLowEdge(i)}, and QCD ph2 has {h_distributions['QCD_ph2']['parton_flavour'].GetBinContent(i)} events" )
    print(f"lower bin edge: {QCD_full_parton_flavour.GetBinLowEdge(i)}, and signal ph2 has {h_distributions['signal_ph2']['parton_flavour'].GetBinContent(i)} events" )







print("starting to draw the histos")







#! NB DISTRIBUTIONS

c1 = ROOT.TCanvas("c1", "Signal discriminator distribution nb 0", 800, 700)


legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

h_distributions["signal_full"]['nb_0'].Draw("HIST")
h_distributions["signal_full"]['nb_0'].SetTitle("Discriminator distribution for signal, nb = 0")
h_distributions["signal_full"]['nb_0'].SetLineWidth(2)
h_distributions["signal_full"]['nb_0'].SetLineColor(ROOT.kBlue +1)
h_distributions["signal_full"]['nb_0'].Scale(1 / h_distributions["signal_full"]['nb_0'].Integral())
h_distributions['signal_full']['nb_0'].SetMinimum(10e-4)
h_distributions['signal_full']['nb_0'].SetMaximum(1)

legend.AddEntry(h_distributions["signal_full"]['nb_0'], "Run2 fullsim", "l")

h_distributions["signal_flash"]['nb_0'].Draw("HIST SAME")
h_distributions["signal_flash"]['nb_0'].SetLineWidth(2)
h_distributions["signal_flash"]['nb_0'].SetLineColor(ROOT.kRed +1)
legend.AddEntry(h_distributions["signal_flash"]['nb_0'], " flashsim", "l")
h_distributions["signal_flash"]['nb_0'].Scale(1 / h_distributions["signal_flash"]['nb_0'].Integral())


h_distributions["signal_ph2"]['nb_0'].Draw("HIST SAME")
h_distributions["signal_ph2"]['nb_0'].SetLineWidth(2)
h_distributions["signal_ph2"]['nb_0'].SetLineColor(ROOT.kBlack)
h_distributions["signal_ph2"]['nb_0'].Scale(1 / h_distributions["signal_ph2"]['nb_0'].Integral())

legend.AddEntry(h_distributions["signal_ph2"]['nb_0'], "phase2 fullsim", "l")
c1.SetLogy()
legend.Draw()


c2 = ROOT.TCanvas("c2", "Signal discriminator distribution nb 1", 800, 700)


legend2 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

h_distributions["signal_full"]['nb_1'].Draw("HIST")
h_distributions["signal_full"]['nb_1'].SetTitle("Discriminator distribution for signal, nb = 1")
h_distributions["signal_full"]['nb_1'].SetLineWidth(2)
h_distributions["signal_full"]['nb_1'].SetLineColor(ROOT.kBlue +1)
h_distributions["signal_full"]['nb_1'].Scale(1 / h_distributions["signal_full"]['nb_1'].Integral())
h_distributions['signal_full']['nb_1'].SetMinimum(10e-4)
h_distributions['signal_full']['nb_1'].SetMaximum(1)

legend2.AddEntry(h_distributions["signal_full"]['nb_1'], "Run2 fullsim", "l")

h_distributions["signal_flash"]['nb_1'].Draw("HIST SAME")
h_distributions["signal_flash"]['nb_1'].SetLineWidth(2)
h_distributions["signal_flash"]['nb_1'].SetLineColor(ROOT.kRed +1)
legend2.AddEntry(h_distributions["signal_flash"]['nb_1'], " flashsim", "l")
h_distributions["signal_flash"]['nb_1'].Scale(1 / h_distributions["signal_flash"]['nb_1'].Integral())


h_distributions["signal_ph2"]['nb_1'].Draw("HIST SAME")
h_distributions["signal_ph2"]['nb_1'].SetLineWidth(2)
h_distributions["signal_ph2"]['nb_1'].SetLineColor(ROOT.kBlack)
h_distributions["signal_ph2"]['nb_1'].Scale(1 / h_distributions["signal_ph2"]['nb_1'].Integral())

legend2.AddEntry(h_distributions["signal_ph2"]['nb_1'], "phase2 fullsim", "l")
c2.SetLogy()
legend2.Draw()



c3 = ROOT.TCanvas("c3", "Signal discriminator distribution nb 2", 800, 700)


legend3 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

h_distributions["signal_full"]['nb_2'].Draw("HIST")
h_distributions["signal_full"]['nb_2'].SetTitle("Discriminator distribution for signal, nb = 2")
h_distributions["signal_full"]['nb_2'].SetLineWidth(2)
h_distributions["signal_full"]['nb_2'].SetLineColor(ROOT.kBlue +1)
h_distributions["signal_full"]['nb_2'].Scale(1 / h_distributions["signal_full"]['nb_2'].Integral())
h_distributions['signal_full']['nb_2'].SetMinimum(10e-4)
h_distributions['signal_full']['nb_2'].SetMaximum(1)


legend3.AddEntry(h_distributions["signal_full"]['nb_2'], "Run2 fullsim", "l")

h_distributions["signal_flash"]['nb_2'].Draw("HIST SAME")
h_distributions["signal_flash"]['nb_2'].SetLineWidth(2)
h_distributions["signal_flash"]['nb_2'].SetLineColor(ROOT.kRed +1)
h_distributions["signal_flash"]['nb_2'].Scale(1 / h_distributions["signal_flash"]['nb_2'].Integral())

legend3.AddEntry(h_distributions["signal_flash"]['nb_2'], " flashsim", "l")

h_distributions["signal_ph2"]['nb_2'].Draw("HIST SAME")
h_distributions["signal_ph2"]['nb_2'].SetLineWidth(2)
h_distributions["signal_ph2"]['nb_2'].SetLineColor(ROOT.kBlack)
h_distributions["signal_ph2"]['nb_2'].Scale(1 / h_distributions["signal_ph2"]['nb_2'].Integral())

legend3.AddEntry(h_distributions["signal_ph2"]['nb_2'], "phase2 fullsim", "l")
c3.SetLogy()

legend3.Draw()

#TODO BACKGROUND


c4 = ROOT.TCanvas("c4", "Background discriminator distribution nb 0", 800, 700)


legend4 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

QCD_full_nb0.Draw("HIST")
QCD_full_nb0.SetTitle("Discriminator distribution for background, nb = 0")
QCD_full_nb0.SetLineWidth(2)
QCD_full_nb0.SetLineColor(ROOT.kBlue +1)
QCD_full_nb0.Scale(1 / QCD_full_nb0.Integral())
QCD_full_nb0.SetMinimum(10e-4)
QCD_full_nb0.SetMaximum(1)

legend4.AddEntry(QCD_full_nb0, "Run2 fullsim", "l")

QCD_flash_nb0.Draw("HIST SAME")
QCD_flash_nb0.SetLineWidth(2)
QCD_flash_nb0.SetLineColor(ROOT.kRed +1)
QCD_flash_nb0.Scale(1 / QCD_flash_nb0.Integral())

legend4.AddEntry(QCD_flash_nb0, " flashsim", "l")

h_distributions["QCD_ph2"]['nb_0'].Draw("HIST SAME")
h_distributions["QCD_ph2"]['nb_0'].SetLineWidth(2)
h_distributions["QCD_ph2"]['nb_0'].SetLineColor(ROOT.kBlack)
h_distributions["QCD_ph2"]['nb_0'].Scale(1 / h_distributions["QCD_ph2"]['nb_0'].Integral())

legend4.AddEntry(h_distributions["QCD_ph2"]['nb_0'], "phase2 fullsim", "l")
c4.SetLogy()
legend4.Draw()


c5 = ROOT.TCanvas("c5", "Background discriminator distribution nb 1", 800, 700)


legend5 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

QCD_full_nb1.Draw("HIST")
QCD_full_nb1.SetTitle("Discriminator distribution for background, nb = 1")
QCD_full_nb1.SetLineWidth(2)
QCD_full_nb1.SetLineColor(ROOT.kBlue +1)
QCD_full_nb1.Scale(1 / QCD_full_nb1.Integral())
QCD_full_nb1.SetMinimum(10e-4)
QCD_full_nb1.SetMaximum(1)


legend5.AddEntry(QCD_full_nb1, "Run2 fullsim", "l")

QCD_flash_nb1.Draw("HIST SAME")
QCD_flash_nb1.SetLineWidth(2)
QCD_flash_nb1.SetLineColor(ROOT.kRed +1)
QCD_flash_nb1.Scale(1 / QCD_flash_nb1.Integral())

legend5.AddEntry(QCD_flash_nb1, " flashsim", "l")

h_distributions["QCD_ph2"]['nb_1'].Draw("HIST SAME")
h_distributions["QCD_ph2"]['nb_1'].SetLineWidth(2)
h_distributions["QCD_ph2"]['nb_1'].SetLineColor(ROOT.kBlack)
h_distributions["QCD_ph2"]['nb_1'].Scale(1 / h_distributions["QCD_ph2"]['nb_1'].Integral())

legend5.AddEntry(h_distributions["QCD_ph2"]['nb_1'], "phase2 fullsim", "l")
c5.SetLogy()
legend5.Draw()



c6 = ROOT.TCanvas("c6", "Background discriminator distribution nb 2", 800, 700)


legend6 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

QCD_full_nb2.Draw("HIST")
QCD_full_nb2.SetTitle("Discriminator distribution for background, nb = 2")
QCD_full_nb2.SetLineWidth(2)
QCD_full_nb2.SetLineColor(ROOT.kBlue +1)
QCD_full_nb2.Scale(1 / QCD_full_nb2.Integral())
QCD_full_nb2.SetMinimum(10e-4)
QCD_full_nb2.SetMaximum(1)

legend6.AddEntry(QCD_full_nb2, "Run2 fullsim", "l")

QCD_flash_nb2.Draw("HIST SAME")
QCD_flash_nb2.SetLineWidth(2)
QCD_flash_nb2.SetLineColor(ROOT.kRed +1)
QCD_flash_nb2.Scale(1 / QCD_flash_nb2.Integral())

legend6.AddEntry(QCD_flash_nb2, " flashsim", "l")

h_distributions["QCD_ph2"]['nb_2'].Draw("HIST SAME")
h_distributions["QCD_ph2"]['nb_2'].SetLineWidth(2)
h_distributions["QCD_ph2"]['nb_2'].SetLineColor(ROOT.kBlack)
h_distributions["QCD_ph2"]['nb_2'].Scale(1 / h_distributions["QCD_ph2"]['nb_2'].Integral())

legend6.AddEntry(h_distributions["QCD_ph2"]['nb_2'], "phase2 fullsim", "l")
c6.SetLogy()

legend6.Draw()


#TODO DISTRIBUTIONS OF NB

c7 = ROOT.TCanvas("c7", "Background discriminator distribution nb 2", 800, 700)


legend7 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

QCD_full_nb_distr.Draw("HIST")
QCD_full_nb_distr.SetTitle("Number of b")
QCD_full_nb_distr.SetLineWidth(2)
QCD_full_nb_distr.SetLineColor(ROOT.kBlue +1)
QCD_full_nb_distr.Scale(1 / QCD_full_nb_distr.Integral())
# QCD_full_nb_distr.SetMinimum(10e-4)
#QCD_full_nb_distr.SetMaximum(10e7)

legend7.AddEntry(QCD_full_nb_distr, "Run2 fullsim, background", "l")


h_distributions["signal_full"]['matching_nb'].Draw("HIST SAME")
h_distributions["signal_full"]['matching_nb'].SetLineWidth(2)
h_distributions["signal_full"]['matching_nb'].SetLineColor(ROOT.kBlue +1)
h_distributions["signal_full"]['matching_nb'].Scale(1 / h_distributions["signal_full"]['matching_nb'].Integral())
h_distributions['signal_full']['matching_nb'].SetLineStyle(2)
legend7.AddEntry(h_distributions["signal_full"]['matching_nb'], "Run2 fullsim, signal", "l")



QCD_flash_nb_distr.Draw("HIST SAME")
QCD_flash_nb_distr.SetLineWidth(2)
QCD_flash_nb_distr.SetLineColor(ROOT.kRed +1)
QCD_flash_nb_distr.Scale(1 / QCD_flash_nb_distr.Integral())

legend7.AddEntry(QCD_flash_nb_distr, " flashsim, background", "l")


h_distributions["signal_flash"]['matching_nb'].Draw("HIST SAME")
h_distributions["signal_flash"]['matching_nb'].SetLineWidth(2)
h_distributions["signal_flash"]['matching_nb'].SetLineColor(ROOT.kRed +1)
h_distributions["signal_flash"]['matching_nb'].Scale(1 / h_distributions["signal_flash"]['matching_nb'].Integral())
h_distributions['signal_flash']['matching_nb'].SetLineStyle(2)

legend7.AddEntry(h_distributions["signal_flash"]['matching_nb'], "flashsim, signal", "l")


h_distributions["QCD_ph2"]['matching_nb'].Draw("HIST SAME")
h_distributions["QCD_ph2"]['matching_nb'].SetLineWidth(2)
h_distributions["QCD_ph2"]['matching_nb'].SetLineColor(ROOT.kBlack)
h_distributions["QCD_ph2"]['matching_nb'].Scale(1 / h_distributions["QCD_ph2"]['matching_nb'].Integral())

legend7.AddEntry(h_distributions["QCD_ph2"]['matching_nb'], "phase2 fullsim, background", "l")

h_distributions["signal_ph2"]['matching_nb'].Draw("HIST SAME")
h_distributions["signal_ph2"]['matching_nb'].SetLineWidth(2)
h_distributions["signal_ph2"]['matching_nb'].SetLineColor(ROOT.kBlack)
#h_distributions['signal_ph2']['matching_nb'].Scale(100)
h_distributions["signal_ph2"]['matching_nb'].Scale(1 / h_distributions["signal_ph2"]['matching_nb'].Integral())
h_distributions['signal_ph2']['matching_nb'].SetLineStyle(2)

legend7.AddEntry(h_distributions["signal_ph2"]['matching_nb'], "phase2 fullsim, signal", "l")


c7.SetLogy()

legend7.Draw()

#! UPPER AND LOWER PT EDGES

c8 = ROOT.TCanvas("c8", "Background discriminator distribution nb 2", 800, 700)


legend8 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

QCD_full_lower_edge_discr.Draw("HIST")
QCD_full_lower_edge_discr.SetTitle("Discriminator for lower pt edge")
QCD_full_lower_edge_discr.SetLineWidth(2)
QCD_full_lower_edge_discr.SetLineColor(ROOT.kBlue +1)
QCD_full_lower_edge_discr.Scale(1 / QCD_full_lower_edge_discr.Integral())
# QCD_full_lower_edge_discr.SetMinimum(10e-4)
#QCD_full_lower_edge_discr.SetMaximum(10e7)

legend8.AddEntry(QCD_full_lower_edge_discr, "Run2 fullsim, background", "l")


h_distributions["signal_full"]['lower_edge_discr'].Draw("HIST SAME")
h_distributions["signal_full"]['lower_edge_discr'].SetLineWidth(2)
h_distributions["signal_full"]['lower_edge_discr'].SetLineColor(ROOT.kBlue +1)
h_distributions["signal_full"]['lower_edge_discr'].Scale(1 / h_distributions["signal_full"]['lower_edge_discr'].Integral())
h_distributions['signal_full']['lower_edge_discr'].SetLineStyle(2)
legend8.AddEntry(h_distributions["signal_full"]['lower_edge_discr'], "Run2 fullsim, signal", "l")



QCD_flash_lower_edge_discr.Draw("HIST SAME")
QCD_flash_lower_edge_discr.SetLineWidth(2)
QCD_flash_lower_edge_discr.SetLineColor(ROOT.kRed +1)
QCD_flash_lower_edge_discr.Scale(1 / QCD_flash_lower_edge_discr.Integral())

legend8.AddEntry(QCD_flash_lower_edge_discr, " flashsim, background", "l")


h_distributions["signal_flash"]['lower_edge_discr'].Draw("HIST SAME")
h_distributions["signal_flash"]['lower_edge_discr'].SetLineWidth(2)
h_distributions["signal_flash"]['lower_edge_discr'].SetLineColor(ROOT.kRed +1)
h_distributions["signal_flash"]['lower_edge_discr'].Scale(1 / h_distributions["signal_flash"]['lower_edge_discr'].Integral())
h_distributions['signal_flash']['lower_edge_discr'].SetLineStyle(2)

legend8.AddEntry(h_distributions["signal_flash"]['lower_edge_discr'], "flashsim, signal", "l")


h_distributions["QCD_ph2"]['lower_edge_discr'].Draw("HIST SAME")
h_distributions["QCD_ph2"]['lower_edge_discr'].SetLineWidth(2)
h_distributions["QCD_ph2"]['lower_edge_discr'].SetLineColor(ROOT.kBlack)
h_distributions["QCD_ph2"]['lower_edge_discr'].Scale(1 / h_distributions["QCD_ph2"]['lower_edge_discr'].Integral())

legend8.AddEntry(h_distributions["QCD_ph2"]['lower_edge_discr'], "phase2 fullsim, background", "l")

h_distributions["signal_ph2"]['lower_edge_discr'].Draw("HIST SAME")
h_distributions["signal_ph2"]['lower_edge_discr'].SetLineWidth(2)
h_distributions["signal_ph2"]['lower_edge_discr'].SetLineColor(ROOT.kBlack)
#h_distributions['signal_ph2']['lower_edge_discr'].Scale(100)
h_distributions["signal_ph2"]['lower_edge_discr'].Scale(1 / h_distributions["signal_ph2"]['lower_edge_discr'].Integral())
h_distributions['signal_ph2']['lower_edge_discr'].SetLineStyle(2)

legend8.AddEntry(h_distributions["signal_ph2"]['lower_edge_discr'], "phase2 fullsim, signal", "l")


c8.SetLogy()

legend8.Draw()

c9 = ROOT.TCanvas("c9", "Background discriminator distribution nb 2", 800, 700)


legend9 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

QCD_full_upper_edge_discr.Draw("HIST")
QCD_full_upper_edge_discr.SetTitle("Discriminator for upper pt edge ")
QCD_full_upper_edge_discr.SetLineWidth(2)
QCD_full_upper_edge_discr.SetLineColor(ROOT.kBlue +1)
QCD_full_upper_edge_discr.Scale(1 / QCD_full_upper_edge_discr.Integral())
# QCD_full_upper_edge_discr.SetMinimum(10e-4)
#QCD_full_upper_edge_discr.SetMaximum(10e7)

legend9.AddEntry(QCD_full_upper_edge_discr, "Run2 fullsim, background", "l")


h_distributions["signal_full"]['upper_edge_discr'].Draw("HIST SAME")
h_distributions["signal_full"]['upper_edge_discr'].SetLineWidth(2)
h_distributions["signal_full"]['upper_edge_discr'].SetLineColor(ROOT.kBlue +1)
h_distributions["signal_full"]['upper_edge_discr'].Scale(1 / h_distributions["signal_full"]['upper_edge_discr'].Integral())
h_distributions['signal_full']['upper_edge_discr'].SetLineStyle(2)
legend9.AddEntry(h_distributions["signal_full"]['upper_edge_discr'], "Run2 fullsim, signal", "l")



QCD_flash_upper_edge_discr.Draw("HIST SAME")
QCD_flash_upper_edge_discr.SetLineWidth(2)
QCD_flash_upper_edge_discr.SetLineColor(ROOT.kRed +1)
QCD_flash_upper_edge_discr.Scale(1 / QCD_flash_upper_edge_discr.Integral())

legend9.AddEntry(QCD_flash_upper_edge_discr, " flashsim, background", "l")


h_distributions["signal_flash"]['upper_edge_discr'].Draw("HIST SAME")
h_distributions["signal_flash"]['upper_edge_discr'].SetLineWidth(2)
h_distributions["signal_flash"]['upper_edge_discr'].SetLineColor(ROOT.kRed +1)
h_distributions["signal_flash"]['upper_edge_discr'].Scale(1 / h_distributions["signal_flash"]['upper_edge_discr'].Integral())
h_distributions['signal_flash']['upper_edge_discr'].SetLineStyle(2)

legend9.AddEntry(h_distributions["signal_flash"]['upper_edge_discr'], "flashsim, signal", "l")


h_distributions["QCD_ph2"]['upper_edge_discr'].Draw("HIST SAME")
h_distributions["QCD_ph2"]['upper_edge_discr'].SetLineWidth(2)
h_distributions["QCD_ph2"]['upper_edge_discr'].SetLineColor(ROOT.kBlack)
h_distributions["QCD_ph2"]['upper_edge_discr'].Scale(1 / h_distributions["QCD_ph2"]['upper_edge_discr'].Integral())

legend9.AddEntry(h_distributions["QCD_ph2"]['upper_edge_discr'], "phase2 fullsim, background", "l")

h_distributions["signal_ph2"]['upper_edge_discr'].Draw("HIST SAME")
h_distributions["signal_ph2"]['upper_edge_discr'].SetLineWidth(2)
h_distributions["signal_ph2"]['upper_edge_discr'].SetLineColor(ROOT.kBlack)
#h_distributions['signal_ph2']['upper_edge_discr'].Scale(100)
h_distributions["signal_ph2"]['upper_edge_discr'].Scale(1 / h_distributions["signal_ph2"]['upper_edge_discr'].Integral())
h_distributions['signal_ph2']['upper_edge_discr'].SetLineStyle(2)

legend9.AddEntry(h_distributions["signal_ph2"]['upper_edge_discr'], "phase2 fullsim, signal", "l")


c9.SetLogy()

legend9.Draw()



c10 = ROOT.TCanvas("c10", "Background discriminator distribution nb 2", 800, 700)


legend10 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

QCD_full_parton_flavour.Draw("HIST")
QCD_full_parton_flavour.SetTitle("Parton flavour")
QCD_full_parton_flavour.SetLineWidth(2)
QCD_full_parton_flavour.SetLineColor(ROOT.kBlue +1)
#QCD_full_parton_flavour.Scale(1 / QCD_full_parton_flavour.Integral())
QCD_full_parton_flavour.SetMinimum(1)
#QCD_full_parton_flavour.SetMaximum(10e7)

legend10.AddEntry(QCD_full_parton_flavour, "Run2 fullsim, background", "l")


h_distributions["signal_full"]['parton_flavour'].Draw("HIST SAME")
h_distributions["signal_full"]['parton_flavour'].SetLineWidth(3)
h_distributions["signal_full"]['parton_flavour'].SetLineColor(ROOT.kBlue +1)
#h_distributions["signal_full"]['parton_flavour'].Scale(1 / h_distributions["signal_full"]['parton_flavour'].Integral())
h_distributions['signal_full']['parton_flavour'].SetLineStyle(2)
legend10.AddEntry(h_distributions["signal_full"]['parton_flavour'], "Run2 fullsim, signal", "l")



QCD_flash_parton_flavour.Draw("HIST SAME")
QCD_flash_parton_flavour.SetLineWidth(2)
QCD_flash_parton_flavour.SetLineColor(ROOT.kRed +1)
#QCD_flash_parton_flavour.Scale(1 / QCD_flash_parton_flavour.Integral())

legend10.AddEntry(QCD_flash_parton_flavour, " flashsim, background", "l")


h_distributions["signal_flash"]['parton_flavour'].Draw("HIST SAME")
h_distributions["signal_flash"]['parton_flavour'].SetLineWidth(3)
h_distributions["signal_flash"]['parton_flavour'].SetLineColor(ROOT.kRed +1)
#h_distributions["signal_flash"]['parton_flavour'].Scale(1 / h_distributions["signal_flash"]['parton_flavour'].Integral())
h_distributions['signal_flash']['parton_flavour'].SetLineStyle(2)

legend10.AddEntry(h_distributions["signal_flash"]['parton_flavour'], "flashsim, signal", "l")


h_distributions["QCD_ph2"]['parton_flavour'].Draw("HIST SAME")
h_distributions["QCD_ph2"]['parton_flavour'].SetLineWidth(2)
h_distributions["QCD_ph2"]['parton_flavour'].SetLineColor(ROOT.kBlack)
#h_distributions["QCD_ph2"]['parton_flavour'].Scale(1 / h_distributions["QCD_ph2"]['parton_flavour'].Integral())

legend10.AddEntry(h_distributions["QCD_ph2"]['parton_flavour'], "phase2 fullsim, background", "l")

h_distributions["signal_ph2"]['parton_flavour'].Draw("HIST SAME")
h_distributions["signal_ph2"]['parton_flavour'].SetLineWidth(3)
h_distributions["signal_ph2"]['parton_flavour'].SetLineColor(ROOT.kBlack)
#h_distributions["signal_ph2"]['parton_flavour'].Scale(1 / h_distributions["signal_ph2"]['parton_flavour'].Integral())
h_distributions['signal_ph2']['parton_flavour'].SetLineStyle(2)

legend10.AddEntry(h_distributions["signal_ph2"]['parton_flavour'], "phase2 fullsim, signal", "l")


c10.SetLogy()

legend10.Draw()



c11 = ROOT.TCanvas("c11", "Background discriminator distribution nb 2", 800, 700)


legend11 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

QCD_full_hadron_flavour.Draw("HIST")
QCD_full_hadron_flavour.SetTitle("Hadron flavour ")
QCD_full_hadron_flavour.SetLineWidth(2)
QCD_full_hadron_flavour.SetLineColor(ROOT.kBlue +1)
QCD_full_hadron_flavour.Scale(1 / QCD_full_hadron_flavour.Integral())
# QCD_full_hadron_flavour.SetMinimum(10e-4)
#QCD_full_hadron_flavour.SetMaximum(10e7)

legend11.AddEntry(QCD_full_hadron_flavour, "Run2 fullsim, background", "l")


h_distributions["signal_full"]['hadron_flavour'].Draw("HIST SAME")
h_distributions["signal_full"]['hadron_flavour'].SetLineWidth(2)
h_distributions["signal_full"]['hadron_flavour'].SetLineColor(ROOT.kBlue +1)
h_distributions["signal_full"]['hadron_flavour'].Scale(1 / h_distributions["signal_full"]['hadron_flavour'].Integral())
h_distributions['signal_full']['hadron_flavour'].SetLineStyle(2)
legend11.AddEntry(h_distributions["signal_full"]['hadron_flavour'], "Run2 fullsim, signal", "l")



QCD_flash_hadron_flavour.Draw("HIST SAME")
QCD_flash_hadron_flavour.SetLineWidth(2)
QCD_flash_hadron_flavour.SetLineColor(ROOT.kRed +1)
QCD_flash_hadron_flavour.Scale(1 / QCD_flash_hadron_flavour.Integral())

legend11.AddEntry(QCD_flash_hadron_flavour, " flashsim, background", "l")


h_distributions["signal_flash"]['hadron_flavour'].Draw("HIST SAME")
h_distributions["signal_flash"]['hadron_flavour'].SetLineWidth(2)
h_distributions["signal_flash"]['hadron_flavour'].SetLineColor(ROOT.kRed +1)
h_distributions["signal_flash"]['hadron_flavour'].Scale(1 / h_distributions["signal_flash"]['hadron_flavour'].Integral())
h_distributions['signal_flash']['hadron_flavour'].SetLineStyle(2)

legend11.AddEntry(h_distributions["signal_flash"]['hadron_flavour'], "flashsim, signal", "l")


h_distributions["QCD_ph2"]['hadron_flavour'].Draw("HIST SAME")
h_distributions["QCD_ph2"]['hadron_flavour'].SetLineWidth(2)
h_distributions["QCD_ph2"]['hadron_flavour'].SetLineColor(ROOT.kBlack)
h_distributions["QCD_ph2"]['hadron_flavour'].Scale(1 / h_distributions["QCD_ph2"]['hadron_flavour'].Integral())

legend11.AddEntry(h_distributions["QCD_ph2"]['hadron_flavour'], "phase2 fullsim, background", "l")

h_distributions["signal_ph2"]['hadron_flavour'].Draw("HIST SAME")
h_distributions["signal_ph2"]['hadron_flavour'].SetLineWidth(2)
h_distributions["signal_ph2"]['hadron_flavour'].SetLineColor(ROOT.kBlack)
h_distributions["signal_ph2"]['hadron_flavour'].Scale(1 / h_distributions["signal_ph2"]['hadron_flavour'].Integral())
h_distributions['signal_ph2']['hadron_flavour'].SetLineStyle(2)

legend11.AddEntry(h_distributions["signal_ph2"]['hadron_flavour'], "phase2 fullsim, signal", "l")


c11.SetLogy()

legend11.Draw()


print(f"number of entries for QCD, run2 fullsim is {QCD_full_nb_distr.GetEntries()}")
print(f"number of entries for QCD, flashsim is {QCD_flash_nb_distr.GetEntries()}")
print(f"number of entries for QCD, phase2 fullsim is {h_distributions['QCD_ph2']['matching_nb'].GetEntries()}")

print(f"number of entries for signal, run2 fullsim is {h_distributions['signal_full']['matching_nb'].GetEntries()}")
print(f"number of entries for signal, flashsim is {h_distributions['signal_flash']['matching_nb'].GetEntries()}")
print(f"number of entries for signal, phase2 fullsim is {h_distributions['signal_ph2']['matching_nb'].GetEntries()}")





# c1 = ROOT.TCanvas("c1", "Discriminator distribution", 800, 700)


# legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

# h_clone_discr1["signal_full"].Draw("HIST")
# h_clone_discr1["signal_full"].SetTitle("Discriminator distribution for Jet1 and Jet2")
# h_clone_discr1["signal_full"].SetLineWidth(2)
# h_clone_discr1["signal_full"].SetLineColor(ROOT.kBlue +1)
# legend.AddEntry(h_clone_discr1["signal_full"], " fullsim", "l")

# h_clone_discr1["signal_flash"].Draw("HIST SAME")
# h_clone_discr1["signal_flash"].SetLineWidth(2)
# h_clone_discr1["signal_flash"].SetLineColor(ROOT.kRed +1)
# legend.AddEntry(h_clone_discr1["signal_flash"], " flashsim", "l")

# h_clone_discr1["signal_ph2"].Draw("HIST SAME")
# h_clone_discr1["signal_ph2"].SetLineWidth(2)
# h_clone_discr1["signal_ph2"].SetLineColor(ROOT.kBlack)
# legend.AddEntry(h_clone_discr1["signal_ph2"], "phase2 fullsim", "l")
# c1.SetLogy()

# legend.Draw()

# underflow_full = h_clone_discr1["signal_full"].GetBinContent(0)

# print(f"the number of underflow events in fullsim is {underflow_full}")

# underflow_flash = h_clone_discr1["signal_flash"].GetBinContent(0)

# print(f"the number of underflow events in flashsim is {underflow_flash}")


# underflow_ph2 = h_clone_discr1["signal_ph2"].GetBinContent(0)

# print(f"the number of underflow events in phase 2 is {underflow_ph2}")




# overflow_full = h_clone_discr1["signal_full"].GetBinContent(101)

# print(f"the number of overflow events in fullsim is {overflow_full}")

# overflow_flash = h_clone_discr1["signal_flash"].GetBinContent(101)

# print(f"the number of overflow events in flashsim is {overflow_flash}")


# overflow_ph2 = h_clone_discr1["signal_ph2"].GetBinContent(101)

# print(f"the number of overflow events in phase 2 is {overflow_ph2}")




# c2 = ROOT.TCanvas("c2", "Discriminator distribution", 800, 700)


# legend2 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

# h_discr1["signal_full"].Draw("HIST")
# h_discr1["signal_full"].SetTitle("Discriminator distribution for Jet1 only")
# h_discr1["signal_full"].SetLineWidth(2)
# h_discr1["signal_full"].SetLineColor(ROOT.kBlue +1)
# legend2.AddEntry(h_discr1["signal_full"], " fullsim", "l")

# h_discr1["signal_flash"].Draw("HIST SAME")
# h_discr1["signal_flash"].SetLineWidth(2)
# h_discr1["signal_flash"].SetLineColor(ROOT.kRed +1)
# legend2.AddEntry(h_discr1["signal_flash"], " flashsim", "l")

# h_discr1["signal_ph2"].Draw("HIST SAME")
# h_discr1["signal_ph2"].SetLineWidth(2)
# h_discr1["signal_ph2"].SetLineColor(ROOT.kBlack)
# legend2.AddEntry(h_discr1["signal_ph2"], "phase2 fullsim", "l")
# c2.SetLogy()

# legend2.Draw()



# #TODO ALL JETS

# c3 = ROOT.TCanvas("c3", "Discriminator distribution", 800, 700)


# legend3 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

# h_discr["signal_full"].Draw("HIST")
# h_discr["signal_full"].SetTitle("Discriminator distribution for all jets")
# h_discr["signal_full"].SetLineWidth(2)
# h_discr["signal_full"].SetLineColor(ROOT.kBlue +1)
# h_discr["signal_full"].SetMinimum(1)
# legend3.AddEntry(h_discr["signal_full"], " fullsim", "l")

# h_discr["signal_flash"].Draw("HIST SAME")
# h_discr["signal_flash"].SetLineWidth(2)
# h_discr["signal_flash"].SetLineColor(ROOT.kRed +1)
# legend3.AddEntry(h_discr["signal_flash"], " flashsim", "l")

# h_discr["signal_ph2"].Draw("HIST SAME")
# h_discr["signal_ph2"].SetLineWidth(2)
# h_discr["signal_ph2"].SetLineColor(ROOT.kBlack)
# legend3.AddEntry(h_discr["signal_ph2"], "phase2 fullsim", "l")
# c3.SetLogy()

# legend3.Draw()

# print(h_discr1["signal_full"].GetEntries())

bckg_full_jet1 = np.array([])

bckg_flash_jet1 = np.array([])

bckg_ph2_jet1 = np.array([])


old_full_jet1 = np.array([])


temp_bckg_full_jet1 = 0

temp_bckg_flash_jet1 = 0

temp_bckg_ph2_jet1 = 0

temp_old_full_jet1 = 0 

for i in reversed(range(0, 101)):

    # temp_full = temp_full + h_clone_discr1['signal_full'].GetBinContent(i)

    # full = np.append(temp_full, full)

    # temp_flash = temp_flash + h_clone_discr1['signal_flash'].GetBinContent(i)

    # flash = np.append(temp_flash, flash)

    # temp_ph2 = temp_ph2 + h_clone_discr1['signal_ph2'].GetBinContent(i)

    # ph2 = np.append(temp_ph2, ph2)



    # temp_old_full_jet1 = temp_old_full_jet1 + h_discr1['old_signal_full'].GetBinContent(i)

    # old_full_jet1 = np.append(temp_old_full_jet1, old_full_jet1)



    # temp_full_jet1 = temp_full_jet1 + h_discr1['signal_full'].GetBinContent(i)

    # temp_bckg_full_jet1 = temp_bckg_full_jet1 + QCD_full_1.GetBinContent(i)

    # full_jet1 = np.append(temp_full_jet1, full_jet1)

    # bckg_full_jet1 = np.append(temp_bckg_full_jet1, bckg_full_jet1)

    # temp_flash_jet1 = temp_flash_jet1 + h_discr1['signal_flash'].GetBinContent(i)

    # temp_bckg_flash_jet1 = temp_bckg_flash_jet1 + QCD_flash_1.GetBinContent(i)

    # flash_jet1 = np.append(temp_flash_jet1, flash_jet1)

    # bckg_flash_jet1 = np.append(temp_bckg_flash_jet1, bckg_flash_jet1)

    # temp_ph2_jet1 = temp_ph2_jet1 + h_discr1['signal_ph2'].GetBinContent(i)

    # temp_bckg_ph2_jet1 = temp_bckg_ph2_jet1 + h_discr['QCD_ph2'].GetBinContent(i)

    # ph2_jet1 = np.append(temp_ph2_jet1, ph2_jet1)

    # bckg_ph2_jet1 = np.append(temp_bckg_ph2_jet1, bckg_ph2_jet1)



    bin_lower = np.append(h_distributions['signal_full']['alljets_discr'].GetBinLowEdge(i), bin_lower)

QCD_temp_full_had_fl_0 = 0
QCD_full_had_flav_0 = np.array([])

QCD_temp_flash_had_fl_0 = 0
QCD_flash_had_flav_0 = np.array([])

QCD_temp_ph2_had_fl_0 = 0
QCD_ph2_had_flav_0 = np.array([])

for i in reversed(range(0, 101)):

    QCD_temp_full_had_fl_0 = QCD_temp_full_had_fl_0 + QCD_full_discr_had_flav_0.GetBinContent(i)

    QCD_full_had_flav_0 = np.append(QCD_temp_full_had_fl_0, QCD_full_had_flav_0)


    QCD_temp_flash_had_fl_0 = QCD_temp_flash_had_fl_0 + QCD_flash_discr_had_flav_0.GetBinContent(i)

    QCD_flash_had_flav_0 = np.append(QCD_temp_flash_had_fl_0, QCD_flash_had_flav_0)


    QCD_temp_ph2_had_fl_0 = QCD_temp_ph2_had_fl_0 + h_distributions['QCD_ph2']['discr_hadron_0'].GetBinContent(i)

    QCD_ph2_had_flav_0 = np.append(QCD_temp_ph2_had_fl_0, QCD_ph2_had_flav_0)

#! ~~~ EFFICIENCY FOR HADRON FLAVOUR = 0 ~~~

total_QCD_full = QCD_full_discr_had_flav_0.GetEntries()

total_QCD_flash = QCD_flash_discr_had_flav_0.GetEntries()

total_QCD_ph2 = h_distributions['QCD_ph2']['discr_hadron_0'].GetEntries()

QCD_efficiency_full_had_flav_0 = np.array([])

QCD_efficiency_flash_had_flav_0 = np.array([])

QCD_efficiency_ph2_had_flav_0 = np.array([])


QCD_efficiency_full_had_flav_0 = 1- ((total_QCD_full - QCD_full_had_flav_0)/total_QCD_full)

QCD_efficiency_flash_had_flav_0 = 1- ((total_QCD_flash - QCD_flash_had_flav_0)/total_QCD_flash)

QCD_efficiency_ph2_had_flav_0 = 1- ((total_QCD_ph2 - QCD_ph2_had_flav_0)/total_QCD_ph2)

QCD_efficiency_full_had_flav_0_wo_underflow = QCD_efficiency_full_had_flav_0[1:-2]

QCD_efficiency_flash_had_flav_0_wo_underflow = QCD_efficiency_flash_had_flav_0[1:-2]

QCD_efficiency_ph2_had_flav_0_wo_underflow = QCD_efficiency_ph2_had_flav_0[1:-2]




#! EFFICIENCY ESTIMATION FOR NB DIVIDED

temp_full_nb0 = 0
temp_full_nb1 = 0
temp_full_nb2 = 0

temp_bckg_full_nb0 = 0
temp_bckg_full_nb1 = 0
temp_bckg_full_nb2 = 0

full_nb0 = np.array([])
full_nb1 = np.array([])
full_nb2 = np.array([])

bckg_full_nb0 = np.array([])
bckg_full_nb1 = np.array([])
bckg_full_nb2 = np.array([])


temp_flash_nb0 = 0
temp_flash_nb1 = 0
temp_flash_nb2 = 0

temp_bckg_flash_nb0 = 0
temp_bckg_flash_nb1 = 0
temp_bckg_flash_nb2 = 0

flash_nb0 = np.array([])
flash_nb1 = np.array([])
flash_nb2 = np.array([])

bckg_flash_nb0 = np.array([])
bckg_flash_nb1 = np.array([])
bckg_flash_nb2 = np.array([])


temp_ph2_nb0 = 0
temp_ph2_nb1 = 0
temp_ph2_nb2 = 0

temp_bckg_ph2_nb0 = 0
temp_bckg_ph2_nb1 = 0
temp_bckg_ph2_nb2 = 0

ph2_nb0 = np.array([])
ph2_nb1 = np.array([])
ph2_nb2 = np.array([])

bckg_ph2_nb0 = np.array([])
bckg_ph2_nb1 = np.array([])
bckg_ph2_nb2 = np.array([])


# for i in reversed(range(0, 101)):
#     temp_full_nb0 = temp_full_nb0 + h_pt_leading_jet['signal_full']['nb_0'].GetBinContent(i)

#     temp_bckg_full_nb0 = temp_bckg_full_nb0 + QCD_full_nb0.GetBinContent(i)

#     full_nb0 = np.append(temp_full_nb0, full_nb0)

#     bckg_full_nb0 = np.append(temp_bckg_full_nb0, bckg_full_nb0)


#     temp_full_nb1 = temp_full_nb1 + h_pt_leading_jet['signal_full']['nb_1'].GetBinContent(i)

#     temp_bckg_full_nb1 = temp_bckg_full_nb1 + QCD_full_nb1.GetBinContent(i)

#     full_nb1 = np.append(temp_full_nb1, full_nb1)

#     bckg_full_nb1 = np.append(temp_bckg_full_nb1, bckg_full_nb1)



#     temp_full_nb2 = temp_full_nb2 + h_pt_leading_jet['signal_full']['nb_2'].GetBinContent(i)

#     temp_bckg_full_nb2 = temp_bckg_full_nb2 + QCD_full_nb2.GetBinContent(i)

#     full_nb2 = np.append(temp_full_nb2, full_nb2)

#     bckg_full_nb2 = np.append(temp_bckg_full_nb2, bckg_full_nb2)


#     temp_flash_nb0 = temp_flash_nb0 + h_pt_leading_jet['signal_flash']['nb_0'].GetBinContent(i)

#     temp_bckg_flash_nb0 = temp_bckg_flash_nb0 + QCD_flash_nb0.GetBinContent(i)

#     flash_nb0 = np.append(temp_flash_nb0, flash_nb0)

#     bckg_flash_nb0 = np.append(temp_bckg_flash_nb0, bckg_flash_nb0)


#     temp_flash_nb1 = temp_flash_nb1 + h_pt_leading_jet['signal_flash']['nb_1'].GetBinContent(i)

#     temp_bckg_flash_nb1 = temp_bckg_flash_nb1 + QCD_flash_nb1.GetBinContent(i)

#     flash_nb1 = np.append(temp_flash_nb1, flash_nb1)

#     bckg_flash_nb1 = np.append(temp_bckg_flash_nb1, bckg_flash_nb1)



#     temp_flash_nb2 = temp_flash_nb2 + h_pt_leading_jet['signal_flash']['nb_2'].GetBinContent(i)

#     temp_bckg_flash_nb2 = temp_bckg_flash_nb2 + QCD_flash_nb2.GetBinContent(i)

#     flash_nb2 = np.append(temp_flash_nb2, flash_nb2)

#     bckg_flash_nb2 = np.append(temp_bckg_flash_nb2, bckg_flash_nb2)


#     temp_ph2_nb0 = temp_ph2_nb0 + h_pt_leading_jet['signal_ph2']['nb_0'].GetBinContent(i)

#     temp_bckg_ph2_nb0 = temp_bckg_ph2_nb0 + h_pt_leading_jet['QCD_ph2']['nb_0'].GetBinContent(i)

#     ph2_nb0 = np.append(temp_ph2_nb0, ph2_nb0)

#     bckg_ph2_nb0 = np.append(temp_bckg_ph2_nb0, bckg_ph2_nb0)


#     temp_ph2_nb1 = temp_ph2_nb1 + h_pt_leading_jet['signal_ph2']['nb_1'].GetBinContent(i)

#     temp_bckg_ph2_nb1 = temp_bckg_ph2_nb1 + h_pt_leading_jet['QCD_ph2']['nb_1'].GetBinContent(i)

#     ph2_nb1 = np.append(temp_ph2_nb1, ph2_nb1)

#     bckg_ph2_nb1 = np.append(temp_bckg_ph2_nb1, bckg_ph2_nb1)


#     temp_ph2_nb2 = temp_ph2_nb2 + h_pt_leading_jet['signal_ph2']['nb_2'].GetBinContent(i)

#     temp_bckg_ph2_nb2 = temp_bckg_ph2_nb2 + h_pt_leading_jet['QCD_ph2']['nb_2'].GetBinContent(i)

#     ph2_nb2 = np.append(temp_ph2_nb2, ph2_nb2)

#     bckg_ph2_nb2 = np.append(temp_bckg_ph2_nb2, bckg_ph2_nb2)




# print(bin_lower)

# # #! JET1 + JET2
# # total_full = h_clone_discr1["signal_full"].GetEntries()
# # total_flash = h_clone_discr1['signal_flash'].GetEntries()
# # total_ph2 = h_clone_discr1["signal_ph2"].GetEntries()

# # efficiency_full = np.array([])
# # efficiency_flash = np.array([])
# # efficiency_ph2 = np.array([])

# # efficiency_full = full/total_full
# # efficiency_flash = flash/total_flash
# # efficiency_ph2 = ph2/total_ph2


bin_lower_wo_underflow = bin_lower[1:-2]


# # efficiency_full_wo_underflow = efficiency_full[1:-2]
# # efficiency_flash_wo_underflow = efficiency_flash[1:-2]
# # efficiency_ph2_wo_underflow = efficiency_ph2[1:-2]

# # #! JET1 ONLY

# # total_full_jet1 = h_discr1["signal_full"].GetEntries()
# # total_flash_jet1 = h_discr1['signal_flash'].GetEntries()
# # total_ph2_jet1 = h_discr1["signal_ph2"].GetEntries()
# # #total_old_full_jet1 = h_discr1['old_signal_full'].GetEntries()


# # efficiency_full_jet1 = np.array([])
# # efficiency_flash_jet1 = np.array([])
# # efficiency_ph2_jet1 = np.array([])
# # #efficiency_old_full_jet1 = np.array([])

# # efficiency_full_jet1 = full_jet1/total_full_jet1
# # efficiency_flash_jet1 = flash_jet1/total_flash_jet1
# # efficiency_ph2_jet1 = ph2_jet1/total_ph2_jet1
# # #efficiency_old_full_jet1 = old_full_jet1/total_old_full_jet1


# # rejection_full_jet1 = np.array([])
# # rejection_flash_jet1 = np.array([])
# # rejection_ph2_jet1 = np.array([])


# # rejection_full_jet1 = 1 - ((QCD_entries_full_jet1 - bckg_full_jet1)/ QCD_entries_full_jet1)
# # rejection_flash_jet1 = 1- ((QCD_entries_flash_jet1 - bckg_flash_jet1)/ QCD_entries_flash_jet1)
# # rejection_ph2_jet1 = 1- ((QCD_entries_ph2_jet1 - bckg_ph2_jet1)/ QCD_entries_ph2_jet1)


# # efficiency_full_wo_underflow_jet1 = efficiency_full_jet1[1:-2]
# # efficiency_flash_wo_underflow_jet1 = efficiency_flash_jet1[1:-2]
# # efficiency_ph2_wo_underflow_jet1 = efficiency_ph2_jet1[1:-2]
# # #efficiency_old_full_wo_undeflow_jet1 = efficiency_old_full_jet1[1:-2]

# # rejection_full_wo_underflow_jet1 = rejection_full_jet1[1:-2]
# # rejection_flash_wo_underflow_jet1 = rejection_flash_jet1[1:-2]
# # rejection_ph2_wo_underflow_jet1 = rejection_ph2_jet1[1:-2]


# #! NB DIVIDED

# total_full_nb0 = h_pt_leading_jet['signal_full']['nb_0'].GetEntries()
# total_full_nb1 = h_pt_leading_jet['signal_full']['nb_1'].GetEntries()
# total_full_nb2 = h_pt_leading_jet['signal_full']['nb_2'].GetEntries()

# total_flash_nb0 = h_pt_leading_jet['signal_flash']['nb_0'].GetEntries()
# total_flash_nb1 = h_pt_leading_jet['signal_flash']['nb_1'].GetEntries()
# total_flash_nb2 = h_pt_leading_jet['signal_flash']['nb_2'].GetEntries()

# total_ph2_nb0 = h_pt_leading_jet['signal_ph2']['nb_0'].GetEntries()
# total_ph2_nb1 = h_pt_leading_jet['signal_ph2']['nb_1'].GetEntries()
# total_ph2_nb2 = h_pt_leading_jet['signal_ph2']['nb_2'].GetEntries()

# efficiency_full_nb0 = np.array([])
# efficiency_full_nb1 = np.array([])
# efficiency_full_nb2 = np.array([])


# efficiency_flash_nb0 = np.array([])
# efficiency_flash_nb1 = np.array([])
# efficiency_flash_nb2 = np.array([])


# efficiency_ph2_nb0 = np.array([])
# efficiency_ph2_nb1 = np.array([])
# efficiency_ph2_nb2 = np.array([])

# efficiency_full_nb0 = full_nb0/total_full_nb0
# efficiency_full_nb1 = full_nb1/total_full_nb1 
# efficiency_full_nb2 = full_nb2/total_full_nb2 


# efficiency_flash_nb0 = flash_nb0/total_flash_nb0
# efficiency_flash_nb1 = flash_nb1/total_flash_nb1 
# efficiency_flash_nb2 = flash_nb2/total_flash_nb2 


# efficiency_ph2_nb0 = ph2_nb0/total_ph2_nb0
# efficiency_ph2_nb1 = ph2_nb1/total_ph2_nb1 
# efficiency_ph2_nb2 = ph2_nb2/total_ph2_nb2 

# efficiency_full_nb0_wo_underflow = efficiency_full_nb0[1:-2]
# efficiency_full_nb1_wo_underflow = efficiency_full_nb1[1:-2]
# efficiency_full_nb2_wo_underflow = efficiency_full_nb2[1:-2]

# efficiency_flash_nb0_wo_underflow = efficiency_flash_nb0[1:-2]
# efficiency_flash_nb1_wo_underflow = efficiency_flash_nb1[1:-2]
# efficiency_flash_nb2_wo_underflow = efficiency_flash_nb2[1:-2]

# efficiency_ph2_nb0_wo_underflow = efficiency_ph2_nb0[1:-2]
# efficiency_ph2_nb1_wo_underflow = efficiency_ph2_nb1[1:-2]
# efficiency_ph2_nb2_wo_underflow = efficiency_ph2_nb2[1:-2]


# rejection_full_nb0 = np.array([])
# rejection_full_nb1 = np.array([])
# rejection_full_nb2 = np.array([])


# rejection_flash_nb0 = np.array([])
# rejection_flash_nb1 = np.array([])
# rejection_flash_nb2 = np.array([])


# rejection_ph2_nb0 = np.array([])
# rejection_ph2_nb1 = np.array([])
# rejection_ph2_nb2 = np.array([])



# rejection_full_nb0 = 1- ((QCD_full_nb0_entries - bckg_full_nb0)/QCD_full_nb0_entries)
# rejection_full_nb1 = 1- ((QCD_full_nb1_entries - bckg_full_nb1)/QCD_full_nb1_entries)
# rejection_full_nb2 = 1- ((QCD_full_nb2_entries - bckg_full_nb2)/QCD_full_nb2_entries)


# rejection_flash_nb0 = 1- ((QCD_flash_nb0_entries - bckg_flash_nb0)/QCD_flash_nb0_entries)
# rejection_flash_nb1 = 1- ((QCD_flash_nb1_entries - bckg_flash_nb1)/QCD_flash_nb1_entries)
# rejection_flash_nb2 = 1- ((QCD_flash_nb2_entries - bckg_flash_nb2)/QCD_flash_nb2_entries)


# rejection_ph2_nb0 = 1- ((QCD_ph2_nb0_entries - bckg_ph2_nb0)/QCD_ph2_nb0_entries)
# rejection_ph2_nb1 = 1- ((QCD_ph2_nb1_entries - bckg_ph2_nb1)/QCD_ph2_nb1_entries)
# rejection_ph2_nb2 = 1- ((QCD_ph2_nb2_entries - bckg_ph2_nb2)/QCD_ph2_nb2_entries)

# rejection_full_nb0_wo_underflow = rejection_full_nb0[1:-2]
# rejection_full_nb1_wo_underflow = rejection_full_nb1[1:-2]
# rejection_full_nb2_wo_underflow = rejection_full_nb2[1:-2]


# rejection_flash_nb0_wo_underflow = rejection_flash_nb0[1:-2]
# rejection_flash_nb1_wo_underflow = rejection_flash_nb1[1:-2]
# rejection_flash_nb2_wo_underflow = rejection_flash_nb2[1:-2]


# rejection_ph2_nb0_wo_underflow = rejection_ph2_nb0[1:-2]
# rejection_ph2_nb1_wo_underflow = rejection_ph2_nb1[1:-2]
# rejection_ph2_nb2_wo_underflow = rejection_ph2_nb2[1:-2]


#! JET1 + JET2


# plt.plot(bin_lower_wo_underflow, efficiency_full_wo_underflow, label = 'run2 fullsim', color = 'seagreen', marker = '.', markersize=3 )
# plt.plot(bin_lower_wo_underflow, efficiency_flash_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
# plt.plot(bin_lower_wo_underflow, efficiency_ph2_wo_underflow, label = 'phase2 fullsim', color = 'lightcoral', marker = '.', markersize=3 )
# plt.axhline(y = 0.85, color = 'r', linestyle = '-')
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Discriminator values')
# plt.ylabel('Signal efficiency')

# plt.show()
# #plt.yscale('log')

# #plt.savefig('cdf_no_nb_NO_gen_sel_cleaned_fats_no_cleaning_no_index_req_old_eta.png')

# plt.close()



# #! JET1 ONLY

# plt.plot(bin_lower_wo_underflow, efficiency_full_wo_underflow_jet1, label = 'run2 fullsim', color = 'mediumseagreen', marker = '.', markersize=3)
# plt.plot(bin_lower_wo_underflow, efficiency_flash_wo_underflow_jet1, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3)
# plt.plot(bin_lower_wo_underflow, efficiency_ph2_wo_underflow_jet1, label = 'phase2 fullsim', color = 'palevioletred', marker = '.', markersize=3)
# #plt.plot(bin_lower_wo_underflow, efficiency_old_full_wo_undeflow_jet1, label = 'old fullsim', color = 'burlywood', marker = '.', markersize=5 )
# plt.title("Signal efficiency for abs(eta)<2.4")
# plt.axhline(y = 0.86, color = 'r', linestyle = '-')
# #plt.axvline(x=0.85, color = 'blue', linestyle = '-')
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Discriminator values')
# plt.ylabel('Signal efficiency')

# plt.show()
# #plt.yscale('log')

# plt.savefig('cdf_no_nb_old_eta_from_0_7.png')

# plt.close()

# #TODO REJECTION


# plt.plot(bin_lower_wo_underflow, rejection_full_wo_underflow_jet1, label = 'run2 fullsim', color = 'seagreen', marker = '.', markersize=3 )
# plt.plot(bin_lower_wo_underflow, rejection_flash_wo_underflow_jet1, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
# plt.plot(bin_lower_wo_underflow, rejection_ph2_wo_underflow_jet1, label = 'phase2 fullsim', color = 'lightcoral', marker = '.', markersize=3 )
# #plt.axhline(y = 0.86, color = 'r', linestyle = '-')
# #plt.axvline(x=0.85, color = 'blue', linestyle = '-')
# plt.title("Background efficiency for abs(eta) < 2.4")
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Discriminator values')
# plt.ylabel('Background efficiency')

# plt.show()
# plt.yscale('log')

# plt.savefig('cdf_bckg_efficiency_jet1_old_eta_from_0_7.png')

# plt.close()


# #! ROC 

# plt.plot(efficiency_full_wo_underflow_jet1, rejection_full_wo_underflow_jet1, label = 'run2 fullsim', color = 'seagreen', marker = '.', markersize=3 )
# plt.plot(efficiency_flash_wo_underflow_jet1, rejection_flash_wo_underflow_jet1, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
# plt.plot(efficiency_ph2_wo_underflow_jet1, rejection_ph2_wo_underflow_jet1, label = 'phase2 fullsim', color = 'lightcoral', marker = '.', markersize=3 )
# #plt.axhline(y = 0.86, color = 'r', linestyle = '-')
# #plt.axvline(x=0.85, color = 'blue', linestyle = '-')
# plt.title("ROC for abs(eta) < 2.4")
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Signal efficiency')
# plt.ylabel('Background efficiency')

# plt.show()
# plt.yscale('log')

# plt.savefig('roc_jet1_old_eta_from_0_7_bckg_eff.png')

# plt.close()


#! NB DIVIDED PLOTS

# #TODO NB 0

# plt.plot(bin_lower_wo_underflow, efficiency_full_nb0_wo_underflow, label = 'run2 fullsim', color = 'mediumseagreen', marker = '.', markersize=3)
# plt.plot(bin_lower_wo_underflow, efficiency_flash_nb0_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3)
# plt.plot(bin_lower_wo_underflow, efficiency_ph2_nb0_wo_underflow, label = 'phase2 fullsim', color = 'palevioletred', marker = '.', markersize=3)
# plt.title("Signal efficiency for pt-leading jet, nb = 0")
# #plt.axhline(y = 0.86, color = 'r', linestyle = '-')
# #plt.axvline(x=0.85, color = 'blue', linestyle = '-')
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Discriminator values')
# plt.ylabel('Signal efficiency')

# plt.show()
# #plt.yscale('log')

# plt.savefig('comparison_roc_et_al/efficiency_nb0.png')

# plt.close()



# plt.plot(bin_lower_wo_underflow, rejection_full_nb0_wo_underflow, label = 'run2 fullsim', color = 'mediumseagreen', marker = '.', markersize=3 )
# plt.plot(bin_lower_wo_underflow, rejection_flash_nb0_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
# plt.plot(bin_lower_wo_underflow, rejection_ph2_nb0_wo_underflow, label = 'phase2 fullsim', color = 'palevioletred', marker = '.', markersize=3 )
# #plt.axhline(y = 0.86, color = 'r', linestyle = '-')
# #plt.axvline(x=0.85, color = 'blue', linestyle = '-')
# plt.title("Background efficiency for pt-leading jet, nb = 0")
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Discriminator values')
# plt.ylabel('Background efficiency')

# plt.show()
# plt.yscale('log')

# plt.savefig('comparison_roc_et_al/bckg_rej_nb0.png')

# plt.close()



# plt.plot(efficiency_full_nb0_wo_underflow, rejection_full_nb0_wo_underflow, label = 'run2 fullsim', color = 'mediumseagreen', marker = '.', markersize=3 )
# plt.plot(efficiency_flash_nb0_wo_underflow, rejection_flash_nb0_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
# plt.plot(efficiency_ph2_nb0_wo_underflow, rejection_ph2_nb0_wo_underflow, label = 'phase2 fullsim', color = 'palevioletred', marker = '.', markersize=3 )
# #plt.axhline(y = 0.86, color = 'r', linestyle = '-')
# #plt.axvline(x=0.85, color = 'blue', linestyle = '-')
# plt.title("ROC for pt-leading jet, nb = 0")
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Signal efficiency')
# plt.ylabel('Background efficiency')

# plt.show()
# plt.yscale('log')

# plt.savefig('comparison_roc_et_al/roc_nb0.png')

# plt.close()



# #TODO NB 1

# plt.plot(bin_lower_wo_underflow, efficiency_full_nb1_wo_underflow, label = 'run2 fullsim', color = 'mediumseagreen', marker = '.', markersize=3)
# plt.plot(bin_lower_wo_underflow, efficiency_flash_nb1_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3)
# plt.plot(bin_lower_wo_underflow, efficiency_ph2_nb1_wo_underflow, label = 'phase2 fullsim', color = 'palevioletred', marker = '.', markersize=3)
# plt.title("Signal efficiency for pt-leading jet, nb = 1")
# #plt.axhline(y = 0.86, color = 'r', linestyle = '-')
# #plt.axvline(x=0.85, color = 'blue', linestyle = '-')
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Discriminator values')
# plt.ylabel('Signal efficiency')

# plt.show()
# #plt.yscale('log')

# plt.savefig('comparison_roc_et_al/efficiency_nb1.png')

# plt.close()



# plt.plot(bin_lower_wo_underflow, rejection_full_nb1_wo_underflow, label = 'run2 fullsim', color = 'mediumseagreen', marker = '.', markersize=3 )
# plt.plot(bin_lower_wo_underflow, rejection_flash_nb1_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
# plt.plot(bin_lower_wo_underflow, rejection_ph2_nb1_wo_underflow, label = 'phase2 fullsim', color = 'palevioletred', marker = '.', markersize=3 )
# #plt.axhline(y = 0.86, color = 'r', linestyle = '-')
# #plt.axvline(x=0.85, color = 'blue', linestyle = '-')
# plt.title("Background efficiency for pt-leading jet, nb = 1")
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Discriminator values')
# plt.ylabel('Background efficiency')

# plt.show()
# plt.yscale('log')

# plt.savefig('comparison_roc_et_al/bckg_rej_nb1.png')

# plt.close()



# plt.plot(efficiency_full_nb1_wo_underflow, rejection_full_nb1_wo_underflow, label = 'run2 fullsim', color = 'mediumseagreen', marker = '.', markersize=3 )
# plt.plot(efficiency_flash_nb1_wo_underflow, rejection_flash_nb1_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
# plt.plot(efficiency_ph2_nb1_wo_underflow, rejection_ph2_nb1_wo_underflow, label = 'phase2 fullsim', color = 'palevioletred', marker = '.', markersize=3 )
# #plt.axhline(y = 0.86, color = 'r', linestyle = '-')
# #plt.axvline(x=0.85, color = 'blue', linestyle = '-')
# plt.title("ROC for pt-leading jet, nb = 1")
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Signal efficiency')
# plt.ylabel('Background efficiency')

# plt.show()
# plt.yscale('log')

# plt.savefig('comparison_roc_et_al/roc_nb1.png')

# plt.close()



# #TODO NB 2

# plt.plot(bin_lower_wo_underflow, efficiency_full_nb2_wo_underflow, label = 'run2 fullsim', color = 'mediumseagreen', marker = '.', markersize=3)
# plt.plot(bin_lower_wo_underflow, efficiency_flash_nb2_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3)
# plt.plot(bin_lower_wo_underflow, efficiency_ph2_nb2_wo_underflow, label = 'phase2 fullsim', color = 'palevioletred', marker = '.', markersize=3)
# plt.title("Signal efficiency for pt-leading jet, nb = 2")
# #plt.axhline(y = 0.86, color = 'r', linestyle = '-')
# #plt.axvline(x=0.85, color = 'blue', linestyle = '-')
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Discriminator values')
# plt.ylabel('Signal efficiency')

# plt.show()
# #plt.yscale('log')

# plt.savefig('comparison_roc_et_al/efficiency_nb2.png')

# plt.close()



# plt.plot(bin_lower_wo_underflow, rejection_full_nb2_wo_underflow, label = 'run2 fullsim', color = 'mediumseagreen', marker = '.', markersize=3 )
# plt.plot(bin_lower_wo_underflow, rejection_flash_nb2_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
# plt.plot(bin_lower_wo_underflow, rejection_ph2_nb2_wo_underflow, label = 'phase2 fullsim', color = 'palevioletred', marker = '.', markersize=3 )
# #plt.axhline(y = 0.86, color = 'r', linestyle = '-')
# #plt.axvline(x=0.85, color = 'blue', linestyle = '-')
# plt.title("Background efficiency for pt-leading jet, nb = 2")
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Discriminator values')
# plt.ylabel('Background efficiency')

# plt.show()
# plt.yscale('log')

# plt.savefig('comparison_roc_et_al/bckg_rej_nb2.png')

# plt.close()



# plt.plot(efficiency_full_nb2_wo_underflow, rejection_full_nb2_wo_underflow, label = 'run2 fullsim', color = 'mediumseagreen', marker = '.', markersize=3 )
# plt.plot(efficiency_flash_nb2_wo_underflow, rejection_flash_nb2_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
# plt.plot(efficiency_ph2_nb2_wo_underflow, rejection_ph2_nb2_wo_underflow, label = 'phase2 fullsim', color = 'palevioletred', marker = '.', markersize=3 )
# #plt.axhline(y = 0.86, color = 'r', linestyle = '-')
# #plt.axvline(x=0.85, color = 'blue', linestyle = '-')
# plt.title("ROC for pt-leading jet, nb = 2")
# plt.grid(which ='both')

# plt.legend()

# plt.xlabel('Signal efficiency')
# plt.ylabel('Background efficiency')

# plt.show()
# plt.yscale('log')

# plt.savefig('comparison_roc_et_al/roc_nb2.png')

# plt.close()


#! HISTO FOR BCKG EFFICIENCY HADRON FLAVOUR == 0

plt.plot(bin_lower_wo_underflow, QCD_efficiency_full_had_flav_0_wo_underflow, label = 'run2 fullsim', color = 'mediumseagreen', marker = '.', markersize=3 )
plt.plot(bin_lower_wo_underflow, QCD_efficiency_flash_had_flav_0_wo_underflow, label = 'flashsim', color = 'lightskyblue', marker = '.', markersize=3 )
plt.plot(bin_lower_wo_underflow, QCD_efficiency_ph2_had_flav_0_wo_underflow, label = 'phase2 fullsim', color = 'palevioletred', marker = '.', markersize=3 )
#plt.axhline(y = 0.86, color = 'r', linestyle = '-')
#plt.axvline(x=0.85, color = 'blue', linestyle = '-')
plt.title("Background efficiency for jets with hadron flavour = 0")
plt.grid(which ='both')

plt.legend()

plt.xlabel('Discriminator values')
plt.ylabel('Background efficiency')

plt.show()
plt.yscale('log')

plt.savefig('comparison_roc_et_al/bckg_eff_had_flav_0.png')

plt.close()



print("saving the histos")



# c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_leading_discr_signal_nb0.pdf")
# c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_leading_discr_signal_nb1.pdf")
# c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_leading_discr_signal_nb2.pdf")
# c4.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_leading_discr_bckg_nb0.pdf")
# c5.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_leading_discr_bckg_nb1.pdf")
# c6.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/pt_leading_discr_bckg_nb2.pdf")
# c7.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/nb_distribution_normalized.pdf")

# c8.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/lower_edge_pt_discr.pdf")
# c9.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/upper_edge_pt_discr.pdf")
# c10.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/parton_flavour.pdf")
# c11.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/hadron_flavour.pdf")

