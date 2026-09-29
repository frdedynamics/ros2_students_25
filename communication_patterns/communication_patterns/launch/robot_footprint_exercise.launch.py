from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    robot_footprint_server = Node(
        package="communication_patterns",
        executable="robot_footprint_server",
        name="robot_footprint_server_node" 
    )

    robot_footprint_client = Node(
        package="communication_patterns",
        executable="robot_footprint_client",
        name="robot_footprint_client_node" 
    )
    
    return LaunchDescription([
        robot_footprint_server, 
        robot_footprint_client,
    ])