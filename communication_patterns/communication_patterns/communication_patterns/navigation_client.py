import random

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from communication_patterns_interfaces.msg import Pose
#TODO: import RobotNavigation action type



class RobotNavigationActionClient(Node):

    def __init__(self):
        super().__init__('robot_navigation_action_client')
        #TODO: create an action client that can send a goal to the previously defined server
        

    def send_goal(self):
        #TODO: create a goal message and assign it to the variable goal_msg
        

        goal_msg.goal_pose = Pose()
        goal_msg.goal_pose.position.x = random.randrange(1,50000)/10000
        goal_msg.goal_pose.position.y = random.randrange(1,50000)/10000
        goal_msg.goal_pose.orientation.gamma = random.randrange(1,10000)/10000

        #TODO: wait for the action server to become active
        

        #TODO: send the goal to the action server. define the feedback callback function to be self.feedback_callback
        

        #TODO: to the future object add as a done callback the self.goal_response_callback function
        
        

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

        # future = goal_handle.cancel_goal_async()

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f"Success: {result.success}; Final Pose: x={result.final_pose.position.x}, y={result.final_pose.position.y}, gamma={result.final_pose.orientation.gamma}")

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f"Current Pose: x={feedback.current_pose.position.x}, y={feedback.current_pose.position.y}, gamma={feedback.current_pose.orientation.gamma}; Distance to goal: {feedback.distance_to_goal}")


def main(args=None):
    rclpy.init(args=args)

    action_client = RobotNavigationActionClient()

    action_client.send_goal()

    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
