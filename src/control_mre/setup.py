import os
from setuptools import find_packages, setup
from glob import glob


package_name = 'control_mre'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name), glob('launch/*.py')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*.stl')),
        (os.path.join('share', package_name, 'robots'), glob('robots/*.xacro')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
        (os.path.join('share', package_name, 'viz'), glob('viz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mr337',
    maintainer_email='TODO',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
