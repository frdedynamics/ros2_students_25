import rclpy
from rclpy.node import Node

#TODO: import the required message types



class PosePublisher(Node):

    def __init__(self):
        super().__init__('pose_publisher')

        self.position = Position()
        self.orienation = Orientation()

        #TODO: create a subscriber to the "position" topic. As a callback function use self.clbk_position
        

        #TODO: create a subscriber to the "position" topic. As a callback function use self.clbk_position
        

        #TODO: create a publisher to teh "pose" topic.
        
        
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):

        #TODO: create a message object of type Pose and fill it with the information from your subscribers
        

        #TODO: publish the message
        
        pass


    def clbk_position(self, msg):
        self.position = msg

    def clbk_orientation(self, msg):
        self.orienation = msg


def main(args=None):
    rclpy.init(args=args)

    pose_publisher = PosePublisher()

    rclpy.spin(pose_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pose_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()