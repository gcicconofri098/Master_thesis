import ROOT

file_path = '/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_signal_SM_VBF_with_partid_flag.root'

df = ROOT.RDataFrame("MJets", file_path)

df = (df
      .Filter("Mfatjet_pt.size()>=2")
      .Filter("Mfatjet_pt[0]>500 && Mfatjet_pt[1]>400 && abs(TVector2::Phi_mpi_pi(Mfatjet_phi[0] - Mfatjet_phi[1]))>2.6 && abs(Mfatjet_eta[0] - Mfatjet_eta[1])<2.0")
    )

print(df.Count().GetValue()*0.585*59.7/86000)