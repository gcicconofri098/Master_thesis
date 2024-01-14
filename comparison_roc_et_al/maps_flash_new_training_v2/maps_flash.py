import ROOT
import os
import numpy as np
from decimal import *
import re

ROOT.EnableImplicitMT()

# module_path = os.path.join(os.path.dirname(__file__), "utils.h")
# module_path2 = os.path.join(os.path.dirname(__file__), "nb.h")
# module_path_3 = os.path.join(os.path.dirname(__file__), "utils_calibration.h")
module_path_4 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_higgs_within_nbd.h")


ROOT.gStyle.SetOptStat(0)


# ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')
# ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')
# ROOT.gInterpreter.ProcessLine(f'#include "{module_path2}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_4}"')

ROOT.gStyle.SetPaintTextFormat("1.f")


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
    "QCD4_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/snapshots_no_nb/root_files_new_training_flashsim_v2/QCD4_flash_no_pt_window_calibrated_mass_no_nb.root",
    "QCD5_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/snapshots_no_nb/root_files_new_training_flashsim_v2/QCD5_flash_no_pt_window_calibrated_mass_no_nb.root",
    "QCD6_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/snapshots_no_nb/root_files_new_training_flashsim_v2/QCD6_flash_no_pt_window_calibrated_mass_no_nb.root",
    "QCD7_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/snapshots_no_nb/root_files_new_training_flashsim_v2/QCD7_flash_no_pt_window_calibrated_mass_no_nb.root",
    "QCD8_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/snapshots_no_nb/root_files_new_training_flashsim_v2/QCD8_flash_no_pt_window_calibrated_mass_no_nb.root",
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

n_events = {}

processes = list(df_files.keys())
#processes = ['QCD4_flash','QCD5_flash','QCD6_flash','QCD7_flash','QCD8_flash']
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
    n_events[i] = df[i].Count().GetValue()
    print(n_events[i])
    df[i] = df[i].Filter("MET_pt<100")

    df[i] = df[i].Filter("jet1_softdrop>50 && jet2_softdrop>50")

    df[i] = df[i].Define("jet1_discriminator_low", "jet1_discr < 0.98 && jet1_discr >=0.9").Define("jet1_discriminator_high", "jet1_discr >=0.98 && jet1_discr <=1")


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

    histos[i]['1d_discr_jet1_low'] = df[i].Histo1D(("Discriminator Jet1", "0.9 < Jet 1 discriminator <0.98; Discriminator; Events", 20, 0.9, 0.98), "jet1_discr").GetValue()

    histos[i]['1d_discr_jet1_high'] = df[i].Histo1D(("Discriminator Jet1", "Jet 1 discriminator >=0.95; Discriminator; Events", 25, 0.95, 1), "jet1_discr").GetValue()



    histos[i]['1d_eta'] = df[i].Histo1D(("Eta", "Eta; Eta; Events", 15, -4, 4), "Second_selection_eta").GetValue()

    histos[i]['1d_phi'] = df[i].Histo1D(("Phi", "Phi; Phi; Events", 15, -4, 4), "Second_selection_phi").GetValue()

    histos[i]['1d_pt'] = df[i].Histo1D(("Pt", "Pt; Pt; Events", 120, 0, 3000), "Second_selection_pt").GetValue()

    histos[i]['1d_softdrop'] = df[i].Histo1D(("Pt", "Pt; Softdrop mass; Events", 120, 0, 350), "Second_selection_mass").GetValue()

    histos[i]['1d_discr'] = df[i].Histo1D(("Pt", "Pt; Discriminator; Events", 25, 0.95, 1), "Second_selection_discriminator").GetValue()

    print("number of entries before weighting:", histos[i]['discr'].Integral())

for key_full in existing_processes:
    key_nofull=key_full.split("_")[0]

    print(f"weight for dataset {key_full} is: {weights[key_nofull]*2.27/n_events[key_full]}")

    histos[key_full]['discr'].Scale(weights[key_nofull]*2.27/n_events[key_full]) #* 2.27 is the luminosity factor that has to be compensated

    histos[key_full]['softdrop'].Scale(weights[key_nofull]*2.27/n_events[key_full])

    histos[key_full]['1d_softdrop_jet1'].Scale(weights[key_nofull]*2.27/n_events[key_full])

    histos[key_full]['1d_softdrop_jet2'].Scale(weights[key_nofull]*2.27/n_events[key_full])

    histos[key_full]['1d_discr_jet1'].Scale(weights[key_nofull]*2.27/n_events[key_full])

    histos[key_full]['1d_discr_jet2'].Scale(weights[key_nofull]*2.27/n_events[key_full])

    histos[key_full]['reshape'].Scale(weights[key_nofull]*2.27/n_events[key_full])

    histos[key_full]['mass_vs_discr'].Scale(weights[key_nofull]*2.27/n_events[key_full])

    histos[key_full]['1d_discr_jet1_low'].Scale(weights[key_nofull]*2.27/n_events[key_full])

    histos[key_full]['1d_discr_jet1_high'].Scale(weights[key_nofull]*2.27/n_events[key_full])


    histos[key_full]['1d_eta'].Scale(weights[key_nofull]*2.27/n_events[key_full])

    histos[key_full]['1d_phi'].Scale(weights[key_nofull]*2.27/n_events[key_full])

    histos[key_full]['1d_pt'].Scale(weights[key_nofull]*2.27/n_events[key_full])

    histos[key_full]['1d_softdrop'].Scale(weights[key_nofull]*2.27/n_events[key_full])

    histos[key_full]['1d_discr'].Scale(weights[key_nofull]*2.27/n_events[key_full])


    print("number of entries after weighting:", histos[key_full]['discr'].Integral())


r_flash = re.compile("QCD._flash")


QCD_flash_processes = list(filter(r_flash.match, existing_processes))

print("QCD flashsim processes:", QCD_flash_processes)


print("starting to stack histos")



#! QCD FLASHSIM STACKING

QCD_flash_discr = histos[str(QCD_flash_processes[0])]['discr'].Clone()
QCD_flash_softdrop = histos[str(QCD_flash_processes[0])]['softdrop'].Clone()

QCD_flash_softdrop_jet1 = histos[str(QCD_flash_processes[0])]['1d_softdrop_jet1'].Clone()
QCD_flash_softdrop_jet2 = histos[str(QCD_flash_processes[0])]['1d_softdrop_jet2'].Clone()

QCD_flash_discr_jet1 = histos[str(QCD_flash_processes[0])]['1d_discr_jet1'].Clone()
QCD_flash_discr_jet2 = histos[str(QCD_flash_processes[0])]['1d_discr_jet2'].Clone()

QCD_flash_reshape = histos[str(QCD_flash_processes[0])]['reshape'].Clone()

QCD_flash_mass_vs_discr = histos[str(QCD_flash_processes[0])]['mass_vs_discr'].Clone()

QCD_flash_jet1_discr_low = histos[str(QCD_flash_processes[0])]['1d_discr_jet1_low'].Clone()

QCD_flash_jet1_discr_high = histos[str(QCD_flash_processes[0])]['1d_discr_jet1_high'].Clone()

QCD_flash_eta = histos[str(QCD_flash_processes[0])]['1d_eta'].Clone()

QCD_flash_phi = histos[str(QCD_flash_processes[0])]['1d_phi'].Clone()

QCD_flash_pt = histos[str(QCD_flash_processes[0])]['1d_pt'].Clone()

QCD_flash_softdrop_1d  = histos[str(QCD_flash_processes[0])]['1d_softdrop'].Clone()

QCD_flash_discr_1d = histos[str(QCD_flash_processes[0])]['1d_discr'].Clone()



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

        QCD_flash_jet1_discr_low.Add(histos[i]['1d_discr_jet1_low'])

        QCD_flash_jet1_discr_high.Add(histos[i]['1d_discr_jet1_high'])


        QCD_flash_eta.Add(histos[i]['1d_eta'])

        QCD_flash_phi.Add(histos[i]['1d_phi'])

        QCD_flash_pt.Add(histos[i]['1d_pt'])

        QCD_flash_softdrop_jet1.Add(histos[i]['1d_softdrop'])

        QCD_flash_discr_jet1.Add(histos[i]['1d_discr'])
            


    print(f"adding histo for {i}")

QCD_flash_discr_entries = QCD_flash_discr.Integral()

print("entries flashsim QCD after preselection:", QCD_flash_discr_entries)

#! QCD RESHAPE IS DONE HERE

# total_full = QCD_full_reshape.Integral(1, 18, 1, 18)

# mass_full = QCD_full_reshape.Integral(7,8,7,8)

# ratio_full = mass_full/total_full
# print("ratio fullsim", ratio_full)

total_flash = QCD_flash_reshape.Integral(1, 18, 1, 18)

mass_flash = QCD_flash_reshape.Integral(7,8,7,8)

ratio_flash = mass_flash/total_flash

print("ratio flashsim", ratio_flash)


# QCD_flash_discr.Scale(ratio_flash)
# QCD_flash_softdrop.Scale(ratio_flash)
# QCD_flash_softdrop_jet1.Scale(ratio_flash)
# QCD_flash_softdrop_jet2.Scale(ratio_flash)
# QCD_flash_discr_jet1.Scale(ratio_flash)
# QCD_flash_discr_jet2.Scale(ratio_flash)

QCD_flash_mass_vs_discr.Scale(ratio_flash)

#! ~~~~~ RESHAPING DONE ~~~~~~

# maps_full = {}

# maps_flash = {}


# maps_flash['yield'] = histos['signal_flash']['discr'].Clone()
# maps_flash['norm_yield'] = histos['signal_flash']['discr'].Clone()
# maps_flash['efficiency'] = histos['signal_flash']['discr'].Clone()
# maps_flash['s_b'] = histos['signal_flash']['discr'].Clone()
# maps_flash['s_b_diff'] = histos['signal_flash']['discr'].Clone()
# maps_flash['s_sqrt_b'] = histos['signal_flash']['discr'].Clone()
# maps_flash['s_sqrt_b_diff'] = histos['signal_flash']['discr'].Clone()

# for binx in reversed(range(1, 11)):
#     for biny in reversed(range(1, 11)):
#         if binx >= biny:
        

#         #TODO FLASHSIM

#             stacked_sig_flash = histos['signal_flash']['discr'].Integral(binx, 10, biny, 10)
            
#             #print("stacked signal: ", stacked_sig_flash)

#             stacked_bckg_flash = QCD_flash_discr.Integral(binx, 10, biny, 10)

#             sig_bin_content_flash = histos['signal_flash']['discr'].GetBinContent(binx, biny)

#             bckg_bin_content_flash = QCD_flash_discr.GetBinContent(binx, biny)

#             #! efficiency

#             if stacked_sig_flash > 0:
#                 temp_flash = (stacked_sig_flash) / (histos['signal_flash']['discr'].Integral())
#                 #print(temp_flash)
#                 maps_flash['efficiency'].SetBinContent(binx, biny, temp_flash)
#             else:
#                 maps_flash['efficiency'].SetBinContent(binx, biny, 0)

#             #! S/B

#             if stacked_sig_flash> 0 and stacked_bckg_flash>0:
#                 temp_flash = stacked_sig_flash/stacked_bckg_flash
#                 maps_flash['s_b'].SetBinContent(binx, biny, temp_flash)
#             else:
#                 maps_flash['s_b'].SetBinContent(binx, biny, 0)

#             #! differential S/B


#             if sig_bin_content_flash!= 0 and bckg_bin_content_flash!=0:

#                 temp_flash = sig_bin_content_flash/bckg_bin_content_flash

#                 maps_flash['s_b_diff'].SetBinContent(binx, biny, temp_flash)
#             else:
#                 maps_flash['s_b_diff'].SetBinContent(binx, biny, 0)
            
#             #! S/sqrt(B)

#             if stacked_sig_flash>0 and stacked_bckg_flash>0:

#                 sqrt_stacked_bckg_flash = ROOT.sqrt(stacked_bckg_flash)

#                 temp_flash = stacked_sig_flash/sqrt_stacked_bckg_flash

#                 maps_flash['s_sqrt_b'].SetBinContent(binx, biny, temp_flash)
#             else:
#                 maps_flash['s_sqrt_b'].SetBinContent(binx, biny,0)

#             #! differential S/sqrt(B)

#             if sig_bin_content_flash!=0 and bckg_bin_content_flash!=0:
                
#                 sqrt_bckg_bin_content_flash = ROOT.sqrt(bckg_bin_content_flash)
                
#                 temp_flash = sig_bin_content_flash/sqrt_bckg_bin_content_flash

#                 maps_flash['s_sqrt_b_diff'].SetBinContent(binx, biny, temp_flash)
            
#             else:
#                 maps_flash['s_sqrt_b_diff'].SetBinContent(binx, biny, 0)



# c2 = ROOT.TCanvas("c2", "Efficiency plot", 5000, 3500)
# c2.SetGrid()
# histos['signal_flash']['discr'].Draw("text COLZ")
# histos['signal_flash']['discr'].SetTitle("Distribution of signal for flashsim")

# c4 = ROOT.TCanvas("c4", "Efficiency plot flashsim", 5000, 3500)
# c4.SetGrid()
# maps_flash['efficiency'].Draw("text COLZ")
# maps_flash['efficiency'].SetTitle("Efficiency map flashsim")



# c6 = ROOT.TCanvas("c6", "S/B plot flashsim", 5000, 3500)
# c6.SetGrid()
# maps_flash['s_b'].Draw("text COLZ")
# maps_flash['s_b'].SetTitle("Integrated S/B map flashsim")


# c8 = ROOT.TCanvas("c8", "Differential S/B plot flashsim", 5000, 3500)
# c8.SetGrid()
# maps_flash['s_b_diff'].Draw("text COLZ")
# maps_flash['s_b_diff'].SetTitle("Differential S/B map flashsim")


# c10 = ROOT.TCanvas("c10", "IntegratedS / #sqrt{B} plot flashsim", 5000, 3500)
# c10.SetGrid()
# maps_flash['s_sqrt_b'].Draw("text COLZ")
# maps_flash['s_sqrt_b'].SetTitle("IntegratedS / #sqrt{B} map flashsim")



# c12 = ROOT.TCanvas("c12", "DifferentialS / #sqrt{B} plot flashsim", 5000, 3500)
# c12.SetGrid()
# maps_flash['s_sqrt_b_diff'].Draw("text COLZ")
# maps_flash['s_sqrt_b_diff'].SetTitle("DifferentialS / #sqrt{B} map flashsim")

c14 = ROOT.TCanvas("c14", "Background distribution flashsim", 5000, 3500)
c14.SetGrid()
QCD_flash_discr.Draw("text COLZ")
QCD_flash_discr.SetTitle("Background distributions flashsim")



# c16 = ROOT.TCanvas("c16", "Background distribution fullsim", 5000, 3500)

# legend16 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)


# QCD_flash_softdrop_jet1.SetTitle("Softdrop mass for Jet1, Run2 flashsim")
# QCD_flash_softdrop_jet1.SetLineWidth(2)
# #QCD_flash_softdrop_jet1.SetLineStyle(2)
# QCD_flash_softdrop_jet1.Draw("HIST")
# QCD_flash_softdrop_jet1.SetLineColor(ROOT.kGreen +2)
# QCD_flash_softdrop_jet1.SetFillColorAlpha(ROOT.kGreen -10, 0.5)
# legend16.AddEntry(QCD_flash_softdrop_jet1, "Run2 flashsim, background", "f")

# histos["signal_flash"]['1d_softdrop_jet1'].Draw("SAME HIST")
# histos["signal_flash"]['1d_softdrop_jet1'].SetLineWidth(3)
# #histos["signal_flash"]['1d_softdrop_jet1'].SetLineStyle(2)

# histos["signal_flash"]['1d_softdrop_jet1'].SetLineColor(ROOT.kBlack)
# histos["signal_flash"]['1d_softdrop_jet1'].Scale(50000)
# legend16.AddEntry(histos["signal_flash"]['1d_softdrop_jet1'], "Run2 flashsim, signal x 50000", "l")

# legend16.Draw()

# c18 = ROOT.TCanvas("c18", "Background distribution fullsim", 5000, 3500)


# legend18 = ROOT.TLegend(0.62, 0.70, 0.9, 0.9)

# QCD_flash_softdrop_jet2.SetTitle("Softdrop mass for Jet2, Run2 flashsim")
# QCD_flash_softdrop_jet2.SetLineWidth(2)
# QCD_flash_softdrop_jet2.Draw("HIST")
# #QCD_flash_softdrop_jet2.SetLineStyle(2)
# QCD_flash_softdrop_jet2.SetLineColor(ROOT.kGreen +2)
# QCD_flash_softdrop_jet2.SetFillColorAlpha(ROOT.kGreen -10, 0.5)
# legend18.AddEntry(QCD_flash_softdrop_jet2, "Run2 flashsim, background", "f")



# histos["signal_flash"]['1d_softdrop_jet2'].Draw("SAME HIST")
# histos["signal_flash"]['1d_softdrop_jet2'].SetLineWidth(3)
# #histos["signal_flash"]['1d_softdrop_jet2'].SetLineStyle(2)

# histos["signal_flash"]['1d_softdrop_jet2'].SetLineColor(ROOT.kBlack)
# histos["signal_flash"]['1d_softdrop_jet2'].Scale(70000)
# legend18.AddEntry(histos["signal_flash"]['1d_softdrop_jet2'], "Run2 flashsim, signal x 70000", "l")

# legend18.Draw()

c22 = ROOT.TCanvas("c22", "Mass vs Discr background", 6700, 3500)

QCD_flash_mass_vs_discr.Draw("COLZ text")
QCD_flash_mass_vs_discr.SetTitle("Mass vs Discriminator distribution Run2 flashsim; Softdrop mass; Discriminator")


c24 = ROOT.TCanvas("c24", "Jet 1 discr <0.98", 5000, 3500)

QCD_flash_jet1_discr_low.Draw("HIST")
QCD_flash_jet1_discr_low.SetTitle("Jet1 discriminator <0.98; Discriminator; Events")
QCD_flash_jet1_discr_low.SetLineWidth(2)
#QCD_flash_jet1_discr_low.Scale(1/QCD_flash_jet1_discr_low.Integral())

c25 = ROOT.TCanvas("c25", "Jet 1 discr >=0.95", 5000, 3500)

QCD_flash_jet1_discr_high.Draw("HIST")
QCD_flash_jet1_discr_high.SetTitle("Jet1 discriminator >=0.95; Discriminator; Events")
QCD_flash_jet1_discr_high.SetLineWidth(2)
#QCD_flash_jet1_discr_high.Scale(1/QCD_flash_jet1_discr_high.Integral())

c26 = ROOT.TCanvas("c26", "flash eta", 5000, 3500)

QCD_flash_eta.Draw("HIST")
QCD_flash_eta.SetTitle("Eta flashsim; Eta; Events")
QCD_flash_eta.SetLineWidth(2)
c26.SetLogy(1)
#QCD_flash_eta.Scale(1/QCD_flash_eta.Integral())


c27 = ROOT.TCanvas("c27", "flash phi", 5000, 3500)

QCD_flash_phi.Draw("HIST")
QCD_flash_phi.SetTitle("Flashsim phi; Phi; Events")
QCD_flash_phi.SetLineWidth(2)
c27.SetLogy()
#QCD_flash_phi.Scale(1/QCD_flash_phi.Integral())


c28 = ROOT.TCanvas("c28", "flashsim pt", 5000, 3500)

QCD_flash_pt.Draw("HIST")
QCD_flash_pt.SetTitle("Flashsim pt; Pt; Events")
QCD_flash_pt.SetLineWidth(2)
c28.SetLogy(1)

#QCD_flash_pt.Scale(1/QCD_flash_pt.Integral())


c29 = ROOT.TCanvas("c29", "flashsim softdrop", 5000, 3500)

QCD_flash_softdrop_1d.Draw("HIST")
QCD_flash_softdrop_1d.SetTitle("Flashsim softdrop; Softdrop; Events")
QCD_flash_softdrop_1d.SetLineWidth(2)
#QCD_flash_softdrop_1d.Scale(1/QCD_flash_softdrop_1d.Integral())
c29.SetLogy(1)


c30 = ROOT.TCanvas("c30", "flashsim discriminator", 5000, 3500)

QCD_flash_discr_1d.Draw("HIST")
QCD_flash_discr_1d.SetTitle("Flashsim Discriminator; Discriminator; Events")
QCD_flash_discr_1d.SetLineWidth(2)
c30.SetLogy(1)

#QCD_flash_discr_1d.Scale(1/QCD_flash_discr_1d.Integral())


#c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/sig_distr_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/sig_distr_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
# c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/efficiency_map_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c4.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/efficiency_map_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
#c5.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/integrated_s_b_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c6.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/integrated_s_b_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
#c7.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/differential_s_b_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c8.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/differential_s_b_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
#c9.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/integrated_s_sqrt_b_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c10.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/integrated_s_sqrt_b_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
#c11.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/differential_s_sqrt_b_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c12.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/differential_s_sqrt_b_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
#c13.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/bckg_distr_full_softdrop_window_plus_QCD_reshape_MET.pdf")
# c14.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/bckg_distr_flash_softdrop_window_plus_QCD_reshape_MET.pdf")
# c15.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/softdrop_jet1_full_QCD_6_7_8_NO_softdrop_window_MET_no_discr_cut.pdf")
# c16.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/softdrop_jet1_flash_QCD_6_7_8_NO_softdrop_window_MET_no_discr_cut.pdf")
# c17.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/softdrop_jet2_full_QCD_6_7_8_NO_softdrop_window_MET_no_discr_cut.pdf")
# c18.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/softdrop_jet2_flash_QCD_6_7_8_NO_softdrop_window_MET_no_discr_cut.pdf")
# c19.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/distr_discr_divided_softdrop_window_plus_QCD_reshape_MET.pdf")
# c20.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/discr_jet1_softdrop_window_plus_QCD_reshape_MET.pdf")
# c21.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/discr_jet2_softdrop_window_plus_QCD_reshape_MET.pdf")
c22.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/mass_vs_discr_flash_QCD_all_QCD_fixed_norm.pdf")
#c23.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/mass_vs_discr_full_QCD.pdf")
c24.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/jet1_discr_low_all_QCD_fixed_norm.pdf")
c25.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/jet1_discr_0_95_all_QCD_fixed_norm.pdf")
c26.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/flashsim_eta_all_QCD_fixed_norm.pdf")
c27.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/flashsim_phi_all_QCD_fixed_norm.pdf")
c28.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/flashsim_pt_all_QCD_fixed_norm.pdf")
c29.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/flashsim_softdrop_all_QCD_fixed_norm.pdf")
c30.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/maps_flash_new_training_v2/flashsim_discriminator_0_95_incl_all_QCD_fixed_norm.pdf")





