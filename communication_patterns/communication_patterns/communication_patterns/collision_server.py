import math
import random

import rclpy
from rclpy.node import Node

from communication_patterns_interfaces.msg import Position
#TODO: Import the correct service type for the service server


class CheckCollisionService(Node):

    def __init__(self):
        super().__init__('check_collision_service')

        #TODO: Create a service server with the following parameters: 
        # is available under "check_collision"
        # uses the CheckCollision service type
        # uses self.clbk_collision as a callback function
        

    def clbk_collision(self, request, response):
        self.robot_position = Position()
        self.robot_position.x = random.randrange(1,10000)/10000
        self.robot_position.y = random.randrange(1,10000)/10000
        self.robot_radius = 0.3

        #TODO: from the clients request save 
        # the position of the object in self.object_position
        # and the radius of the object in self.object_radius
        

        
        dist = math.sqrt(math.pow(self.robot_position.x - self.object_position.x,2)+math.pow(self.robot_position.y - self.object_position.y,2))
        if dist < (self.robot_radius + self.object_radius):
            #TODO: response should specify that the object is in collision with the object
            
            pass
        else:
            #TODO: response should specify that the object is NOT in collision with the object
            
            pass
        
        return response


def main(args=None):
    rclpy.init(args=args)

    check_collision_service = CheckCollisionService()

    rclpy.spin(check_collision_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()