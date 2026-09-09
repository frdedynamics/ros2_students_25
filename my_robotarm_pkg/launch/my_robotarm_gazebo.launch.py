from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

import os
import xacro
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    package_name = 'my_robotarm_pkg'

    package_path = get_package_share_directory(package_name)

    # This is our robot. If you change the xacro file to another one without inertia and collision tags, you won't see the robot in Gazebo.
    xacro_file = os.path.join(package_path, 'urdf', 'my_robotarm_gazebo.xacro')
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

    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )

    node_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'two_dof_robot',
            '-z', '0.1'
        ],
        output='screen'
    )

    node_ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        # Makes Gazebo's clock and joint states available to ROS.
        # Without ros2_control, this bridge is the ONLY source of /joint_states:
        # they come from the JointStatePublisher plugin inside the XACRO.
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/world/empty/model/two_dof_robot/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model'
        ],
        remappings=[
            ('/world/empty/model/two_dof_robot/joint_state', '/joint_states')
        ],
        output='screen'
    )

    node_tf = Node(
        package="tf2_ros", 
        executable="static_transform_publisher",
        arguments=["--frame-id", "world", "--child-frame-id", "base_link"],
        parameters=[params]
    )

    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d' + os.path.join(get_package_share_directory(package_name), 'config', 'config.rviz')],
        parameters=[params]
    )

    return LaunchDescription([
        node_robot_state_publisher,
        gazebo_sim,
        node_spawn_entity,
        node_ros_gz_bridge,
        node_tf,
        node_rviz
    ])