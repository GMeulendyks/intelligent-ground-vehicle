import os
import sys
import torch
from torchvision.transforms import ToTensor
import cv2
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from . import dataset
import torch.optim as optim
from PIL import Image
import time
import io
# import nvidia_smi
# nvidia_smi.nvmlInit()


'''
Build NN for the following parameters:

Input:
    Left Camera
    Right Camera

Output:
    Steering
    Throttle
'''
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()

        # Process images
        self.conv1 = nn.Conv2d(2, 8, kernel_size=7, groups=2)
        self.relu1 = nn.ReLU()
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv2 = nn.Conv2d(8, 8, kernel_size=5, groups=2)
        self.relu2 = nn.ReLU()
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv3 = nn.Conv2d(8, 4, kernel_size=3, groups=2)
        self.relu3 = nn.ReLU()
        self.maxpool3 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv4 = nn.Conv2d(16, 16, kernel_size=3, groups=2)
        self.relu4 = nn.ReLU()
        self.maxpool4 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv5= nn.Conv2d(32, 16, kernel_size=3, groups=2)
        self.relu5 = nn.ReLU()
        self.maxpool5 = nn.MaxPool2d(kernel_size=2, stride=2)

        # self.fc1 = nn.Linear(3552, 256)
        self.fc1 = nn.Linear(444, 256)
        self.relu6 = nn.ReLU()
        self.fc2 = nn.Linear(256, 128)
        self.relu7 = nn.ReLU()
        self.fc3 = nn.Linear(128, 2)  # Output has 2 dimensions for steering and throttle
        
        

    def forward(self, x):
        # Input shape: (batch_size, channels, height, width)

        # Convolutional layers
        x = self.maxpool1(self.relu1(self.conv1(x)))
        x = self.maxpool2(self.relu2(self.conv2(x)))
        x = self.maxpool3(self.relu3(self.conv3(x)))
        # x = self.maxpool4(self.relu4(self.conv4(x)))
        # x = self.maxpool5(self.relu5(self.conv5(x)))

        # Flatten before fully connected layers
        x = torch.flatten(x, start_dim=1)

        # Fully connected layers
        x = self.relu6(self.fc1(x))
        x = self.relu7(self.fc2(x))
        x = self.fc3(x)

        return x
    


def setDevice():
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
    print(f"Using {device} device")

def train(model, train_loader, criterion, optimizer, num_epochs=10):

    # Specify the devices you want to use (e.g., GPU device 0 and 1)
    # device_ids = [0, 1, 2, 3]  # Adjust as needed based on your available GPUs
    # model = nn.DataParallel(model, device_ids=device_ids)
    # Move the model to GPU
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    if torch.cuda.device_count() > 1:
        print("Let's use", torch.cuda.device_count(), "GPUs!")
        model = nn.DataParallel(model)
        model.cuda()
    else:
        print(device)
        # device = torch.device("cpu")
        model = model.to(device)
    
    modelPath = "src/autoNN/model"
    prevLoss = 0

    for epoch in range(num_epochs):
        model.train()  # Set the model to training mode
        running_loss = 0.0
        print("Training epoch...")

        for index, (inputs, labels_steering, labels_throttle) in enumerate(train_loader):
            sys.stdout.write(f"index: {index}/528 | ")
            memory_allocated = torch.cuda.memory_allocated(device) / (1024 ** 3)  # Convert bytes to GB
            memory_cached = torch.cuda.memory_reserved(device) / (1024 ** 3)  # Convert bytes to GB
            # handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)  # Assuming GPU index 0
            # utilization = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
            sys.stdout.write(f"  Memory Allocated: {memory_allocated:.2f} GB | ")
            sys.stdout.write(f"  Memory Cached: {memory_cached:.2f} GB\r")
            # sys.stdout.write(f"  GPU Utilization: {utilization}%\r")
            optimizer.zero_grad()

            # Move input data to GPU
            inputs = inputs.cuda()
            labels_steering = labels_steering.cuda()
            labels_throttle = labels_throttle.cuda()

            # Forward pass
            outputs = model(inputs)

            # Assuming labels_steering and labels_throttle are torch tensors
            loss = criterion(outputs, torch.cat((labels_steering, labels_throttle), dim=1))

            # Backward pass and optimization
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        
        sys.stdout.write("\n")
        # validate(model, train_loader, criterion)

        # Calculate average loss for the epoch
        average_loss = running_loss / len(train_loader)
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {average_loss:.4f}')

        print("Saving model...")
        torch.save(model.state_dict(), f"{modelPath}/last.pt")
        print("Latest model saved!")
        if average_loss < prevLoss:
            torch.save(model.state_dict(), f"{modelPath}/best.pt")
            print("Best model saved!")
        else:
            print("Previous model better!")
        print("Epoch complete!\n\n")

        prevLoss = average_loss
    # return model


def validate(model, val_loader, criterion):
    
    model.eval()
    total_loss = 0.0
    start_time = time.time()
    with torch.no_grad():
        for inputs, labels_steering, labels_throttle in val_loader:
            outputs = model(inputs)
            print(f"Steering: {outputs[0][0].item()}, Throttle: {outputs[0][1].item()}")
            loss = criterion(outputs, torch.cat((labels_steering, labels_throttle), dim=1))
            total_loss += loss.item()
    elapsed_time = time.time() - start_time
    print(f"Validation completed in {elapsed_time:.2f}s with average loss {total_loss / len(val_loader):.4f}")


def main():
    setDevice()
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.benchmark = True
    
    dataPath = f"src/autoNN/data/training"
    steeringPath = f"{dataPath}/steering/steering_data.txt"
    throttlePath = f"{dataPath}/throttle/throttle_data.txt"
    cam0Path = f"{dataPath}/cam0"
    cam1Path = f"{dataPath}/cam1"
    myData = dataset.CustomImageDataset(cam0Path, cam1Path, steeringPath, throttlePath)

    dataSize = len(myData)
    trainingRatio = 0.8
    trainingSize = int(trainingRatio * dataSize)
    validationSize = int(dataSize-trainingSize)
    train_dataset, val_dataset = random_split(myData, [trainingSize, validationSize])
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=16, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=1, shuffle=True)
    
    

    model = NeuralNetwork()
    weightsPath = "src/autoNN/model/best.pt"
    # model.load_state_dict(torch.load(weightsPath))
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    

    train(model, train_loader, criterion, optimizer, 20)

    model.load_state_dict(torch.load(weightsPath, map_location=torch.device('cpu')))
    validate(model, val_loader, criterion)
    
    
    


if __name__ == '__main__':
    main()