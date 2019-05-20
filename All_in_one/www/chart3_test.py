import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from torch.autograd import Variable
from torchvision import transforms
import torch.optim as optim
from config import *
import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt
from chart3_train import MYCNN

class MyDataset(Dataset):
    """
     root：图像存放地址根路径
     augment：是否需要图像增强
    """
    def __init__(self, root, cut_len=time_len, augment=None):
        # 这个list存放所有图像的地址
        # self.image_files = np.array([x.path for x in os.scandir(root) if x.name.endswith(".jpg")]
        df = pd.read_csv(root)
        df = df[int(0.8*len(df)):]
        df = df.reset_index(drop=True)
        self.radiant_gold_adv = df["radiant_gold_adv"]
        self.radiant_xp_adv = df["radiant_xp_adv"]
        # temp = self.radiant_gold_adv.apply(lambda x:eval(x)[:time_len])
        # temp = np.array(temp.tolist())
        # self.gold_mean, self.gold_std  = np.mean(temp), np.std(temp)
        # print(self.gold_mean, self.gold_std)
        self.transform_gold = lambda x: (x - -120.77453220660516) / 5591.068864620627
        self.anti_gold = lambda x: x * 5591.068864620627 + -120.77453220660516
        self.transform_xp = lambda x: (x - -361.1073401336045) / 6297.316406573604
        self.anti_xp = lambda x: x * 6297.316406573604 + -361.1073401336045
        self.cut_len = cut_len

    def __getitem__(self, index):
        # 读取图像数据并返回
        # 这里的open_image是读取图像函数，可以用PIL、opencv等库进行读取
        # return open_image(self.image_files[index])
        data_, target_ = eval(self.radiant_gold_adv[index]), eval(self.radiant_xp_adv[index])
        data, target = np.array(data_[:self.cut_len]), np.array(target_[:self.cut_len])
        data = np.apply_along_axis(self.transform_gold, 0, data)
        target = np.apply_along_axis(self.transform_xp, 0, target)
        data, target = data.reshape(1,-1), target.reshape(1,-1)
        return data, target

    def __len__(self):
        return len(self.radiant_gold_adv)

my_dataset = MyDataset(root=r"chart3_dataset.csv")
dataloader = torch.utils.data.DataLoader(dataset=my_dataset, batch_size=1, shuffle=True)

model = MYCNN()
checkpoint = torch.load("./checkpoints/2.pth")
model.load_state_dict(checkpoint['state_dict'])

for i, (data, target) in enumerate(dataloader):
    data, target = Variable(data.float()), Variable(target.float())
    predict = model(data)
    data = data.numpy().flatten()
    target = target.numpy().flatten()
    predict = predict.detach().numpy().flatten()
    data = np.apply_along_axis(my_dataset.anti_gold, 0, data)
    target = np.apply_along_axis(my_dataset.anti_xp, 0, target)
    predict = np.apply_along_axis(my_dataset.anti_xp, 0, predict)
    plt.plot(data, label="data")
    plt.plot(predict, label="predict")
    plt.plot(target, label="target")
    plt.legend()
    plt.show()
    if i == 2:
        break

"""pop_mean, pop_std0 = [], []
for i, (img, label) in enumerate(dataloader):
    numpy_image = label.numpy()
    pop_mean.append(np.mean(numpy_image))
    pop_std0.append(np.std(numpy_image))
pop_mean = np.array(pop_mean).mean(axis=0)
pop_std0 = np.array(pop_std0).mean(axis=0)
print(pop_mean, pop_std0)"""