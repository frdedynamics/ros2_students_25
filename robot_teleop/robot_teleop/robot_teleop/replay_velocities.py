import rclpy
import time
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node

from geometry_msgs.msg import Twist, Pose
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from nav_msgs.msg import Odometry

#----------------------------------------------------------------------------------------------------
#TODO: import action definition
from robot_teleop_interfaces.action import ReplayVel
#----------------------------------------------------------------------------------------------------

class ReplayVelocitiesActionServer(Node):

    def __init__(self):
        super().__init__('replay_velocities_action_server')

        self.current_poses = [Pose(), Pose()]
        
        self.robot_vel_publishers = []
        #create robot velocity publishers
        self.robot_vel_publishers.append(self.create_publisher(Twist, '/tb3_0/cmd_vel', 10))
        self.robot_vel_publishers.append(self.create_publisher(Twist, '/tb3_1/cmd_vel', 10))

        self.create_subscription(Odometry, "/tb3_0/odom", self.clbk_odom, 10)
        self.create_subscription(Odometry, "/tb3_1/odom", self.clbk_odom, 10)

        #----------------------------------------------------------------------------------------------------
        #TODO: create action server
        self._action_server = ActionServer(
            self,
            ReplayVel,
            '/replay_velocities',
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup(),
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)
        #----------------------------------------------------------------------------------------------------
        
    def clbk_odom(self, msg):
        # self.get_logger().info(f"{msg.child_frame_id}")
        self.current_poses[int(msg.child_frame_id[5])] = msg.pose.pose

    #----------------------------------------------------------------------------------------------------
    #TODO: define goal callback function
    def goal_callback(self, goal_request):
        """Accept or reject a client request to begin an action."""
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT
    #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------
    #TODO: define cancel callback function
    def cancel_callback(self, goal_handle):
        """Accept or reject a client request to cancel an action."""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT
    #----------------------------------------------------------------------------------------------------

    async def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        req = goal_handle.request
        robot_id = req.robot_id

        #----------------------------------------------------------------------------------------------------
        #TODO: create a feedback message with the name feedback_msg
        feedback_msg = ReplayVel.Feedback()
        #----------------------------------------------------------------------------------------------------

        for cmd_vel in req.cmd_vel_list:
            self.robot_vel_publishers[robot_id].publish(cmd_vel)
            feedback_msg.current_pose = self.current_poses[robot_id]

            #----------------------------------------------------------------------------------------------------
            #TODO: publish feedback message
            goal_handle.publish_feedback(feedback_msg)
            #----------------------------------------------------------------------------------------------------

            #----------------------------------------------------------------------------------------------------
            #TODO: react to cancel request
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')

                return ReplayVel.Result()
            #----------------------------------------------------------------------------------------------------

            time.sleep(0.1)

        
        #----------------------------------------------------------------------------------------------------
        #TODO: Mark goal as successful
        goal_handle.succeed()
        #----------------------------------------------------------------------------------------------------

        #----------------------------------------------------------------------------------------------------
        #TODO: Create a result message named result and add the final pose of the robot to it
        result = ReplayVel.Result()
        result.final_pose = self.current_poses[robot_id]
        #----------------------------------------------------------------------------------------------------
        
        return result


def main(args=None):
    rclpy.init(args=args)

    replay_vel_action_server = ReplayVelocitiesActionServer()

    executor = MultiThreadedExecutor()
    rclpy.spin(replay_vel_action_server, executor=executor)


if __name__ == '__main__':
    main()