#!/usr/bin/env python3

import os
os.environ["KERAS_BACKEND"] = "tensorflow"  # Or "jax" or "torch"!

from tensorflow import data as tf_data
import tensorflow_datasets as tfds
import keras
import keras_cv
from keras_cv import bounding_box
import tqdm
import rclpy
from rclpy.node import Node
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image

class ProjectMLIdea(Node):
    def __init__(self):
        super().__init__('project_ml_idea_node')
        self.bridge = CvBridge()
        
        self.subscription = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)

        self.pretrained_model = keras_cv.models.YOLOV8Detector.from_preset(
            "yolo_v8_m_pascalvoc", bounding_box_format="xywh"
        )

        self.class_ids = [
            "Aeroplane",
            "Bicycle",
            "Bird",
            "Boat",
            "Bottle",
            "Bus",
            "Car",
            "Cat",
            "Chair",
            "Cow",
            "Dining Table",
            "Dog",
            "Horse",
            "Motorbike",
            "Person",
            "Potted Plant",
            "Sheep",
            "Sofa",
            "Train",
            "Tvmonitor",
            "Total",
        ]

        self.threshold = 0.5
        
        self.class_mapping = dict(zip(range(len(self.class_ids)), self.class_ids))

        self.inference_resizing = keras_cv.layers.Resizing(
            640, 640, pad_to_aspect_ratio=True, bounding_box_format="xywh"
        )

        
    def image_callback(self, data):
        # This converts the image from ROS Image message to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(f"CvBridge Error: {e}")
            return

        image_batch = self.inference_resizing([cv_image])

        predictions = self.pretrained_model.predict(image_batch)

        boxes = predictions['boxes'][0]  # Accessing the first (and only) batch
        confidences = predictions['confidence'][0]
        classes = predictions['classes'][0]

        # Filter boxes based on a confidence threshold        
        for box, score, cls in zip(boxes, confidences, classes):
            if score > self.threshold and cls != -1:  # -1 indicates no detection
                print(self.class_ids[cls])
                print(score)
        
def main(args=None):
    rclpy.init(args=args)
    project_ml_idea = ProjectMLIdea()
    rclpy.spin(project_ml_idea)
    project_ml_idea.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
