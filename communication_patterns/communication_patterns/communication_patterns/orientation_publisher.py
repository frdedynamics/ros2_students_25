import random
import rclpy
from rclpy.node import Node

from communication_patterns_interfaces.msg import Orientation 


class OrientationPublisher(Node):

    def __init__(self):
        super().__init__('orientation_publisher')
        self.publisher_ = self.create_publisher(Orientation, 'orientation', 10)    

        alpha = random.randrange(1,30000)/30000
        beta = random.randrange(1,30000)/30000
        gamma = random.randrange(1,30000)/30000

        self.msg = Orientation()                                           
        self.msg.alpha = alpha
        self.msg.beta = beta
        self.msg.gamma = gamma

        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        self.publisher_.publish(self.msg)


def main(args=None):
    rclpy.init(args=args)

    orientation_publisher = OrientationPublisher()

    rclpy.spin(orientation_publisher)

    orientation_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()