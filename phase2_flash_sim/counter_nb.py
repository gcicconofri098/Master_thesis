import ROOT
import os
import numpy as np

module_path = os.path.join(os.path.dirname(__file__), "nb.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')

file_path = "/scratchnvme/cicco/QCD6/64C8D56A-0144-A344-AF48-EAE3EA799441.root"

#ROOT.EnableImplicitMT()


df = ROOT.RDataFrame("Events", file_path)

df = df.Define(
    "GenPart_IsLastB",
    "(GenPart_pdgId >=500 && GenPart_pdgId < 600) | (GenPart_pdgId >=5000 && GenPart_pdgId < 6000) && (GenPart_statusFlags &(1<<13))!=0",
)

df = df.Define("GenPart_IsLastB_m", "Take(GenPart_IsLastB, GenPart_genPartIdxMother)")

df = df.Define(
    "GenPart_parent_IsNotLastB",
    "(GenPart_genPartIdxMother == -1 | GenPart_IsLastB_m ==0)",
)

df = (df.Define(
    "GenPart_IsGoodB", "GenPart_IsLastB && GenPart_parent_IsNotLastB")
    .Define("GenPart_eta_good", "GenPart_eta[GenPart_IsGoodB]")
    .Define("GenPart_phi_good", "GenPart_phi[GenPart_IsGoodB]")

    .Define("genjetAK8_nbFlavour_manual", "count_nHadrons(GenPart_eta_good, GenPart_phi_good, FatJet_eta, FatJet_phi)")
)
df = df.Define("delta_b", "genjetAK8_nbFlavour_manual - FatJet_nBHadrons")

histo = df.Histo1D(
        ("delta_B", "delta_B ; delta_b ; Events", 25, -3, 3), "delta_b")

c1 = ROOT.TCanvas("c1", "Stacked contributions for jet2 after preselection", 800, 700)

histo.Draw()

c1.SaveAs(
    "/gpfs/ddn/cms/user/cicco/miniconda3/analysis/phase2_flash_sim/test.pdf"
)

#df.Snapshot("test", "test.root" , ["FatJet_pt", "genjetAK8_nbFlavour_manual", "FatJet_nBHadrons"])


