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

from .Robot import *

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy
import math
# import lgpio
import time
import serial
from . import serialComm
from data_interface.msg import Data


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        controller = XboxController()
        self.robot = Robot(controller)
        self.prevStates = Joy()
        self.prevStates.buttons = [0] * 21
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0)
        self.auto = False

        self.dataSubscription = self.create_subscription(
            Data,
            'data_topic',
            self.data_callback,
            10
        )
    
    def data_callback(self, msg):
        self.auto = msg.auto_active
        self.cam0 = msg.cam0
        self.cam1 = msg.cam1
        self.steering = msg.steering
        self.throttle = msg.throttle

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    
    def getM0(self, states, a=None, b=None):
        throttle = 5
        steering = 0
        reversing = 1

        # Convert values to match equation notation
        if a == None:
            a = -(states.axes[throttle] - 1.0)/2 * (-2*states.buttons[reversing]+1)
        if b == None:
            b = -states.axes[steering]

        result = (-(a/4)*(b + math.sqrt(b*b))*b) + ((a+1)/2)
        return result
    
    def getM1(self, states, a=None, b=None):
        throttle = 5
        steering = 0
        reversing = 1

        # Convert values to match equation notation
        if a == None:
            a = -(states.axes[throttle] - 1.0)/2 * (-2*states.buttons[reversing]+1)
        if b == None:
            b = -states.axes[steering]

        result = (-(a/4)*(b - math.sqrt(b*b))*b) + ((a+1)/2)
        return result
    
    def sendMessage(self, message):
        self.ser.open()
        self.ser.write(message.encode('UTF-8'))
        self.ser.close()
    
    def driveMotors(self, dutyCycle_M0, dutyCycle_M1):
        ser = serial.Serial('/dev/ttyACM0', 115200)
        dutyCycle_M0 = int(dutyCycle_M0)
        dutyCycle_M1 = int(dutyCycle_M1)

        # dutyCycle_M0 = int(self.map(dutyCycle_M0, 0, 100, 45, 80))
        # dutyCycle_M1 = int(self.map(dutyCycle_M1, 0, 100, 45, 80))

        message = "<motor, " + str(dutyCycle_M0) + ", " + str(dutyCycle_M1) + ">"

        # serialComm.sendToArduino(ser, message)
        
        ser.write(message.encode('UTF-8'))

        
    def listener_callback(self, states):
        
        if not self.auto:
            print(f"Auto status: {self.auto}")
            dutyCycle_M0 = int(self.getM0(states) * 100)
            dutyCycle_M1 = int(self.getM1(states) * 100)
            print(f"Motor0 Signal: {dutyCycle_M0}\n Motor1 Signal: {dutyCycle_M1}")
        else:
            print(f"Auto status: {self.auto}")
            # Get steering and throttle values from NN
            dutyCycle_M0 = int(self.getM0(states, self.steering, self.throttle) * 100)
            dutyCycle_M1 = int(self.getM1(states, self.steering, self.throttle) * 100)
            print(f"Steering: {self.steering}\n Throttle: {self.throttle}")
            print(f"Motor0 Signal: {dutyCycle_M0}\n Motor1 Signal: {dutyCycle_M1}")

        self.driveMotors(dutyCycle_M0, dutyCycle_M1)
        


def main(args=None):
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
