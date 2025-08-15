#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class CameraViz(Node):
    def __init__(self):
        super().__init__('camera_viz')
        self.bridge = CvBridge()
        
        self.subscription = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        
    def image_callback(self, data):
        # This converts the image from ROS Image message to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(f"CvBridge Error: {e}")
            return
        
        cv2.imshow("Camera viz", cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    camera_viz = CameraViz()
    rclpy.spin(camera_viz)
    camera_viz.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
