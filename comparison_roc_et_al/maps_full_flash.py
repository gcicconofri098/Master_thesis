import ROOT
import os
import numpy as np
from decimal import *
import re

ROOT.EnableImplicitMT()

# module_path = os.path.join(os.path.dirname(__file__), "utils.h")
# module_path2 = os.path.join(os.path.dirname(__file__), "nb.h")
# module_path_3 = os.path.join(os.path.dirname(__file__), "utils_calibration.h")

ROOT.gStyle.SetOptStat(0)


# ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')
# ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')
# ROOT.gInterpreter.ProcessLine(f'#include "{module_path2}"')

ROOT.gStyle.SetPaintTextFormat("1.3f")


getcontext().prec = 3

entries1 = {}
events = {}
events_chain = {}
full_chain = {}
df = {}
dataset_events = {}

integrated_luminosity = 59830

pre_selection_signal = 0

binx_n = 1
biny_n = 1


df_files = {
    # "QCD1_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD1_fullno_pt_window.root",
    # "QCD2_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD2_fullno_pt_window.root",
    # "QCD3_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD3_fullno_pt_window.root",
    # "QCD4_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD4_fullno_pt_window.root",
    # "QCD5_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD5_fullno_pt_window.root",
    "QCD6_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD6_fullno_pt_window.root",
    "QCD7_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD7_fullno_pt_window.root",
    "QCD8_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD8_fullno_pt_window.root",
    "signal_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/signal_fullno_pt_window.root",
    "QCD6_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD6_flashno_pt_window.root",
    "QCD7_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD7_flashno_pt_window.root",
    "QCD8_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/QCD8_flashno_pt_window.root",
    "signal_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/signal_flashno_pt_window.root",
}

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

processes = list(df_files.keys())
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

histos = {}

events_before_discr_preselection = {}

events_after_discr_preselection = {}


for i in existing_processes:

    df[i] = ROOT.RDataFrame("Events", existing_files[i])
    df[i] = df[i].Filter("MET_pt<100")

    df[i] = df[i].Filter("jet1_softdrop>50 && jet2_softdrop>50")
    # if str(i) == 'signal_full' or str(i) == 'signal_flash':
    #     df[i] = df[i].Filter("jet1_softdrop >115 && jet1_softdrop <145").Filter("jet2_softdrop > 115 && jet2_softdrop <145")

    events_before_discr_preselection[i] = df[i].Count().GetValue()
    print("preselection events", events_before_discr_preselection[i])

    # if str(i)!='QCD6_flash' and str(i)!='QCD7_flash' and str(i)!='QCD8_flash' and str(i)!='signal_flash': #* that is, if fullsim
    #     df[i] = df[i].Filter("jet1_discr>0.955")

    # else: #* that is, if flashsim
    #     df[i] = df[i].Filter("jet1_discr>0.95")
    
    events_after_discr_preselection[i] = df[i].Count().GetValue()

    if str(i) == 'signal_full' or str(i) == 'signal_flash':
        print(f"efficiency for {i} is: {events_after_discr_preselection[i]/events_before_discr_preselection[i]}")

for i in existing_processes:

    histos[i] = {}

    histos[i]['discr'] = df[i].Histo2D(("Discriminator Jet1 vs Jet2", "Discriminator Jet1 vs Jet2; Jet1; Jet2", 10, 0.95, 1, 10, 0.95, 1),
         "jet1_discr",
         "jet2_discr").GetValue()

    histos[i]['softdrop'] = df[i].Histo2D(("Softdrop mass Jet1 vs Jet2", "Softdrop mass Jet1 vs Jet2; Jet1; Jet2", 50, 40, 300, 50, 40, 300),
         "jet1_softdrop",
         "jet2_softdrop").GetValue()
    
    histos[i]['1d_softdrop_jet1'] = df[i].Histo1D(("Softdrop mass Jet1", "Softdrop mass Jet1; Softdrop mass; Events", 25, 0, 500), "jet1_softdrop").GetValue()

    histos[i]['1d_softdrop_jet2'] = df[i].Histo1D(("Softdrop mass Jet2", "Softdrop mass Jet2; Softdrop mass; Events", 25, 0, 500), "jet2_softdrop").GetValue()

    histos[i]['1d_discr_jet1'] = df[i].Histo1D(("Discriminator Jet1", "Discriminator Jet1; Discriminator; Events", 25, 0.95, 1), "jet1_discr").GetValue()

    histos[i]['1d_discr_jet2'] = df[i].Histo1D(("Discriminator Jet2", "Discriminator Jet2; Discriminator; Events", 25, 0.95, 1), "jet2_discr").GetValue()

    histos[i]['reshape'] = df[i].Histo2D((str(i), str(i), 18, 25, 295, 18, 25, 295), "jet1_softdrop", "jet2_softdrop").GetValue()

    histos[i]['mass_vs_discr'] = df[i].Histo2D((str(i), str(i), 25, 50, 200, 18, 0.9, 1), "jet1_softdrop", "jet1_discr").GetValue()

    print("number of entries before weighting:", histos[i]['discr'].Integral())

for key_full in existing_processes:
    key_nofull=key_full.split("_")[0]

    print(f"weight for dataset {key_full} is: {weights[key_nofull]*2.27/n_events[key_nofull]}")

    histos[key_full]['discr'].Scale(weights[key_nofull]*2.27/n_events[key_nofull]) #* 2.27 is the luminosity factor that has to be compensated

    histos[key_full]['softdrop'].Scale(weights[key_nofull]*2.27/n_events[key_nofull])

    histos[key_full]['1d_softdrop_jet1'].Scale(weights[key_nofull]*2.27/n_events[key_nofull])

    histos[key_full]['1d_softdrop_jet2'].Scale(weights[key_nofull]*2.27/n_events[key_nofull])

    histos[key_full]['1d_discr_jet1'].Scale(weights[key_nofull]*2.27/n_events[key_nofull])

    histos[key_full]['1d_discr_jet2'].Scale(weights[key_nofull]*2.27/n_events[key_nofull])

    histos[key_full]['reshape'].Scale(weights[key_nofull]*2.27/n_events[key_nofull])

    histos[key_full]['mass_vs_discr'].Scale(weights[key_nofull]*2.27/n_events[key_nofull])



    print("number of entries after weighting:", histos[key_full]['discr'].Integral())


r_full = re.compile("QCD._full")
r_flash = re.compile("QCD._flash")


QCD_full_processes = list(filter(r_full.match, existing_processes))
QCD_flash_processes = list(filter(r_flash.match, existing_processes))

print("QCD fullsim processes:", QCD_full_processes)
print("QCD flashsim processes:", QCD_flash_processes)


print("starting to stack histos")

QCD_full_discr = histos[str(QCD_full_processes[0])]['discr'].Clone()
QCD_full_softdrop = histos[str(QCD_full_processes[0])]['softdrop'].Clone()
QCD_full_softdrop_jet1 = histos[str(QCD_full_processes[0])]['1d_softdrop_jet1'].Clone()
QCD_full_softdrop_jet2 = histos[str(QCD_full_processes[0])]['1d_softdrop_jet2'].Clone()
QCD_full_discr_jet1 = histos[str(QCD_full_processes[0])]['1d_discr_jet1'].Clone()
QCD_full_discr_jet2 = histos[str(QCD_full_processes[0])]['1d_discr_jet2'].Clone()
QCD_full_reshape = histos[str(QCD_full_processes[0])]['reshape'].Clone()
QCD_full_mass_vs_discr = histos[str(QCD_full_processes[0])]['mass_vs_discr'].Clone()


for i in QCD_full_processes:
    if str(i) == QCD_full_processes[0]:
        continue
    else:
        QCD_full_discr.Add(histos[i]['discr'])
        QCD_full_softdrop.Add(histos[i]['softdrop'])

        QCD_full_softdrop_jet1.Add(histos[i]['1d_softdrop_jet1'])
        QCD_full_softdrop_jet2.Add(histos[i]['1d_softdrop_jet2'])

        QCD_full_discr_jet1.Add(histos[i]['1d_discr_jet1'])
        QCD_full_discr_jet2.Add(histos[i]['1d_discr_jet2'])
        QCD_full_reshape.Add(histos[i]['reshape'])
 
        QCD_full_mass_vs_discr.Add(histos[i]['mass_vs_discr'])

    
    print(f"adding histo for {i}")

QCD_full_discr_entries = (QCD_full_discr.Integral())

signal_full_entries = histos['signal_full']['discr'].Integral()
print("entries signal fullsim", signal_full_entries)
print("entries fullsim QCD after preselection:", QCD_full_discr_entries)

print("entries with integral:", QCD_full_discr.Integral())

#! QCD FLASHSIM STACKING

QCD_flash_discr = histos[str(QCD_flash_processes[0])]['discr'].Clone()
QCD_flash_softdrop = histos[str(QCD_flash_processes[0])]['softdrop'].Clone()

QCD_flash_softdrop_jet1 = histos[str(QCD_flash_processes[0])]['1d_softdrop_jet1'].Clone()
QCD_flash_softdrop_jet2 = histos[str(QCD_flash_processes[0])]['1d_softdrop_jet2'].Clone()

QCD_flash_discr_jet1 = histos[str(QCD_flash_processes[0])]['1d_discr_jet1'].Clone()
QCD_flash_discr_jet2 = histos[str(QCD_flash_processes[0])]['1d_discr_jet2'].Clone()

QCD_flash_reshape = histos[str(QCD_flash_processes[0])]['reshape'].Clone()

QCD_flash_mass_vs_discr = histos[str(QCD_flash_processes[0])]['mass_vs_discr'].Clone()


for i in QCD_flash_processes:
    if str(i) == QCD_flash_processes[0]:
        continue
    else:
        QCD_flash_discr.Add(histos[i]['discr'])
        QCD_flash_softdrop.Add(histos[i]['softdrop'])
    
        QCD_flash_softdrop_jet1.Add(histos[i]['1d_softdrop_jet1'])
        QCD_flash_softdrop_jet2.Add(histos[i]['1d_softdrop_jet2'])

        QCD_flash_discr_jet1.Add(histos[i]['1d_discr_jet1'])
        QCD_flash_discr_jet2.Add(histos[i]['1d_discr_jet2'])

        QCD_flash_reshape.Add(histos[i]['reshape'])

        QCD_flash_mass_vs_discr.Add(histos[i]['mass_vs_discr'])

    print(f"adding histo for {i}")

QCD_flash_discr_entries = (QCD_flash_discr.Integral())

signal_flash_entries = histos['signal_flash']['discr'].Integral()

print("entries signal flashsim", signal_flash_entries)


print("entries flashsim QCD after preselection:", QCD_flash_discr_entries)

#! QCD RESHAPE IS DONE HERE

# total_full = QCD_full_reshape.Integral(1, 18, 1, 18)

# mass_full = QCD_full_reshape.Integral(7,8,7,8)

# ratio_full = mass_full/total_full
# print("ratio fullsim", ratio_full)

# total_flash = QCD_flash_reshape.Integral(1, 18, 1, 18)

# mass_flash = QCD_flash_reshape.Integral(7,8,7,8)

# ratio_flash = mass_flash/total_flash

# print("ratio flashsim", ratio_flash)


# QCD_full_discr.Scale(ratio_full)
# QCD_full_softdrop.Scale(ratio_full)
# QCD_full_softdrop_jet1.Scale(ratio_full)
# QCD_full_softdrop_jet2.Scale(ratio_full)
# QCD_full_discr_jet1.Scale(ratio_full)
# QCD_full_discr_jet2.Scale(ratio_full)

# QCD_full_mass_vs_discr.Scale(ratio_full)


# QCD_flash_discr.Scale(ratio_flash)
# QCD_flash_softdrop.Scale(ratio_flash)
# QCD_flash_softdrop_jet1.Scale(ratio_flash)
# QCD_flash_softdrop_jet2.Scale(ratio_flash)
# QCD_flash_discr_jet1.Scale(ratio_flash)
# QCD_flash_discr_jet2.Scale(ratio_flash)

# QCD_flash_mass_vs_discr.Scale(ratio_flash)

#! ~~~~~ RESHAPING DONE ~~~~~~

maps_full = {}

maps_flash = {}

maps_full['yield'] = histos['signal_full']['discr'].Clone()
maps_full['norm_yield'] = histos['signal_full']['discr'].Clone()
maps_full['efficiency'] = histos['signal_full']['discr'].Clone()
maps_full['s_b'] = histos['signal_full']['discr'].Clone()
maps_full['s_b_diff'] = histos['signal_full']['discr'].Clone()
maps_full['s_sqrt_b'] = histos['signal_full']['discr'].Clone()
maps_full['s_sqrt_b_diff'] = histos['signal_full']['discr'].Clone()


maps_flash['yield'] = histos['signal_flash']['discr'].Clone()
maps_flash['norm_yield'] = histos['signal_flash']['discr'].Clone()
maps_flash['efficiency'] = histos['signal_flash']['discr'].Clone()
maps_flash['s_b'] = histos['signal_flash']['discr'].Clone()
maps_flash['s_b_diff'] = histos['signal_flash']['discr'].Clone()
maps_flash['s_sqrt_b'] = histos['signal_flash']['discr'].Clone()
maps_flash['s_sqrt_b_diff'] = histos['signal_flash']['discr'].Clone()

for binx in reversed(range(1, 11)):
    for biny in reversed(range(1, 11)):
        if binx >= biny:
        
        #TODO FULLSIM

            stacked_sig_full = histos['signal_full']['discr'].Integral(binx, 10, biny, 10)
            
            #print("stacked signal: ", stacked_sig_full)

            stacked_bckg_full = QCD_full_discr.Integral(binx, 10, biny, 10)

            sig_bin_content_full = histos['signal_full']['discr'].GetBinContent(binx, biny)

            bckg_bin_content_full = QCD_full_discr.GetBinContent(binx, biny)

            #! efficiency

            if stacked_sig_full > 0:
                temp_full = (stacked_sig_full) / (histos['signal_full']['discr'].Integral())
                #print(temp_full)
                maps_full['efficiency'].SetBinContent(binx, biny, temp_full)
            else:
                maps_full['efficiency'].SetBinContent(binx, biny, 0)

            #! S/B

            if stacked_sig_full> 0 and stacked_bckg_full>0:
                temp_full = stacked_sig_full/stacked_bckg_full
                maps_full['s_b'].SetBinContent(binx, biny, temp_full)
            else:
                maps_full['s_b'].SetBinContent(binx, biny, 0)

            #! differential S/B


            if sig_bin_content_full!= 0 and bckg_bin_content_full!=0:

                temp_full = sig_bin_content_full/bckg_bin_content_full

                maps_full['s_b_diff'].SetBinContent(binx, biny, temp_full)
            else:
                maps_full['s_b_diff'].SetBinContent(binx, biny, 0)
            
            #! S /sqrt{B}

            if stacked_sig_full>0 and stacked_bckg_full>0:

                sqrt_stacked_bckg_full = ROOT.sqrt(stacked_bckg_full)

                temp_full = stacked_sig_full/sqrt_stacked_bckg_full

                maps_full['s_sqrt_b'].SetBinContent(binx, biny, temp_full)
            else:
                maps_full['s_sqrt_b'].SetBinContent(binx, biny,0)

            #! differential S/sqrt(B)

            if sig_bin_content_full!=0 and bckg_bin_content_full!=0:
                
                sqrt_bckg_bin_content_full = ROOT.sqrt(bckg_bin_content_full)
                
                temp_full = sig_bin_content_full/sqrt_bckg_bin_content_full

                maps_full['s_sqrt_b_diff'].SetBinContent(binx, biny, temp_full)
            
            else:
                maps_full['s_sqrt_b_diff'].SetBinContent(binx, biny, 0)



        #TODO FLASHSIM

            stacked_sig_flash = histos['signal_flash']['discr'].Integral(binx, 10, biny, 10)
            
            #print("stacked signal: ", stacked_sig_flash)

            stacked_bckg_flash = QCD_flash_discr.Integral(binx, 10, biny, 10)

            sig_bin_content_flash = histos['signal_flash']['discr'].GetBinContent(binx, biny)

            bckg_bin_content_flash = QCD_flash_discr.GetBinContent(binx, biny)

            #! efficiency

            if stacked_sig_flash > 0:
                temp_flash = (stacked_sig_flash) / (histos['signal_flash']['discr'].Integral())
                #print(temp_flash)
                maps_flash['efficiency'].SetBinContent(binx, biny, temp_flash)
            else:
                maps_flash['efficiency'].SetBinContent(binx, biny, 0)

            #! S/B

            if stacked_sig_flash> 0 and stacked_bckg_flash>0:
                temp_flash = stacked_sig_flash/stacked_bckg_flash
                maps_flash['s_b'].SetBinContent(binx, biny, temp_flash)
            else:
                maps_flash['s_b'].SetBinContent(binx, biny, 0)

            #! differential S/B


            if sig_bin_content_flash!= 0 and bckg_bin_content_flash!=0:

                temp_flash = sig_bin_content_flash/bckg_bin_content_flash

                maps_flash['s_b_diff'].SetBinContent(binx, biny, temp_flash)
            else:
                maps_flash['s_b_diff'].SetBinContent(binx, biny, 0)
            
            #! S/sqrt(B)

            if stacked_sig_flash>0 and stacked_bckg_flash>0:

                sqrt_stacked_bckg_flash = ROOT.sqrt(stacked_bckg_flash)

                temp_flash = stacked_sig_flash/sqrt_stacked_bckg_flash

                maps_flash['s_sqrt_b'].SetBinContent(binx, biny, temp_flash)
            else:
                maps_flash['s_sqrt_b'].SetBinContent(binx, biny,0)

            #! differential S/sqrt(B)

            if sig_bin_content_flash!=0 and bckg_bin_content_flash!=0:
                
                sqrt_bckg_bin_content_flash = ROOT.sqrt(bckg_bin_content_flash)
                
                temp_flash = sig_bin_content_flash/sqrt_bckg_bin_content_flash

                maps_flash['s_sqrt_b_diff'].SetBinContent(binx, biny, temp_flash)
            
            else:
                maps_flash['s_sqrt_b_diff'].SetBinContent(binx, biny, 0)


c1 = ROOT.TCanvas("c1", "plot", 5000, 3500)
c1.SetGrid()
histos['signal_full']['discr'].Draw("text COLZ")
histos['signal_full']['discr'].SetTitle("Distribution of signal for fullsim")
#histos['signal_full']['discr'].Scale(1/(histos['signal_full']['discr'].Integral()))


c2 = ROOT.TCanvas("c2", "Efficiency plot", 5000, 3500)
c2.SetGrid()
histos['signal_flash']['discr'].Draw("text COLZ")
histos['signal_flash']['discr'].SetTitle("Distribution of signal for flashsim")


c3 = ROOT.TCanvas("c3", "Efficiency plot fullsim", 5000, 3500)
c3.SetGrid()
maps_full['efficiency'].Draw("text COLZ")
maps_full['efficiency'].SetTitle("Efficiency map fullsim")

c4 = ROOT.TCanvas("c4", "Efficiency plot flashsim", 5000, 3500)
c4.SetGrid()
maps_flash['efficiency'].Draw("text COLZ")
maps_flash['efficiency'].SetTitle("Efficiency map flashsim")


c5 = ROOT.TCanvas("c5", "S/B plot fullsim", 5000, 3500)
c5.SetGrid()
maps_full['s_b'].Draw("text COLZ")
maps_full['s_b'].SetTitle("Integrated S/B map fullsim")


c6 = ROOT.TCanvas("c6", "S/B plot flashsim", 5000, 3500)
c6.SetGrid()
maps_flash['s_b'].Draw("text COLZ")
maps_flash['s_b'].SetTitle("Integrated S/B map flashsim")


c7 = ROOT.TCanvas("c7", "Differential S/B plot fullsim", 5000, 3500)
c7.SetGrid()
maps_full['s_b_diff'].Draw("text COLZ")
maps_full['s_b_diff'].SetTitle("Differential S/B map fullsim")


c8 = ROOT.TCanvas("c8", "Differential S/B plot flashsim", 5000, 3500)
c8.SetGrid()
maps_flash['s_b_diff'].Draw("text COLZ")
maps_flash['s_b_diff'].SetTitle("Differential S/B map flashsim")

c9 = ROOT.TCanvas("c9", "IntegratedS / #sqrt{B} plot fullsim", 5000, 3500)
c9.SetGrid()
maps_full['s_sqrt_b'].Draw("text COLZ")
maps_full['s_sqrt_b'].SetTitle("IntegratedS / #sqrt{B} map fullsim")


c10 = ROOT.TCanvas("c10", "IntegratedS / #sqrt{B} plot flashsim", 5000, 3500)
c10.SetGrid()
maps_flash['s_sqrt_b'].Draw("text COLZ")
maps_flash['s_sqrt_b'].SetTitle("IntegratedS / #sqrt{B} map flashsim")


c11 = ROOT.TCanvas("c11", "DifferentialS / #sqrt{B} plot fullsim", 5000, 3500)
c11.SetGrid()
maps_full['s_sqrt_b_diff'].Draw("text COLZ")
maps_full['s_sqrt_b_diff'].SetTitle("DifferentialS / #sqrt{B} map fullsim")


c12 = ROOT.TCanvas("c12", "DifferentialS / #sqrt{B} plot flashsim", 5000, 3500)
c12.SetGrid()
maps_flash['s_sqrt_b_diff'].Draw("text COLZ")
maps_flash['s_sqrt_b_diff'].SetTitle("DifferentialS / #sqrt{B} map flashsim")

c13 = ROOT.TCanvas("c13", "Background distribution fullsim", 5000, 3500)
c13.SetGrid()
QCD_full_discr.Draw("text COLZ")
QCD_full_discr.SetTitle("Background distributions fullsim")

c14 = ROOT.TCanvas("c14", "Background distribution flashsim", 5000, 3500)
c14.SetGrid()
QCD_flash_discr.Draw("text COLZ")
QCD_flash_discr.SetTitle("Background distributions flashsim")


c15 = ROOT.TCanvas("c15", "Background distribution fullsim", 5000, 3500)

legend15 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)

QCD_full_softdrop_jet1.Draw("HIST")
QCD_full_softdrop_jet1.SetTitle("Softdrop mass for Jet1, Run2 fullsim")
QCD_full_softdrop_jet1.SetLineWidth(2)
QCD_full_softdrop_jet1.SetFillColorAlpha(ROOT.kCyan - 10, 0.6)
legend15.AddEntry(QCD_full_softdrop_jet1, "Run2 fullsim, background", "f")



histos["signal_full"]['1d_softdrop_jet1'].Draw("SAME HIST")
histos["signal_full"]['1d_softdrop_jet1'].SetLineWidth(3)
histos["signal_full"]['1d_softdrop_jet1'].SetLineColor(ROOT.kRed +3)
histos["signal_full"]['1d_softdrop_jet1'].Scale(50000)
legend15.AddEntry(histos["signal_full"]['1d_softdrop_jet1'], "Run2 fullsim, signal x 50000", "l")

legend15.Draw()

c16 = ROOT.TCanvas("c16", "Background distribution fullsim", 5000, 3500)

legend16 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)


QCD_flash_softdrop_jet1.SetTitle("Softdrop mass for Jet1, Run2 flashsim")
QCD_flash_softdrop_jet1.SetLineWidth(2)
#QCD_flash_softdrop_jet1.SetLineStyle(2)
QCD_flash_softdrop_jet1.Draw("HIST")
QCD_flash_softdrop_jet1.SetLineColor(ROOT.kGreen +2)
QCD_flash_softdrop_jet1.SetFillColorAlpha(ROOT.kGreen -10, 0.5)
legend16.AddEntry(QCD_flash_softdrop_jet1, "Run2 flashsim, background", "f")

histos["signal_flash"]['1d_softdrop_jet1'].Draw("SAME HIST")
histos["signal_flash"]['1d_softdrop_jet1'].SetLineWidth(3)
#histos["signal_flash"]['1d_softdrop_jet1'].SetLineStyle(2)

histos["signal_flash"]['1d_softdrop_jet1'].SetLineColor(ROOT.kBlack)
histos["signal_flash"]['1d_softdrop_jet1'].Scale(50000)
legend16.AddEntry(histos["signal_flash"]['1d_softdrop_jet1'], "Run2 flashsim, signal x 50000", "l")

legend16.Draw()

c17 = ROOT.TCanvas("c17", "Background distribution fullsim", 5000, 3500)

legend17 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)


QCD_full_softdrop_jet2.Draw("HIST")
QCD_full_softdrop_jet2.SetTitle("Softdrop mass for Jet2, Run2 fullsim")
QCD_full_softdrop_jet2.SetLineWidth(2)
QCD_full_softdrop_jet2.SetFillColorAlpha(ROOT.kCyan - 10, 0.5)
legend17.AddEntry(QCD_full_softdrop_jet2, "Run2 fullsim, background", "f")



histos["signal_full"]['1d_softdrop_jet2'].Draw("SAME HIST")
histos["signal_full"]['1d_softdrop_jet2'].SetLineWidth(3)
histos["signal_full"]['1d_softdrop_jet2'].SetLineColor(ROOT.kRed +3)
histos["signal_full"]['1d_softdrop_jet2'].Scale(70000)
legend17.AddEntry(histos["signal_full"]['1d_softdrop_jet2'], "Run2 fullsim, signal x 70000", "l")

legend17.Draw()

c18 = ROOT.TCanvas("c18", "Background distribution fullsim", 5000, 3500)


legend18 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)

QCD_flash_softdrop_jet2.SetTitle("Softdrop mass for Jet2, Run2 flashsim")
QCD_flash_softdrop_jet2.SetLineWidth(2)
QCD_flash_softdrop_jet2.Draw("HIST")
#QCD_flash_softdrop_jet2.SetLineStyle(2)
QCD_flash_softdrop_jet2.SetLineColor(ROOT.kGreen +2)
QCD_flash_softdrop_jet2.SetFillColorAlpha(ROOT.kGreen -10, 0.5)
legend18.AddEntry(QCD_flash_softdrop_jet2, "Run2 flashsim, background", "f")



histos["signal_flash"]['1d_softdrop_jet2'].Draw("SAME HIST")
histos["signal_flash"]['1d_softdrop_jet2'].SetLineWidth(3)
#histos["signal_flash"]['1d_softdrop_jet2'].SetLineStyle(2)

histos["signal_flash"]['1d_softdrop_jet2'].SetLineColor(ROOT.kBlack)
histos["signal_flash"]['1d_softdrop_jet2'].Scale(70000)
legend18.AddEntry(histos["signal_flash"]['1d_softdrop_jet2'], "Run2 flashsim, signal x 70000", "l")

legend18.Draw()

# c19 = ROOT.TCanvas("c19", "Background distribution fullsim", 5000, 3500)

# c19.Divide(3,4)


# c19.cd(1)

# histos['QCD4_full']['discr'].Draw("COLZ")
# histos['QCD4_full']['discr'].SetTitle("QCD4 fullsim")

# c19.cd(2)

# histos['QCD5_full']['discr'].Draw("COLZ")
# histos['QCD5_full']['discr'].SetTitle("QCD5 fullsim")

# c19.cd(3)

# histos['QCD6_full']['discr'].Draw("COLZ")
# histos['QCD6_full']['discr'].SetTitle("QCD6 fullsim")

# c19.cd(4)

# histos['QCD7_full']['discr'].Draw("COLZ")
# histos['QCD7_full']['discr'].SetTitle("QCD7 fullsim")

# c19.cd(5)

# histos['QCD8_full']['discr'].Draw("COLZ")
# histos['QCD8_full']['discr'].SetTitle("QCD8 fullsim")

# c19.cd(6)

# histos['signal_full']['discr'].Draw("COLZ")
# histos['signal_full']['discr'].SetTitle("signal fullsim")

# c19.cd(7)

# histos['QCD6_flash']['discr'].Draw("COLZ")
# histos['QCD6_flash']['discr'].SetTitle("QCD6 flashsim")


# c19.cd(8)

# histos['QCD7_flash']['discr'].Draw("COLZ")
# histos['QCD7_flash']['discr'].SetTitle("QCD7 flashsim")

# c19.cd(9)

# histos['QCD8_flash']['discr'].Draw("COLZ")
# histos['QCD8_flash']['discr'].SetTitle("QCD8 flashsim")

# c19.cd(10)

# histos['signal_flash']['discr'].Draw("COLZ")
# histos['signal_flash']['discr'].SetTitle("signal flashsim")


c20 = ROOT.TCanvas("c20", "Background distribution fullsim", 5000, 3500)

legend20 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)

QCD_full_discr_jet1.Draw("HIST")
QCD_full_discr_jet1.SetTitle("discriminator for Jet1")
QCD_full_discr_jet1.SetLineWidth(2)
QCD_full_discr_jet1.SetFillColorAlpha(ROOT.kCyan - 10, 0.6)
QCD_full_discr_jet1.SetMaximum(400e3)
legend20.AddEntry(QCD_full_discr_jet1, "Run2 fullsim, background", "f")



histos["signal_full"]['1d_discr_jet1'].Draw("SAME HIST")
histos["signal_full"]['1d_discr_jet1'].SetLineWidth(3)
histos["signal_full"]['1d_discr_jet1'].SetLineColor(ROOT.kRed +3)
histos["signal_full"]['1d_discr_jet1'].Scale(35000)
legend20.AddEntry(histos["signal_full"]['1d_discr_jet1'], "Run2 fullsim, signal x 35000", "l")

QCD_flash_discr_jet1.Draw("HIST SAME")
QCD_flash_discr_jet1.SetLineWidth(2)
QCD_flash_discr_jet1.SetFillColorAlpha(ROOT.kGreen - 10, 0.6)
QCD_flash_discr_jet1.SetMaximum(400e3)
legend20.AddEntry(QCD_flash_discr_jet1, "Run2 flashsim, background", "f")



histos["signal_flash"]['1d_discr_jet1'].Draw("SAME HIST")
histos["signal_flash"]['1d_discr_jet1'].SetLineWidth(3)
histos["signal_flash"]['1d_discr_jet1'].SetLineColor(ROOT.kBlack)
histos["signal_flash"]['1d_discr_jet1'].Scale(35000)
legend20.AddEntry(histos["signal_flash"]['1d_discr_jet1'], "Run2 flashsim, signal x 35000", "l")

legend20.Draw()

c21 = ROOT.TCanvas("c21", "Background distribution fullsim", 5000, 3500)

legend21 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)


histos["signal_full"]['1d_discr_jet2'].Draw("HIST")
histos["signal_full"]['1d_discr_jet2'].SetLineWidth(3)
#histos["signal_full"]['1d_discr_jet2'].SetLineStyle(2)
histos["signal_full"]['1d_discr_jet2'].SetLineColor(ROOT.kBlack)
histos["signal_full"]['1d_discr_jet2'].Scale(1000)
legend21.AddEntry(histos["signal_full"]['1d_discr_jet2'], "Run2 fullsim, signal x 1000", "l")
histos['signal_full']['1d_discr_jet2'].SetMaximum(1500)

QCD_full_discr_jet2.SetTitle("discriminator for Jet2")
QCD_full_discr_jet2.SetLineWidth(2)
#QCD_full_discr_jet2.SetLineStyle(2)
QCD_full_discr_jet2.Draw("HIST SAME")
QCD_full_discr_jet2.SetLineColor(ROOT.kGreen +2)
QCD_full_discr_jet2.SetFillColorAlpha(ROOT.kCyan -8, 0.5)
legend21.AddEntry(QCD_full_discr_jet2, "Run2 fullsim, background", "f")
QCD_full_discr_jet2.SetMaximum(1500)



QCD_flash_discr_jet2.SetLineWidth(2)
#QCD_flash_discr_jet2.SetLineStyle(2)
QCD_flash_discr_jet2.Draw("HIST SAME")
QCD_flash_discr_jet2.SetLineColor(ROOT.kGreen +2)
QCD_flash_discr_jet2.SetFillColorAlpha(ROOT.kGreen -10, 0.5)
legend21.AddEntry(QCD_flash_discr_jet2, "Run2 flashsim, background", "f")

histos["signal_flash"]['1d_discr_jet2'].Draw("SAME HIST")
histos["signal_flash"]['1d_discr_jet2'].SetLineWidth(3)
#histos["signal_flash"]['1d_discr_jet2'].SetLineStyle(2)

histos["signal_flash"]['1d_discr_jet2'].SetLineColor(ROOT.kRed + 3)
histos["signal_flash"]['1d_discr_jet2'].Scale(1000)
legend21.AddEntry(histos["signal_flash"]['1d_discr_jet2'], "Run2 flashsim, signal x 1000", "l")

legend21.Draw()

c22 = ROOT.TCanvas("c22", "Mass vs Discr background", 5000, 3500)

QCD_flash_mass_vs_discr.Draw("COLZ text")
QCD_flash_mass_vs_discr.SetTitle("Mass vs Discriminator distribution Run2 flashsim; Softdrop mass; Discriminator")

c23 = ROOT.TCanvas("c23", "Mass vs Discr background", 5000, 3500)

QCD_full_mass_vs_discr.Draw("COLZ text")
QCD_full_mass_vs_discr.SetTitle("Mass vs Discriminator distribution Run2 fullsim; Softdrop mass; Discriminator")




#c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/sig_distr_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/sig_distr_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
# c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/efficiency_map_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c4.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/efficiency_map_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
#c5.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/integrated_s_b_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c6.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/integrated_s_b_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
#c7.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/differential_s_b_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c8.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/differential_s_b_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
#c9.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/integrated_s_sqrt_b_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c10.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/integrated_s_sqrt_b_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
#c11.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/differential_s_sqrt_b_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c12.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/differential_s_sqrt_b_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
#c13.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/bckg_distr_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c14.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/bckg_distr_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
c15.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/softdrop_jet1_full_QCD_6_7_8_NO_softdrop_window_MET_no_discr_cut.pdf")
c16.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/softdrop_jet1_flash_QCD_6_7_8_NO_softdrop_window_MET_no_discr_cut.pdf")
c17.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/softdrop_jet2_full_QCD_6_7_8_NO_softdrop_window_MET_no_discr_cut.pdf")
c18.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/softdrop_jet2_flash_QCD_6_7_8_NO_softdrop_window_MET_no_discr_cut.pdf")
# c19.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/distr_discr_divided_softdrop_window_plus_QCD_reshape_MET.pdf")
# c20.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/discr_jet1_softdrop_window_plus_QCD_reshape_MET.pdf")
# c21.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/discr_jet2_softdrop_window_plus_QCD_reshape_MET.pdf")
#c22.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/mass_vs_discr_flash_QCD.pdf")
#c23.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/mass_vs_discr_full_QCD.pdf")



