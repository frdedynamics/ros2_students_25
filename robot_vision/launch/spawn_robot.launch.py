import os
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
    package_name = 'robot_vision'  # Replace with your package name
    world_file_path = os.path.join(get_package_share_directory(package_name), 'worlds', 'rv_world.world')

    # Get the path to the Xacro file
    package_name_robot = 'braitenberg_vehicle'
    xacro_file_path = os.path.join(get_package_share_directory(package_name_robot), 'urdf', 'turtlebot3_waffle_pi.urdf.xacro')
    sphere_urdf_path = os.path.join(get_package_share_directory(package_name), 'urdf', 'moving_sphere.urdf.xacro')

    tb3_pos = ['0.0', '0.0', '0.0']
    tb3_yaw = '1.57079632679'

    # Use xacro to process the file
    robot_description_raw = xacro.process_file(xacro_file_path).toxml()

    # Use xacro to process the sphere file
    sphere_description_raw = xacro.process_file(sphere_urdf_path).toxml()

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

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_raw,
            'use_sim_time': use_sim_time
        }]
    )

    # State publisher for the sphere
    node_sphere_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': sphere_description_raw,
            'use_sim_time': use_sim_time
        }],
        namespace='moving_sphere'
    )

    spawn_entity = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'tb3',
            '-x', tb3_pos[0], '-y', tb3_pos[1], '-z', tb3_pos[2], '-Y', tb3_yaw
        ],
        output='screen'
    )

    # Spawn the sphere in Gazebo
    spawn_sphere_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'moving_sphere/robot_description',
            '-entity', 'moving_sphere',
            '-x', '0.0', '-y', '2.0', '-z', '0.1'
        ],
        output='screen'
    )
    
    # Sphere commander node
    command_sphere_node = Node(
        package=package_name,
        executable='command_sphere',
        name='command_sphere',
        output='screen',
    )


    # Run the node
    return LaunchDescription([
        sim_time_arg,
        gazebo,
        node_robot_state_publisher,
        node_sphere_state_publisher,
        spawn_entity,
        spawn_sphere_entity,
        command_sphere_node
    ])
