import rclpy
from rclpy.node import Node

#TODO: Import the message types that you need for your publishers and subscribers here:

class BraitenbergController(Node):
    def __init__(self):
        #TODO: Initialze a ros node

        #TODO: Create a subscriber to the /scan topic using as a callback function the existing function self.clbk_laser and queue size of 10

        #TODO: Create a publisher to the /cmd_vel topic with a queue size of 10

        #Default values for the lidar variables as a placeholder until the actual sensor values are recieved through from the ros topic
        self.lidar_left_front = 100
        self.lidar_right_front = 100

        #Creates a timer definition -> during rclpy.spin() the function self.timer_callback() will be executed every 0.1 seconds
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback) 

    #Callback function for the Turtlebots Lidar topic /scan
    def clbk_laser(self, msg):
        self.lidar_left_front = msg.ranges[12]
        self.lidar_right_front = msg.ranges[348]

    def timer_callback(self):
        #Creates a message from type Twist
        vel_msg = Twist()
        #Defines the speed at which the robot will move forward (value between 0 and 1)
        vel_msg.linear.x = 0.7
        #Defines the speed at which the robot will turn around its own axis (value between -1 and 1)
        vel_msg.angular.z = 0.0

        #TODO: Set vel_msg.linear.x and vel_msg.angular.z depending on the values from self.lidar_left_front and self.lidar_right_front

        #TODO: Publish vel_msg using the previously defined publisher


def main(args=None):
    rclpy.init(args=args)

    controller = BraitenbergController()

    rclpy.spin(controller)

    controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()