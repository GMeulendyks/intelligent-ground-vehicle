import torch
import numpy as np
from torch.utils import data
from torchvision.io import ImageReadMode, decode_image
import pandas as pd


class DatasetV2(data.Dataset):

    def __init__(self, data_dir: str) -> None:
        # label is "what should this set be classified as"
        # we'll be using [throttle,steering] as our labels
        self.labels_file = pd.read_csv(data_dir + 'joy.csv', header=None)
        self.cam0_dir = data_dir + '/cam0/'
        self.cam1_dir = data_dir + '/cam1/'
        self.lidar_dir = data_dir + '/lidar/'

        self.imu_data = pd.read_csv(data_dir + 'imu.csv', header=None)

    def __len__(self):
        return len(self.labels_file)

    def __getitem__(self, index):
        #Files are named as the index with up to 10 leading zeros
        # eg: 0000000000.jpg / .csv / etc
        # except for ones that are directly put into a single file,
        # where each file line represents the proper index. eg:
        # line 0 -> 0000000000.jpg
        
        cam0 = decode_image(self.cam0_dir + str(index).zfill(10) + '.jpg', mode=ImageReadMode.GRAY).float() / 255.0
        cam1 = decode_image(self.cam1_dir + str(index).zfill(10) + '.jpg', mode=ImageReadMode.GRAY).float() / 255.0

        lidar = pd.read_csv(self.lidar_dir + str(index).zfill(10) + '.csv', header=None)
        lidar.iloc[:,0] = lidar.iloc[:,0].replace(np.inf, -1.0).astype(float)

        # 2x256x256x3 tensor
        img_tensor = torch.stack((cam0,cam1))

        # 9200x3 tensor
        lidar_tensor = torch.tensor(lidar.values).to(torch.float)
        if lidar_tensor.shape[0] < 1080:
            fake_sample = torch.Tensor((-1.0, -3.14159,0.0)).reshape((1,3))
            lidar_tensor = torch.cat((lidar_tensor, fake_sample),dim=0)
            if lidar_tensor.shape[0] != 1080:
                exit(-1)

        # size 3 tensor (x,y,z) linear acceleration
        imu_tensor = torch.tensor(self.imu_data.iloc[index]).to(torch.float)
        imu_tensor = imu_tensor[0:3]

        label = torch.tensor(self.labels_file.iloc[index]).to(torch.float)

        return (img_tensor, lidar_tensor, imu_tensor), label










