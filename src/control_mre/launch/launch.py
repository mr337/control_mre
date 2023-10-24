import os

from ament_index_python.packages import get_package_share_directory

import launch
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource

import xacro


def generate_launch_description():
    simulation_dir = get_package_share_directory('control_mre')
    gazebo_ros = get_package_share_directory('gazebo_ros')

    gzserver = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource([gazebo_ros, '/launch', '/gzserver.launch.py']),
        # condition=IfCondition(LaunchConfiguration('server'))
        # launch_arguments={'verbose': 'true'}.items()
        launch_arguments={'verbose': 'true', 'world': os.path.join(simulation_dir, 'worlds', 'empty.world')}.items()
    )

    gzclient = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource([gazebo_ros, '/launch', '/gzclient.launch.py']),
        # condition=IfCondition(LaunchConfiguration('gui'))
    )

    robot_description = xacro.process_file(os.path.join(simulation_dir, 'robots', 'example_robot.xacro')).toxml()
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description,
                     'use_sim_time': True,
                     }])

    gazebo_spawner = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        output='screen',
        arguments=[
            '-entity', 'example_robot',
            '-topic', 'robot_description',
            '-x', '0', '-y', '0', '-z', '0.750',
            '-R', '0', '-P', '0', '-Y', '0'])

    rviz_client = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        parameters=[{'use_sim_time': True}],
        arguments=['-d', os.path.join(simulation_dir, 'viz', 'rviz.rviz')]
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"]
    )

    rear_wheels_cont_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["rear_wheels_cont"]
    )

    wheel_brackets_cont_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["wheel_brackets_cont"]
    )

    return launch.LaunchDescription([
        launch.actions.SetEnvironmentVariable(name='GAZEBO_RESOURCE_PATH', value='/usr/share/gazebo-11/'),  # does not seem to work :(
        gzserver,
        gzclient,
        robot_state_publisher,
        gazebo_spawner,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=gazebo_spawner,
                on_exit=[joint_broad_spawner])
        ),
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=joint_broad_spawner,
                on_exit=[wheel_brackets_cont_spawner,
                         rear_wheels_cont_spawner,
                         ])
        ),
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=wheel_brackets_cont_spawner,
                on_exit=[rviz_client])
        ),
    ])
