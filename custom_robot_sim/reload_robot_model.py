from pynput import keyboard
import rclpy
import time
from rclpy.node import Node
import xacro

from geometry_msgs.msg import Pose
# from robot_teleop_interfaces.msg import Teleop
from gazebo_msgs.srv import DeleteEntity, SpawnEntity
#import teleop msg type

class KeyboardNode(Node):
    def __init__(self):
        super().__init__('keyboard_node')

        #create teleop publisher
        # self.publisher = self.create_publisher(Teleop, '/teleop_device', 10)
        
        self.declare_parameter('xacro_file_path', '')
        self.xacro_file_path = self.get_parameter('xacro_file_path').get_parameter_value().string_value

        self.key_k = False
        self.robot_reseting = False
        self.robot_name = "mobile_manipulator"
        self.robot_init_pose = Pose()

        # self.max_linear_vel = 0.5
        # self.max_angular_vel = 1.0
        # self.linear_vel_step = 0.05
        self.srv_del_entity = self.create_client(DeleteEntity, '/delete_entity')
        self.srv_spawn_entity = self.create_client(SpawnEntity, '/spawn_entity')
        while not self.srv_del_entity.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for gazebo delete service")
        while not self.srv_spawn_entity.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("waiting for gazebo spawn service")

        listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        listener.start()

        # timer_period = 0.1  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        
    
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
        # spawn_req.robot_namespace = name
        spawn_req.initial_pose = initial_pose
        
        self.future = self.srv_spawn_entity.call_async(spawn_req)
        time.sleep(1.0)

    def reset_robot(self):
        self.robot_reseting = True
        self.robot_description = xacro.process_file(self.xacro_file_path).toxml()
        self.delete_robot(self.robot_name)
        self.spawn_robot(name=self.robot_name, robot_description=self.robot_description, initial_pose=self.robot_init_pose)


    def _on_press(self, key):
        if key == keyboard.KeyCode.from_char('k'):
            self.key_k = True

        if self.key_k and not self.robot_reseting:
            self.reset_robot()

    def _on_release(self, key):
        if key == keyboard.KeyCode.from_char('k'):
            self.key_k = False

        if self.robot_reseting: self.robot_reseting = False

    # def timer_callback(self):
    #     # if a is pressed turn left; if d is pressed turn right; if both a and d are pressed don't turn
    #     self.vel_msg.angular.z = 0.0
    #     if self.key_a:
    #         self.vel_msg.angular.z += self.max_angular_vel
    #     if self.key_d:
    #         self.vel_msg.angular.z -= self.max_angular_vel

    #     # w or s is pressed increase target velocity over time
    #     if self.key_w and self.vel_msg.linear.x < self.max_linear_vel:
    #         self.vel_msg.linear.x += self.linear_vel_step
    #     elif self.key_s and self.vel_msg.linear.x > -self.max_linear_vel:
    #         self.vel_msg.linear.x -= self.linear_vel_step

    #     #Create teleop msg
    #     msg = Teleop()
    #     msg.velocity = self.vel_msg
    #     msg.buttons = self.btns

    #     #Publish teleop msg
    #     self.publisher.publish(msg)
        

def main(args=None):
    rclpy.init(args=args)

    keyboard_node = KeyboardNode()

    rclpy.spin(keyboard_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    keyboard_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()