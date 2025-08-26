#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class myPublisherNode(Node):
    def __init__(self) -> None:
        super().__init__("my_publisher")
        self.pub = self.create_publisher(String, 'topic', 10)
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World'
        self.pub.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    node = myPublisherNode()
    rclpy.spin(node)

    rclpy.shutdown()

if __name__ == '__main__':
    main()