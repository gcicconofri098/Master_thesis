import ROOT
import os

# ROOT.EnableImplicitMT()


# * Run2 files

# f = os.listdir("/scratchnvme/cicco/run2_comp_files")
# num = len(f)
# print(num)
# files = []

# for i in range(0, num-1):
#     files.append("/scratchnvme/cicco/run2_comp_files/" + str(f[i]))
#     print(files)

df_run = ROOT.RDataFrame(
    "Events",
    "/scratchnvme/cicco/run2_SM_comp_files/015D588B-ED64-C14D-959B-C68EE9E0DF3C.root",
)

print(df_run.Count().GetValue())

# df_run.Display("FatJet_genJetAK8Idx").Print()
df_run = (
    df_run.Filter("!FatJet_genJetAK8Idx.empty()")
    .Define(
        "good_jets",
        "FatJet_genJetAK8Idx>=0",
    )
    .Define("new_index", "FatJet_genJetAK8Idx[good_jets]")
)


df_run = (
    df_run.Define("Matched_GenJet_mass", "Take(GenJetAK8_mass, new_index)")
    .Define("Matched_GenJet_pt", "Take(GenJetAK8_pt, new_index)")
    .Define("Matched_FatJet_pt", "FatJet_pt[good_jets]")
    .Define("Matched_FatJet_mass", "FatJet_msoftdrop[good_jets]")
)

df_run.Count().GetValue()


df_run = (
    df_run.Define(
        "gen_cuts",
        "Matched_GenJet_mass>80 && Matched_GenJet_pt>200 && Matched_GenJet_pt<400",
    )
    .Define("Selected_GenJet_mass", "Matched_GenJet_mass[gen_cuts]")
    .Define("Selected_GenJet_pt", "Matched_GenJet_pt[gen_cuts]")
    .Define("Selected_FatJet_pt", "Matched_FatJet_pt[gen_cuts]")
    .Define("Selected_FatJet_mass", "Matched_FatJet_mass[gen_cuts]")
    .Define("Pt_ratio_run", "Matched_FatJet_pt/Matched_GenJet_pt")
    .Define("Mass_ratio_run", "Matched_FatJet_mass/Matched_GenJet_mass")
)


# df_run.Display("good_jets").Print()


# df_run.Display("Matched_FatJet_pt").Print()

# df_run.Display("new_index").Print()


ROOT.gStyle.SetOptStat(0)


# * Phase2 files
#!NDR Entrambi i dataset sono MINIAOD

QCD_phase2 = (
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/run2_phase_comp/files_phase2_QCD.txt"
)

signal_phase2 = (
    "/scratchnvme/cicco/CMSSW_11_3_0_pre4/src/TreeMaker/Ntuplzr/test/file.root"
)

phase2 = open(QCD_phase2, "r")
lines = phase2.readlines()
files = []
for i in lines:
    files.append(i[:-1])
# print(files)

print("creating the df for phase2")


df_ph = ROOT.RDataFrame("myana/mytree", signal_phase2)

print(df_ph.Count().GetValue())

df_ph = (
    df_ph.Filter("!fatjet_genindex.empty()")
    .Define("good_jets", "fatjet_genindex>=0 ")
    .Define("new_index", "fatjet_genindex[good_jets]")
)

df_ph = (
    df_ph.Define("Matched_genjet_pt", "Take(genjetAK8_pt, new_index)")
    .Define("Matched_genjet_mass", "Take(genjetAK8_mass, new_index)")
    .Define("Matched_fatjet_pt", "fatjet_pt[good_jets]")
    .Define("Matched_fatjet_mass", "fatjet_msoftdrop[good_jets]")
)

df_ph = (
    df_ph.Define(
        "gen_cuts",
        "Matched_genjet_mass>80 && 200<Matched_genjet_pt && Matched_genjet_pt<400",
    )
    .Define("Selected_genjet_pt", "Matched_genjet_pt[gen_cuts]")
    .Define("Selected_genjet_mass", "Matched_genjet_mass[gen_cuts]")
    .Define("Selected_fatjet_pt", "Matched_fatjet_pt[gen_cuts]")
    .Define("Selected_fatjet_mass", "Matched_fatjet_mass[gen_cuts]")
    .Define("Pt_ratio_ph", "Matched_fatjet_pt/Matched_genjet_pt")
    .Define("Mass_ratio_ph", "Matched_fatjet_mass/Matched_genjet_mass")
)


# print(len(df_ph.Display("new_index").AsString()))

# print(len(df_ph.Display("Matched_fatjet_pt").AsString()))
# print(len(df_ph.Display("Matched_genjet_pt").AsString()))


# df_ph.Display("Mass_ratio_ph").Print()


# TODO histograms maker

softdrop_run_hist = df_run.Histo1D(
    ("softdrop_run_hist", "Softdrop mass; Softdrop mass [GeV]; Events", 50, 0, 200),
    "Matched_FatJet_mass",
)
fatjet_run_hist = df_run.Histo1D(
    ("fatjet_run_hist", "Transverse Momentum; p_T [GeV]; Events", 50, 0, 800),
    "Matched_FatJet_pt",
)

softdrop_ph_hist = df_ph.Histo1D(
    ("softdrop_ph_hist", "Softdrop mass for Phase2", 50, 0, 200), "Matched_fatjet_mass"
)
fatjet_ph_hist = df_ph.Histo1D(
    ("fatjet_ph_hist", "Fatjet for Phase2", 50, 0, 800), "Matched_fatjet_pt"
)


genjet_mass_run_hist = df_run.Histo1D(
    ("genjet_mass_run_hist", "Gen mass; jet mass [GeV]; Events", 50, 60, 300),
    "Matched_GenJet_mass",
)
genjet_pt_run_hist = df_run.Histo1D(
    ("genjet_pt_run_hist", "Transverse Momentum; p_T [GeV]; Events",80, 0, 1000),
    "Matched_GenJet_pt",
)

genjet_mass_ph_hist = df_ph.Histo1D(
    ("genjet_mass_ph_hist", "genjet mass for Phase2", 50, 60, 300),
    "Matched_genjet_mass",
)
genjet_pt_ph_hist = df_ph.Histo1D(
    ("genjet_pt_ph_hist", "genjet_pt for Phase2",80, 0, 1000), "Matched_genjet_pt"
)


pt_ratio_ph_hist = df_ph.Histo1D(
    ("pt_ratio_ph", "pt Ratio for Phase2; reco/gen; Events", 50, 0, 2), "Pt_ratio_ph"
)

pt_ratio_run_hist = df_run.Histo1D(
    ("pt_ratio_run", "pt Ratio for Run2; reco/gen; Events", 50, 0, 2), "Pt_ratio_run"
)

mass_ratio_ph_hist = df_ph.Histo1D(
    ("mass_ratio_ph", "Mass Ratio for Phase2; reco/gen; Events", 50, 0, 2),
    "Mass_ratio_ph",
)

mass_ratio_run_hist = df_run.Histo1D(
    ("mass_ratio_run", "Mass Ratio for Run2; reco/gen; Events", 50, 0, 2),
    "Mass_ratio_run",
)

print("creating histograms")

c1 = ROOT.TCanvas("c1", "Softdrop mass", 2500, 1500)

legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


softdrop_run_hist.Draw("HIST")
softdrop_run_hist.SetLineWidth(2)
softdrop_run_hist.SetLineColor(ROOT.kBlue + 2)
softdrop_run_hist.Scale(1 / softdrop_run_hist.Integral())
legend.AddEntry("softdrop_run_hist", "Run2", "l")

softdrop_ph_hist.Draw("SAME HIST")
softdrop_ph_hist.SetLineWidth(2)
softdrop_ph_hist.Scale(1 / softdrop_ph_hist.Integral())
legend.AddEntry("softdrop_ph_hist", "Phase2", "l")
softdrop_ph_hist.SetLineColor(ROOT.kRed + 2)

legend.Draw()


c2 = ROOT.TCanvas("c2", "Fat Jet pt", 2500, 1500)

legend2 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


fatjet_ph_hist.Draw("HIST")
fatjet_ph_hist.SetLineWidth(2)
fatjet_ph_hist.SetLineColor(ROOT.kRed + 2)
fatjet_ph_hist.Scale(1 / fatjet_ph_hist.Integral())
legend2.AddEntry("fatjet_ph_hist", "Phase2", "l")

fatjet_run_hist.Draw("SAME HIST")
fatjet_run_hist.SetLineWidth(2)
fatjet_run_hist.SetLineColor(ROOT.kBlue + 2)
fatjet_run_hist.Scale(1 / fatjet_run_hist.Integral())
legend2.AddEntry("fatjet_run_hist", "Run2", "l")


legend2.Draw()

c3 = ROOT.TCanvas("c3", "Pt ratio", 800, 700)
# ROOT.gPad.SetLogy(1)
legend3 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


pt_ratio_run_hist.Draw("HIST")
scale2 = pt_ratio_run_hist.Integral()
pt_ratio_run_hist.SetLineWidth(2)
pt_ratio_run_hist.Scale(1 / scale2)
pt_ratio_run_hist.SetLineColor(ROOT.kBlue + 2)

pt_ratio_ph_hist.Draw("SAME HIST")
pt_ratio_ph_hist.SetLineWidth(2)
pt_ratio_ph_hist.SetLineColor(ROOT.kRed + 2)
scale1 = 1 / (pt_ratio_ph_hist.Integral())
pt_ratio_ph_hist.Scale(scale1)
legend3.AddEntry("pt_ratio_ph", "Phase2 data", "l")


legend3.AddEntry("pt_ratio_run", "Run2 data", "l")

legend3.Draw()

c4 = ROOT.TCanvas("c4", "Mass ratio", 800, 700)

legend4 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


scale3 = mass_ratio_run_hist.Integral()
mass_ratio_run_hist.SetLineWidth(2)
mass_ratio_run_hist.Scale(1 / scale3)
mass_ratio_run_hist.SetLineColor(ROOT.kBlue + 2)
# mass_ratio_run_hist.SetFillColorAlpha(ROOT.kBlue -9, 0.4)


mass_ratio_ph_hist.Draw("HIST")
legend4.AddEntry("mass_ratio_ph", "Phase2 data", "l")

mass_ratio_run_hist.Draw("SAME HIST")
legend4.AddEntry("mass_ratio_run", "Run2 data", "l")

scale4 = mass_ratio_ph_hist.Integral()
mass_ratio_ph_hist.SetLineWidth(2)
mass_ratio_ph_hist.Scale(1 / scale4)
mass_ratio_ph_hist.SetLineColor(ROOT.kRed + 2)
# mass_ratio_ph_hist.SetFillColorAlpha(ROOT.kRed -9, 0.4)



legend4.Draw()

#*gen histos

c5 = ROOT.TCanvas("c5", "Gen mass", 2500, 1500)

legend5 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)


genjet_mass_run_hist.Draw("HIST")
genjet_mass_run_hist.SetLineWidth(2)
genjet_mass_run_hist.SetLineColor(ROOT.kBlue + 2)
genjet_mass_run_hist.Scale(1 / genjet_mass_run_hist.Integral())
legend5.AddEntry("genjet_mass_run_hist", "Run2", "l")

genjet_mass_ph_hist.Draw("HIST SAME")
genjet_mass_ph_hist.SetLineWidth(2)
genjet_mass_ph_hist.Scale(1 / genjet_mass_ph_hist.Integral())
legend5.AddEntry("genjet_mass_ph_hist", "Phase2", "l")
genjet_mass_ph_hist.SetLineColor(ROOT.kRed + 2)

legend5.Draw()


c6 = ROOT.TCanvas("c6", "Gen Jet pt", 2500, 1500)

legend6 = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)

genjet_pt_run_hist.Draw("HIST")
genjet_pt_ph_hist.Draw("SAME HIST")
genjet_pt_ph_hist.SetLineWidth(2)
genjet_pt_ph_hist.SetLineColor(ROOT.kRed + 2)
genjet_pt_ph_hist.Scale(1 / genjet_pt_ph_hist.Integral())
legend6.AddEntry("genjet_pt_ph_hist", "Phase2", "l")


genjet_pt_run_hist.SetLineWidth(2)
genjet_pt_run_hist.SetLineColor(ROOT.kBlue + 2)
genjet_pt_run_hist.Scale(1 / genjet_pt_run_hist.Integral())
legend6.AddEntry("genjet_pt_run_hist", "Run2", "l")

legend6.Draw()


# c5 = ROOT.TCanvas("c4", "Mass ratio", 2500, 1500)

# test1.Draw()
# test1.SetLineColor(ROOT.kRed + 4)
# test1.SetLineWidth(2)

# print(test1.GetEntries())

# test2.Draw("SAME")
# test2.SetLineColor(ROOT.kBlue + 4)
# test2.SetLineWidth(2)

# print(test2.GetEntries())


c1.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/run2_phase_comp/figures/test/softdrop_test.pdf"
)

c2.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/run2_phase_comp/figures/test/fatjet_pt_test.pdf"
)

c3.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/run2_phase_comp/figures/test/pt_ratio_test.pdf"
)

c4.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/run2_phase_comp/figures/test/mass_ratio_test.pdf"
)

c5.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/run2_phase_comp/figures/test/genmass_test.pdf"
)

c6.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/run2_phase_comp/figures/test/genjet_pt_test.pdf"
)
