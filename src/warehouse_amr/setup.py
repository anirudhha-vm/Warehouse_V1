from setuptools import find_packages, setup

package_name = 'warehouse_amr'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ani',
    maintainer_email='anirudhha1008@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        	'odom_tf_broadcaster = warehouse_amr.odom_tf_broadcaster:main',
        	'static_lidar_tf = warehouse_amr.static_lidar_tf:main',
        	'odom_filter_2d = warehouse_amr.odom_filter_2d:main',
        ],
    },
)
