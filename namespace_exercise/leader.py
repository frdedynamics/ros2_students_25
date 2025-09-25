import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64

class LeaderClass(Node):
    def __init__(self):
        super().__init__('RobotLeaderNode')

        #-----------------------------------------------------------------------------------
        #TODO: Create a subscriber to each of the robot_handler publishers
        #      using the existing callback functions (clbk_tb3_0_test and clbk_tb3_1_test)    


        #-----------------------------------------------------------------------------------

        self.tb3_0_lidar_value = 1000
        self.tb3_1_lidar_value = 1000

        timer_period = 1.0  # seconds
        # Create timer function that gets executed once per second
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def clbk_tb3_0_test(self, msg):
        self.tb3_0_lidar_value = msg.data

    def clbk_tb3_1_test(self, msg):
        self.tb3_1_lidar_value = msg.data

    def timer_callback(self):
        self.get_logger().info('TB3_0 Lidar Value: '+ str(self.tb3_0_lidar_value))
        self.get_logger().info('TB3_1 Lidar Value: '+ str(self.tb3_1_lidar_value))


def main(args=None):
    rclpy.init(args=args)

    robot_leader = LeaderClass()

    rclpy.spin(robot_leader)

    robot_leader.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()