import ROOT

file_path = '/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file_bckg.root'

df = ROOT.RDataFrame("MJets", file_path)
zeros = 0

df = df.Define("has_H_within_0_8", str(zeros))

col_to_save = {"Mfatjet_pt", "Mfatjet_eta", "Mfatjet_phi", "Mfatjet_msoftdrop","Mfatjet_particleNetMD_XbbvsQCD", "MgenjetAK8_pt", "MgenjetAK8_eta", "MgenjetAK8_phi",  "MgenjetAK8_partonFlavour", "MgenjetAK8_hadronFlavour", "MgenjetAK8_nbFlavour", "MgenjetAK8_ncFlavour", "MgenjetAK8_mass", "Mpt_ratio", "Meta_sub", "Mphi_sub", "new_index", "has_H_within_0_8"}

df.Snapshot("MJets", "/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/old_QCD_flat_no_PU_with_partid_flag.root", col_to_save)
