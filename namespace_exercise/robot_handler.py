import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64

class RobotHandlerClass(Node):
    def __init__(self):
        super().__init__('RobotHandlerNode')

        #---------------------------------------------------------------
        #TODO: Create a Subscriber to the lidar topic (named scan) 
        #      of the turtlebot in the same namespace. As a callback 
        #      function use the existing clbk_lidar function 

        #---------------------------------------------------------------


	    #---------------------------------------------------------------
        #TODO: Create Publisher that publishes messages of type Float64     


        #---------------------------------------------------------------

        self.lidar_value = 100.0
        timer_period = 1.0  # seconds
        # Create timer function that gets executed once per second
        self.timer = self.create_timer(timer_period, self.timer_callback)

    # Callback function for lidar subscriber
    def clbk_lidar(self, msg):
        # Safte the lidar value at 180 degrees in a class wide variable
        self.lidar_value = msg.ranges[180]


    # timer function that is executed 1 time per second
    def timer_callback(self):
        # Create a message of type Float64
        pub_msg = Float64()
        # Fill the data object of the message with the lidar value saved in the lidar subscriber callback function
        pub_msg.data = self.lidar_value

        #---------------------------------------------------------------
        #TODO: Publish pub_msg using the previously created publisher   


        #---------------------------------------------------------------


def main(args=None):
    rclpy.init(args=args)

    robot_handler = RobotHandlerClass()

    rclpy.spin(robot_handler)

    robot_handler.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
