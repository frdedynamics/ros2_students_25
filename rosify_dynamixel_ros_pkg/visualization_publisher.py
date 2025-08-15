#!/usr/bin/env python

from adatools import config_generator as cg
from adatools import plotting_tools as pt
from math import radians as d2r

#TODO: Add necessary ROS libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

from math import degrees as r2d


class myDynamixelVisualizationPub(Node):
    def __init__(self) -> None:
        super().__init__("my_dynamixel_visualizer")
        self.pub = self.create_publisher(Int32, '/dxl_joint_cmd', 10)
        self.create_config()
        self.create_visualizer()
        self.last_q = 0
        self.published_q_deg = Int32()
        self.create_timer(1.0, self.timer_callback)
        
        print("Created")

    def create_config(self):
        #TODO: Modify according to your robot
        self.my_conf_robot = cg.get_robot_config_2(link1=0.3, link1_offset=0.0,
                                        link2=0.3, link2_offset=0.0)
        
    def create_visualizer(self):
        self.robot_teach = self.my_conf_robot.teach(self.my_conf_robot.q, backend='pyplot', block=False)
        self.plot = pt.plot_baseplate(self.robot_teach)

    def timer_callback(self):
        self.published_q_deg.data = int(r2d(self.my_conf_robot.q[0]))
        print(self.my_conf_robot.q[0], self.published_q_deg.data)
        self.pub.publish(self.published_q_deg)  
        self.plot.step()     
    
def main(args=None):
    rclpy.init(args=args)
    node = myDynamixelVisualizationPub()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == '__main__':
    main()

