from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

import os
import xacro
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # The name of the package the robot description is in.
    package_name = 'custom_robot_sim'

    package_path = get_package_share_directory(package_name)

    # Compile the URDF Xacro description of the robot into pure XML.
    xacro_file = os.path.join(package_path, 'urdf', 'robot_description.urdf.xacro')
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
        launch_arguments={'gz_args': '-r ' + world_file}.items()
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

    return LaunchDescription([
        node_robot_state_publisher,
        gazebo_sim,
        node_spawn_entity,
        node_ros_gz_bridge,
    ])