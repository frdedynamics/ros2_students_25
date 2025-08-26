from setuptools import setup

package_name = 'my_gui_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rocotics',
    maintainer_email='gizem.ates@hvl.no',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_gui_pkg = my_gui_pkg.my_gui_pkg:main',
            'my_publisher = my_gui_pkg.my_publisher:main',
            'service = my_gui_pkg.service_member_function:main',
            'client = my_gui_pkg.client_member_function:main'
        ],
    },
)
