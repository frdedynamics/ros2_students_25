import random

import rclpy
from rclpy.node import Node

from communication_patterns_interfaces.msg import Position
from communication_patterns_interfaces.srv import GetRobotFootprint

class RobotFootprintService(Node):

    def __init__(self):
        super().__init__('robot_footprint_service')
        self.srv = self.create_service(GetRobotFootprint, 'get_robot_footprint', self.service_clbk)

    def service_clbk(self, request, response):
        if request.robot_id == "tb3_0":
            response.success = True
            response.robot_position = Position()
            response.robot_position.x = random.randrange(1,10000)/10000
            response.robot_position.y = random.randrange(1,10000)/10000
            response.robot_position.z = random.randrange(1,10000)/10000
            response.footprint_radius = 0.3
        else:
            response.success = False
            response.robot_position = Position()
            response.footprint_radius = 0.0

        return response


def main(args=None):
    rclpy.init(args=args)

    robot_footprint_service = RobotFootprintService()

    rclpy.spin(robot_footprint_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()