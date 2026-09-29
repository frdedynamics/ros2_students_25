import rclpy
from rclpy.node import Node

#TODO: import the required service type that is needed for the client


class RobotFootprintClient(Node):
    def __init__(self):
        super().__init__('robot_footprint_client')

        #TODO: Create a client to the "get_robot_footprint" service
        

        #TODO: Wait for the service to become active
        
        

    def send_request(self):
        #TODO: Create a request object for the service client and define the ID of the robot in that object as "tb3_0"
        

        #TODO: Send the request to the server and wait for the server to awnser
       

        #TODO: Use the response of the server to do the following: 
        # assign the x and y position of the robot to the variables x and y 
        # and assign the radius of the footprint to the variable r 
        

        self.get_logger().info(f"Robot Position: x={x}, y={y}")
        self.get_logger().info(f"Robot Footprint Radius: {r}")



def main(args=None):
    rclpy.init(args=args)

    robot_footprint_client = RobotFootprintClient()
    robot_footprint_client.send_request()

    robot_footprint_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()