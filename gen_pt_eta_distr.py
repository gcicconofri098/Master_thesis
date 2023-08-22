import ROOT
import os

#! ALL FILES ARE OF SIGNAL 

path_VBF_ph2_c2v_2 = (
    "/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file1.root"
)
path_VBF_ph2_c2v_1 = ("/scratchnvme/cicco/CMSSW_11_3_0_pre4/src/TreeMaker/Ntuplzr/test/file.root")

path_VBF_run2_c2v_1 = ("/scratchnvme/cicco/run2_SM_comp_files/")

path_ggH_run2 = ("/scratchnvme/cicco/signal_RunIISummer20UL16/")

files = {
    "ph2_VBF_c2v_2": path_VBF_ph2_c2v_2,
    "ph2_VBF_c2v_1": path_VBF_ph2_c2v_1,
    "run2_VBF" : path_VBF_run2_c2v_1,
    "run2_ggH": path_ggH_run2,
}

entries1 = {}
df = {}
hist_eta = {}

hist_pt = {}


h_eta = {}

h_pt = {}

ROOT.gStyle.SetOptStat(0)


processes = list(files.keys())

for i in processes:
    if str(i) != 'ph2_VBF_c2v_2' and str(i)!= 'ph2_VBF_c2v_1':

        f = os.listdir(files.get(i))
        num = len(f)
        entries1[i] = []

        for j in range(0, num):
            entries1[i].append(str(files.get(i)) + str(f[j]))

        df[i] = ROOT.RDataFrame("Events", entries1[i])

        print("added file to: {}".format(i))
    elif str(i) =='ph2_VBF_c2v_1':

        df[i]= ROOT.RDataFrame("myana/mytree", str(files[i]))

    else:
        df[i]= ROOT.RDataFrame("MJets", str(files[i]))


for i in processes:
    if str(i) != 'ph2_VBF_c2v_2' and str(i)!= 'ph2_VBF_c2v_1':

        df[i] = (df[i]
                .Define("Selection", "GenJetAK8_pt > 300 && GenJetAK8_pt < 500 && abs(GenJetAK8_eta)<2.5")
                .Define("Selected_eta", "GenJetAK8_eta[Selection]")
                .Define("Selected_pt", "GenJetAK8_pt[Selection]")
        )
    
    elif str(i) == 'ph2_VBF_c2v_2':

        df[i] = (df[i]
                .Define("Selection", "MgenjetAK8_pt > 300 && MgenjetAK8_pt < 500 && abs(MgenjetAK8_eta)<2.5")
                .Define("Selected_eta", "MgenjetAK8_eta[Selection]")
                .Define("Selected_pt", "MgenjetAK8_pt[Selection]")
        )

    else:

        df[i] = (df[i]
                .Define("Selection", "genjetAK8_pt > 300 && genjetAK8_pt < 500 && abs(genjetAK8_eta)<2.5")
                .Define("Selected_eta", "genjetAK8_eta[Selection]")
                .Define("Selected_pt", "genjetAK8_pt[Selection]")
        )
    hist_pt[i] = df[i].Histo1D(
        (str(i), str(i) + "; Pt; Events", 80, 300, 500), "Selected_pt"
    )
    
    hist_eta[i] = df[i].Histo1D(
        (str(i), str(i) + "; Eta; Events", 80, -2.5, 2.5), "Selected_eta"
    )

    h_pt[i] = hist_pt[i].GetValue()
    h_eta[i] = hist_eta[i].GetValue()

#! PT

c1 = ROOT.TCanvas("c1", "Flashsim distribution", 800, 700)


legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.86)


h_pt['ph2_VBF_c2v_1'].Draw("HIST")
h_pt['ph2_VBF_c2v_1'].SetTitle("pt distribution for GenJetAK8")
h_pt['ph2_VBF_c2v_1'].SetMaximum(0.5)

h_pt['ph2_VBF_c2v_1'].SetLineWidth(3)
h_pt['ph2_VBF_c2v_1'].SetLineColor(ROOT.kTeal+3)
h_pt['ph2_VBF_c2v_1'].Scale(1/h_pt['ph2_VBF_c2v_1'].Integral())
legend.AddEntry(h_pt['ph2_VBF_c2v_1'], "phase 2, VBF, c_{2v} = 1", "l")



h_pt['ph2_VBF_c2v_2'].Draw("HIST SAME")
h_pt['ph2_VBF_c2v_2'].SetLineWidth(3)
h_pt['ph2_VBF_c2v_2'].SetLineColor(ROOT.kBlue +1)
h_pt['ph2_VBF_c2v_2'].Scale(1/h_pt['ph2_VBF_c2v_2'].Integral())
legend.AddEntry(h_pt['ph2_VBF_c2v_2'], "phase 2, VBF, c_{2v} = 2", "l")


h_pt['run2_VBF'].Draw("HIST SAME")
h_pt['run2_VBF'].SetLineWidth(3)
h_pt['run2_VBF'].SetLineColor(ROOT.kRed +1)
h_pt['run2_VBF'].Scale(1/h_pt['run2_VBF'].Integral())
legend.AddEntry(h_pt['run2_VBF'], "run 2, VBF", "l")


h_pt['run2_ggH'].Draw("HIST SAME")
h_pt['run2_ggH'].SetLineWidth(3)
h_pt['run2_ggH'].SetLineColor(ROOT.kBlack)
h_pt['run2_ggH'].Scale(1/h_pt['run2_ggH'].Integral())
legend.AddEntry(h_pt['run2_ggH'], "run 2, ggH", "l")

legend.Draw()

#! ETA

c2 = ROOT.TCanvas("c2", "Flashsim distribution", 800, 700)


legend2 = ROOT.TLegend(0.62, 0.70, 0.82, 0.86)

h_eta['ph2_VBF_c2v_2'].Draw("HIST")
h_eta['ph2_VBF_c2v_2'].SetTitle("eta distribution for GenJetAK8")
h_eta['ph2_VBF_c2v_2'].SetLineWidth(3)
h_eta['ph2_VBF_c2v_2'].SetLineColor(ROOT.kBlue +1)
h_eta['ph2_VBF_c2v_2'].Scale(1/h_eta['ph2_VBF_c2v_2'].Integral())
legend2.AddEntry(h_eta['ph2_VBF_c2v_2'], "phase 2, VBF, c_{2v} = 2", "l")


h_eta['ph2_VBF_c2v_1'].Draw("HIST SAME")
h_eta['ph2_VBF_c2v_1'].SetLineWidth(3)
h_eta['ph2_VBF_c2v_1'].SetLineColor(ROOT.kTeal+3)
h_eta['ph2_VBF_c2v_1'].Scale(1/h_eta['ph2_VBF_c2v_1'].Integral())
legend2.AddEntry(h_eta['ph2_VBF_c2v_1'], "phase 2, VBF, c_{2v} = 1", "l")


h_eta['run2_VBF'].Draw("HIST SAME")
h_eta['run2_VBF'].SetLineWidth(3)
h_eta['run2_VBF'].SetLineColor(ROOT.kRed +1)
h_eta['run2_VBF'].Scale(1/h_eta['run2_VBF'].Integral())
legend2.AddEntry(h_eta['run2_VBF'], "run 2, VBF", "l")


h_eta['run2_ggH'].Draw("HIST SAME")
h_eta['run2_ggH'].SetLineWidth(3)
h_eta['run2_ggH'].SetLineColor(ROOT.kBlack)
h_eta['run2_ggH'].Scale(1/h_eta['run2_ggH'].Integral())
legend2.AddEntry(h_eta['run2_ggH'], "run 2, ggH", "l")

legend2.Draw()

c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/test_genjetak8_pt_distr.pdf")
c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/figures_master_thesis/test_genjetak8_eta_distr.pdf")
