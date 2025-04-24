import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    EmitEvent,
    IncludeLaunchDescription,
    OpaqueFunction,
    RegisterEventHandler,
)
from launch.events import Shutdown
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
import launch_ros.actions
from launch.launch_description_sources import PythonLaunchDescriptionSource


def launch_setup(context, *args, **kwargs):

    microstrain_ld = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                get_package_share_directory("microstrain_inertial_driver"),
                "/launch/microstrain_launch.py",
            ]
        )
    )

    realsense_node = launch_ros.actions.Node(
        package="realsense2_camera",
        executable="realsense2_camera_node",
        output="screen",
    )

    ublox_ntrip_ld = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                get_package_share_directory("spark_gnss_ros"),
                "/launch/ublox_gps_ntrip.launch.py",
            ]
        ),
        launch_arguments={
            "gnss_device": LaunchConfiguration("gnss_device"),
            "host": LaunchConfiguration("host"),
            "port": LaunchConfiguration("port"),
            "mountpoint": LaunchConfiguration("mountpoint"),
            "username": LaunchConfiguration("username"),
            "password": LaunchConfiguration("password"),
        }.items(),
    )

    vlp16_driver_ld = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                get_package_share_directory("velodyne_driver"),
                "/launch/velodyne_driver_node-VLP16-launch.py",
            ]
        )
    )

    vlp16_transform_ld = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                get_package_share_directory("velodyne_pointcloud"),
                "/launch/velodyne_transform_node-VLP16-launch.py",
            ]
        )
    )

    return [
        microstrain_ld,
        realsense_node,
        ublox_ntrip_ld,
        vlp16_driver_ld,
        vlp16_transform_ld,
    ]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "gnss_device", default_value="/dev/ttyACM0"
            ),
            DeclareLaunchArgument(
                "host", default_value="macorsrtk.massdot.state.ma.us"
            ),
            DeclareLaunchArgument(
                "port", default_value="10000"
            ),
            DeclareLaunchArgument(
                "mountpoint", default_value="RTCM3_NEAR"
            ),
            DeclareLaunchArgument("username"),
            DeclareLaunchArgument("password"),
            OpaqueFunction(function=launch_setup),
        ]
    )
