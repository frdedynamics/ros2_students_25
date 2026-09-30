from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    navigation_server = Node(
        package="communication_patterns",
        executable="navigation_server",
        name="navigation_server_node" 
    )

    navigation_client = Node(
        package="communication_patterns",
        executable="navigation_client",
        name="navigation_client_node" 
    )
    
    return LaunchDescription([
        navigation_server, 
        navigation_client,
    ])