import os 
import ROOT
import numpy as np

ROOT.EnableImplicitMT()


module_path = os.path.join(os.path.dirname(__file__), "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/utils_genpart_id.h")

ROOT.gInterpreter.ProcessLine(f'#include "{module_path}"')


path = '/scratchnvme/cicco/CMSSW_11_3_0_pre4/src/TreeMaker/Ntuplzr/test/new_ntuplized_files/QCD_flat_PU200.root'

df = ROOT.RDataFrame("myana/mytree", path)

df = df.Define("JetMask", "fatjet_genindex>=0").Define("new_index", "fatjet_genindex[JetMask]").Filter("!fatjet_genindex.empty()")

df= df.Define("is_closest_genpart_H", "closest_genpart_id(genpart_eta, genpart_phi, genpart_pid, genjetAK8_eta, genjetAK8_phi)")

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

col_to_save = {"Mfatjet_pt", "Mfatjet_eta", "Mfatjet_phi", "Mfatjet_msoftdrop","Mfatjet_particleNetMD_XbbvsQCD", "MgenjetAK8_pt", "MgenjetAK8_eta", "MgenjetAK8_phi",  "MgenjetAK8_partonFlavour", "MgenjetAK8_hadronFlavour", "MgenjetAK8_nbFlavour", "MgenjetAK8_ncFlavour", "MgenjetAK8_mass", "Mpt_ratio", "Meta_sub", "Mphi_sub", "new_index", "is_closest_genpart_H"}


df.Snapshot("MJets", "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_QCD_flat_PU200_with_partid_flag.root", col_to_save)