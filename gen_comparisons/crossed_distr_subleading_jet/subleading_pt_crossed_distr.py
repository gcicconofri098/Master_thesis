import ROOT
import os

module_path = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils.h")
module_path2 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/nb.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_calibration.h")


ROOT.gStyle.SetOptStat(1111)

ROOT.EnableImplicitMT()


ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path2}"')

files = {
    "signal_full": "/scratchnvme/cicco/signal_RunIISummer20UL16/",
    "signal_flash": "/scratchnvme/cicco/signal_RunIISummer20UL16_flash/",
}

processes = list(files.keys())

entries1 = {}
events = {}
df = {}

for i in processes:
    if str(i)!= 'signal_ph2':
        f = os.listdir(files.get(i))
        num = len(f)
        entries1[i] = []
        events[i] = []

        for j in range(0, num):
            entries1[i].append(str(files.get(i)) + str(f[j]))

        df[i] = ROOT.RDataFrame("Events", entries1[i])
        print("added file to: {}".format(i))
    else:
        df[i]= ROOT.RDataFrame("MJets", str(files[i]))

print("created the dataframes")

print(processes)

histos = {}

for i in processes:
    if str(i) == 'signal_flash':
        df[i] = (df[i]
            .Define("matching_index" , "lepton_matching_index(FatJet_eta, FatJet_phi, GenJetAK8_eta, GenJetAK8_phi)")
            .Define("Matched_gen_pt", "Take(GenJetAK8_pt, matching_index)")
            .Define("Post_calibration_pt", "calibrate_pt_double_n_bins(FatJet_eta, FatJet_pt)")

        )

        df[i] = (df[i]
                 .Define("RECO_leading_RECO", "Post_calibration_pt[0]")
                 .Define("RECO_subleading_RECO", "Post_calibration_pt[1]")
                 .Define("GEN_subleading_GEN", "Matched_gen_pt[1]")
                 .Define("RECO_pt_subleading_GEN", "Post_calibration_pt[matching_index==1]")
                 .Define("sub_leading_RECO_idx", "matching_index ==1")
                 .Define("GEN_pt_subleading_RECO", "Take(Matched_gen_pt, sub_leading_RECO_idx)")
        )
        histos[i] = {}

        histos[i]['RECO_subleading_GEN'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "RECO_pt_subleading_GEN").GetValue()
        histos[i]['GEN_subleading_RECO'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "GEN_pt_subleading_RECO").GetValue()
        histos[i]['RECO_subleading_RECO'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "RECO_subleading_RECO").GetValue()
        histos[i]['GEN_subleading_GEN'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "GEN_subleading_GEN").GetValue()

        df[i] = df[i].Filter("RECO_leading_RECO<300")

        histos[i]['Problematic_RECO'] = df[i].Histo1D((str(i), str(i), 40, 0, 450), "RECO_leading_RECO").GetValue()
    
    elif str(i) == 'signal_full':

        df[i] = df[i].Filter("FatJet_pt.size()>=2 && GenJetAK8_pt[0]>250 && GenJetAK8_pt[1]>250")

        df[i] = (df[i]
            .Define("Matched_gen_pt", "Take(GenJetAK8_pt, FatJet_genJetAK8Idx)")
        )


        df[i] = (df[i]
                 .Define("RECO_leading_RECO", "FatJet_pt[0]")
                 .Define("RECO_subleading_RECO", "FatJet_pt[1]")
                 .Define("GEN_subleading_GEN", "Matched_gen_pt[1]")
                 .Define("RECO_pt_subleading_GEN", "FatJet_pt[FatJet_genJetAK8Idx==1]")
                 .Define("sub_leading_RECO_idx", "FatJet_genJetAK8Idx ==1")
                 .Define("GEN_pt_subleading_RECO", "Take(Matched_gen_pt, sub_leading_RECO_idx)")
        )

        histos[i] = {}

        histos[i]['RECO_subleading_GEN'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "RECO_pt_subleading_GEN").GetValue()
        histos[i]['GEN_subleading_RECO'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "GEN_pt_subleading_RECO").GetValue()
        histos[i]['RECO_subleading_RECO'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "RECO_subleading_RECO").GetValue()
        histos[i]['GEN_subleading_GEN'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "GEN_subleading_GEN").GetValue()

        df[i] = df[i].Filter("RECO_leading_RECO<300")

        histos[i]['Problematic_RECO'] = df[i].Histo1D((str(i), str(i), 40, 0, 450), "RECO_leading_RECO").GetValue()


c1 = ROOT.TCanvas("c1", "RECO_subleading_GEN", 4500, 3500)

c1.SetLogy()

legend1 = ROOT.TLegend(0.62, 0.32, 0.9, 0.2)

histos['signal_full']['RECO_subleading_GEN'].Draw("HIST")
histos['signal_full']['RECO_subleading_GEN'].SetLineWidth(2)
histos['signal_full']['RECO_subleading_GEN'].SetTitle("RECO distribution for pt-subleading GEN jet; Pt; Events")
histos['signal_full']['RECO_subleading_GEN'].SetLineColor(ROOT.kTeal -6)
legend1.AddEntry(histos['signal_full']['RECO_subleading_GEN'], "Run2 fullsim", 'l')
c1.GetPad(0).Update()
stats1 = histos['signal_full']['RECO_subleading_GEN'].GetListOfFunctions().FindObject("stats").Clone("stats1")
stats1.SetY1NDC(.55)
stats1.SetY2NDC(.7)
c1.GetPad(0).Update()


histos['signal_flash']['RECO_subleading_GEN'].Draw("HIST")
histos['signal_flash']['RECO_subleading_GEN'].SetLineWidth(2)
histos['signal_flash']['RECO_subleading_GEN'].SetLineColor(ROOT.kRed +2)
legend1.AddEntry(histos['signal_flash']['RECO_subleading_GEN'], "Run2 flashsim", 'l')
c1.GetPad(0).Update()
stats2 = histos['signal_flash']['RECO_subleading_GEN'].GetListOfFunctions().FindObject("stats").Clone("stats2")
c1.GetPad(0).Update()
histos['signal_full']['RECO_subleading_GEN'].Draw("SAME HIST")
stats1.Draw()
stats2.Draw()


legend1.Draw()



c2 = ROOT.TCanvas("c2", "GEN_subleading_RECO", 4500, 3500)

c2.SetLogy()

legend2 = ROOT.TLegend(0.62, 0.32, 0.9, 0.2)

histos['signal_full']['GEN_subleading_RECO'].Draw("HIST")
histos['signal_full']['GEN_subleading_RECO'].SetLineWidth(2)
histos['signal_full']['GEN_subleading_RECO'].SetTitle("GEN distribution for pt-subleading RECO jet; Pt; Events")
histos['signal_full']['GEN_subleading_RECO'].SetLineColor(ROOT.kTeal -6)
legend2.AddEntry(histos['signal_full']['GEN_subleading_RECO'], "Run2 fullsim", 'l')
c2.GetPad(0).Update()
stats1 = histos['signal_full']['GEN_subleading_RECO'].GetListOfFunctions().FindObject("stats").Clone("stats1")
stats1.SetY1NDC(.55)
stats1.SetY2NDC(.7)
c2.GetPad(0).Update()

histos['signal_flash']['GEN_subleading_RECO'].Draw("HIST")
histos['signal_flash']['GEN_subleading_RECO'].SetLineWidth(2)
histos['signal_flash']['GEN_subleading_RECO'].SetLineColor(ROOT.kRed +2)
legend2.AddEntry(histos['signal_flash']['GEN_subleading_RECO'], "Run2 flashsim", 'l')

c2.GetPad(0).Update()
stats2 = histos['signal_flash']['GEN_subleading_RECO'].GetListOfFunctions().FindObject("stats").Clone("stats2")
c2.GetPad(0).Update()
histos['signal_full']['GEN_subleading_RECO'].Draw("SAME HIST")
stats1.Draw()
stats2.Draw()


legend2.Draw()


c3 = ROOT.TCanvas("c3", "RECO_subleading_RECO", 4500, 3500)

c3.SetLogy()

legend3 = ROOT.TLegend(0.62, 0.32, 0.9, 0.2)

histos['signal_full']['RECO_subleading_RECO'].Draw("HIST")
histos['signal_full']['RECO_subleading_RECO'].SetLineWidth(2)
histos['signal_full']['RECO_subleading_RECO'].SetTitle("RECO distribution for pt-subleading RECO jet; Pt; Events")
histos['signal_full']['RECO_subleading_RECO'].SetLineColor(ROOT.kTeal -6)
legend3.AddEntry(histos['signal_full']['RECO_subleading_RECO'], "Run2 fullsim", 'l')

c3.GetPad(0).Update()
stats1 = histos['signal_full']['RECO_subleading_RECO'].GetListOfFunctions().FindObject("stats").Clone("stats1")
stats1.SetY1NDC(.55)
stats1.SetY2NDC(.7)
c3.GetPad(0).Update()

histos['signal_flash']['RECO_subleading_RECO'].Draw("HIST")
histos['signal_flash']['RECO_subleading_RECO'].SetLineWidth(2)
histos['signal_flash']['RECO_subleading_RECO'].SetLineColor(ROOT.kRed +2)
legend3.AddEntry(histos['signal_flash']['RECO_subleading_RECO'], "Run2 flashsim", 'l')

c3.GetPad(0).Update()
stats2 = histos['signal_flash']['RECO_subleading_RECO'].GetListOfFunctions().FindObject("stats").Clone("stats2")
c3.GetPad(0).Update()
histos['signal_full']['RECO_subleading_RECO'].Draw("SAME HIST")
stats1.Draw()
stats2.Draw()


legend3.Draw()





c4 = ROOT.TCanvas("c4", "GEN_subleading_GEN", 4500, 3500)

c4.SetLogy()

legend4 = ROOT.TLegend(0.62, 0.32, 0.9, 0.2)

histos['signal_full']['GEN_subleading_GEN'].Draw("HIST")
histos['signal_full']['GEN_subleading_GEN'].SetLineWidth(2)
histos['signal_full']['GEN_subleading_GEN'].SetTitle("GEN distribution for pt-subleading GEN jet; Pt; Events")
histos['signal_full']['GEN_subleading_GEN'].SetLineColor(ROOT.kTeal -6)
legend4.AddEntry(histos['signal_full']['GEN_subleading_GEN'], "Run2 fullsim", 'l')

c4.GetPad(0).Update()
stats1 = histos['signal_full']['GEN_subleading_GEN'].GetListOfFunctions().FindObject("stats").Clone("stats1")
stats1.SetY1NDC(.55)
stats1.SetY2NDC(.7)
c4.GetPad(0).Update()

histos['signal_flash']['GEN_subleading_GEN'].Draw("HIST")
histos['signal_flash']['GEN_subleading_GEN'].SetLineWidth(2)
histos['signal_flash']['GEN_subleading_GEN'].SetLineColor(ROOT.kRed +2)
legend4.AddEntry(histos['signal_flash']['GEN_subleading_GEN'], "Run2 flashsim", 'l')

c4.GetPad(0).Update()
stats2 = histos['signal_flash']['GEN_subleading_GEN'].GetListOfFunctions().FindObject("stats").Clone("stats2")
c4.GetPad(0).Update()
histos['signal_full']['GEN_subleading_GEN'].Draw("SAME HIST")
stats1.Draw()
stats2.Draw()

legend4.Draw()



c5 = ROOT.TCanvas("c5", "GEN_subleading_GEN", 4500, 3500)

c5.SetLogy()

legend5 = ROOT.TLegend(0.62, 0.32, 0.9, 0.2)

histos['signal_full']['Problematic_RECO'].Draw("HIST")
histos['signal_full']['Problematic_RECO'].SetLineWidth(2)
histos['signal_full']['Problematic_RECO'].SetTitle("RECO distribution for RECO pt-leading jet with pt<300; Pt; Events")
histos['signal_full']['Problematic_RECO'].SetLineColor(ROOT.kTeal -6)
legend5.AddEntry(histos['signal_full']['Problematic_RECO'], "Run2 fullsim", 'l')

c5.GetPad(0).Update()
stats1 = histos['signal_full']['Problematic_RECO'].GetListOfFunctions().FindObject("stats").Clone("stats1")
stats1.SetY1NDC(.55)
stats1.SetY2NDC(.7)
c5.GetPad(0).Update()

histos['signal_flash']['Problematic_RECO'].Draw("HIST")
histos['signal_flash']['Problematic_RECO'].SetLineWidth(2)
histos['signal_flash']['Problematic_RECO'].SetLineColor(ROOT.kRed +2)
legend5.AddEntry(histos['signal_flash']['Problematic_RECO'], "Run2 flashsim", 'l')

c5.GetPad(0).Update()
stats2 = histos['signal_flash']['Problematic_RECO'].GetListOfFunctions().FindObject("stats").Clone("stats2")
c5.GetPad(0).Update()
histos['signal_full']['Problematic_RECO'].Draw("SAME HIST")
stats1.Draw()
stats2.Draw()

legend5.Draw()



c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/gen_comparisons/crossed_distr_subleading_jet/RECO_subleading_GEN.pdf")
c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/gen_comparisons/crossed_distr_subleading_jet/GEN_subleading_RECO.pdf")
c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/gen_comparisons/crossed_distr_subleading_jet/RECO_subleading_RECO.pdf")
c4.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/gen_comparisons/crossed_distr_subleading_jet/GEN_subleading_GEN.pdf")
c5.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/gen_comparisons/crossed_distr_subleading_jet/problematic_pt_distr_leading.pdf")
