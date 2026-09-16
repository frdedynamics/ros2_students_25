# Copyright 2024 ros2_control Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Get URDF via xacro
    table_description = Command(
        [
            PathJoinSubstitution([FindExecutable(name='xacro')]),
            ' ',
            PathJoinSubstitution(
                [FindPackageShare('custom_robot_sim'),
                    'urdf', 'table.urdf.xacro']
            ),
        ]
    )

    box_description = Command(
        [
            PathJoinSubstitution([FindExecutable(name='xacro')]),
            ' ',
            PathJoinSubstitution(
                [FindPackageShare('custom_robot_sim'),
                    'urdf', 'box.urdf.xacro']
            ),
        ]
    )

    cube_description = Command(
        [
            PathJoinSubstitution([FindExecutable(name='xacro')]),
            ' ',
            PathJoinSubstitution(
                [FindPackageShare('custom_robot_sim'),
                    'urdf', 'cube.urdf.xacro']
            ),
        ]
    )

    gz_spawn_table_1 = Node(
            package='ros_gz_sim',
            executable='create',
            output='screen',
            parameters=[{
                'string': table_description,
                'name': 'table_1',
                'allow_renaming': True,
                'x': 0.0,
                'y': 0.6,
                'z': 1.0,
            }],
        )

    gz_spawn_table_2 = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        parameters=[{
            'string': table_description,
            'name': 'table_2',
            'allow_renaming': True,
            'x': 0.0,
            'y': -0.6,
            'z': 1.0,
        }],
    )

    gz_spawn_box = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        parameters=[{
            'string': box_description,
            'name': 'box',
            'allow_renaming': True,
            'x': 0.0,
            'y': -0.6,
            'z': 1.5,
        }],
    )

    gz_spawn_cube = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        parameters=[{
            'string': cube_description,
            'name': 'cube',
            'allow_renaming': True,
            'x': 0.0,
            'y': 0.6,
            'z': 1.5,
        }],
    )
    
    return LaunchDescription([
        gz_spawn_table_1,
        gz_spawn_table_2,
        gz_spawn_box,
        gz_spawn_cube,
    ])