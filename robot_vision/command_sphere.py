import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rosgraph_msgs.msg import Clock
import numpy as np

# DO NOT MODIFY THIS FILE
class CommandSphereNode(Node):
    def __init__(self):
        super().__init__('command_sphere')
        self.publisher_ = self.create_publisher(Twist, '/moving_sphere/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.subscription = self.create_subscription(
            Clock,
            '/clock',
            self.clock_callback,
            10)
        self.subscription  # prevent unused variable warning
        # Define waypoints
        self.waypoints = np.array([[0, 0], [7, 5], [0, 10], [7, 15]])
        self.times = np.linspace(0, 30, len(self.waypoints))  # Assume we spend 30 seconds to go through all waypoints
        self.last_position_x = 0.0   
        self.last_position_y = 0.0
        self.current_time = 0.0
        self.last_time = 0.0

    def clock_callback(self, msg):
        self.current_time = msg.clock.sec + msg.clock.nanosec / 1e9

    def timer_callback(self):
        msg = Twist()
        delta_t = (self.current_time - self.last_time)
        
        # Get position from interpolations
        position_x = np.interp(self.current_time, self.times, self.waypoints[:, 0])
        position_y = np.interp(self.current_time, self.times, self.waypoints[:, 1])

        # Calculate velocity
        velocity_x = (position_x - self.last_position_x) / delta_t
        velocity_y = (position_y - self.last_position_y) / delta_t

        # Set velocities
        msg.linear.x = velocity_x
        msg.linear.y = velocity_y

        self.publisher_.publish(msg)

        # Update last position
        self.last_position_x = position_x
        self.last_position_y = position_y
        self.last_time = self.current_time

def main(args=None):
    rclpy.init(args=args)
    node = CommandSphereNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
