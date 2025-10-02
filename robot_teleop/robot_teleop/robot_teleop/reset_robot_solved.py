import rclpy
import time
from rclpy.node import Node

from gazebo_msgs.srv import DeleteEntity, SpawnEntity

#----------------------------------------------------------------------------------------------------
#TODO: import service definition
from robot_teleop_interfaces.srv import ResetRobot
#----------------------------------------------------------------------------------------------------

class ResetRobotService(Node):

    def __init__(self):
        super().__init__('reset_robot_service')

        #----------------------------------------------------------------------------------------------------
        #TODO: create a reset robot service which has the following variables:
        #      request:
        #           robot_name (string)
        #           robot_description (string)      
        #           reset_pose (geometry_msgs Pose)    
        #      response:
        #           success (bool)
        self.srv = self.create_service(ResetRobot, '/reset_robot', self.clbk_reset_robot)
        #----------------------------------------------------------------------------------------------------

        self.srv_del_entity = self.create_client(DeleteEntity, '/delete_entity')
        self.srv_spawn_entity = self.create_client(SpawnEntity, '/spawn_entity')
        while not self.srv_del_entity.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for gazebo delete service")
        while not self.srv_spawn_entity.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for gazebo spawn service")

    #----------------------------------------------------------------------------------------------------
    #TODO: create a callback function for the reset robot service
    #      use delete_robot() and spawn_robot() functions
    def clbk_reset_robot(self, request, response):
        self.delete_robot(request.robot_name)
        self.spawn_robot(
            name=request.robot_name,
            robot_description=request.robot_description,
            initial_pose=request.reset_pose
        )

        response.success = True

        return response
    #----------------------------------------------------------------------------------------------------

    def delete_robot(self, robot_name):
        self.get_logger().info("Deleting robot")

        del_req = DeleteEntity.Request()
        del_req.name = robot_name

        self.future = self.srv_del_entity.call_async(del_req)
        time.sleep(1.0)

    def spawn_robot(self, name, robot_description, initial_pose):
        self.get_logger().info(f"Spawning Robot")

        spawn_req = SpawnEntity.Request()
        spawn_req.xml = robot_description
        spawn_req.name = name
        spawn_req.robot_namespace = name
        spawn_req.initial_pose = initial_pose
        
        self.future = self.srv_spawn_entity.call_async(spawn_req)
        time.sleep(1.0)

def main(args=None):
    rclpy.init(args=args)

    reset_robot_service = ResetRobotService()

    rclpy.spin(reset_robot_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()