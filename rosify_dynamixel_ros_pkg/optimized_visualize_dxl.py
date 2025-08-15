#!/usr/bin/env python

from adatools import config_generator as cg
from adatools import plotting_tools as pt
from math import radians as d2r

#TODO: Add necessary ROS libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class myDynamixelVisualizer(Node):
    def __init__(self) -> None:
        super().__init__("my_dynamixel_visualizer")
        self.sub = self.create_subscription(Int32, '/dxl_joint_cmd', self.listener_callback, 10)
        self.create_config()
        self.create_visualizer()
        self.last_q = 0.0
        
        print("Created")

    def create_config(self):
        #TODO: Modify according to your robot
        self.my_conf_robot = cg.get_robot_config_2(link1=0.3, link1_offset=0.0,
                                        link2=0.3, link2_offset=0.0)
        
    def create_visualizer(self):
        self.robot_teach = self.my_conf_robot.teach(self.my_conf_robot.q, backend='pyplot', block=False)
        self.plot = pt.plot_baseplate(self.robot_teach)

    def listener_callback(self, msg):
        print("Received new data")
        ## Optimize:
        if d2r(int(msg.data)) == self.last_q:
            print("No update required")
        else:
            print("Plot updated")
            self.last_q = d2r(int(msg.data))
            self.my_conf_robot.q[0] = self.last_q
            print(self.my_conf_robot.q)
            # Jog the robot on base plate
            self.plot.step()
    
def main(args=None):
    rclpy.init(args=args)
    node = myDynamixelVisualizer()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == '__main__':
    main()

