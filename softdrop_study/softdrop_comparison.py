import os
import ROOT
import numpy as np

ROOT.EnableImplicitMT()

ROOT.gStyle.SetOptStat(1111)


module_path = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils.h")
module_path2 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/nb.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_calibration.h")


ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path2}"')


df_files = {
    "signal_flash": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/signal_flashno_pt_window.root",
    "signal_ph2": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/signal_ph2no_pt_window.root",
    "signal_full": "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/comparison_roc_et_al/signal_fullno_pt_window.root",
}

integrated_luminosity = 59830

weight = 0.01053 * integrated_luminosity *2.27

n_events = {
    "signal_flash": 540000,
    "signal_full": 540000,
    "signal_ph2": 6912,
}

processes = list(df_files.keys())
df = {}

histos = {}
for i in processes:
    df[i] = ROOT.RDataFrame("Events", df_files[i])

    histos[i] = {}

    histos[i]['jet1_softdrop_mass'] = df[i].Histo1D((str(i), str(i), 100, 35, 200), "jet1_softdrop").GetValue()
    histos[i]['jet2_softdrop_mass'] = df[i].Histo1D((str(i), str(i), 100, 35, 200), "jet2_softdrop").GetValue()

    # histos[i]['jet1_softdrop_mass'].Scale(weight/n_events[i])
    # histos[i]['jet2_softdrop_mass'].Scale(weight/n_events[i])




c1 = ROOT.TCanvas("c1", "softdrop jet1", 4500, 3500)

legend1 = ROOT.TLegend(0.13, 0.9, 0.35, 0.77)


histos['signal_flash']['jet1_softdrop_mass'].Draw("HIST")
histos['signal_flash']['jet1_softdrop_mass'].SetLineWidth(2)
histos['signal_flash']['jet1_softdrop_mass'].SetLineColor(ROOT.kRed +2)
legend1.AddEntry(histos['signal_flash']['jet1_softdrop_mass'], "Run2 flashsim", 'l')

c1.GetPad(0).Update()
stats1 = histos['signal_flash']['jet1_softdrop_mass'].GetListOfFunctions().FindObject("stats").Clone("stats1")
stats1.SetY1NDC(.4)
stats1.SetY2NDC(.53)
stats1.SetX2NDC(0.9)
stats1.SetX1NDC(0.73)


c1.GetPad(0).Update()

histos['signal_full']['jet1_softdrop_mass'].Draw("HIST")
histos['signal_full']['jet1_softdrop_mass'].SetLineWidth(2)
histos['signal_full']['jet1_softdrop_mass'].SetLineColor(ROOT.kTeal -6)
legend1.AddEntry(histos['signal_full']['jet1_softdrop_mass'], "Run2 fullsim", 'l')
c1.GetPad(0).Update()
stats3 = histos['signal_full']['jet1_softdrop_mass'].GetListOfFunctions().FindObject("stats").Clone("stats3")
stats3.SetY1NDC(.58)
stats3.SetY2NDC(.71)
stats3.SetX2NDC(0.9)
stats3.SetX1NDC(0.73)


c1.GetPad(0).Update()


histos['signal_ph2']['jet1_softdrop_mass'].Draw("HIST")
histos['signal_ph2']['jet1_softdrop_mass'].SetTitle("Softdrop mass for Jet1, no mass window, no discriminator cut, no pt window; Softdrop mass (Not calibrated); Events")
histos['signal_ph2']['jet1_softdrop_mass'].SetLineWidth(2)
histos['signal_ph2']['jet1_softdrop_mass'].SetLineColor(ROOT.kBlue +2)
histos['signal_ph2']['jet1_softdrop_mass'].Scale(1/(histos['signal_ph2']['jet1_softdrop_mass'].Integral()))
legend1.AddEntry(histos['signal_ph2']['jet1_softdrop_mass'], "Phase2 fullsim", 'l')
c1.GetPad(0).Update()
stats2 = histos['signal_ph2']['jet1_softdrop_mass'].GetListOfFunctions().FindObject("stats")
stats2.SetX2NDC(0.9)
stats2.SetY2NDC(0.89)
stats2.SetX1NDC(0.73)
stats2.SetY1NDC(0.76)

c1.GetPad(0).Update()
histos['signal_flash']['jet1_softdrop_mass'].Draw("SAME HIST")
histos['signal_flash']['jet1_softdrop_mass'].Scale(1/(histos['signal_flash']['jet1_softdrop_mass'].Integral()))

histos['signal_full']['jet1_softdrop_mass'].Draw("SAME HIST")
histos['signal_full']['jet1_softdrop_mass'].Scale(1/(histos['signal_full']['jet1_softdrop_mass'].Integral()))


c1.GetPad(0).Update()

stats1.Draw()
stats2.Draw()
stats3.Draw()


legend1.Draw()




c2 = ROOT.TCanvas("c2", "softdrop jet2", 4500, 3500)

legend = ROOT.TLegend(0.13, 0.9, 0.37, 0.77)


text = ROOT.TText(0.15, 72, "calibrated pt and mass on Run2 flashsim")
text.SetTextSize(60)
text.Draw()

histos['signal_flash']['jet2_softdrop_mass'].Draw("HIST")
histos['signal_flash']['jet2_softdrop_mass'].SetLineWidth(2)
histos['signal_flash']['jet2_softdrop_mass'].SetLineColor(ROOT.kRed +2)
legend.AddEntry(histos['signal_flash']['jet2_softdrop_mass'], "Run2 flashsim", 'l')
c2.GetPad(0).Update()
stats1 = histos['signal_flash']['jet2_softdrop_mass'].GetListOfFunctions().FindObject("stats").Clone("stats1")
stats1.SetY1NDC(.4)
stats1.SetY2NDC(.53)
stats1.SetX2NDC(0.9)
stats1.SetX1NDC(0.73)

c2.GetPad(0).Update()

histos['signal_full']['jet2_softdrop_mass'].Draw("HIST")
histos['signal_full']['jet2_softdrop_mass'].SetLineWidth(2)
histos['signal_full']['jet2_softdrop_mass'].SetLineColor(ROOT.kTeal -6)
legend.AddEntry(histos['signal_full']['jet2_softdrop_mass'], "Run2 fullsim", 'l')
c2.GetPad(0).Update()
stats3 = histos['signal_full']['jet2_softdrop_mass'].GetListOfFunctions().FindObject("stats").Clone("stats3")
stats3.SetY1NDC(.58)
stats3.SetY2NDC(.71)
stats3.SetX2NDC(0.9)
stats3.SetX1NDC(0.73)

c2.GetPad(0).Update()



histos['signal_ph2']['jet2_softdrop_mass'].Draw("HIST")
histos['signal_ph2']['jet2_softdrop_mass'].SetTitle("Softdrop mass for Jet2, no mass window, no discriminator cut, no pt window; Softdrop mass (Not calibrated); Events")

histos['signal_ph2']['jet2_softdrop_mass'].SetLineWidth(2)
histos['signal_ph2']['jet2_softdrop_mass'].SetLineColor(ROOT.kBlue +2)

legend.AddEntry(histos['signal_ph2']['jet2_softdrop_mass'], "Phase2 fullsim", 'l')
c2.GetPad(0).Update()
stats2 = histos['signal_ph2']['jet2_softdrop_mass'].GetListOfFunctions().FindObject("stats")
stats2.SetX2NDC(0.9)
stats2.SetX1NDC(0.73)
stats2.SetY2NDC(0.89)
stats2.SetY1NDC(0.76)



c2.GetPad(0).Update()
histos['signal_flash']['jet2_softdrop_mass'].Draw("SAME HIST")
histos['signal_flash']['jet2_softdrop_mass'].Scale(1/(histos['signal_flash']['jet2_softdrop_mass'].Integral()))
histos['signal_ph2']['jet2_softdrop_mass'].Scale(1/(histos['signal_ph2']['jet2_softdrop_mass'].Integral()))

histos['signal_full']['jet2_softdrop_mass'].Draw("SAME HIST")
histos['signal_full']['jet2_softdrop_mass'].Scale(1/(histos['signal_full']['jet2_softdrop_mass'].Integral()))



c2.GetPad(0).Update()

stats1.Draw()
stats2.Draw()
stats3.Draw()
legend.Draw()


c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/softdrop_study/jet1_softdrop_no_pt_window_no_mass_window_no_discr_cut.pdf")
c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/softdrop_study/jet2_softdrop_no_pt_window_no_mass_window_no_discr_cut.pdf")



