from setuptools import setup
import os 
from glob import glob 

package_name = 'communication_patterns'

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
            'position_publisher = communication_patterns.position_publisher:main',
            'orientation_publisher = communication_patterns.orientation_publisher:main',
            'pose_publisher = communication_patterns.pose_publisher:main',
            'pose_subscriber = communication_patterns.pose_subscriber:main',
            'collision_client = communication_patterns.collision_client:main',
            'collision_server = communication_patterns.collision_server:main',
            'robot_footprint_server = communication_patterns.robot_footprint_server:main',
            'robot_footprint_client = communication_patterns.robot_footprint_client:main',
            'coffee_server = communication_patterns.coffee_server:main',
            'coffee_client = communication_patterns.coffee_client:main',
            'navigation_server = communication_patterns.navigation_server:main',
            'navigation_client = communication_patterns.navigation_client:main',
        ],
    },
)
