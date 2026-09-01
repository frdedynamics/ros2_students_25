from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

import os, time
import xacro
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    package_name = 'my_robotarm_pkg'

    package_path = os.path.join(
        get_package_share_directory(package_name))
    xacro_file = os.path.join(package_path,
                              'urdf/',
                              'my_robotarm_with_ee.xacro')
    
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

    node_joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    node_tf = Node(package = "tf2_ros", 
                       executable = "static_transform_publisher",
                       arguments = ["0", "0", "0", "0", "0", "0", "map", "base_link"])

    node_rviz = Node(
        package='rviz2',
        namespace='',
        executable='rviz2',
        name='rviz2',
        arguments=['-d' + os.path.join(get_package_share_directory(package_name), 'config', 'config.rviz')]
    )

    return LaunchDescription([
        node_robot_state_publisher,
        node_joint_state_publisher_gui,
        node_tf,
        node_rviz
    ])
