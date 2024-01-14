#%%
import uproot

sig_path = '/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_signal_SM_VBF_with_partid_flag.root'

bckg_path = '/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_QCD_flat_PU200_with_partid_flag.root'


tree_sig = uproot.open(sig_path +':MJets')
#%%
vars_to_save = tree_sig.keys()
tree_bckg = uproot.open(bckg_path + ':MJets')
vars_to_save_bckg = tree_bckg.keys()

#print(vars_to_save)

df_sig = tree_sig.arrays(library="pd").dropna().reset_index(drop=True)
#%%
df_bckg = tree_bckg.arrays(library="pd").dropna().reset_index(drop=True)

df_sig.to_pickle("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/extracted_signal.pkl")

df_bckg.to_pickle("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/extracted_background.pkl")


