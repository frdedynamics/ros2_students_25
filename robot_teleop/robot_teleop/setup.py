from setuptools import setup
import os
from glob import glob

package_name = 'robot_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rocotics',
    maintainer_email='rocotics@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'keyboard_control = robot_teleop.keyboard_control:main',
            'robot_teleop = robot_teleop.robot_teleop:main',
            'reset_robot = robot_teleop.reset_robot:main',
            'replay_velocities = robot_teleop.replay_velocities:main'
        ],
    },
)
