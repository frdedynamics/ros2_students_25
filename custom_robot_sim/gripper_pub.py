import rclpy

from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class GripperPublisher(Node):

    def __init__(self):
        super().__init__('gripper_controller')

        self.gripper_publisher = self.create_publisher(Float64MultiArray, "gripper_controller/commands", 10)
        
        self.open_pos_msg = Float64MultiArray()
        self.open_pos_msg.data = [0.0]
        
        self.closed_pos_msg = Float64MultiArray()
        self.closed_pos_msg.data = [0.08]

        self.move_to_target  = False
        self.cntr = 0

        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        self.cntr += 1
        if self.cntr > 20:
            self.move_to_target = not self.move_to_target
            self.cntr = 0
        

        if self.move_to_target:
            self.gripper_publisher.publish(self.open_pos_msg)
        else:
            self.gripper_publisher.publish(self.closed_pos_msg)



def main(args=None):

    rclpy.init(args=args)
    gripper_object = GripperPublisher()

    rclpy.spin(gripper_object)
    
    gripper_object.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()