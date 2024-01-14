import os 
import ROOT
import numpy as np

ROOT.EnableImplicitMT()


module_path = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_genpart_id.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')


path = '/scratchnvme/cicco/CMSSW_11_3_0_pre4/src/TreeMaker/Ntuplzr/test/new_ntuplized_files/QCD_PU200_600_Inf_sample.root'

df = ROOT.RDataFrame("myana/mytree", path)

df = df.Define("JetMask", "fatjet_genindex>=0").Define("new_index", "fatjet_genindex[JetMask]").Filter("!fatjet_genindex.empty()")

df= df.Define("has_H_within_0_8", "closest_genpart_id(genpart_eta, genpart_phi, genpart_pid, genjetAK8_eta, genjetAK8_phi)")

     
df = df.Define("higgs_distance_matching", "higgs_distance(genpart_eta, genpart_phi, genpart_pt,genpart_pid, genjetAK8_eta, genjetAK8_phi, genjetAK8_pt, genjetAK8_mass)")

df = (df
        .Define("MgenjetAK8_pt", "Take(genjetAK8_pt, new_index)")
        .Define("MgenjetAK8_eta", "Take(genjetAK8_eta, new_index)")
        .Define("MgenjetAK8_phi", "Take(genjetAK8_phi, new_index)")
        .Define("MgenjetAK8_hadronFlavour", "Take(genjetAK8_hadronFlavour, new_index)")
        .Define("MgenjetAK8_partonFlavour", "Take(genjetAK8_partonFlavour, new_index)")
        .Define("MgenjetAK8_nbFlavour", "Take(genjetAK8_nbFlavour, new_index)")
        .Define("MgenjetAK8_ncFlavour", "Take(genjetAK8_ncFlavour, new_index)")
        .Define("MgenjetAK8_mass", "Take(genjetAK8_mass, new_index)")
        .Define("Mfatjet_pt", "fatjet_pt[JetMask]")
        .Define("Mfatjet_eta", "fatjet_eta[JetMask]")
        .Define("Mfatjet_phi", "fatjet_phi[JetMask]")
        .Define("Mfatjet_msoftdrop", "fatjet_msoftdrop[JetMask]")
        .Define("Mfatjet_particleNetMD_XbbvsQCD", "fatjet_particleNetMD_XbbvsQCD[JetMask]")
        .Define("Mpt_ratio", "Mfatjet_pt/MgenjetAK8_pt")
        .Define("Meta_sub", "MgenjetAK8_eta - Mfatjet_eta")
        .Define("Mphi_sub", "DeltaPhi(Mfatjet_phi, MgenjetAK8_phi)")
        .Define("Mhas_H_within_0_8", "Take(has_H_within_0_8, new_index)")
)

col_to_save = {"Mfatjet_pt", "Mfatjet_eta", "Mfatjet_phi", "Mfatjet_msoftdrop","Mfatjet_particleNetMD_XbbvsQCD", "MgenjetAK8_pt", "MgenjetAK8_eta", "MgenjetAK8_phi",  "MgenjetAK8_partonFlavour", "MgenjetAK8_hadronFlavour", "MgenjetAK8_nbFlavour", "MgenjetAK8_ncFlavour", "MgenjetAK8_mass", "Mpt_ratio", "Meta_sub", "Mphi_sub", "new_index", "Mhas_H_within_0_8"}


df.Snapshot("MJets", "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_files_after_extraction/corrected_QCD_600_Inf_PU200.root", col_to_save)


# c1 = ROOT.TCanvas("c1", "c1", 4500, 3500)
# hist = df.Histo1D(("h", "h", 50, 0, 300), "Mfatjet_msoftdrop")
# hist.Draw()

# c2 = ROOT.TCanvas("c2", "c2", 4500, 3500)

# hist2 = df.Histo1D(("h2", "h2", 50, 0, 1), "Mfatjet_particleNetMD_XbbvsQCD")
# hist2.Draw()

# c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/test_softdrop_aligned.pdf")
# c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/test_discr_aligned.pdf")
