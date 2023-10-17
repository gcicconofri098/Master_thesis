import ROOT
import os

module_path = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils.h")
module_path2 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/nb.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_calibration.h")


ROOT.gStyle.SetOptStat(0)


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

histos = {}

for i in processes:
    if str(i) == 'signal_flash':
        df[i] = (df[i]
            .Define("matching_index" , "lepton_matching_index(FatJet_eta, FatJet_phi, GenJetAK8_eta, GenJetAK8_phi)")
            .Define("Matched_gen_pt", "Take(GenJetAK8_pt, matching_index)")
            .Define("Post_calibration_pt", "calibrate_pt_double_n_bins(FatJet_eta, FatJet_pt)")
        )

        df[i] = (df[i]
                 .Define("RECO_subleading", "Post_calibration_pt[1]")
                 .Define("GEN_subleading", "Matched_gen_pt[1]")
                 .Define("RECO_pt_subleading_GEN", "Post_calibration_pt[matching_index==1]")
                 .Define("sub_leading_RECO_idx", "matching_index ==1")
                 .Define("GEN_pt_subleading_RECO", "Take(Matched_gen_pt, sub_leading_RECO_idx)")
        )
        histos[i] = {}

        histos[i]['RECO_subleading_GEN'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "RECO_pt_subleading_GEN")
        histos[i]['GEN_subleading_RECO'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "GEN_pt_subleading_RECO")
        histos[i]['RECO_subleading_RECO'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "RECO_subleading")
        histos[i]['GEN_subleading_GEN'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "GEN_subleading")

        

        
    
    if str(i) == 'signal_full':

        df[i] = df[i].Filter("FatJet_pt.size()>=2 && GenJetAK8_pt[0]>250 && GenJetAK8_pt[1]>250")

        df[i] = (df[i]
            .Define("Matched_gen_pt", "Take(GenJetAK8_pt, FatJet_genJetAK8Idx)")
        )

        df[i] = (df[i]
                 .Define("RECO_subleading", "FatJet_pt[1]")
                 .Define("GEN_subleading", "Matched_gen_pt[1]")
                 .Define("RECO_pt_subleading_GEN", "Post_calibration[FatJet_genJetAK8Idx==1]")
                 .Define("sub_leading_RECO_idx", "FatJet_genJetAK8Idx ==1")
                 .Define("GEN_pt_subleading_RECO", "Take(Matched_gen_pt, sub_leading_RECO_idx)")
        )

        histos[i]['RECO_subleading_GEN'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "RECO_pt_subleading_GEN")
        histos[i]['GEN_subleading_RECO'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "GEN_pt_subleading_RECO")
        histos[i]['RECO_subleading_RECO'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "RECO_subleading")
        histos[i]['GEN_subleading_GEN'] = df[i].Histo1D((str(i), str(i), 100, 0, 2000), "GEN_subleading")


c1 = ROOT.TCanvas("c1", "RECO_subleading_GEN", 4500, 3500)

c1.SetLogy()

legend1 = ROOT.TLegend(0.62, 0.72, 0.9, 0.9)

histos['signal_full']['RECO_subleading_GEN'].Draw("HIST")
histos['signal_full']['RECO_subleading_GEN'].SetLineWidth(2)
histos['signal_full']['RECO_subleading_GEN'].SetTitle("RECO distribution for pt-subleading GEN jet; Pt; Events")
histos['signal_full']['RECO_subleading_GEN'].SetLineColor(ROOT.kTeal -6)
legend1.AddEntry(histos['signal_full']['RECO_subleading_GEN'], "Run2 fullsim", 'l')

histos['signal_flash']['RECO_subleading_GEN'].Draw("HIST SAME")
histos['signal_flash']['RECO_subleading_GEN'].SetLineWidth(2)
histos['signal_flash']['RECO_subleading_GEN'].SetLineColor(ROOT.kRed +2)
legend1.AddEntry(histos['signal_flash']['RECO_subleading_GEN'], "Run2 flashsim", 'l')

legend1.Draw()



c2 = ROOT.TCanvas("c2", "GEN_subleading_RECO", 4500, 3500)

c2.SetLogy()

legend2 = ROOT.TLegend(0.62, 0.72, 0.9, 0.9)

histos['signal_full']['GEN_subleading_RECO'].Draw("HIST")
histos['signal_full']['GEN_subleading_RECO'].SetLineWidth(2)
histos['signal_full']['GEN_subleading_RECO'].SetTitle("GEN distribution for pt-subleading RECO jet; Pt; Events")
histos['signal_full']['GEN_subleading_RECO'].SetLineColor(ROOT.kTeal -6)
legend2.AddEntry(histos['signal_full']['GEN_subleading_RECO'], "Run2 fullsim", 'l')

histos['signal_flash']['GEN_subleading_RECO'].Draw("HIST SAME")
histos['signal_flash']['GEN_subleading_RECO'].SetLineWidth(2)
histos['signal_flash']['GEN_subleading_RECO'].SetLineColor(ROOT.kRed +2)
legend2.AddEntry(histos['signal_flash']['GEN_subleading_RECO'], "Run2 flashsim", 'l')

legend2.Draw()


c3 = ROOT.TCanvas("c3", "RECO_subleading_RECO", 4500, 3500)

c3.SetLogy()

legend3 = ROOT.TLegend(0.62, 0.72, 0.9, 0.9)

histos['signal_full']['RECO_subleading_RECO'].Draw("HIST")
histos['signal_full']['RECO_subleading_RECO'].SetLineWidth(2)
histos['signal_full']['RECO_subleading_RECO'].SetTitle("RECO distribution for pt-subleading RECO jet; Pt; Events")
histos['signal_full']['RECO_subleading_RECO'].SetLineColor(ROOT.kTeal -6)
legend3.AddEntry(histos['signal_full']['RECO_subleading_RECO'], "Run2 fullsim", 'l')

histos['signal_flash']['RECO_subleading_RECO'].Draw("HIST SAME")
histos['signal_flash']['RECO_subleading_RECO'].SetLineWidth(2)
histos['signal_flash']['RECO_subleading_RECO'].SetLineColor(ROOT.kRed +2)
legend3.AddEntry(histos['signal_flash']['RECO_subleading_RECO'], "Run2 flashsim", 'l')

legend3.Draw()





c4 = ROOT.TCanvas("c4", "GEN_subleading_GEN", 4500, 3500)

c4.SetLogy()

legend4 = ROOT.TLegend(0.62, 0.72, 0.9, 0.9)

histos['signal_full']['GEN_subleading_GEN'].Draw("HIST")
histos['signal_full']['GEN_subleading_GEN'].SetLineWidth(2)
histos['signal_full']['GEN_subleading_GEN'].SetTitle("GEN distribution for pt-subleading GEN jet; Pt; Events")
histos['signal_full']['GEN_subleading_GEN'].SetLineColor(ROOT.kTeal -6)
legend4.AddEntry(histos['signal_full']['GEN_subleading_GEN'], "Run2 fullsim", 'l')

histos['signal_flash']['GEN_subleading_GEN'].Draw("HIST SAME")
histos['signal_flash']['GEN_subleading_GEN'].SetLineWidth(2)
histos['signal_flash']['GEN_subleading_GEN'].SetLineColor(ROOT.kRed +2)
legend4.AddEntry(histos['signal_flash']['GEN_subleading_GEN'], "Run2 flashsim", 'l')

legend4.Draw()


c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/gen_comparisons/crossed_distr_subleading_jet/RECO_subleading_GEN.pdf")
c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/gen_comparisons/crossed_distr_subleading_jet/GEN_subleading_RECO.pdf")
c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/gen_comparisons/crossed_distr_subleading_jet/RECO_subleading_RECO.pdf")
c4.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/gen_comparisons/crossed_distr_subleading_jet/GEN_subleading_GEN.pdf")
