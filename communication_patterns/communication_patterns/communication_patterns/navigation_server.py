import time
import math

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from communication_patterns_interfaces.msg import Pose
#TODO: import RobotNavigation action type


class RobotNavigationAction(Node):

    def __init__(self):
        super().__init__('replay_velocities_action_server')

        #TODO: create action server that uses the importet action type with the following parameters:
        # execute_callback=self.self.execute_callback
        # callback_group=ReentrantCallbackGroup()
        # goal_callback=self.goal_callback
        # cancel_callback=self.cancel_callback
        
      

    def goal_callback(self, goal_request):
        """Accept or reject a client request to begin an action."""
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Accept or reject a client request to cancel an action."""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT
    

    async def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        #TODO: assign the pose sent by the client to the variable goal_pose
        

        self.get_logger().info(f"Goal Pose: {goal_pose}")
        self.current_pose = Pose()

        #TODO: create a feedback message with the name feedback_msg
        
        
        goal_reached = False

        while not goal_reached:
            delta_x = goal_pose.position.x - self.current_pose.position.x
            delta_y = goal_pose.position.y - self.current_pose.position.y
            delta_gamma = goal_pose.orientation.gamma - self.current_pose.orientation.gamma
            
            self.current_pose.position.x += max(min(delta_x, 0.1), -0.1)
            self.current_pose.position.y += max(min(delta_y, 0.1), -0.1)
            self.current_pose.orientation.gamma += max(min(delta_gamma, 0.1), -0.1)

         
            if self.current_pose == goal_pose:
                goal_reached = True
            else:
                feedback_msg.current_pose = self.current_pose
                feedback_msg.distance_to_goal = math.sqrt(math.pow(goal_pose.position.x - self.current_pose.position.x,2)+math.pow(goal_pose.position.y - self.current_pose.position.y,2))
                #TODO: publish the feedback message
                

            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                result = RobotNavigation.Result()
                result.success = False
                result.final_pose = self.current_pose
                return result

            time.sleep(0.1)

        goal_handle.succeed()
        

        #TODO: Create a result message named result and add the final pose of the robot to it
        # and set success to True
        
        
        return result


def main(args=None):
    rclpy.init(args=args)

    robot_navigation_action = RobotNavigationAction()

    executor = MultiThreadedExecutor()
    rclpy.spin(robot_navigation_action, executor=executor)

if __name__ == '__main__':
    main()