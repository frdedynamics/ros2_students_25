import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'multi_robot_challenge_23'

    # Get the path to the world, map and rviz configuration file
    world_file_path = os.path.join(get_package_share_directory(package_name), 'worlds', 'dat160_w2.world')
    map_file_path = os.path.join(get_package_share_directory(package_name), 'maps', 'map_dat160_w2.yaml')
    rviz_config_file_path = os.path.join(get_package_share_directory(package_name), 'rviz', 'model.rviz')

    # Namespace of each robot
    first_tb3 = 'tb3_0'
    second_tb3 = 'tb3_1'
    # Starting position in the gazebo world of each robot
    first_tb3_pos = ['-1.0', '1.0', '0.0']
    second_tb3_pos = ['-1.0', '-1.0', '0.0']
    #Starting orientation in the gazebo world of each robot
    first_tb3_yaw = '0.0'
    second_tb3_yaw = '0.0'

    # Declaring use_sim_time as a launch argument that can then be used in all launch files
    sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    # Get launch argument use_sim_time as a launch configuration object
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Starting Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
        launch_arguments={'world': world_file_path}.items()
    )

    # Starting Map Server
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{"yaml_filename": map_file_path, "topic_name": "map", "frame_id": "map"}],
        # remappings=remappings
    )
    # Starting a lifecycle manager that takes care of the map server
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time},
                    {'autostart': True},
                    {'node_names': ["map_server"]}]
    )

    # Spawning the first robot
    tb3_0 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(package_name), 'launch'), '/spawn_robot.launch.py']),
        launch_arguments={
            'namespace': first_tb3,
            'x': first_tb3_pos[0],
            'y': first_tb3_pos[1],
            'yaw': first_tb3_yaw,
        }.items()
    )

    # Spawning the second robot 
    tb3_1 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(package_name), 'launch'), '/spawn_robot.launch.py']),
        launch_arguments={
            'namespace': second_tb3,
            'x': second_tb3_pos[0],
            'y': second_tb3_pos[1],
            'yaw': second_tb3_yaw,
        }.items()
    )

    # Starting rviz
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file_path],
        parameters=[{'use_sim_time': use_sim_time}],
        output='screen'
    )

    return LaunchDescription([
        sim_time_arg,
        gazebo,
        map_server,
        lifecycle_manager,
        tb3_0,
        tb3_1,
        rviz_node,
    ])