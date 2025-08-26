#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from custom_dxl.CustomDXL import CustomDXL

from std_msgs.msg import Int32

class myDynamixelController(Node):
    def __init__(self) -> None:
        super().__init__("my_dynamixel_controller")
        self.sub = self.create_subscription(Int32, '/dxl_joint_cmd', self.listener_callback, 10)
        self.dxls = CustomDXL([0, 4])
        self.dxls.open_port()
        self.dxls.send_goal(goal_pos=[250, 500]) ## Random initial positions to all motors

        print("Created")
        print("Publish data between [0, 4095] to the topic /dxl_joint_cmd")

    def listener_callback(self, msg):
        print("Position command received.")
        self.dxls.send_single_goal(motor_order=0, goal_pos=[msg.data])
        
    
def main(args=None):
    rclpy.init(args=args)
    node = myDynamixelController()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == '__main__':
    main()
    