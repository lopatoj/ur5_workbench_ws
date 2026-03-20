from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
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
        )
    ]

    description_file = LaunchConfiguration("urdf_file")

    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                description_file,
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
