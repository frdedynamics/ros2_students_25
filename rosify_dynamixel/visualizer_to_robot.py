#!/usr/bin/env python

from adatools import config_generator as cg
from adatools import plotting_tools as pt
from math import radians as d2r

#TODO: Add necessary ROS libraries
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32


class myDynamixelVisualizerToController(Node):
    def __init__(self) -> None:
        super().__init__("dynamixel_visualizer_to_controller")
        self.pub = self.create_publisher(Int32, '/dxl_actual_joint_cmd', 10)
        self.sub = self.create_subscription(Int32, '/dxl_joint_cmd', self.listener_callback, 10)
        self.create_timer(1.0, self.timer_callback)
        self.declare_parameter('update_robot')
        self.actual_q = Int32()
        print("Created")

    def listener_callback(self, msg):
        # Copy the data from visualize msg to actual msg
        self.actual_q.data = msg.data

    def timer_callback(self):
        if self.has_parameter('update_robot'):
            update_robot_param = self.get_parameter('update_robot').get_parameter_value().bool_value

            # Publish to the actual robot topic
            if update_robot_param == True:
                self.pub.publish(self.actual_q)
                # Then set the parameter "update_robot" back to False
                my_new_param = rclpy.parameter.Parameter(
                    'update_robot',
                    rclpy.Parameter.Type.BOOL,
                    False
                )
                all_new_parameters = [my_new_param]
                self.set_parameters(all_new_parameters)
        else:
            print("No parameter set")

    
def main(args=None):
    rclpy.init(args=args)
    node = myDynamixelVisualizerToController()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == '__main__':
    main()



# from adatools import config_generator as cg
# from adatools import plotting_tools as pt


# my_conf2_robot = cg.get_robot_config_2(link1=0.3, link1_offset=0.0,
#                                        link2=0.3, link2_offset=0.0)

# # Plot the robot on base plate
# robot_plot = my_conf2_robot.plot(my_conf2_robot.q, backend='pyplot')
# pt.plot_baseplate(robot_plot)
# # robot_plot.hold()

# # Jog the robot on base plate
# robot_teach = my_conf2_robot.teach(my_conf2_robot.q, backend='pyplot', block=False)
# pt.plot_baseplate(robot_teach)
# robot_teach.hold()