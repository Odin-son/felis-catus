import numpy as np
import os

from .utility import *
from torch.utils.data import dataloader

if __name__ == "__main__":
    files = glob(os.path.join(os.getcwd(), 'dataset/train', '*/*.jpg'))
    print('total : {}'.format(len(files)))
