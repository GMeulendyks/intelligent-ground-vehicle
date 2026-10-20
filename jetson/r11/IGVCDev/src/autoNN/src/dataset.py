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
import glob


class CustomImageDataset(Dataset):
    def __init__(self, cam0Path, cam1Path, steeringPath, throttlePath):
        self.cam0Path = cam0Path
        self.cam1Path = cam1Path
        self.steeringPath = steeringPath
        self.throttlePath = throttlePath
        self.transform = transforms.Compose([
            # Add any necessary transformations (e.g., resizing, normalization) here
            # transforms.ToTensor(),
            self.normalize
        ])

        # Load labels once during initialization
        self.steering_labels = np.loadtxt(self.steeringPath)
        self.throttle_labels = np.loadtxt(self.throttlePath)

    def __len__(self):
        # Assuming steering_labels and throttle_labels have the same length
        return len(self.steering_labels)

    def __getitem__(self, index):
        cam0Data = sorted(glob.glob(os.path.join(self.cam0Path, '*.jpg')), key=lambda x: int(x.split("_")[-1].split(".")[0]))
        cam1Data = sorted(glob.glob(os.path.join(self.cam1Path, '*.jpg')), key=lambda x: int(x.split("_")[-1].split(".")[0]))

        # print(f"Index: {index}\nFile Name: {cam0Data[index]}")

        image_left = Image.open(cam0Data[index]).convert('L')
        image_right = Image.open(cam1Data[index]).convert('L')

        # Perform normalization
        # image_left = np.array(image_left).astype(np.float32)
        # image_right = np.array(image_right).astype(np.float32)
        # image_left = (image_left / 127.5) - 1.0
        # image_right = (image_right / 127.5) - 1.0
        
        image_left = self.crop(image_left)
        image_right = self.crop(image_right)

        image_left = self.transform(image_left)
        image_right = self.transform(image_right)
        
        image = torch.cat((image_left, image_right), dim=0)
        # image = torch.unsqueeze(image, 0)
        

        # Retrieve labels directly from pre-loaded arrays
        steering_label = torch.tensor(self.steering_labels[index], dtype=torch.float32)
        throttle_label = torch.tensor(self.throttle_labels[index], dtype=torch.float32)

        steering_label = torch.unsqueeze(steering_label, 0)
        throttle_label = torch.unsqueeze(throttle_label, 0)

        return image, steering_label, throttle_label
    
    def crop(self, image):
        # Define bounding box based on percentages (left_percentage, top_percentage, right_percentage, bottom_percentage)
        left_percentage = 0
        top_percentage = 0.6
        right_percentage = 1
        bottom_percentage = 0.8

        # Calculate pixel coordinates based on percentages
        image_width, image_height = image.size
        left = int(left_percentage * image_width)
        top = int(top_percentage * image_height)
        right = int(right_percentage * image_width)
        bottom = int(bottom_percentage * image_height)

        # Crop the image
        return image.crop((left, top, right, bottom))
    
    def normalize(self, image):
        # Convert the image to a tensor
        tensor_image = transforms.ToTensor()(image)

        # Flatten the tensor and collect pixel values
        pixel_values = tensor_image.view(-1).numpy()

        # Calculate mean and standard deviation
        mean = np.mean(pixel_values)
        std_dev = np.std(pixel_values)

        # Define Normalize transform
        normalize_transform = transforms.Normalize(mean=[mean], std=[std_dev])

        # Apply normalization transform
        normalized_image = normalize_transform(tensor_image)

        return normalized_image
    

def main():
    dataPath = f"src/autoNN/data/training"
    steeringPath = f"{dataPath}/steering/steering_data.txt"
    throttlePath = f"{dataPath}/throttle/throttle_data.txt"
    cam0Path = f"{dataPath}/cam0"
    cam1Path = f"{dataPath}/cam1"
    
    
    myData = CustomImageDataset(cam0Path, cam1Path, steeringPath, throttlePath)
    print(myData.__getitem__(5)[0])
    
    

if __name__ == '__main__':
    main()