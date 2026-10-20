import os
import torch
from torchvision.transforms import ToTensor
import cv2
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms
from . import dataset
import torch.optim as optim
from PIL import Image



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
        self.conv1 = nn.Conv2d(6, 64, kernel_size=3)
        self.relu1 = nn.ReLU()
        self.maxpool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv2 = nn.Conv2d(64, 128, kernel_size=3)
        self.relu2 = nn.ReLU()
        self.maxpool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.fc1 = nn.Linear(2386432, 256)
        self.relu3 = nn.ReLU()
        self.fc2 = nn.Linear(256, 2)  # Output has 2 dimensions for steering and throttle
        
        

    def forward(self, x):
        # Input shape: (batch_size, channels, height, width)

        # Convolutional layers
        x = self.maxpool1(self.relu1(self.conv1(x)))
        x = self.maxpool2(self.relu2(self.conv2(x)))

        # Flatten before fully connected layers
        x = torch.flatten(x, start_dim=1)

        # Fully connected layers
        x = self.relu3(self.fc1(x))
        x = self.fc2(x)

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
    model.train()  # Set the model to training mode
    modelPath = "src/autoNN/model"
    prevLoss = 0

    for epoch in range(num_epochs):
        running_loss = 0.0
        print("Training epoch..")

        for inputs, labels_steering, labels_throttle in train_loader:
            optimizer.zero_grad()

            # Forward pass
            outputs = model(inputs)

            # Assuming labels_steering and labels_throttle are torch tensors
            loss = criterion(outputs, torch.cat((labels_steering, labels_throttle), dim=1))

            # Backward pass and optimization
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

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


def validate(model, val_loader, criterion):
    model.eval()  # Set the model to evaluation mode

    total_loss = 0.0
    num_samples = 0

    with torch.no_grad():
        for inputs, labels_steering, labels_throttle in val_loader:
            # Forward pass
            outputs = model(inputs)

            # Assuming labels_steering and labels_throttle are torch tensors
            loss = criterion(outputs, torch.cat((labels_steering, labels_throttle), dim=1))

            total_loss += loss.item()
            num_samples += len(inputs)

            print(f"Loss value: {loss}")

    average_loss = total_loss / num_samples
    print(f"Average loss: {average_loss}")

    return average_loss

def main():
    setDevice()
    
    dataPath = f"src/autoNN/data"
    timestamp = "24-02-19-17_38_47"
    steeringPath = f"{dataPath}/steering/{timestamp}_steering.txt"
    throttlePath = f"{dataPath}/throttle/{timestamp}_throttle.txt"
    cam0Path = f"{dataPath}/cam0/{timestamp}"
    cam1Path = f"{dataPath}/cam1/{timestamp}"
    myData = dataset.CustomImageDataset(cam0Path, cam1Path, steeringPath, throttlePath)

    dataSize = len(myData)
    trainingRatio = 0.8
    trainingSize = int(trainingRatio * dataSize)
    validationSize = int(dataSize-trainingSize)
    train_dataset, val_dataset = random_split(myData, [trainingSize, validationSize])

    weightsPath = "src/autoNN/model/best.pt"
    model = NeuralNetwork()
    # model.load_state_dict(torch.load(weightsPath))
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # train(model, train_loader, criterion, optimizer, 5)
    # validate(model, val_loader, criterion)

    image1 = Image.open(f"{cam0Path}/Camera_0_Frame_{71}.jpg").convert('RGB')
    image2 = Image.open(f"{cam1Path}/Camera_1_Frame_{71}.jpg").convert('RGB')
    transform = transforms.Compose([
            # Add any necessary transformations (e.g., resizing, normalization) here
            transforms.ToTensor(),
        ])
    image1 = transform(image1)
    image2 = transform(image2)
    image = torch.cat((image1, image2), dim=0)
    image = torch.unsqueeze(image, 0)
    model.eval()
    with torch.no_grad():
        result = model(image)
    print(result)
    
    
    
    
    


if __name__ == '__main__':
    main()