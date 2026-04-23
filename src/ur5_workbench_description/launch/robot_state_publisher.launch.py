from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    description_package = FindPackageShare("ur5_workbench_description")

    arguments = [
        DeclareLaunchArgument(
            "urdf_file",
            default_value=PathJoinSubstitution(
                [description_package, "urdf", "ur5_workbench.urdf.xacro"]
            ),
            description="Path to the URDF file",
        ),
        DeclareLaunchArgument(
            name="use_sim_time",
            default_value="false",
            description="Use simulation clock if true",
        ),
        DeclareLaunchArgument(
            name="include_ros2_control",
            default_value="true",
            description="Whether to include ros2_control components in the URDF",
        ),
        DeclareLaunchArgument(
            name="include_thing1",
            default_value="true",
            description="",
        ),
        DeclareLaunchArgument(
            name="include_thing2",
            default_value="true",
            description="",
        ),
        DeclareLaunchArgument(
            name="thing1_wrist_camera_model",
            default_value="",
            description="",
        ),
        DeclareLaunchArgument(
            name="thing2_wrist_camera_model",
            default_value="",
            description="",
        ),
        DeclareLaunchArgument(
            name="thing1_robot_ip",
            default_value="192.168.1.1",
            description="",
        ),
        DeclareLaunchArgument(
            name="thing2_robot_ip",
            default_value="192.168.1.1",
            description="",
        ),
    ]

    description_file = LaunchConfiguration("urdf_file")

    robot_description = ParameterValue(
        Command(
            [
                PathJoinSubstitution([FindExecutable(name="xacro")]),
                " ",
                description_file,
                " ",
                "include_ros2_control:=",
                LaunchConfiguration("include_ros2_control"),
                " ",
                "include_thing1:=",
                LaunchConfiguration("include_thing1"),
                " ",
                "include_thing2:=",
                LaunchConfiguration("include_thing2"),
                " ",
                "thing1_wrist_camera_model:=",
                LaunchConfiguration("thing1_wrist_camera_model"),
                " ",
                "thing2_wrist_camera_model:=",
                LaunchConfiguration("thing2_wrist_camera_model"),
                " ",
                "thing1_robot_ip:=",
                LaunchConfiguration("thing1_robot_ip"),
                " ",
                "thing2_robot_ip:=",
                LaunchConfiguration("thing2_robot_ip"),
            ]
        ),
        value_type=str,
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {"robot_description": robot_description},
            {"use_sim_time": LaunchConfiguration("use_sim_time")},
        ],
    )

    return LaunchDescription(arguments + [robot_state_publisher_node])
