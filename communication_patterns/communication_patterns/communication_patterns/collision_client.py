import random

import rclpy
from rclpy.node import Node

from communication_patterns_interfaces.msg import Position
from communication_patterns_interfaces.srv import CheckCollision

class CheckCollisionClient(Node):

    def __init__(self):
        super().__init__('check_collision_client')
        self.cli = self.create_client(CheckCollision, 'check_collision')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = CheckCollision.Request()

    def send_request(self):
        self.req.object_position = Position()
        self.req.object_position.x = random.randrange(1,10000)/10000
        self.req.object_position.y = random.randrange(1,10000)/10000
        self.req.object_position.z = random.randrange(1,10000)/10000
        self.req.object_radius = 0.3

        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)

    check_collision_client = CheckCollisionClient()
    response = check_collision_client.send_request()
    if response.in_collision:
        check_collision_client.get_logger().info(f"Object is in collision with the robot!")
    else:
        check_collision_client.get_logger().info(f"Object is NOT colliding with the robot.")

    check_collision_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()