import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd


class MyDataset(Dataset):
    def __init__(self, file_path):

        self.path = file_path
        self._archives = pd.read_pickle(r'path')

        y = self.archives[0]["data"]["MgenjetAK8_pt", "MgenjetAK8_phi", "MgenjetAK8_eta", "MgenjetAK8_hadronFlavour", "MgenjetAK8_partonFlavour", "MgenjetAK8_mass", "MgenjetAK8_ncFlavour", "MgenjetAK8_nbFlavour", "Mpt_ratio", "Meta_sub", "Mphi_sub"] #conditioning variables
        x = self.archives[0]["data"]["Mfatjet_pt", "Mfatjet_eta", "Mfatjet_phi", "Mfatjet_msoftdrop", "Mfatjet_particleNetMD_XbbvsQCD"] #target variables
        self.x_train = torch.tensor(x, dtype=torch.float32)
        self.y_train = torch.tensor(y, dtype=torch.float32)
    
    def __len__(self):
        return len(self.archives)


    def __getitem__(self, idx):
        return self.x_train[idx], self.y_train[idx]

    @property 
    def archives(self):
        return self._archives


    


