# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
from datetime import datetime
import numpy as np
import cv2
from queue import Queue
import csv

import rclpy
from rclpy.node import Node
from data_interface.msg import Data
from PIL import Image
import zlib
import base64

class MinimalSubscriber(Node):

    def __init__(self):
        start = time.time()
        super().__init__('minimal_subscriber')

        self.get_logger().set_level(10)
        

        self.mat = None
        self.subscription = self.create_subscription(
            Data,
            'data_topic',
            self.listener_callback,
            5)
        self.subscription  # prevent unused variable warning


        self.frameCount = 0
        self.counter = 0
        self.user = os.getlogin()
        self.data_dir = f"/home/{self.user}/IGVCDev/src/data_collection_ws/data"
        self.makeDirectories(self.data_dir)

        MAXSIZE = 100
        self.cam0_queue = Queue(maxsize=MAXSIZE)
        self.cam1_queue = Queue(maxsize=MAXSIZE)
        self.steering_queue = Queue(maxsize=MAXSIZE)
        self.throttle_queue = Queue(maxsize=MAXSIZE)

        end = time.time()
        self.get_logger().debug(f"Listener object has been instantiated after {end - start} seconds")
        

    def appendCSV(self, dataFile, data):
        with open(dataFile, 'a', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    
    def compress_line(self, line):
        compressed_data = zlib.compress(line.encode('utf-8'))
        return base64.b64encode(compressed_data).decode('utf-8')
    
    def shape(self, img):
        height = 240
        width = 320
        channel = 3
        img = np.array(img)
        img = img.reshape(height, width, channel)
        return img
    
    
    def listener_callback(self, msg):
        dataFile = f"{self.data_dir}/training_data.csv"
        self.counter += 1
        self.get_logger().info("listener_callback() executing")
        self.get_logger().info(f"Auto status: {msg.auto_active}")
        self.get_logger().info(f"Data Status: {msg.data_active}")

        # steering = [msg.gamepad.axes[0]]
        # throttle = [msg.gamepad.axes[5]]
        # cam0 = list(msg.cam0.data)
        # cam1 = list(msg.cam1.data)
        # self.get_logger().debug(f"Stering: {steering}")
        # self.get_logger().debug(f"Throttle: {throttle}")
        # self.get_logger().debug(f"cam0: {cam0}")
        # self.get_logger().debug(f"cam1: {cam1}")
        # data = [steering + throttle + cam0 + cam1]
        # self.get_logger().debug(f"Data: {data}")
        

        if self.steering_queue.full():
            self.get_logger().info("Saving data to disk storage")
            start_loop = time.time()
            while not self.steering_queue.empty():
                start = time.time()
                msg.gamepad.axes[0] = self.steering_queue.get()
                msg.gamepad.axes[5] = self.throttle_queue.get()
                msg.cam0 = self.cam0_queue.get()
                msg.cam1 = self.cam1_queue.get()
                steering = [msg.gamepad.axes[0]]
                throttle = [msg.gamepad.axes[5]]
                cam0 = list(msg.cam0.data)
                cam1 = list(msg.cam1.data)
                data = [steering + throttle + cam0 + cam1]


                data = self.compress_line(data)
                self.appendCSV(dataFile, data)
                end = time.time()
                self.get_logger().debug(f"Time to store one index of data: {end - start} seconds")
                self.frameCount += 1
            end_loop = time.time()
            self.get_logger().debug(f"Time to store all data: {end_loop - start_loop} seconds")

        if msg.data_active:
            self.get_logger().info("Data capture is active")
            if not self.frameCount%100:
                self.get_logger().info(f"Number of datapoints collected: {self.frameCount}")
            
            if msg.gamepad.axes[0]:
                self.get_logger().info("-----Data recording-----")
                self.steering_queue.put(msg.gamepad.axes[0])
                self.throttle_queue.put(msg.gamepad.axes[5])
                self.get_logger().debug(f"Steering value: {msg.gamepad.axes[0]}")
                self.get_logger().debug(f"Throttle value: {msg.gamepad.axes[5]}")
                self.cam0_queue.put(msg.cam0)
                self.cam1_queue.put(msg.cam1)
                # self.get_logger().debug(f"Cam0 Data: {msg.cam0}")
                # self.get_logger().debug(f"Cam1 Data: {msg.cam1}")
            else:
                if not self.counter % 5: # Save non-steering data 1/10th the frequency as steering data
                    self.get_logger().info("-----Data recording-----")
                    self.steering_queue.put(msg.gamepad.axes[0])
                    self.throttle_queue.put(msg.gamepad.axes[5])
                    self.get_logger().debug(f"Steering value: {msg.gamepad.axes[0]}")
                    self.get_logger().debug(f"Throttle value: {msg.gamepad.axes[5]}")
                    self.cam0_queue.put(msg.cam0)
                    self.cam1_queue.put(msg.cam1)
                    # self.get_logger().debug(f"Cam0 Data: {msg.cam0}")
                    # self.get_logger().debug(f"Cam1 Data: {msg.cam1}")

                self.get_logger().info("-----Data not recording-----")
                self.get_logger().debug(f"Steering value: {msg.gamepad.axes[0]}")
                self.get_logger().debug(f"Throttle value: {msg.gamepad.axes[5]}")

    def crop(self, img, crop):
        left = crop[0]*img.width
        top = crop[1]*img.height
        right = crop[2]*img.width
        bottom = crop[3]*img.height
        return img.crop((left, top, right, bottom))


def main(args=None):
    os.environ['ROS_LOG_DIR'] = f"/home/{os.getlogin()}/IGVCDev/src/data_collection_ws/log/listener_logs"

    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
