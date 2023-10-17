import ROOT
import os

module_path_1 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils.h")
module_path_2 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/fatjets_utils.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_calibration.h")


ROOT.gInterpreter.ProcessLine(f'#include "{module_path_1}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_2}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')


ROOT.gStyle.SetOptStat(0)

ROOT.EnableImplicitMT()
df ={}
events = {}
entries1 ={}
files = {

    "signal_full": "/scratchnvme/cicco/signal_RunIISummer20UL16/",
    "signal_flash": "/scratchnvme/cicco/signal_RunIISummer20UL16_flash/",
    "signal_ph2": "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file1.root"
}

processes = list(files.keys())

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

print("created all the dataframes")

histos = {}

for i in processes:
    if str(i)== 'signal_full':

        df[i] = df[i].Filter("GenJetAK8_pt[0]>250 && GenJetAK8_pt[1]>250")

        df[i] = df[i].Define("Matched_gen_pt", "Take(GenJetAK8_pt, FatJet_genJetAK8Idx)").Define("pt_ratio", "FatJet_pt/Matched_gen_pt")


        histos[i] = {}

        histos[i]['GEN_pt'] = df[i].Histo1D((str(i), str(i), 200, 0, 3000), "Matched_gen_pt").GetValue()
        
        histos[i]['RECO_pt'] = df[i].Histo1D((str(i), str(i), 200, 0, 3000), "FatJet_pt").GetValue()

        histos[i]['pt_ratio'] = df[i].Histo1D((str(i), str(i), 40, -0.5, 2.5), "pt_ratio").GetValue()


    elif str(i)== 'signal_flash':

        df[i] = (df[i]
        .Define("matching_index" , "lepton_matching_index(FatJet_eta, FatJet_phi, GenJetAK8_eta, GenJetAK8_phi)")
        .Define("Post_calibration_pt", "calibrate_pt_double_n_bins(FatJet_eta, FatJet_pt)")
        .Define("Matched_gen_pt", "Take(GenJetAK8_pt, matching_index)")
        .Define("pt_ratio", "Post_calibration_pt/Matched_gen_pt")
        )
        histos[i] = {}

        histos[i]['GEN_pt'] = df[i].Histo1D((str(i), str(i), 200, 0, 3000), "Matched_gen_pt").GetValue()
        
        histos[i]['RECO_pt'] = df[i].Histo1D((str(i), str(i), 200, 0, 3000), "Post_calibration_pt").GetValue()

        histos[i]['pt_ratio'] = df[i].Histo1D((str(i), str(i), 40, -0.5, 2.5), "pt_ratio").GetValue()

    else:
        df[i] = (df[i]
            .Define("Post_calibration_pt", "calibrate_pt_double_n_bins(Mfatjet_eta, Mfatjet_pt)")    
            .Define("pt_ratio", "Post_calibration_pt/MgenjetAK8_pt")
        )
        histos[i] = {}

        histos[i]['GEN_pt'] = df[i].Histo1D((str(i), str(i), 200, 0, 3000), "MgenjetAK8_pt").GetValue()
        
        histos[i]['RECO_pt'] = df[i].Histo1D((str(i), str(i), 200, 0, 3000), "Post_calibration_pt").GetValue()

        histos[i]['pt_ratio'] = df[i].Histo1D((str(i), str(i), 40, -0.5, 2.5), "pt_ratio").GetValue()
        

c1 = ROOT.TCanvas("c1", "GEN pt distributions")
c1.SetLogy()

legend1 = ROOT.TLegend(0.62, 0.72, 0.9, 0.9)

histos['signal_full']['GEN_pt'].Draw("HIST")
histos['signal_full']['GEN_pt'].SetTitle("GEN distribution for signal; Pt; Events")
histos["signal_full"]['GEN_pt'].SetLineWidth(2)
histos["signal_full"]["GEN_pt"].SetLineColor(ROOT.kTeal -6)

legend1.AddEntry(histos["signal_full"]["GEN_pt"], "Run2 fullsim", 'l')

histos['signal_flash']['GEN_pt'].Draw("SAME HIST")
histos["signal_flash"]['GEN_pt'].SetLineWidth(2)
histos["signal_flash"]["GEN_pt"].SetLineColor(ROOT.kRed +2 )

legend1.AddEntry(histos["signal_flash"]["GEN_pt"], "Run2 flashsim", 'l')

histos['signal_ph2']['GEN_pt'].Draw("SAME HIST")
histos["signal_ph2"]['GEN_pt'].SetLineWidth(2)
histos["signal_ph2"]["GEN_pt"].SetLineColor(ROOT.kBlue +2 )

legend1.AddEntry(histos["signal_ph2"]["GEN_pt"], "Phase2 fullsim", 'l')

legend1.Draw()



c2 = ROOT.TCanvas("c2", "RECO pt distributions")
c2.SetLogy()

legend2 = ROOT.TLegend(0.62, 0.72, 0.9, 0.9)

histos['signal_full']['RECO_pt'].Draw("HIST")
histos['signal_full']['RECO_pt'].SetTitle("RECO distribution for signal; Pt; Events")
histos["signal_full"]['RECO_pt'].SetLineWidth(2)
histos["signal_full"]["RECO_pt"].SetLineColor(ROOT.kTeal -6)

legend2.AddEntry(histos["signal_full"]["RECO_pt"], "Run2 fullsim", 'l')


histos['signal_flash']['RECO_pt'].Draw("SAME HIST")
histos["signal_flash"]['RECO_pt'].SetLineWidth(2)
histos["signal_flash"]["RECO_pt"].SetLineColor(ROOT.kRed +2 )

legend2.AddEntry(histos["signal_flash"]["RECO_pt"], "Run2 flashsim", 'l')


histos['signal_ph2']['RECO_pt'].Draw("SAME HIST")
histos["signal_ph2"]['RECO_pt'].SetLineWidth(2)
histos["signal_ph2"]["RECO_pt"].SetLineColor(ROOT.kBlue +2 )

legend2.AddEntry(histos["signal_ph2"]["RECO_pt"], "Phase2 fullsim", 'l')

legend2.Draw()



c3 = ROOT.TCanvas("c3", "RECO pt distributions")
c3.SetLogy()

legend3 = ROOT.TLegend(0.62, 0.72, 0.9, 0.9)

histos['signal_full']['pt_ratio'].Draw("HIST")
histos['signal_full']['pt_ratio'].SetTitle("pt ratio for signal; RECO/GEN pt; Events")
histos["signal_full"]['pt_ratio'].SetLineWidth(2)
histos["signal_full"]["pt_ratio"].SetLineColor(ROOT.kTeal -6)

legend3.AddEntry(histos["signal_full"]["pt_ratio"], "Run2 fullsim", 'l')

histos['signal_flash']['pt_ratio'].Draw("SAME HIST")
histos["signal_flash"]['pt_ratio'].SetLineWidth(2)
histos["signal_flash"]["pt_ratio"].SetLineColor(ROOT.kRed +2 )

legend3.AddEntry(histos["signal_flash"]["pt_ratio"], "Run2 flashsim", 'l')

histos['signal_ph2']['pt_ratio'].Draw("SAME HIST")
histos["signal_ph2"]['pt_ratio'].SetLineWidth(2)
histos["signal_ph2"]["pt_ratio"].SetLineColor(ROOT.kBlue +2 )

legend3.AddEntry(histos["signal_ph2"]["pt_ratio"], "Phase2 fullsim", 'l')

legend3.Draw()

c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/gen_comparisons/GEN_distr_GEN_sel.pdf")
c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/gen_comparisons/RECO_distr_GEN_sel.pdf")
c3.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/gen_comparisons/pt_ratio_GEN_sel.pdf")
