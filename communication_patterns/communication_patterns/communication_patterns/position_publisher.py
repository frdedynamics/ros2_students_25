import random
import rclpy
from rclpy.node import Node

from communication_patterns_interfaces.msg import Position 


class PositionPublisher(Node):

    def __init__(self):
        super().__init__('position_publisher')
        self.publisher_ = self.create_publisher(Position, 'position', 10)    

        x = random.randrange(1,30000)/30000
        y = random.randrange(1,30000)/30000
        z = random.randrange(1,30000)/30000

        self.msg = Position()                                           
        self.msg.x = x
        self.msg.y = y
        self.msg.z = z

        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        self.publisher_.publish(self.msg)


def main(args=None):
    rclpy.init(args=args)

    position_publisher = PositionPublisher()

    rclpy.spin(position_publisher)

    position_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()