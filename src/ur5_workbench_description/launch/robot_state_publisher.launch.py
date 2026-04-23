from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution, FindExecutable
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    description_package = FindPackageShare("ur5_workbench_description")

    args = [
        DeclareLaunchArgument(
            "urdf_file",
            default_value=PathJoinSubstitution(
                [description_package, "urdf", "ur5_workbench.urdf.xacro"]
            ),
            description="Path to the URDF file",
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
            name="write_to_file",
            default_value="true",
        )
    ]

    description_file = LaunchConfiguration("urdf_file")

    robot_description = ParameterValue(
        Command(
            [
                PathJoinSubstitution([FindExecutable(name="xacro")]),
                " ",
                description_file,
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
            ]
        ),
        value_type=str,
    )
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
    )


    return LaunchDescription(args + [robot_state_publisher_node])
