import rclpy
import copy
from rclpy.node import Node
from rclpy.action import ActionClient

from geometry_msgs.msg import Twist
from gazebo_msgs.srv import GetEntityState

#----------------------------------------------------------------------------------------------------
#TODO: import custom msg, service and action type
from robot_teleop_interfaces.msg import Teleop
from robot_teleop_interfaces.srv import ResetRobot
from robot_teleop_interfaces.action import ReplayVel
#----------------------------------------------------------------------------------------------------

class RobotTeleopNode(Node):
    def __init__(self):
        super().__init__('robot_control_node')

        self.robot_descriptions = []
        #----------------------------------------------------------------------------------------------------
        #TODO: retrieve turtlebot description parameters and add them to the self.robot_descriptions array
        self.declare_parameter('tb3_0_description', '')
        self.robot_descriptions.append(self.get_parameter('tb3_0_description').get_parameter_value().string_value)
        self.declare_parameter('tb3_1_description', '')
        self.robot_descriptions.append(self.get_parameter('tb3_1_description').get_parameter_value().string_value)
        #----------------------------------------------------------------------------------------------------

        self.robot_names = ['tb3_0', 'tb3_1']
        self.robot_reset_poses = []

        self.robot_vel_publishers = []
        
        
        self.robot_vel_publishers.append(self.create_publisher(Twist, '/tb3_0/cmd_vel', 10))
        self.robot_vel_publishers.append(self.create_publisher(Twist, '/tb3_1/cmd_vel', 10))


        #----------------------------------------------------------------------------------------------------
        #TODO: subscribe to the teleop device publisher with the self.clbk_teleop_device callback function
        self.create_subscription(Teleop, 'teleop_device', self.clbk_teleop_device,10)
        #----------------------------------------------------------------------------------------------------
        

        #----------------------------------------------------------------------------------------------------
        #TODO: Create a service client to the reset robot server defined in reset_robot.py
        #      Assign it to self.client_reset_robot
        self.client_reset_robot = self.create_client(ResetRobot, '/reset_robot')
        while not self.client_reset_robot.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        #----------------------------------------------------------------------------------------------------

        self.client_entity_state = self.create_client(GetEntityState, '/gazebo/get_entity_state')
        while not self.client_entity_state.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('waiting for gazebo entity state service')

 
        #----------------------------------------------------------------------------------------------------
        #TODO: Create an action client to the server defined in replay_velocities.py 
        #      Assign it to self._action_client
        self._action_client = ActionClient(self, ReplayVel, '/replay_velocities')
        self._action_client.wait_for_server()
        #----------------------------------------------------------------------------------------------------

        #----------------------------------------------------------------------------------------------------
        #TODO: Add default values for the action goal request under the name self.replay_vel_goal_msg
        self.replay_vel_goal_msg = ReplayVel.Goal()
        #----------------------------------------------------------------------------------------------------

        self.vel_msg = Twist()
        self.reset_world = False
        self.replay_demonstration = False
        self.cancel_replay = False
        self.wait_for_replay = False
        self.swapping = False
        self.wait_for_service  = False
        self.robot_id = 0
        self.cmd_vel_lists = []
        self.cmd_vel_lists.append([])
        self.cmd_vel_lists.append([])

        #Read the initial pose of the robot
        for robot in self.robot_names:
            robot_state = self.get_model_state(robot)
            self.robot_reset_poses.append(robot_state.state.pose)

        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def clbk_teleop_device(self, msg):
        #----------------------------------------------------------------------------------------------------
        #TODO: assign the velocity part of the msg to target_velocity and the boolean array to button_array
        target_velocity = msg.velocity
        button_array = msg.buttons
        #----------------------------------------------------------------------------------------------------

        self.vel_msg = target_velocity
        if button_array[0] and not self.swapping:
            self.swapping = True
        elif not button_array[0] and self.swapping:
            self.swapping = False
            if self.robot_id == 0: self.robot_id = 1
            else: self.robot_id = 0

        if button_array[1]:
            self.reset_world = True

        if button_array[2]:
            self.replay_demonstration = True

        if button_array[3]:
            if self.replay_demonstration: 
                self.cancel_replay = True


    def timer_callback(self):
        if self.reset_world:
            if not self.wait_for_service:
                #----------------------------------------------------------------------------------------------------
                #TODO: send a request to the reset robot service.
                #      as values use self.robot_names, self.robot_descriptions and self.robot_reset_poses 
                #           (array index is given by self.robot_id)
                #      save future in self.reset_robot_future
                reset_request = ResetRobot.Request()
                reset_request.robot_name = self.robot_names[self.robot_id]
                reset_request.robot_description = self.robot_descriptions[self.robot_id]
                reset_request.reset_pose = self.robot_reset_poses[self.robot_id]

                self.reset_robot_future = self.client_reset_robot.call_async(reset_request)
                #----------------------------------------------------------------------------------------------------

                self.wait_for_service = True

            elif self.wait_for_service and self.reset_robot_future.done():
                self.get_logger().info(f"reset service response: {self.reset_robot_future.result().success}")
                self.wait_for_service = False
                self.reset_world = False

                #----------------------------------------------------------------------------------------------------
                #TODO: create action goal message. velocity list is given by self.cmd_vel_lists[self.robot_id]
                self.replay_vel_goal_msg = ReplayVel.Goal()
                self.replay_vel_goal_msg.robot_id = self.robot_id
                self.replay_vel_goal_msg.cmd_vel_list = copy.deepcopy(self.cmd_vel_lists[self.robot_id])
                #----------------------------------------------------------------------------------------------------

                self.cmd_vel_lists[self.robot_id].clear()
        elif self.replay_demonstration:
            if not self.wait_for_replay:
                self.wait_for_replay = True

                #----------------------------------------------------------------------------------------------------
                #TODO: send previously created action goal  message to action server
                #      include the optional parameter to define a feedback callback function
                #      add a done callback to the future
                self._send_goal_future = self._action_client.send_goal_async(self.replay_vel_goal_msg, feedback_callback=self.feedback_callback)
                self._send_goal_future.add_done_callback(self.goal_response_callback)
                #----------------------------------------------------------------------------------------------------
            elif self.cancel_replay:
                #----------------------------------------------------------------------------------------------------
                #TODO: send a cancel request and add to the future object self.cancel_done_callback as the done callback function
                self._cancel_goal_future = self.goal_handle.cancel_goal_async()
                self._cancel_goal_future.add_done_callback(self.cancel_done_callback)
                #----------------------------------------------------------------------------------------------------
                self.cancel_replay = False

        else:
            if (len(self.cmd_vel_lists[self.robot_id]) == 0 and (self.vel_msg.linear.x != 0.0 or self.vel_msg.angular.z != 0)) or len(self.cmd_vel_lists[self.robot_id]) > 0:
                self.cmd_vel_lists[self.robot_id].append(self.vel_msg)

            #----------------------------------------------------------------------------------------------------
            #TODO: publish velocity message to the currently selected robot
            self.robot_vel_publishers[self.robot_id].publish(self.vel_msg)
            #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------
    #TODO: goal response callback function
    def goal_response_callback(self, future):
        self.goal_handle = future.result()
        if not self.goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')

        self._get_result_future = self.goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
    #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------
    #TODO: result callback function
    def get_result_callback(self, future):
        self.get_logger().info('get_result_callback')
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.final_pose.position))
        self.replay_demonstration = False
        self.wait_for_replay = False
    #----------------------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------------------
    #TODO: feedback callback function
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.current_pose.position))
    #----------------------------------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------------------------------
    #TODO: cancel response callback
    def cancel_done_callback(self, future):
        cancel_response = future.result()
        if len(cancel_response.goals_canceling) > 0:
            self.get_logger().info('Goal successfully canceled')
            self.replay_demonstration = False
            self.wait_for_replay = False
            self.cancel_replay = False
        else:
            self.get_logger().info('Goal failed to cancel')
    #----------------------------------------------------------------------------------------------------

    def get_model_state(self, model_name):
        """
        Returns state information about a model from gazebo using the models name
        """
        req = GetEntityState.Request()
        req.name = model_name
        self.future = self.client_entity_state.call_async(req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
        

def main(args=None):
    rclpy.init(args=args)

    robot_teleop_node = RobotTeleopNode()

    rclpy.spin(robot_teleop_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    robot_teleop_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()