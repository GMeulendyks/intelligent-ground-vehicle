import torch
from torch import nn
import torch.nn.functional as nnFunc
# Accepts a 256x256x3 input image

# todo:
# set up another stack for lidar data, probably just do linear
# get imu data in
# feed that all together into a linear output
class NeuralNetwork(nn.Module):

    def __init__(self):
        super().__init__()
        img_layers = []

        self.flatten = nn.Flatten()

        # Will divide the input by 16
        for _ in range(4):
            img_layers.extend(NeuralNetwork.create_cnn_layer())
        
        img_layers.append(nn.Flatten())
        img_layers.append(nn.Linear(16*16, 32))
        img_layers.append(nn.ReLU())

        self.img_stack = nn.Sequential(*(img_layers[:]))
        self.img_stack2 = nn.Sequential(*(img_layers[:]))

        # takes in 1080 samples of (r,theta,intensity), should output 16 channels
        self.lidar_stack = nn.Sequential(
                nn.Flatten(),
                nn.Linear(1080*3, 512),
                nn.ReLU(),
                nn.Linear(512, 256),
                nn.ReLU(),
                nn.Linear(256, 128),
                nn.ReLU(),
                nn.Linear(128, 16),
                )

        # input [cam0,cam1,lidar,imu]
        # Output, [throttle,steering]
        self.output_stack = nn.Sequential(
                nn.Linear(32+32+16+3,2),
                #                nn.ReLU(),
                #                nn.Linear(10, 2),
            )

    # x should be a list (maybe tensor?) of
    # x[0][0] = cam0
    # x[0][1] = cam1
    # x[1] = lidar
    # x[2] = imu
    def forward(self, cam0, cam1, lidar, imu):
        out_cam0 = self.img_stack(cam0)
        out_cam1 = self.img_stack2(cam1)
        out_lidar = self.lidar_stack(lidar)
        total_output = torch.cat((out_cam0, out_cam1, out_lidar, imu), dim=1)
        total_output = self.output_stack(total_output)

        return total_output

    @staticmethod
    def create_cnn_layer():
        # for now we just make the same conv layer
        
        # creates a convolution of the same input and output channel dimension
        # and pads it so the output height and width are the same
        conv = nn.Conv2d(1,1,kernel_size=3, padding='same')
        #relu is non-linear which allows the nn to extract information from the input
        relu = nn.ReLU()
        #maxpool reduces the overall size of the output to the next layer
        #specifically kernel_size=2, stride=2 halves the output size
        maxpool = nn.MaxPool2d(kernel_size=2, stride=2)

        return [conv,relu,maxpool]



# Default values taken from pytorch docs
def train_nn(data_loader: torch.utils.data.DataLoader, model: NeuralNetwork, loss_fn, optimizer, device: str | None = None):
    model.train()
    if device is None:
        device = 'cpu'

    sum_loss = 0.0

    size = len(data_loader.dataset)

    for X, y in data_loader:
        optimizer.zero_grad()

        with torch.autocast(device_type=device):
            cam0 = X[0][:, 0].to(device)
            cam1 = X[0][:, 1].to(device)
            lidar = X[1].to(device)
            imu = X[2].to(device)
            pred = model(cam0,cam1,lidar,imu)
            loss = loss_fn(pred, y.to(device))
            sum_loss += loss
            loss.backward()
            optimizer.step()

    return sum_loss / size
        

def test_nn(data_loader, model, loss_fn, device: str | None = None):

    if device is None:
        device = 'cpu'
    model.eval()
    size = len(data_loader.dataset)
    num_batches = len(data_loader)

    throttle_mae = 0.0
    steering_mae = 0.0

    with torch.no_grad():
        for X, y in data_loader:
            with torch.autocast(device_type=device):
                cam0 = X[0][:, 0].to(device)
                cam1 = X[0][:, 1].to(device)
                lidar = X[1].to(device)
                imu = X[2].to(device)
                pred = model(cam0,cam1,lidar,imu)

            pred = pred.to('cpu')
            throttle_mae += nnFunc.l1_loss(pred[:,0], y[:,0], reduction="sum").item()
            steering_mae += nnFunc.l1_loss(pred[:,1], y[:,1], reduction="sum").item()

    avg_throttle = throttle_mae / size
    avg_steering = steering_mae / size
    print(f"Test Error: \n Avg steering MAE: {avg_steering}, Avg throttle mae: {avg_throttle}")

