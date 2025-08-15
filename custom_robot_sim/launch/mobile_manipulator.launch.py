import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
import xacro


def generate_launch_description():
    # Get the path to the Gazebo world file
    package_name = 'custom_robot_sim'
    xacro_file_path = os.path.join(get_package_share_directory(package_name), 'urdf', 'mobile_manipulator.urdf.xacro')

    robot_pos = ['0.0', '0.0', '0.0']
    robot_yaw = '0.0'

    robot_description_raw = xacro.process_file(xacro_file_path).toxml()

    # Declaring use_sim_time as a launch argument that can then be used in all launch files
    sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )
    # Get launch argument use_sim_time as a launch configuration object
    use_sim_time = LaunchConfiguration('use_sim_time')

    #Starting Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
        # launch_arguments={'world': world_file_path}.items()
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

    spawn_entity = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'mobile_manipulator_robot',
            '-x', robot_pos[0], '-y', robot_pos[1], '-z', robot_pos[2], '-Y', robot_yaw
        ],
        output='screen'
    )

    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'start','joint_state_broadcaster'],
        output='screen'
    )

	
    load_joint_trajectory_controller = ExecuteProcess( 
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'start', 'joint_trajectory_controller'], 
        output='screen'
    )

    load_gripper_controller = ExecuteProcess( 
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'start', 'gripper_controller'], 
        output='screen'
    )

    return LaunchDescription([
        sim_time_arg,
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
        load_joint_state_broadcaster,
        load_joint_trajectory_controller,
        load_gripper_controller,
    ])