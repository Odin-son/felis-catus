from mnist import load_mnist
from two_layer_net import TwoLayerNet
from tqdm import tqdm

import numpy as np
import matplotlib.pyplot as plt


def main():
    (x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)

    # hyper-param
    iters_num = 10
    train_size = x_train.shape[0]
    batch_size = 100
    learning_rate = 0.1

    train_loss_list = []
    train_acc_list = []
    test_acc_list = []

    network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

    iter_per_epoch = max(train_size / batch_size, 1)

    for i in tqdm(range(iters_num)):
        batch_mask = np.random.choice(train_size, batch_size)
        x_batch = x_train[batch_mask]
        t_batch = t_train[batch_mask]

        grad = network.numerical_gradient(x_batch, t_batch)

        for key in ('W1', 'b1', 'W2', 'b2'):
            network.params[key] -= learning_rate * grad[key]

        loss = network.loss(x_batch, t_batch)
        train_loss_list.append(loss)

        train_acc = network.accuracy(x_train, t_train)
        test_acc = network.accuracy(x_test, t_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        print("train acc, test acc | " + str(train_acc) + ", " + str(test_acc))

    plt.plot(range(iters_num), train_acc_list, label="train_acc")
    plt.plot(range(iters_num), test_acc_list, lineStyle="--", label="test_acc")
    plt.xlabel("iter_num")
    plt.ylabel("acc")
    plt.title("train & test acc")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()