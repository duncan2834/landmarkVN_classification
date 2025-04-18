# BUILD CNN
import torch
import torch.nn as nn
from torch.nn import MaxPool2d, Linear, Conv2d, ReLU, Module
from torch import flatten

# CONV2D -> RELU -> MAXPOOL -> FLATTEN -> FC -> SOFTMAX
# Linear: Fully Connected Layer, biến đổi feature map(đặc trưng) thành vector đầu vào cho classifier
# Maxpool2d: giảm số chiều không gian của đầu vào(feature map) nhưng vẫn giữ thông tin quan trọng
# flatten: giảm chiều của đầu ra (Convo, Maxpool) để cho FC sau đó

class CNN(nn.Module):
    def __init__(self, num_classes):
        super(CNN, self).__init__()
        
        # Set 1: Conv2d -> RELU -> Maxpool2d
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1) 
        self.relu1 = nn.ReLU()
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2) # stride = 2 => giảm kích thước 2 lần, pool để giảm kích thước NHƯNG vẫn giữ lại info qtrong
        
        # Set 2: Conv2d -> RELU -> Maxpool2d
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU()
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2) # stride = 2 => giảm kích thước 2 lần, pool để giảm kích thước NHƯNG vẫn giữ lại info qtrong
        
        # Set 2: Conv2d -> RELU -> Maxpool2d
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        self.relu3 = nn.ReLU()
        self.maxpool3 = nn.MaxPool2d(kernel_size=2, stride=2) # stride = 2 => giảm kích thước 2 lần, pool để giảm kích thước NHƯNG vẫn giữ lại info qtrong
        # FC
        self.fc1 = nn.Linear(in_features=64 * 28 * 28, out_features=256) # do stride la 2, sau 2 set thi giam 4 lan, => 224/4 = 56
        self.relu4 = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(in_features=256, out_features=num_classes)
        
    def forward(self, x): # input: x
        # pass qua set 1
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.maxpool1(x)
        # pass qua set 2
        x = self.conv2(x)
        x = self.relu2(x)
        x = self.maxpool2(x)
        # pass qua set 3
        x = self.conv3(x)
        x = self.relu3(x)
        x = self.maxpool3(x)
        # qua FC
        x = flatten(x, 1) # hoac la x.view(x.size(0), -1), [batchsize, featuremap]
        x = self.fc1(x)
        x = self.relu4(x)
        x = self.dropout(x)
        x = self.fc2(x)
        # cho x qua softmax de predict xac suat moi lop 
        # output = self.softmax(x), khong can softmax vì trong CrossEntropyLoss đã có softmax rồi
        return x
        
        