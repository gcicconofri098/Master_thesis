import ROOT
import os


module_path_1 = os.path.join(os.path.dirname(__file__), "utils.h")
module_path_2 = os.path.join(os.path.dirname(__file__), "fatjets_utils.h")
module_path_3 = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_calibration.h")


ROOT.gInterpreter.ProcessLine(f'#include "{module_path_1}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_2}"')
ROOT.gInterpreter.ProcessLine(f'#include "{module_path_3}"')


ROOT.gStyle.SetOptStat(0)

ROOT.EnableImplicitMT(10)


files = {
    "QCD6_full": "/scratchnvme/cicco/QCD6/",
    "QCD7_full": "/scratchnvme/cicco/QCD7/",
    "QCD8_full": "/scratchnvme/cicco/QCD8/" ,   
    "QCD6_flash": "/scratchnvme/cicco/QCD6_good_flash/",
    "QCD7_flash": "/scratchnvme/cicco/QCD7_good_flash/",
    "QCD8_flash": "/scratchnvme/cicco/QCD8_good_flash/",
}

integrated_luminosity = 59830

weights =  {
    "QCD6": 1207 * integrated_luminosity,
    "QCD7": 119.9 * integrated_luminosity,
    "QCD8": 25.24 * integrated_luminosity,
}

n_events = {
    "QCD6": 15230975,
    "QCD7": 11887406,
    "QCD8": 5710430,
}


entries1 = {}
events = {}
events_chain = {}
full_chain = {}
df = {}
histos = {}
histos_1d = {}
dataset_events = {}

processes = list(files.keys())

histo_gen_pt = {}

histo_pt_ratio = {}

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

        df[i] = (df[i]
        .Define("matching_index" , "lepton_matching_index(FatJet_eta, FatJet_phi, GenJetAK8_eta, GenJetAK8_phi)")
        .Define("Post_calibration_pt", "calibrate_pt_double_n_bins(FatJet_eta, FatJet_pt)")
        .Define("Matched_gen_pt", "Take(GenJetAK8_pt, matching_index)")
        .Define("Ratio_RecoGen", "Post_calibration_pt/Matched_gen_pt")
        .Define("Abs_eta", "abs(FatJet_eta)")

        )

        #histos[i] = df[i].Histo1D((str(i), str(i), 100, 0, 1000), "Post_calibration_pt").GetValue()
        histo_gen_pt[i] = df[i].Histo1D((str(i), str(i), 100, -100, 2500), "Matched_gen_pt").GetValue()
        histo_pt_ratio[i] = df[i].Histo1D((str(i), str(i), 60, -0.5, 4), "Ratio_RecoGen").GetValue()

    elif str(i) == "QCD6_full" or str(i) == 'QCD7_full' or str(i) == 'QCD8_full':

        df[i] = ROOT.RDataFrame("Events", entries1[i])
        
        df[i] = (df[i]
        .Define("Matched_gen_pt", "Take(GenJetAK8_pt, FatJet_genJetAK8Idx)")
        .Define("Ratio_RecoGen", "FatJet_pt/Matched_gen_pt")
        )

        histo_gen_pt[i] = df[i].Histo1D((str(i), str(i), 100, -100, 2500), "Matched_gen_pt").GetValue()
        histo_pt_ratio[i] = df[i].Histo1D((str(i), str(i), 60, -0.5, 4), "Ratio_RecoGen").GetValue()



for key_full in processes:
    key_nofull=key_full.split("_")[0]

    print(f"weight for dataset {key_full} is: {weights[key_nofull]*2.27/n_events[key_nofull]}")

    histo_gen_pt[key_full].Scale(weights[key_nofull]*2.27/n_events[key_nofull])
    histo_pt_ratio[key_full].Scale(weights[key_nofull]*2.27/n_events[key_nofull])



QCD_6_7_8_flash = histo_gen_pt['QCD6_flash'].Clone()
QCD_6_7_8_flash.Add(histo_gen_pt['QCD7_flash'])
QCD_6_7_8_flash.Add(histo_gen_pt['QCD8_flash'])

QCD_7_8_flash = histo_gen_pt['QCD7_flash'].Clone()
QCD_7_8_flash.Add(histo_gen_pt['QCD8_flash'])

QCD_8_flash = histo_gen_pt['QCD8_flash'].Clone()


c1 = ROOT.TCanvas('c1', "stacked flashsim QCD", 4500, 3500)

legend = ROOT.TLegend(0.62,0.72, 0.9,0.9)

QCD_6_7_8_flash.Draw("HIST")
QCD_6_7_8_flash.SetFillColorAlpha(ROOT.kCyan - 10, 0.5)
QCD_6_7_8_flash.SetTitle("high HT QCD stacked for flashsim ")

#QCD_6_7_8_flash.Scale(1/QCD_6_7_8_flash.Integral())
legend.AddEntry(QCD_6_7_8_flash, "QCD 6", 'f')
QCD_6_7_8_flash.SetMinimum(10e3)

QCD_7_8_flash.Draw("SAME HIST")
QCD_7_8_flash.SetFillColorAlpha(ROOT.kRed -6, 0.5)
legend.AddEntry(QCD_7_8_flash, "QCD 7", 'f')
#QCD_7_8_flash.Scale(1/QCD_7_8_flash.Integral())

QCD_8_flash.Draw("SAME HIST")
QCD_8_flash.SetFillColorAlpha(ROOT.kTeal +6, 0.5)
legend.AddEntry(QCD_8_flash, "QCD 8", 'f')
#QCD_8_flash.Scale(1/QCD_8_flash.Integral())

legend.Draw()
c1.SetLogy(1)

c2 = ROOT.TCanvas("c2", "Not stacked QCD", 5000, 3000)

legend2 = ROOT.TLegend(0.62, 0.72, 0.9, 0.9)

c2.Divide(3,2)

c2.cd(1)
ROOT.gPad.SetLogy()

histo_gen_pt["QCD6_flash"].Draw("HIST")
histo_gen_pt["QCD6_flash"].SetTitle("QCD 6")
histo_gen_pt["QCD6_flash"].SetLineWidth(2)
histo_gen_pt['QCD6_flash'].SetLineColor(ROOT.kAzure +2)

legend2.AddEntry(histo_gen_pt["QCD6_flash"], "Run2 flashsim", 'l')

histo_gen_pt["QCD6_full"].Draw("SAME HIST")
histo_gen_pt["QCD6_full"].SetLineWidth(2)
histo_gen_pt['QCD6_full'].SetLineColor(ROOT.kTeal -6)
#histo_gen_pt['QCD6_full'].SetLineStyle(10)
legend2.AddEntry(histo_gen_pt["QCD6_full"], 'Run2 fullsim', 'l')

legend2.Draw()

c2.cd(2)
ROOT.gPad.SetLogy()

histo_gen_pt["QCD7_flash"].Draw("HIST")
histo_gen_pt["QCD7_flash"].SetTitle("QCD 7")
histo_gen_pt["QCD7_flash"].SetLineWidth(2)
histo_gen_pt['QCD7_flash'].SetLineColor(ROOT.kAzure +2)

histo_gen_pt["QCD7_full"].Draw("SAME HIST")
histo_gen_pt["QCD7_full"].SetLineWidth(2)
histo_gen_pt['QCD7_full'].SetLineColor(ROOT.kTeal -6)
#histo_gen_pt['QCD7_full'].SetLineStyle(10)


legend2.Draw()

c2.cd(3)
ROOT.gPad.SetLogy()

histo_gen_pt["QCD8_flash"].Draw("HIST")
histo_gen_pt["QCD8_flash"].SetTitle("QCD 8")
histo_gen_pt["QCD8_flash"].SetLineWidth(2)
histo_gen_pt['QCD8_flash'].SetLineColor(ROOT.kAzure +2)


histo_gen_pt["QCD8_full"].Draw("SAME HIST")
histo_gen_pt["QCD8_full"].SetLineWidth(2)
histo_gen_pt['QCD8_full'].SetLineColor(ROOT.kTeal -6)
#histo_gen_pt['QCD8_full'].SetLineStyle(10)

legend2.Draw()

c2.cd(4)

ROOT.gPad.SetLogy()

histo_pt_ratio["QCD6_flash"].Draw("HIST")
histo_pt_ratio["QCD6_flash"].SetTitle("QCD 6")
histo_pt_ratio["QCD6_flash"].SetLineWidth(2)
histo_pt_ratio['QCD6_flash'].SetLineColor(ROOT.kAzure +2)


histo_pt_ratio["QCD6_full"].Draw("SAME HIST")
histo_pt_ratio['QCD6_full'].SetLineColor(ROOT.kTeal -6)
histo_pt_ratio["QCD6_full"].SetLineWidth(2)
#histo_pt_ratio["QCD6_full"].SetLineStyle(10)

legend2.Draw()

c2.cd(5)
ROOT.gPad.SetLogy()

histo_pt_ratio["QCD7_flash"].Draw("HIST")
histo_pt_ratio["QCD7_flash"].SetTitle("QCD 7")
histo_pt_ratio["QCD7_flash"].SetLineWidth(2)
histo_pt_ratio['QCD7_flash'].SetLineColor(ROOT.kAzure +2)


histo_pt_ratio["QCD7_full"].Draw("SAME HIST")
histo_pt_ratio['QCD7_full'].SetLineColor(ROOT.kTeal -6)
histo_pt_ratio["QCD7_full"].SetLineWidth(2)
#histo_pt_ratio["QCD7_full"].SetLineStyle(10)

legend2.Draw()

c2.cd(6)
ROOT.gPad.SetLogy()

histo_pt_ratio["QCD8_flash"].Draw("HIST")
histo_pt_ratio["QCD8_flash"].SetTitle("QCD 8")
histo_pt_ratio["QCD8_flash"].SetLineWidth(2)
histo_pt_ratio['QCD8_flash'].SetLineColor(ROOT.kAzure +2)

histo_pt_ratio["QCD8_full"].Draw("SAME HIST")
histo_pt_ratio['QCD8_full'].SetLineColor(ROOT.kTeal -6)
histo_pt_ratio["QCD8_full"].SetLineWidth(2)
#histo_pt_ratio["QCD8_full"].SetLineStyle(10)

legend2.Draw()

#! STACKED FULLSIM 

QCD_6_7_8_full = histo_gen_pt['QCD6_full'].Clone()
QCD_6_7_8_full.Add(histo_gen_pt['QCD7_full'])
QCD_6_7_8_full.Add(histo_gen_pt['QCD8_full'])

QCD_7_8_full = histo_gen_pt['QCD7_full'].Clone()
QCD_7_8_full.Add(histo_gen_pt['QCD8_full'])

QCD_8_full = histo_gen_pt['QCD8_full'].Clone()


c3 = ROOT.TCanvas('c3', "stacked fullsim QCD", 4500, 3500)

legend = ROOT.TLegend(0.62,0.72, 0.9,0.9)

QCD_6_7_8_full.Draw("HIST")
QCD_6_7_8_full.SetFillColorAlpha(ROOT.kCyan - 10, 0.5)
QCD_6_7_8_full.SetTitle("high HT QCD stacked for fullsim ")
#QCD_6_7_8_full.Scale(1/QCD_6_7_8_full.Integral())
legend.AddEntry(QCD_6_7_8_full, "QCD 6", 'f')
QCD_6_7_8_full.SetMinimum(10e3)

QCD_7_8_full.Draw("SAME HIST")
QCD_7_8_full.SetFillColorAlpha(ROOT.kRed -6, 0.5)
legend.AddEntry(QCD_7_8_full, "QCD 7", 'f')
#QCD_7_8_full.Scale(1/QCD_7_8_full.Integral())

QCD_8_full.Draw("SAME HIST")
QCD_8_full.SetFillColorAlpha(ROOT.kTeal +6, 0.5)
legend.AddEntry(QCD_8_full, "QCD 8", 'f')
#QCD_8_full.Scale(1/QCD_8_full.Integral())

legend.Draw()
c3.SetLogy(1)



c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/calibration/matched_gen_pt_stacking_flash.pdf")
c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/calibration/matched_gen_pt_stacking_full.pdf")

c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/calibration/matched_gen_pt_divided.pdf")

