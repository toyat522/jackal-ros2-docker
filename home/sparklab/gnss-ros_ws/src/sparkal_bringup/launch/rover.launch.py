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

    ublox_ntrip_ld = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                get_package_share_directory("ntrip_client"),
                "/ntrip_client_launch.py",
            ]
        ),
    )

    return [
        ublox_ntrip_ld,
    ]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument("device", default_value="/dev/ttyACM0"),
            DeclareLaunchArgument(
                "host", default_value="macorsrtk.massdot.state.ma.us"
            ),
            DeclareLaunchArgument("port", default_value="10000"),
            DeclareLaunchArgument("mountpoint", default_value="RTCM3_NEAR"),
            DeclareLaunchArgument("username"),
            DeclareLaunchArgument("password"),
            OpaqueFunction(function=launch_setup),
        ]
    )
