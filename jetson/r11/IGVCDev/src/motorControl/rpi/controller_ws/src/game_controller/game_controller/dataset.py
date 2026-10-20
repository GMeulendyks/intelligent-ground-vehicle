import os
import pandas as pd
from torchvision.io import read_image

import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms
import numpy as np


class CustomImageDataset(Dataset):
    def __init__(self, cam0Path, cam1Path, steeringPath, throttlePath):
        self.cam0Path = cam0Path
        self.cam1Path = cam1Path
        self.steeringPath = steeringPath
        self.throttlePath = throttlePath
        self.transform = transforms.Compose([
            # Add any necessary transformations (e.g., resizing, normalization) here
            transforms.ToTensor(),
        ])

        # Load labels once during initialization
        self.steering_labels = np.loadtxt(self.steeringPath)
        self.throttle_labels = np.loadtxt(self.throttlePath)

    def __len__(self):
        # Assuming steering_labels and throttle_labels have the same length
        return len(self.steering_labels)

    def __getitem__(self, index):
        image_left = Image.open(f"{self.cam0Path}/Camera_0_Frame_{index}.jpg").convert('RGB')
        image_right = Image.open(f"{self.cam1Path}/Camera_1_Frame_{index}.jpg").convert('RGB')

        image_left = self.transform(image_left)
        image_right = self.transform(image_right)
        
        image = torch.cat((image_left, image_right), dim=0)
        # combined_image = torch.unsqueeze(combined_image, 0)
        

        # Retrieve labels directly from pre-loaded arrays
        steering_label = torch.tensor(self.steering_labels[index], dtype=torch.float32)
        throttle_label = torch.tensor(self.throttle_labels[index], dtype=torch.float32)

        steering_label = torch.unsqueeze(steering_label, 0)
        throttle_label = torch.unsqueeze(throttle_label, 0)

        return image, steering_label, throttle_label
    

def main():
    dataPath = f"src/autoNN/data"
    timestamp = "24-02-19-17_38_47"
    steeringPath = f"{dataPath}/steering/{timestamp}_steering.txt"
    throttlePath = f"{dataPath}/throttle/{timestamp}_throttle.txt"
    cam0Path = f"{dataPath}/cam0/{timestamp}"
    cam1Path = f"{dataPath}/cam1/{timestamp}"
    
    
    myData = CustomImageDataset(cam0Path, cam1Path, steeringPath, throttlePath)
    print(myData.__getitem__(5)[0].shape)
    
    

if __name__ == '__main__':
    main()