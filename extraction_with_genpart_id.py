import os 
import ROOT
import numpy as np

ROOT.EnableImplicitMT()


module_path = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_genpart_id.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')


path = '/scratchnvme/cicco/CMSSW_11_3_0_pre4/src/TreeMaker/Ntuplzr/test/new_ntuplized_files/new_sig_VBF_SM.root'

df = ROOT.RDataFrame("myana/mytree", path)

#df = df.Filter("abs(genjetAK8_pt[1]-371.25170)<0.001").Range(1)

df = df.Define("JetMask", "fatjet_particleNetMD_XbbvsQCD>0.95 && fatjet_msoftdrop>100 && fatjet_msoftdrop < 150 && fatjet_genindex>=0").Define("new_index", "(ROOT::VecOps::RVec<int>) fatjet_genindex[JetMask]").Filter("!fatjet_genindex.empty()")
#df.Display("new_index").Print()

#df.Display("fatjet_pt").Print()

#df.Display("fatjet_particleNetMD_XbbvsQCD").Print()



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
)


df= (df
     .Define("has_H_within_0_8", "closest_genpart_id(genpart_eta, genpart_phi, genpart_pid, MgenjetAK8_eta, MgenjetAK8_phi)")
     .Define("higgs_distance_matching", "higgs_distance(genpart_eta, genpart_phi, genpart_pt,genpart_pid, MgenjetAK8_eta, MgenjetAK8_phi, MgenjetAK8_pt, MgenjetAK8_mass)")
)


#df.Display("genjetAK8_pt").Print()
#df.Display("MgenjetAK8_pt").Print()
# df = (df
#         .Define("request_fatjets", "Mfatjet_particleNetMD_XbbvsQCD>0.95 && Mfatjet_msoftdrop>100 && Mfatjet_msoftdrop < 150")
#         .Define("selected_idx", "new_index[request_fatjets]")
#         .Define("selected_genjet_AK8_eta", "Take(MgenjetAK8_eta, selected_idx)")
#         .Define("selected_genjet_AK8_phi", "Take(MgenjetAK8_phi, selected_idx)")
#         .Define("selected_genjet_AK8_pt", "Take(MgenjetAK8_pt, selected_idx)")
#         .Define("selected_genjet_AK8_mass", "Take(MgenjetAK8_mass, selected_idx)")


#         .Define("higgs_distance_matching", "higgs_distance(genpart_eta, genpart_phi, genpart_pt, genpart_pid, selected_genjet_AK8_eta, selected_genjet_AK8_phi, selected_genjet_AK8_pt, selected_genjet_AK8_mass)")
#         .Define("problematic_deltaR", "higgs_distance_matching>2.5")

# )

## df.Display("selected_genjet_AK8_eta").Print()
## df.Display("selected_genjet_AK8_pt").Print()

## df.Display("selected_idx").Print()

col_to_save = {"Mfatjet_pt", "Mfatjet_eta", "Mfatjet_phi", "Mfatjet_msoftdrop","Mfatjet_particleNetMD_XbbvsQCD", "MgenjetAK8_pt", "MgenjetAK8_eta", "MgenjetAK8_phi",  "MgenjetAK8_partonFlavour", "MgenjetAK8_hadronFlavour", "MgenjetAK8_nbFlavour", "MgenjetAK8_ncFlavour", "MgenjetAK8_mass", "Mpt_ratio", "Meta_sub", "Mphi_sub", "new_index", "has_H_within_0_8", "higgs_distance_matching"}

print("snapshotting")

#df.Snapshot("MJets", "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/test_higgs_flag_VBF_SM.root", col_to_save)

df.Snapshot("MJets", "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/test_problematic_deltaR.root", col_to_save)

#df = df.Filter("higgs_distance_nonmatching.size()!=0")

print("creating relevant histo")

hist = df.Histo1D(("h1", "h1", 50, 0, 250), "Mfatjet_msoftdrop")

c1 = ROOT.TCanvas("c1", "c1", 4500, 3500)
c1.SetLogy()
hist.Draw()

hist2 = df.Histo1D(("h2", "h2", 70, -1.5, 5), "higgs_distance_matching")

c2 = ROOT.TCanvas("c2", "c2", 4500, 3500)
c2.SetLogy()
hist2.Draw()

c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/test_softdrop.pdf")
c2.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_test_distance_higgs.pdf")