#coding=utf-8
import torch.nn as nn
import torch
import torch.nn.functional as F

class FP_Conv2d(nn.Module):
    def __init__(self, input_channels, output_channels,
            kernel_size=-1, stride=-1, padding=-1, dropout=0, groups=1):
        super(FP_Conv2d, self).__init__()
        self.dropout_ratio = dropout
        if dropout!=0:
            self.dropout = nn.Dropout(dropout)
        self.conv = nn.Conv2d(input_channels, output_channels,
                kernel_size=kernel_size, stride=stride, padding=padding, groups=groups)
        self.bn = nn.BatchNorm2d(output_channels)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        if self.first_flag:
            x = self.relu(x)
        if self.dropout_ratio!=0:
            x = self.dropout(x)
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x

class Net(nn.Module):
    def __init__(self, cfg = None):
        super(Net, self).__init__()
        if cfg is None:
            cfg = [192, 160, 96, 192, 192, 192, 192, 192]

        self.tnn_bin = nn.Sequential(
                nn.Conv2d(3, cfg[0], kernel_size=5, stride=1, padding=2),
                nn.BatchNorm2d(cfg[0]),
                FP_Conv2d(cfg[0], cfg[1], kernel_size=1, stride=1, padding=0),

                FP_Conv2d(cfg[1], cfg[2], kernel_size=1, stride=1, padding=0, groups=2),
                nn.MaxPool2d(kernel_size=2, stride=2, padding=0),

                FP_Conv2d(cfg[2], cfg[3], kernel_size=3, stride=1, padding=1, groups=16),
                FP_Conv2d(cfg[3], cfg[4], kernel_size=1, stride=1, padding=0, groups=4),
                FP_Conv2d(cfg[4], cfg[5], kernel_size=1, stride=1, padding=0, groups=4),
                nn.MaxPool2d(kernel_size=2, stride=2, padding=0),

                FP_Conv2d(cfg[5], cfg[6], kernel_size=3, stride=1, padding=1, groups=32),
                FP_Conv2d(cfg[6], cfg[7], kernel_size=1, stride=1, padding=0, groups=8),
                nn.Conv2d(cfg[7],  10, kernel_size=1, stride=1, padding=0),
                nn.BatchNorm2d(10),
                nn.ReLU(inplace=True),
                nn.AvgPool2d(kernel_size=8, stride=1, padding=0),
                )
    def forward(self, x):
        x = self.tnn_bin(x)
        #x = self.dorefa(x)
        x = x.view(x.size(0), 10)
        return x
