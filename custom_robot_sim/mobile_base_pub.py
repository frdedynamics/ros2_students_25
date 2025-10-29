import rclpy

from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class MobileBasePublisher(Node):

    def __init__(self):
        super().__init__('mobile_base_controller')

        self.mobile_base_publisher = self.create_publisher(Float64MultiArray, "mobile_base_controller/commands", 10)

        self.mobile_base_msg = Float64MultiArray()
        
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)


    def timer_callback(self):
        # # Move Forward
        # self.mobile_base_msg.data = [1.0, 1.0, 1.0, 1.0]

        # #Move Backwards
        # self.mobile_base_msg.data = [-1.0, -1.0, -1.0, -1.0]

        # # Turn
        # self.mobile_base_msg.data = [-1.0, 1.0, -1.0, 1.0]

        # Stop
        self.mobile_base_msg.data = [0.0, 0.0, 0.0, 0.0]

        

        self.mobile_base_publisher.publish(self.mobile_base_msg)


def main(args=None):

    rclpy.init(args=args)
    mobile_base_node = MobileBasePublisher()

    rclpy.spin(mobile_base_node)
    
    mobile_base_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()