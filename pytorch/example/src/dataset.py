import numpy as np
import os

from .utility import *
from torch.utils.data import dataloader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    path = os.path.join(ROOT, 'dataset')
    files = glob(os.path.join(path, '*/*.jpg'))
    print('total : {}'.format(len(files)))

    number_of_images = len(files)

    shuffle = np.random.permutation(number_of_images)

    os.mkdir(os.path.join(path, 'valid'))

    for t in ['train', 'valid']:
        for folder in ['dog/', 'cat/']:
            os.mkdir(os.path.join(path, t, folder))

    for i in shuffle[:2000]:
        folder = files[i].split('/')[-1].split('.')[0]
        image = files[i].split('/')[-1]
        os.rename(files[i], os.path.join(path,'valid', folder, image))

    for i in shuffle[2000:]:
        folder = files[i].split('/')[-1].split('.')[0]
        image = files[i].split('/')[-1]
        os.rename(files[i], os.path.join(path, 'train', folder, image))

    print('done')
