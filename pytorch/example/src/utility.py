import numpy as np
import os

from PIL import Image
from glob import glob
from torch.utils.data import Dataset

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Ex1Dataset(Dataset):
    def __init__(self, root_dir, size=(224,224)):
        self.files = glob(root_dir)
        self.size = size

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        img = np.asarray(Image.open(self.files[idx]).resize(self.size))
        label = self.files[idx].split('/')[-2]
        return img, label
