from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    collision_server = Node(
        package="communication_patterns",
        executable="collision_server",
        name="collision_server_node" 
    )

    collision_client = Node(
        package="communication_patterns",
        executable="collision_client",
        name="collision_client_node" 
    )
    
    return LaunchDescription([
        collision_server, 
        collision_client,
    ])