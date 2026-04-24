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
            name="script_filename",
            default_value="",
        ),
        DeclareLaunchArgument(
            name="input_recipe_filename",
            default_value="",
        ),
        DeclareLaunchArgument(
            name="output_recipe_filename",
            default_value="",
        ),
        DeclareLaunchArgument(
            name="use_sim_time",
            default_value="false",
        ),
        DeclareLaunchArgument(
            name="include_ros2_control",
            default_value="true",
        ),
        DeclareLaunchArgument(
            name="include_thing1",
            default_value="true",
        ),
        DeclareLaunchArgument(
            name="include_thing2",
            default_value="true",
        ),
        DeclareLaunchArgument(
            name="thing1_kinematics_parameters_file",
            default_value=PathJoinSubstitution(
                [description_package, "config", "thing1_kinematics.yaml"]
            ),
        ),
        DeclareLaunchArgument(
            name="thing2_kinematics_parameters_file",
            default_value=PathJoinSubstitution(
                [description_package, "config", "thing2_kinematics.yaml"]
            ),
        ),
        DeclareLaunchArgument(
            name="thing1_wrist_camera_model",
            default_value="",
        ),
        DeclareLaunchArgument(
            name="thing2_wrist_camera_model",
            default_value="",
        ),
        DeclareLaunchArgument(
            name="thing1_robot_ip",
            default_value="192.168.50.19",
        ),
        DeclareLaunchArgument(
            name="thing2_robot_ip",
            default_value="192.168.50.20",
        ),
        DeclareLaunchArgument(
            name="thing1_fts_dev",
            default_value="ttyUSB0",
        ),
        DeclareLaunchArgument(
            name="thing2_fts_dev",
            default_value="ttyUSB1",
        ),
        DeclareLaunchArgument(
            name="thing1_use_fts",
            default_value="true",
        ),
        DeclareLaunchArgument(
            name="thing2_use_fts",
            default_value="true",
        ),
        DeclareLaunchArgument(
            name="thing1_use_gripper",
            default_value="true",
        ),
        DeclareLaunchArgument(
            name="thing2_use_gripper",
            default_value="true",
        ),
        DeclareLaunchArgument(
            name="thing1_gripper_com_port",
            default_value="/dev/ttyUSB2",
        ),
        DeclareLaunchArgument(
            name="thing2_gripper_com_port",
            default_value="/dev/ttyUSB3",
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
                "script_filename:=",
                LaunchConfiguration("script_filename"),
                " ",
                "input_recipe_filename:=",
                LaunchConfiguration("input_recipe_filename"),
                " ",
                "output_recipe_filename:=",
                LaunchConfiguration("output_recipe_filename"),
                " ",
                "include_thing1:=",
                LaunchConfiguration("include_thing1"),
                " ",
                "include_thing2:=",
                LaunchConfiguration("include_thing2"),
                " ",
                "thing1_kinematics_parameters_file:=",
                LaunchConfiguration("thing1_kinematics_parameters_file"),
                " ",
                "thing2_kinematics_parameters_file:=",
                LaunchConfiguration("thing2_kinematics_parameters_file"),
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
                " ",
                "thing1_fts_dev:=",
                LaunchConfiguration("thing1_fts_dev"),
                " ",
                "thing2_fts_dev:=",
                LaunchConfiguration("thing2_fts_dev"),
                " ",
                "thing1_use_fts:=",
                LaunchConfiguration("thing1_use_fts"),
                " ",
                "thing2_use_fts:=",
                LaunchConfiguration("thing2_use_fts"),
                " ",
                "thing1_use_gripper:=",
                LaunchConfiguration("thing1_use_gripper"),
                " ",
                "thing2_use_gripper:=",
                LaunchConfiguration("thing2_use_gripper"),
                " ",
                "thing1_gripper_com_port:=",
                LaunchConfiguration("thing1_gripper_com_port"),
                " ",
                "thing2_gripper_com_port:=",
                LaunchConfiguration("thing2_gripper_com_port"),
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
