import matplotlib.pyplot as plt

from .utility import *
from torchvision.datasets import ImageFolder
from torchvision.transforms import transforms


def imshow(inp):
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    plt.show()


if __name__ == "__main__":
    simple_transform = transforms.Compose([transforms.Resize((224, 224)),
                                           transforms.ToTensor(),
                                           transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    train = ImageFolder(os.path.join(ROOT, 'dataset/train'), simple_transform)
    valid = ImageFolder(os.path.join(ROOT, 'dataset/valid'), simple_transform)

    imshow(train[50][0])
    print(train.class_to_idx)
    print(train.classes)
    print(train)

