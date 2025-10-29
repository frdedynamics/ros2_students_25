import rclpy
import math
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState

class RobotArmPublisher(Node):

    def __init__(self):
        super().__init__('robot_arm_controller')
        
        

        self.robot_arm_publisher = self.create_publisher(Float64MultiArray, "robot_arm_controller/commands", 10)
        self.create_subscription(JointState, "/joint_states", self.clbk_joint_states, 10)

        self.zero_pos_msg = Float64MultiArray()
        self.zero_pos_msg.data = [0.0, 0.0, 0.0, 0.0, 0.0]

        self.target_pos_msg = Float64MultiArray()
        self.target_pos_msg.data = [math.pi/4, math.pi/4, math.pi/4, math.pi/4, math.pi/4]
        # self.target_pos_msg.data = [math.pi, math.pi, math.pi, math.pi, math.pi]

        self.move_to_target  = False
        self.cntr = 0

        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def clbk_joint_states(self, msg):
        self.joint_names = msg.name
        self.joint_positions = msg.position
        self.joint_velocities = msg.velocity
        self.joint_efforts = msg.effort

        # self.get_logger().info(f"Joint Names: {self.joint_names}")
        # self.get_logger().info(f"Joint Positions: {self.joint_positions}")

    def timer_callback(self):
        self.cntr += 1
        if self.cntr > 20:
            self.move_to_target = not self.move_to_target
            self.cntr = 0
        
        if self.move_to_target:
            self.robot_arm_publisher.publish(self.target_pos_msg)
        else:
            self.robot_arm_publisher.publish(self.zero_pos_msg)


def main(args=None):

    rclpy.init(args=args)
    robot_arm_node = RobotArmPublisher()

    rclpy.spin(robot_arm_node)
    
    robot_arm_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()