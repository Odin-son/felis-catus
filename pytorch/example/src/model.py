from .utility import *

from torch import nn, cuda, optim
from torchvision import models

if __name__ == "__main__":
    model_ft = models.resnet18(pretrained=True)
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Linear(num_ftrs, 2)

    if cuda.is_available():
        print('cuda')
        model_ft = model_ft.cuda()

    learning_rate = 0.001
    criterion = nn.CrossEntropyLoss()
    optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)
    exp_lr_scheduler = lr_