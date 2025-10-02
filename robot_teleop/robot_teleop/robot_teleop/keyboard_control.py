from pynput import keyboard
import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

#----------------------------------------------------------------------------------------------------
#TODO: import custom message type
from robot_teleop_interfaces.msg import Teleop
#----------------------------------------------------------------------------------------------------

class KeyboardNode(Node):
    def __init__(self):
        super().__init__('keyboard_node')

        #----------------------------------------------------------------------------------------------------
        #TODO: create a publisher with a custom msg type that has a twist object and an array of bool values.
        self.publisher = self.create_publisher(Teleop, '/teleop_device', 10)
        #----------------------------------------------------------------------------------------------------

        self.key_w = False
        self.key_a = False
        self.key_s = False
        self.key_d = False
        self.vel_msg = Twist()
        self.btns = [False, False, False, False]

        self.max_linear_vel = 0.5
        self.max_angular_vel = 1.0
        self.linear_vel_step = 0.05

        listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        listener.start()

        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def _on_press(self, key):
        if key == keyboard.KeyCode.from_char('w'):
            self.key_w = True
        if key == keyboard.KeyCode.from_char('s'):
            self.key_s = True
        if key == keyboard.KeyCode.from_char('a'):
            self.key_a = True
        if key == keyboard.KeyCode.from_char('d'):
            self.key_d = True
        if key == keyboard.KeyCode.from_char('j'):
            self.btns[0] = True
        if key == keyboard.KeyCode.from_char('k'):
            self.btns[1] = True
        if key == keyboard.KeyCode.from_char('l'):
            self.btns[2] = True
        if key == keyboard.KeyCode.from_char('c'):
            self.btns[3] = True

    def _on_release(self, key):
        if key == keyboard.KeyCode.from_char('w'):
            if self.vel_msg.linear.x > 0.0:
                self.vel_msg.linear.x = 0.0
            self.key_w = False
        if key == keyboard.KeyCode.from_char('s'):
            self.key_s = False
            if self.vel_msg.linear.x < 0.0:
                self.vel_msg.linear.x = 0.0
        if key == keyboard.KeyCode.from_char('a'):
            self.key_a = False
        if key == keyboard.KeyCode.from_char('d'):
            self.key_d = False
        if key == keyboard.KeyCode.from_char('j'):
            self.btns[0] = False
        if key == keyboard.KeyCode.from_char('k'):
            self.btns[1] = False
        if key == keyboard.KeyCode.from_char('l'):
            self.btns[2] = False
        if key == keyboard.KeyCode.from_char('c'):
            self.btns[3] = False

    def timer_callback(self):
        # if a is pressed turn left; if d is pressed turn right; if both a and d are pressed don't turn
        self.vel_msg.angular.z = 0.0
        if self.key_a:
            self.vel_msg.angular.z += self.max_angular_vel
        if self.key_d:
            self.vel_msg.angular.z -= self.max_angular_vel

        # w or s is pressed increase target velocity over time
        if self.key_w and self.vel_msg.linear.x < self.max_linear_vel:
            self.vel_msg.linear.x += self.linear_vel_step
        elif self.key_s and self.vel_msg.linear.x > -self.max_linear_vel:
            self.vel_msg.linear.x -= self.linear_vel_step

        #----------------------------------------------------------------------------------------------------
        #TODO: create a msg of the custom message type and assign self.vel_msg and self.btns
        msg = Teleop()
        msg.velocity = self.vel_msg
        msg.buttons = self.btns
        #----------------------------------------------------------------------------------------------------

        #----------------------------------------------------------------------------------------------------
        #TODO: publish the message
        self.publisher.publish(msg)
        #----------------------------------------------------------------------------------------------------

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