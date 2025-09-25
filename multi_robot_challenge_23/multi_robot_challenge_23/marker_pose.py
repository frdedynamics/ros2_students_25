import rclpy
from rclpy.node import Node

from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from ros2_aruco_interfaces.msg import ArucoMarkers
from geometry_msgs.msg import Pose
from std_msgs.msg import Int64

import tf2_geometry_msgs

class MarkerMapPose(Node):
    def __init__(self):
        super().__init__('MarkerMapPose')

        #Initiate a ROS parameter with a default value and then read the parameters value
        self.declare_parameter('namespace', 'tb3_5')
        self.namespace = self.get_parameter('namespace').get_parameter_value().string_value

        self.marker_id = 1000
        self.marker_pose = Pose()
        self.marker_recieved = False

        self.marker_recognition_sub = self.create_subscription(ArucoMarkers, '/'+self.namespace+'/aruco_markers', self.clbk_marker_recognition, 10)
        self.marker_map_pose_pub = self.create_publisher(Pose, '/'+self.namespace+'/marker_map_pose', 10)
        self.marker_id_pub = self.create_publisher(Int64,'/'+self.namespace+'/marker_id', 10)

        #Initialize a transform listener that is later used for looking up tranformations from one frame to another
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)


    def clbk_marker_recognition(self, msg):
        self.marker_id = msg.marker_ids[0]
        self.marker_pose = msg.poses[0]

    def timer_callback(self):
        marker_map_pose = Pose()
        from_frame_rel = self.namespace+'/camera_rgb_optical_frame'
        to_frame_rel = 'map'
        marker_id_msg = Int64()

        #Lookup the tranformation from from_frame_rel to to_frame_rel
        try:
            self.trans_camera_map = self.tf_buffer.lookup_transform(to_frame_rel, from_frame_rel, rclpy.time.Time())
        except TransformException as ex:
            self.get_logger().info(
                f'Could not transform {to_frame_rel} to {from_frame_rel}: {ex}')
            return

        #Tranform a Pose from from_frame_rel to to_frame_rel
        marker_map_pose = tf2_geometry_msgs.do_transform_pose(self.marker_pose, self.trans_camera_map)

        if self.marker_id != 1000:
            self.marker_map_pose_pub.publish(marker_map_pose)
            marker_id_msg.data = self.marker_id
            self.marker_id_pub.publish(marker_id_msg)

def main(args=None):
    rclpy.init(args=args)

    controller = MarkerMapPose()

    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()