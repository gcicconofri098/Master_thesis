import uproot
import pandas as pd
import numpy as np
import matplotlib
import awkward as ak
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
if __name__ == "__main__":

#!SIGNAL

    tree_1 = uproot.open("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_files_after_extraction/corrected_sig_VBF_C_2V_with_partid_flag.root:MJets")
    vars_to_save = tree_1.keys()
    print(vars_to_save)

    sig1 = ak.to_dataframe(tree_1.arrays(library="ak")).dropna().reset_index(drop=True)

    tree_2 = uproot.open("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_files_after_extraction/corrected_sig_VBF_SM_with_partid_flag.root:MJets")
    vars_to_save = tree_2.keys()
    print(vars_to_save)

    sig2 = ak.to_dataframe(tree_2.arrays(library="ak")).dropna().reset_index(drop=True)

    print(sig1)

    sig1 = sig1[~sig1.isin([np.nan, np.inf, -np.inf]).any(1)]
    #sig1=sig1[sig1[["Mfatjet_msoftdrop", "MgenjetAK8_mass"]]>0]

    sig2 = sig2[~sig2.isin([np.nan, np.inf, -np.inf]).any(1)]


    a = sig1["Mfatjet_msoftdrop"].values
    b = sig1["MgenjetAK8_mass"].values

    print("Number of signal events:{}".format(len(a)))
    a1 = np.log1p(a)
    b1 = np.log1p(b)
    print(b)
    #print(b)


    fig, (ax1, ax2) = plt.subplots(2)

    h1 = ax1.hist2d(a,b, bins=[50, 50], cmap='summer',cmin=1, norm=LogNorm())
    plt.colorbar(h1[3], ax=ax1)
    ax1.set_title("signal")

    ax1.set(ylabel='Genjet AK8 mass')
    
    #plt.hist(b[~np.isnan(b)], bins = 100)
    #plt.scatter(b, d)
    #plt.xlabel('soft drop mass')
    #plt.ylabel('gen mass')
    #plt.show()
    #plt.savefig('preprocess.png')
    #plt.savefig('scatter.png')

    print(sig2)

    df_sig= pd.concat([sig1, sig2], axis=0)

    df_sig.insert(0,"is_signal", np.ones(len(df_sig)))

    print("all signal \n")

    print(df_sig)

#!BACKGROUND


    path_list = ['/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_files_after_extraction/corrected_QCD_flat_PU200_FEVT.root:MJets',
                 '/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_files_after_extraction/corrected_QCD_170_300_PU200.root:MJets',
                 '/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_files_after_extraction/corrected_QCD_300_470_PU200.root:MJets',
                 '/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_files_after_extraction/corrected_QCD_470_600_PU200.root:MJets',
                 '/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_files_after_extraction/corrected_QCD_600_Inf_PU200.root:MJets',
                 ]

    length = len(path_list)

    df_bckg_list = [None] *length 

    tree_bckg_list = [None] * length

    df_bckg = pd.DataFrame()    

    for idx in range(len(path_list)): 

        print(idx)  

        tree_bckg_list[idx] = uproot.open(path_list[idx])

        # vars_to_save_bckg_1 = tree_bckg_list[file].keys()
        # print(vars_to_save_bckg_1)

        df_bckg_list[idx] = ak.to_dataframe(tree_bckg_list[idx].arrays(library='ak')).dropna().reset_index(drop=True)

        df_bckg_list[idx] = df_bckg_list[idx][~df_bckg_list[idx].isin([np.nan, np.inf, -np.inf]).any(1)]

        print(df_bckg_list[idx])

        df_bckg = pd.concat([df_bckg, df_bckg_list[idx]], axis=0)

    print(df_bckg)

    # tree_bckg_2 = uproot.open("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/old_QCD_flat_no_PU_with_partid_flag.root:MJets")

    # vars_to_save_bckg_2 = tree_bckg_2.keys()
    # print(vars_to_save_bckg_2)

    # df_bckg_2 = ak.to_dataframe(tree_bckg_2.arrays(library='ak')).dropna().reset_index(drop=True)

    # df_bckg_2 = df_bckg_2[~df_bckg_2.isin([np.nan, np.inf, -np.inf]).any(1)]



    # print(df_bckg_1)


    # c = df_bckg_1["Mfatjet_msoftdrop"].values
    # d = df_bckg_1["MgenjetAK8_mass"].values
    # #d = df_bckg_1["MgenjetAK8_mass"].values

    # print("Number of background events:{}".format(len(c)))


    # print("heatmap")
    # c1 = np.log1p(c)
    # d1 = np.log1p(d)    

        # plt.scatter(c1, d1, s=6, c='c', label='background',alpha=0.5)
        # plt.scatter(a1, b1, s=6, c='m', label='signal',alpha=0.5)
        # plt.legend(loc='upper left')
        # plt.show()
        # plt.savefig('complete.png')


    # h2 = ax2.hist2d(c,d, bins=[50, 50], cmap='summer',cmin=1, norm=LogNorm())
    # ax2.set_title("background")
    # plt.colorbar(h2[3], ax=ax2)
    # ax2.set(xlabel="Soft drop mass", ylabel="Genjet AK8 mass")
    # fig.savefig('heat_bckg.png')


    df_bckg.insert(0, "is_signal", np.zeros(len(df_bckg)))

    df_f = pd.concat([df_bckg, df_sig], axis=0)

    # for i in range(0,16):
    #     df_f = pd.concat([df_f, df], axis = 0)

    df_f = df_f.dropna().reset_index(drop=True) #.sample(frac=1)
    plt.clf()


    plt.hist(df_f["Mfatjet_msoftdrop"].values, bins= 100, range=[-1, 0])


    print("with enriched signal: {}".format(len(df_f["Mfatjet_msoftdrop"].values)))

    plt.savefig('tentative_softdrop.png')
    print("soft drop mass", df_f["Mfatjet_msoftdrop"].value_counts(ascending=True))
    mask_discr = df_f["Mfatjet_particleNetMD_XbbvsQCD"] < 0
    df_f.loc[mask_discr, "Mfatjet_particleNetMD_XbbvsQCD"] = -0.1

    mask_softdrop = df_f["Mfatjet_msoftdrop"] < 0
    df_f.loc[mask_softdrop, "Mfatjet_msoftdrop"] = -1

    


    #df_f["Mfatjet_msoftdrop"] = df_f["Mfatjet_msoftdrop"].apply(lambda x:np.log(2+x))
    #df_f["Mfatjet_particleNetMD_XbbvsQCD"] = df_f["Mfatjet_particleNetMD_XbbvsQCD"].apply(lambda x:np.log(100+x))
    

    
    arr = df_f["Mfatjet_msoftdrop"].values
    arr[arr ==-1] = np.random.normal(
    loc=-1., scale=0.1, size=arr[arr ==-1].shape
    )
    df_f["Mfatjet_msoftdrop"] = arr
    

    arr = df_f["Mfatjet_msoftdrop"].values
    arr1 = df_f["MgenjetAK8_mass"].values
    arr[arr>0] = arr[arr>0]/arr1[arr>0]

    arr[arr>4]= 4

    df_f["Mfatjet_msoftdrop"] = arr

    #df_f["Mfatjet_msoftdrop"] = df_f["Mfatjet_msoftdrop"]/10
    plt.clf()


    plt.hist(df_f["Mfatjet_msoftdrop"].values, bins= 100)
    plt.yscale("log")



    plt.savefig('corrected_softdrop.png')

    arr = df_f["Mpt_ratio"].values

    print(arr[arr>=2].shape)

    print(df_f)


    df_f.to_pickle("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/new_files_after_extraction/preprocessed_all_QCD_PU200_VBF_SM_and_BSM.pkl")
