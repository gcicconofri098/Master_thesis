import pandas as pd
import matplotlib.pyplot as plt

#OLD SAMPLE

df =pd.read_pickle("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/preprocessed.pkl")


selected_columns = ['Meta_sub', 'Mphi_sub', 'Mfatjet_msoftdrop', 'Mfatjet_particleNetMD_XbbvsQCD', 'Mpt_ratio']

fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(10, 20))

for ax, col in zip(axes, selected_columns):
    df[col].hist(ax=ax, bins=50, alpha=0.7)
    ax.set_title(f'Histogram of {col}')
    ax.set_xlabel(col)
    ax.set_ylabel('Frequency')

plt.tight_layout()
plt.show()
plt.savefig("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/test.png")
plt.close()

positive_values = df['Mfatjet_particleNetMD_XbbvsQCD'][df['Mfatjet_particleNetMD_XbbvsQCD'] >= 0]

print(len(df))

plt.figure(figsize=(10, 6))
positive_values.hist(bins=50, alpha=0.7)
plt.title("Histogram of 'Mfatjet_particleNetMD_XbbvsQCD' (Positive Values Only)")
plt.xlabel('Mfatjet_particleNetMD_XbbvsQCD')
plt.ylabel('Frequency')
plt.show()
plt.savefig("/gpfs/ddn/cms/user/cicco/miniconda3/Master_thesis/files_after_extraction_partid_flag/test_pos_only.png")
