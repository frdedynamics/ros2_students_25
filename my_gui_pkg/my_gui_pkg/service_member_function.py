from motor_srvcli.srv import Motor

import rclpy
from rclpy.node import Node

from custom_dxl.CustomDXL import CustomDXL


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(Motor, 'motor', self.motor_callback)
        self.custom_dxl = CustomDXL([0, 4])
        self.custom_dxl.open_port()

    def motor_callback(self, request, response):
        self.custom_dxl.send_single_goal(motor_order=1, goal_pos=request.goal_pos)
        response.complete_flag = True
        self.get_logger().info('Incoming request\ngoal_pos: %d complete_flag: %d' % (request.goal_pos, response.complete_flag))

        return response


def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()