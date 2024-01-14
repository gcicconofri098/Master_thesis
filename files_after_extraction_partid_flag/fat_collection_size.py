import ROOT

file_path = '/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_signal_SM_VBF_with_partid_flag.root'

df = ROOT.RDataFrame("MJets", file_path)

df = df.Define("fat_collection_size", "Mfatjet_pt.size()")

hist = df.Histo1D(("h1", "h1", 40, 0, 10), "fat_collection_size")

c1 = ROOT.TCanvas("c1", "c1", 4500, 3500)

hist.Draw()

c1.SaveAs("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/fat_collection_size.pdf")