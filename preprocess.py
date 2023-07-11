import uproot
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
if __name__ == "__main__":

#!SIGNAL

    tree = uproot.open("/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file1.root:MJets")
    vars_to_save = tree.keys()
    print(vars_to_save)

    df = tree.arrays(library="pd").astype("float32").dropna().reset_index(drop=True)

    print(df)

    df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]
    #df=df[df[["Mfatjet_msoftdrop", "MgenjetAK8_mass"]]>0]


    a = df["Mfatjet_msoftdrop"].values
    b = df["MgenjetAK8_mass"].values

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

    print(df)

    df.insert(0,"is_signal", np.ones(len(df)))


#!BACKGROUND

    tree_bckg = uproot.open("/scratchnvme/cicco/CMSSW_12_2_4_patch1/src/file_bckg.root:MJets")

    vars_to_save_bckg = tree_bckg.keys()
    print(vars_to_save_bckg)

    df_bckg = tree_bckg.arrays(library='pd').astype("float32").dropna().reset_index(drop=True)

    df_bckg = df_bckg[~df_bckg.isin([np.nan, np.inf, -np.inf]).any(1)]

    print(df_bckg)


    c = df_bckg["Mfatjet_msoftdrop"].values
    d = df_bckg["MgenjetAK8_mass"].values
    #d = df_bckg["MgenjetAK8_mass"].values

    print("Number of background events:{}".format(len(c)))


    print("heatmap")
    c1 = np.log1p(c)
    d1 = np.log1p(d)    

        # plt.scatter(c1, d1, s=6, c='c', label='background',alpha=0.5)
        # plt.scatter(a1, b1, s=6, c='m', label='signal',alpha=0.5)
        # plt.legend(loc='upper left')
        # plt.show()
        # plt.savefig('complete.png')


    h2 = ax2.hist2d(c,d, bins=[50, 50], cmap='summer',cmin=1, norm=LogNorm())
    ax2.set_title("background")
    plt.colorbar(h2[3], ax=ax2)
    ax2.set(xlabel="Soft drop mass", ylabel="Genjet AK8 mass")
    fig.savefig('heat_bckg.png')


    df_bckg.insert(0, "is_signal", np.zeros(len(df_bckg)))
    df_f = pd.concat([df_bckg, df], axis=0)
    for i in range(0,16):
        df_f = pd.concat([df_f, df], axis = 0)

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


    df_f.to_pickle("/gpfs/ddn/cms/user/cicco/miniconda3/analysis/preprocessed.pkl")
