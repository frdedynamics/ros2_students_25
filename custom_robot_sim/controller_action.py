#! /usr/bin/env python

import rclpy
import math
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ArmTrajectoryController(Node):
    def __init__(self):
        super().__init__('ArmTrajectoryController')

        self.joint_trajectory_action_client = ActionClient(self, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory')

        self.joint_trajectory_action_client.wait_for_server()

    def feedback_cb(self, feedback_msg):
        desired_pos = feedback_msg.feedback.desired.positions
        desired_vel = feedback_msg.feedback.desired.velocities

        self.get_logger().info(f"Desired Position: {desired_pos}")
        self.get_logger().info(f"Desired Velocity: {desired_vel}")
        
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self.joint_trajectory_get_result_future = goal_handle.get_result_async()
        self.joint_trajectory_get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info("The robot finished")
        rclpy.shutdown()

    def run(self):
        goal_positions = []
        goal_positions.append([math.pi/2, math.pi/2-0.5, 0.4, math.pi/4, 0.0, -0.05])
        goal_positions.append([math.pi/2, math.pi/2-0.18, 0.6, math.pi/4, 0.0, -0.05])
        goal_positions.append([math.pi/2, math.pi/2-0.18, 0.6, math.pi/4, 0.0, -0.02])
        goal_positions.append([math.pi/2, math.pi/2-0.5, 0.4, math.pi/4, 0.0, -0.02])
        goal_positions.append([-math.pi/2, math.pi/2-0.5, 0.6, math.pi/4, 0.0, -0.02])
        goal_positions.append([-math.pi/2, math.pi/2-0.35, 0.7, math.pi/4, 0.0, -0.02])
        goal_positions.append([-math.pi/2, math.pi/2-0.35, 0.7, math.pi/4, 0.0, -0.05])
        goal_positions.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        points = []
        for i in range(len(goal_positions)):
            new_point_msg = JointTrajectoryPoint()
            new_point_msg.positions = goal_positions[i]
            new_point_msg.time_from_start = Duration(sec=i+1)
            points.append(new_point_msg)

        # adding newly created point into trajectory message
        joints = ['arm_base_joint', 'link_1_joint', 'link_2_joint', 'link_3_joint', 'gripper_base_joint', 'gripper_finger_left_joint']

        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.goal_time_tolerance = Duration(sec=1)
        goal_msg.trajectory.joint_names = joints
        goal_msg.trajectory.points = points

        self.joint_trajectory_send_goal_future = self.joint_trajectory_action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_cb)

        self.joint_trajectory_send_goal_future.add_done_callback(self.goal_response_callback)
        return


def main(args=None):
    rclpy.init(args=args)

    robot = ArmTrajectoryController()

    robot.run()

    rclpy.spin(robot)


if __name__ == '__main__':
    main()
