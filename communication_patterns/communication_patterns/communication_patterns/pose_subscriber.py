import rclpy
from rclpy.node import Node

from communication_patterns_interfaces.msg import Pose, Position, Orientation


class PoseSubscriber(Node):

    def __init__(self):
        super().__init__('pose_subscriber')

        self.success = False
        self.position = Position()
        self.orienation = Orientation()


        self.create_subscription(Pose, 'pose', self.clbk_pose, 10)
        self.create_subscription(Position, 'position', self.clbk_position, 10)
        self.create_subscription(Orientation, 'orientation', self.clbk_orientation, 10)



    def clbk_pose(self, msg):
        self.success = True

        if msg.position != self.position:
            self.success = False
        if msg.orientation != self.orienation:
            self.success = False

        self.get_logger().info(f"Success: {self.success}")

    def clbk_position(self, msg):
        self.position = msg

    def clbk_orientation(self, msg):
        self.orienation = msg


def main(args=None):
    rclpy.init(args=args)

    pose_subscriber = PoseSubscriber()

    rclpy.spin(pose_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pose_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()