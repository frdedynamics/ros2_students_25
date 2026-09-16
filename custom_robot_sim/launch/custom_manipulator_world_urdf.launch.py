from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

import os
import xacro
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # The name of the package the robot description is in.
    package_name = 'custom_robot_sim'

    package_path = get_package_share_directory(package_name)

    # Compile the URDF Xacro description of the robot into pure XML.
    xacro_file = os.path.join(package_path, 'urdf', 'robot_stand.urdf.xacro')
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    my_robotarm_description = doc.toxml()
    
    params = {'robot_description': my_robotarm_description, 'use_sim_time': True}

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # We need a world map to run most of the sensor plug-ins in Gazebo.
    # Feel free to change it to another world and see how the simulation will change!
    world_file = os.path.join(package_path, 'worlds', 'empty_world.sdf')

    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r ' + world_file +' --physics-engine gz-physics-bullet-featherstone-plugin'}.items()
    )

    node_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'custom_manipulator_robot',
            '-z', '0.1'
        ],
        output='screen'
    )

    node_ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        # The arguments are to make the entities in the Gazebo GUI to be available to the ROS such as clock, joint states, camera etc.
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo'
        ],
        output='screen'
    )

    node_joint_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    # This is the node allows you to control your robot arm.
    node_arm_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_controller"],
        output="screen",
    )

    gz_spawn_world_objects = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [PathJoinSubstitution([FindPackageShare('custom_robot_sim'), 'launch', 'spawn_world_objects.launch.py'])]
        )
    )

    return LaunchDescription([
        node_robot_state_publisher,
        gazebo_sim,
        node_spawn_entity,
        node_ros_gz_bridge,
        node_joint_broadcaster,
        node_arm_controller,
        gz_spawn_world_objects
    ])