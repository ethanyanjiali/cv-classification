# coding: utf-8
import torch
import torch.nn as nn
import torch.nn.functional as Func
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as Init

# [1] One weird trick for parallelizing convolutional neural networks
# https://arxiv.org/pdf/1404.5997.pdf


class AlexNetV2(nn.Module):
    '''
    This implements the network from the second version of AlexNet
    '''
    def __init__(self):
        super(AlexNetV2, self).__init__()
        # "In detail, the single-column model has 64, 192, 384, 384, 256 filters
        # in the five convolutional layers, respectivel"[1]
        # "It has the same number of layers as the two-tower model, and the
        # (x, y) map dimensions in each layer are equivalent to
        # the (x, y) map dimensions in the two-tower model.
        # The minor difference in parameters and connections
        # arises from a necessary adjustment in the number of
        # kernels in the convolutional layers, due to the unrestricted
        # layer-to-layer connectivity in the single-tower model."[1]

        # According to the above, I just need to change the # of output channels
        # Please refer to ./alexnet1 for detailed calculation
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 11, stride=4, padding=2),
            nn.ReLU(inplace=True),
            # Later in the VGG paper, it demonstrated that LRN is not necessary
            # Hence most of AlexNet implementation doesn't include LRN
            # However, for study purpose, I still added this layer
            nn.LocalResponseNorm(64),
            nn.MaxPool2d(3, 2),
            nn.Conv2d(64, 192, 5, stride=1, padding=2),
            nn.ReLU(inplace=True),
            nn.LocalResponseNorm(192),
            nn.MaxPool2d(3, 2),
            nn.Conv2d(192, 384, 3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 384, 3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, 3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, 2),
        )

        self.classifier = nn.Sequential(
            # This part is same with ./alexnet 1 as mentioned above
            nn.Dropout(p=0.5),
            nn.Linear(6 * 6 * 256, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, 1000),
            # "Another difference is that instead of a softmax
            # final layer with multinomial logistic regression
            # cost, this model’s final layer has 1000 independent logistic
            # units, trained to minimize cross-entropy"[1]
        )


    def forward(self, x):
        x = self.features(x)

        # flatten the output from conv layers, but keep b∏atch size
        x = x.view(x.size(0), 6 * 6 * 256)

        x = self.classifier(x)

        return x
