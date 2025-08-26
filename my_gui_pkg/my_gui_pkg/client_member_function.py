import sys

from motor_srvcli.srv import Motor
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(Motor, 'motor')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Motor.Request()

    def send_request(self, goal_pos):
        self.req.goal_pos = goal_pos
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)

    if len(sys.argv) < 3:
        print("Usage: ros2 run my_gui_pkg client <goal_pos:int> <complete_flag:0|1>")
        return

    minimal_client = MinimalClientAsync()
    response = minimal_client.send_request(int(sys.argv[1]))
    minimal_client.get_logger().info(
        'Received %d, Flag: %d' %
        (int(sys.argv[1]), response.complete_flag))

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()