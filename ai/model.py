import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F

from tqdm import tqdm

""" network model """

class ResBlock(nn.Module):
    def __init__(self, channels):
        super(ResBlock, self).__init__()
        self.sequential = nn.Sequential(
            nn.Conv2d(channels, channels, kernel_size=(3,1), padding=(1,0), bias=False),
            #nn.BatchNorm2d(planes),
            nn.ReLU(),
            nn.Conv2d(channels, channels, kernel_size=(3,1), padding=(1,0), bias=False),
            #nn.BatchNorm2d(planes)
        )

    def forward(self, x):
        x = self.sequential(x) + x
        return F.relu(x)

class DiscardNet(nn.Module):
    def __init__(self, in_channels, channels_num, blocks_num):
        super(DiscardNet, self).__init__()
        self.preproc = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=channels_num, kernel_size=(3,1), padding=(1,0), bias=False),
            #nn.BatchNorm2d(self.channels[0]),
            nn.ReLU()
        )

        blocks = []
        for _i in range(blocks_num):
            blocks.append(ResBlock(channels_num))
        self.res_blocks = nn.Sequential(*blocks)

        self.postproc = nn.Sequential(
            nn.Conv2d(in_channels=channels_num, out_channels=1, kernel_size=(1,1), padding=(0,0), bias=False),
            #nn.ReLU()
        )

    def forward(self, x):
        x = self.preproc(x)
        x = self.res_blocks(x)
        x = self.postproc(x)
        x = x.view(x.size(0), -1)  # [B, C, H, W] -> [B, C*H*W]
        #print(x)
        return x
        #return F.log_softmax(x)

class FuuroNet(nn.Module):
    def __init__(self, in_channels, channels_num, blocks_num):
        super(FuuroNet, self).__init__()
        self.preproc = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=channels_num, kernel_size=(3,1), padding=(1,0), bias=False),
            #nn.BatchNorm2d(self.channels[0]),
            nn.ReLU()
        )

        blocks = []
        for _i in range(blocks_num):
            blocks.append(ResBlock(channels_num))
        self.res_blocks = nn.Sequential(*blocks)

        self.postproc = nn.Sequential(
            nn.Conv2d(in_channels=channels_num, out_channels=32, kernel_size=(3,1), padding=(1,0), bias=False),
            #nn.ReLU()
        )

        self.dence = nn.Sequential(
            #nn.Linear(1024,256),
            nn.Linear(1088,256),
            nn.Linear(256,2)
        )

    def forward(self, x):
        x = self.preproc(x)
        x = self.res_blocks(x)
        x = self.postproc(x)
        x = x.view(x.size(0), -1)
        x = self.dence(x)
        return x
        #return F.log_softmax(x)

""" dataset """

# class FileDatasets(Dataset):
#     def __init__(self, file_path):
#         npz = np.load(file_path)
#         self.data = npz['arr_0']
#         self.label = npz['arr_1']

#     def __len__(self):
#         return len(self.label)

#     def __getitem__(self, idx):
#         return self.data[idx], np.argmax(self.label[idx])
