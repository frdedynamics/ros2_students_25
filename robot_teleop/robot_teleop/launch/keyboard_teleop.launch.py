import launch
import launch_ros
import os
import xacro

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # package_name = 'braitenberg_vehicle'
    # xacro_file_path = os.path.join(get_package_share_directory(package_name), 'urdf', 'turtlebot3_waffle_pi.urdf.xacro')
    # robot_description = xacro.process_file(xacro_file_path).toxml()

    package_name_robot = 'multi_robot_challenge_23'
    xacro_file_name = 'turtlebot3_waffle_pi.urdf.xacro'
    xacro_file_path = os.path.join(get_package_share_directory(package_name_robot), 'urdf', xacro_file_name)
    mesh_dir = os.path.join(get_package_share_directory('turtlebot3_description'),'meshes')

    tb3_0_robot_description = xacro.process_file(
        xacro_file_path, 
        mappings={
            "mesh_dir": mesh_dir,
            "namespace": 'tb3_0',
        },
    ).toxml()

    tb3_1_robot_description = xacro.process_file(
        xacro_file_path, 
        mappings={
            "mesh_dir": mesh_dir,
            "namespace": 'tb3_1',
        },
    ).toxml()

    keyboard_node = launch_ros.actions.Node(
            package='robot_teleop',
            executable='keyboard_control',
            namespace='',
            name='keyboard_control',)
    
    robot_teleop_node = launch_ros.actions.Node(
            package='robot_teleop',
            executable='robot_teleop',
            namespace='',
            name='robot_teleop',
            parameters=[
                {'tb3_0_description': tb3_0_robot_description,
                 'tb3_1_description': tb3_1_robot_description}
            ])
    
    reset_robot_node = launch_ros.actions.Node(
            package='robot_teleop',
            executable='reset_robot',
            namespace='',
            name='reset_robot',)
    
    replay_velocities_node = launch_ros.actions.Node(
        package='robot_teleop',
        executable='replay_velocities',
        namespace='',
        name='replay_velocities',
    )
   

    return launch.LaunchDescription([
        keyboard_node,
        robot_teleop_node,
        reset_robot_node,
        replay_velocities_node
    ])
