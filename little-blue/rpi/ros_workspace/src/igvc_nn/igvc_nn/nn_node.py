import time
import os
import numpy
import rclpy
from rclpy.node import Node
from packager_msgs.msg import LidarSample, MotorControl, Package
import torch
from . import v2


class NeuralNetworkNode(Node):
    def __init__(self, network: v2.nn.NeuralNetwork, device: str):
        super().__init__("neural_network")
        self.get_logger().info('Network created')
        self.get_logger().info(f'Utilizing device: {device}')
        self.network = network

        self.motor_control = self.create_publisher(MotorControl, "motor_control", 10)
        self.packager = self.create_subscription(
            Package, "packages", self.package_cb, 10
        )
        self.device = device

    @staticmethod
    def lidar_to_tensor(lidar: LidarSample):
        return torch.tensor(
            [lidar.magnitude, lidar.angle, lidar.intensity], dtype=torch.float
        )

    def package_cb(self, package: Package):
        now = time.time()
        width = package.cam_width
        height = package.cam_height
        with torch.autocast(device_type=self.device):
            cam0_tensor = torch.tensor(package.cam0).reshape(
                (3, height, width)
            ).to(torch.float)
            cam1_tensor = torch.tensor(package.cam1).reshape(
                (3, height, width)
            ).to(torch.float)
            lidar_arr = numpy.array([[l.magnitude, l.angle, l.intensity] for l in package.lidar_samples], dtype=numpy.float32)
            lidar_tensor = torch.from_numpy(lidar_arr)
            imu = package.linear_acceleration
            imu_tensor = torch.tensor((imu.x, imu.y, imu.z))
            
            throttle, steering = self.network(
                cam0_tensor.unsqueeze(0),
                cam1_tensor.unsqueeze(0),
                lidar_tensor.unsqueeze(0),
                imu_tensor.unsqueeze(0),
            )[0]
            to_send = MotorControl()
            to_send.steering = steering.item()
            to_send.throttle = throttle.item()
            self.motor_control.publish(to_send)
            self.get_logger().info(f'Publishing in total took {time.time() - now}s to complete.')


def main(args=None):

    try:
        model_file = os.environ["NN_MODEL"]
    except:
        print("Failed to load model file: environment variable NN_MODEL not set.")
        return

    model = v2.nn.NeuralNetwork()
    model.load_state_dict(torch.load(model_file, weights_only=True))

    if torch.cuda.is_available():
        device = 'cuda'
    else:
        device = 'cpu'

    rclpy.init(args=args)

    rclpy.spin(NeuralNetworkNode(model, device))

    rclpy.shutdown()


if __name__ == "__main__":
    main()
