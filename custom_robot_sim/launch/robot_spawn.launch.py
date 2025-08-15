import os
import launch_ros
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
import xacro


def generate_launch_description():
    # Get the path to the Gazebo world file
    package_name = 'custom_robot_sim'
    
    # Define location of the xacro file that describes the robot model
    # xacro_file_path = os.path.join(get_package_share_directory(package_name), 'urdf', 'mobile_manipulator.urdf.xacro')
    xacro_file_path = "/home/rocotics/ros2_ws/src/custom_robot_sim/urdf/robot_description.urdf.xacro"

    #Robot starting position and orientation
    robot_pos = ['0.0', '0.0', '0.0']
    robot_yaw = '0.0'

    #Transform the xacro file into an xml description
    robot_description_raw = xacro.process_file(xacro_file_path).toxml()

    # Declaring use_sim_time as a launch argument that can then be used in all launch files
    sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    # Get launch argument use_sim_time as a launch configuration object
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Publish the robot model description
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_raw,
            'use_sim_time': use_sim_time
        }]
    )

    # Spawn the model description published with robot_state_publisher into gazebo with a predefined spawn location
    spawn_entity = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'mobile_manipulator',
            '-x', robot_pos[0], '-y', robot_pos[1], '-z', robot_pos[2], '-Y', robot_yaw
        ],
        output='screen'
    )

    reset_robot_node = launch_ros.actions.Node(
            package='custom_robot_sim',
            executable='reload_robot_model',
            namespace='',
            name='reload_robot_model',
            parameters=[
                {'xacro_file_path': xacro_file_path}
            ])

    return LaunchDescription([
        sim_time_arg,
        node_robot_state_publisher,
        spawn_entity,
        reset_robot_node
    ])