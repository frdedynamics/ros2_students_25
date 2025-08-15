'''
This node subscribes /simple_gripper_cmd which is published by Matlab
and
creates a request for /gripper_controller/gripper_cmd whose server is running on turtlebot.

Make sure that this node is running on your VM before you send gripper commands from Matlab to turtlebot.
'''


import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from control_msgs.action import GripperCommand
from std_msgs.msg import Float64


class GripperCommandActionClient(Node):
    def __init__(self):
        super().__init__('gripper_action_client')
        self.action_client = ActionClient(self, GripperCommand, '/gripper_controller/gripper_cmd')
        self.sub = self.create_subscription(Float64, '/simple_gripper_cmd', self.matlab_gripper_callback, 10)
        print("Created")
        self.data_received_flag = False

    def send_goal(self, position, effort):
        goal_msg = GripperCommand.Goal()
        goal_msg.command.position = position  # Open the gripper
        goal_msg.command.max_effort = effort


        self.action_client.wait_for_server()
        self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

    def feedback_callback(self, feedback_msg):
        # This callback is called when feedback is received from the action server
        print('Received feedback: {0}'.format(feedback_msg))
    
    def matlab_gripper_callback(self, msg):
        print(msg.data)
        self.data_received_flag = True
        self.send_goal(position=msg.data, effort=10.0)

def main(args=None):
    rclpy.init(args=args)
    action_client = GripperCommandActionClient()
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
