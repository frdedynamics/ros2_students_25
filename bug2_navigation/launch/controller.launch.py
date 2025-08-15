import launch
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='bug2_navigation',
            executable='wallfollower_controller',
            name='wallfollower_controller'),
        launch_ros.actions.Node(
            package='bug2_navigation',
            executable='gotopoint_controller',
            name='gotopoint_controller'),
        launch_ros.actions.Node(
            package='bug2_navigation',
            executable='bug2_controller',
            name='bug2_controller'),
        launch_ros.actions.Node(
            package='bug2_navigation',
            executable='robot_controller',
            name='robot_controller'),
  ])