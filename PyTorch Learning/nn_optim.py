import torch
import torchvision.datasets
from torch import nn
from torch.nn import Conv2d, MaxPool2d, Flatten, Linear, Sequential
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter


dataset =torchvision.datasets.CIFAR10("./dataset",train=False,transform=torchvision.transforms.ToTensor(),download=True)
dataloader = DataLoader(dataset,batch_size=64)

class Tudui(nn.Module):
    def __init__(self):
        super(Tudui,self).__init__()
        self.module1 = Sequential(
            Conv2d(3,32,5,padding=2),
            MaxPool2d(2),
            Conv2d(32, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 64, 5, padding=2),
            MaxPool2d(2),
            Flatten(),
            Linear(1024, 64),
            Linear(64, 10)
        )

    def forward(self,x):
        x = self.module1(x)
        return x

loss = nn.CrossEntropyLoss()
tudui = Tudui()
# 优化器,lr:学习速率，一般不能太大也不能太小，
optim = torch.optim.SGD(tudui.parameters(),lr=0.01)
for epoch in range(20):
    running_loss = 0.0
    for data in dataloader:
        imgs,targets = data
        outputs = tudui(imgs)
        result_loss = loss(outputs,targets)
        # 把网络模型中每个参数对应的梯度设置为0
        optim.zero_grad()
        # 反向传播，得到每一个节点的梯度
        result_loss.backward()
        optim.step()
        running_loss = running_loss + result_loss
    print(running_loss)

