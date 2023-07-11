import ROOT
import os

# from decimal import *

ROOT.EnableImplicitMT()

# getcontext().prec = 2

entries1 = {}

df = {}

integrated_luminosity = 59830
dataset_events = {}

module_path = os.path.join(os.path.dirname(__file__), "utils.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')


weights = {
    "QCD1": 27990000 * integrated_luminosity,
    "QCD2": 1712000 * integrated_luminosity,
    "QCD3": 347700 * integrated_luminosity,
    "QCD4": 32100 * integrated_luminosity,
    "QCD5": 6831 * integrated_luminosity,
    "QCD6": 1207 * integrated_luminosity,
    "QCD7": 119.9 * integrated_luminosity,
    "QCD8": 25.24 * integrated_luminosity,
    "WJets1": 315.2 * integrated_luminosity,
    "WJets2": 68.58 * integrated_luminosity,
    "WJets3": 34.69 * integrated_luminosity,
    "ZJets1": 145.3 * integrated_luminosity,
    "ZJets2": 34.29 * integrated_luminosity,
    "ZJets3": 18.57 * integrated_luminosity,
    "TTHad": 370.04 * integrated_luminosity,
    "TTSemilept": 369.49 * integrated_luminosity,
    "ST_tw_antitop": 35.85 * integrated_luminosity,
    "ST_tw_top": 35.85 * integrated_luminosity,
    "GGH": 9.60 * integrated_luminosity,
    "VBFH": 2.20 * integrated_luminosity,
    "ttH": 0.295 * integrated_luminosity,
    "WMinusH": 0.210 * integrated_luminosity,
    "WPlusH": 0.331 * integrated_luminosity,
    "ZH": 0.310 * integrated_luminosity,
    "ggZH": 0.050 * integrated_luminosity,
    "WW": 118.7 * integrated_luminosity,
    "WZ": 47.2 * integrated_luminosity,
    "ZZ": 16.52 * integrated_luminosity,
    "signal": 0.01053 * integrated_luminosity,
}


files = {
    "QCD1": "/scratchnvme/cicco/QCD1/",
    "QCD2": "/scratchnvme/cicco/QCD2/",
    "QCD3": "/scratchnvme/cicco/QCD3/",
    "QCD4": "/scratchnvme/cicco/QCD4/",
    "QCD5": "/scratchnvme/cicco/QCD5/",
    "QCD6": "/scratchnvme/cicco/QCD6/",
    "QCD7": "/scratchnvme/cicco/QCD7/",
    "QCD8": "/scratchnvme/cicco/QCD8/",
    "WJets1": "/scratchnvme/cicco/WJets1/",
    "WJets2": "/scratchnvme/cicco/WJets2/",
    "WJets3": "/scratchnvme/cicco/WJets3/",
    "ZJets1": "/scratchnvme/cicco/ZJets1/",
    "ZJets2": "/scratchnvme/cicco/ZJets2/",
    "ZJets3": "/scratchnvme/cicco/ZJets3/",
    "TTHad": "/scratchnvme/cicco/TTHad/",
    "TTSemilept": "/scratchnvme/cicco/TTSemilept/",
    "ST_tw_antitop": "/scratchnvme/cicco/ST_tw_antitop/",
    "ST_tw_top": "/scratchnvme/cicco/ST_tw_top/",
    "GGH": "/scratchnvme/cicco/GGH/",
    "VBFH": "/scratchnvme/cicco/VBFH/",
    "ttH": "/scratchnvme/cicco/ttH/",
    "WMinusH": "/scratchnvme/cicco/WMinusH/",
    "WPlusH": "/scratchnvme/cicco/WPlusH/",
    "ZH": "/scratchnvme/cicco/ZH/",
    "ggZH": "/scratchnvme/cicco/ggZH/",
    "WW": "/scratchnvme/cicco/WW/",
    "WZ": "/scratchnvme/cicco/WZ/",
    "ZZ": "/scratchnvme/cicco/ZZ/",
    "signal": "/scratchnvme/cicco/signal_RunIISummer20UL16/",
}


ROOT.gStyle.SetOptStat(0)

hist_2d = {}
h2_2 = {}
processes = list(files.keys())

for i in processes:
    f = os.listdir(files.get(i))
    num = len(f)
    print(num)
    entries1[i] = []

    for j in range(0, num):
        entries1[i].append(str(files.get(i)) + str(f[j]))

    df[i] = ROOT.RDataFrame( "Events", entries1[i]) 


    print("added file to: {}".format(i))


print(processes)


for i in processes:

    print("Begin selection: {}".format(i))
    dataset_events[i] = df[i].Count().GetValue()

    weights[i] = weights[i] / dataset_events[i]

    df[i] = df[i].Filter("nFatJet>=2")

    df[i] = (
        df[i]
        .Define(
            # mu = 13, e = 11
            "FatJet_Selection",
            "FatJet_pt > 300 && abs(FatJet_eta) < 2.4 && fatjet_lepton_isolation(FatJet_electronIdx3SJ, Electron_pt, Electron_eta, Electron_pfRelIso03_all, 11)  && fatjet_lepton_isolation(FatJet_muonIdx3SJ, Muon_pt, Muon_eta, Muon_pfRelIso03_all, 13)",
        )
        .Define("Softdrop_sel_jets", "FatJet_msoftdrop[FatJet_Selection]")
        .Define("Discriminator_Xbb", "FatJet_particleNetMD_Xbb[FatJet_Selection]")
        .Define("Discriminator_Xcc", "FatJet_particleNetMD_Xcc[FatJet_Selection]")
        .Define("Discriminator_Xqq", "FatJet_particleNetMD_Xqq[FatJet_Selection]")
        .Define("new_discriminator", "Discriminator_Xbb/(1-Discriminator_Xcc - Discriminator_Xqq)")
        .Define("old_discriminator", "FatJet_deepTagMD_HbbvsQCD[FatJet_Selection]")
        .Define("Eta_sel_jets", "FatJet_eta[FatJet_Selection]")
        .Define("Phi_sel_jets", "FatJet_phi[FatJet_Selection]")
    )

    df[i] = df[i].Filter("new_discriminator.size()>=2")

    #pre_selection_signal = df["signal"].Count().GetValue()

    df[i] = (
        df[i]
        .Define("sorted_FatJet_deepTagMD_HbbvsQCD", "Reverse(Argsort(new_discriminator))")
        .Define("Jet1_index", "sorted_FatJet_deepTagMD_HbbvsQCD[0]")
        .Define("Jet2_index", "sorted_FatJet_deepTagMD_HbbvsQCD[1]")

    )
    df[i] = (df[i]
            .Filter("Softdrop_sel_jets[Jet1_index]> 50 && Softdrop_sel_jets[Jet2_index]> 50")
            .Filter("new_discriminator[Jet1_index]> 0.86")
    )
    print(df[i].Count().GetValue()*weights[i])
    #df[i] = df[i].Define("Weight_column", str(weights[i]))

    df[i] = (
        df[i]
        .Define(
            "VBF_jet_preselection",
            "jet_isolation(Jet_eta, Jet_phi, Eta_sel_jets, Phi_sel_jets) && Jet_pt >25 && abs(Jet_eta) <4.7",
        )
        .Define("Candidate_jets_pt", "Jet_pt[VBF_jet_preselection]")
        .Define("Candidate_jets_mass", "Jet_mass[VBF_jet_preselection]")
        .Define("Candidate_jets_eta", "Jet_eta[VBF_jet_preselection]")
        .Define("Candidate_jets_phi", "Jet_phi[VBF_jet_preselection]")
    )

    df[i] = (
        df[i]
        .Define("Muon_preselection", "Muon_pt >5")
        .Define("Candidate_muon_pt", "Muon_pt[Muon_preselection]")
        .Define("Candidate_muon_eta", "Muon_eta[Muon_preselection]")
        .Define("Candidate_muon_phi", "Muon_phi[Muon_preselection]")
    )
    df[i] = (
        df[i]
        .Define("Electron_preselection", "Electron_pt >7")
        .Define("Candidate_el_pt", "Electron_pt[Electron_preselection]")
        .Define("Candidate_el_eta", "Electron_eta[Electron_preselection]")
        .Define("Candidate_el_phi", "Electron_phi[Electron_preselection]")
    )

    df[i] = (
        df[i]
        .Define(
            "Good_VBF_candidates",
            "part_isolation(Candidate_jets_eta, Candidate_jets_phi, Candidate_muon_eta, Candidate_muon_phi, Candidate_el_eta, Candidate_el_phi)",
        )
        .Define("Good_VBF_jets_eta", "Candidate_jets_eta[Good_VBF_candidates]")
        .Define("Good_VBF_jets_mass", "Candidate_jets_mass[Good_VBF_candidates]")
        .Define("Good_VBF_jets_pt", "Candidate_jets_pt[Good_VBF_candidates]")
        .Define("Good_VBF_jets_phi", "Candidate_jets_phi[Good_VBF_candidates]")
    )
    df[i] = (
        df[i]
        .Define("sorted_VBF_jets_pt", "Reverse(Argsort(Good_VBF_jets_pt))")
        .Define("VBF_Jet1_index", "sorted_VBF_jets_pt[0]")
        .Define("VBF_Jet2_index", "sorted_VBF_jets_pt[1]")
    )
    df[i] = (
        df[i]
        .Define("VBF_Jet1_eta", "Good_VBF_jets_eta[VBF_Jet1_index]")
        .Define("VBF_Jet2_eta", "Good_VBF_jets_eta[VBF_Jet2_index]")
        .Define("VBF_Jet1_mass", "Good_VBF_jets_mass[VBF_Jet1_index]")
        .Define("VBF_Jet2_mass", "Good_VBF_jets_mass[VBF_Jet2_index]")
        .Define("VBF_Jet1_pt", "Good_VBF_jets_pt[VBF_Jet1_index]")
        .Define("VBF_Jet2_pt", "Good_VBF_jets_pt[VBF_Jet2_index]")
        .Define("VBF_Jet1_phi", "Good_VBF_jets_phi[VBF_Jet1_index]")
        .Define("VBF_Jet2_phi", "Good_VBF_jets_phi[VBF_Jet2_index]")
    )

    df[i] = (
        df[i]
        .Define(
            "Delta_eta",
            "VBF_Jet1_eta - VBF_Jet2_eta",
        )
        .Define(
            "Jet_invariant_mass",
            "invariant_mass(VBF_Jet1_pt, VBF_Jet1_eta, VBF_Jet1_phi, VBF_Jet1_mass, VBF_Jet2_pt, VBF_Jet2_eta, VBF_Jet2_phi, VBF_Jet2_mass)",
        )
    )

    df[i] = (
        df[i]
        .Define(
            "VBF_events", "nJet >=2 && abs(Delta_eta) >4.0 && Jet_invariant_mass > 500"
        )
        .Filter("!VBF_events")
    )

    df[i] = (df[i]
        .Define("Jet1_selected", "new_discriminator[Jet1_index]")
        .Define("Jet2_selected", "new_discriminator[Jet2_index]")

    )

    hist_2d[i] = df[i].Histo2D(
        ("Jet1 vs Jet2", "Jet1 vs Jet2; Jet1; Jet2", 20, 0, 1, 20, 0, 1),
        "Jet1_selected",
        "Jet2_selected",
    )

    h2_2[i] = hist_2d[i].GetValue()

    h2_2[i].Scale(weights[i])

print("finished selection")

hist2d_bckg = h2_2["QCD1"].Clone()
hist2d_bckg.Add(h2_2["QCD2"])
hist2d_bckg.Add(h2_2["QCD3"])
hist2d_bckg.Add(h2_2["QCD4"])
hist2d_bckg.Add(h2_2["QCD5"])
hist2d_bckg.Add(h2_2["QCD6"])
hist2d_bckg.Add(h2_2["QCD7"])
hist2d_bckg.Add(h2_2["QCD8"])


hist2d_bckg.Add(h2_2["WJets1"])
hist2d_bckg.Add(h2_2["WJets2"])
hist2d_bckg.Add(h2_2["WJets3"])
hist2d_bckg.Add(h2_2["ZJets1"])
hist2d_bckg.Add(h2_2["ZJets2"])
hist2d_bckg.Add(h2_2["ZJets3"])


hist2d_bckg.Add(h2_2["TTHad"])
hist2d_bckg.Add(h2_2["TTSemilept"])

hist2d_bckg.Add(h2_2["ST_tw_antitop"])
hist2d_bckg.Add(h2_2["ST_tw_top"])

hist2d_bckg.Add(h2_2["GGH"])
hist2d_bckg.Add(h2_2["VBFH"])
hist2d_bckg.Add(h2_2["WMinusH"])
hist2d_bckg.Add(h2_2["WPlusH"])
hist2d_bckg.Add(h2_2["ZH"])
hist2d_bckg.Add(h2_2["ggZH"])

hist2d_bckg.Add(h2_2["WZ"])
hist2d_bckg.Add(h2_2["ZZ"])
hist2d_bckg.Add(h2_2["WW"])


hist = ROOT.TH2F(
    "hist",
    "Signal to background map; Value of Jet1 discriminator; Value of Jet2 discriminator",
    20,
    0,
    1,
    20,
    0,
    1,
)


for binx in reversed(range(1, 21)):
    for biny in reversed(range(1, 21)):
        if binx>=biny:
            new_bckg = hist2d_bckg.Integral(binx, 20, biny, 20)
            new_sig = h2_2["signal"].Integral(binx, 20, biny, 20)

            print("binx", binx)
            print("biny", biny)

            if new_bckg>0:
                new_bin_cont = new_sig / new_bckg
                print(new_bin_cont)
                hist.SetBinContent(binx, biny, new_bin_cont)





c1 = ROOT.TCanvas("c1", "Efficiency plot", 1400, 1000)
c1.SetGrid()
hist.Draw("COLZ")

c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/figures/sig_to_bckg_map_new_disc_veto.pdf")

