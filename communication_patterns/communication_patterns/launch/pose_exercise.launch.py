from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    position_pub = Node(
        package="communication_patterns",
        executable="position_publisher",
        name="position_publisher_node" 
    )

    orientation_pub = Node(
        package="communication_patterns",
        executable="orientation_publisher",
        name="orientation_publisher_node" 
    )

    pose_pub = Node(
        package="communication_patterns",
        executable="pose_publisher",
        name="pose_publisher_node" 
    )

    pose_sub = Node(
        package="communication_patterns",
        executable="pose_subscriber",
        name="pose_subscriber_node" 
    )
    
    return LaunchDescription([
        position_pub, 
        orientation_pub,
        pose_pub,
        pose_sub,
    ])