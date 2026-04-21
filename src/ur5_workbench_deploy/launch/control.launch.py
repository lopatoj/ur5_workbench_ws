from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    Shutdown,
)
from launch.conditions import IfCondition
from launch.substitutions import (
    Command,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterFile, ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    arguments = []
    arguments.append(DeclareLaunchArgument("launch_rviz", default_value="true"))

    description_package = FindPackageShare("ur5_workbench_mujoco_config")

    parameters_file = PathJoinSubstitution(
        [
            FindPackageShare("ur5_workbench_deploy"),
            "config",
            "controllers.yaml",
        ]
    )
    urdf_file = PathJoinSubstitution(
        [description_package, "urdf", "ur5_workbench.urdf.xacro"]
    )
    rviz_config_file = PathJoinSubstitution([description_package, "rviz", "view.rviz"])

    robot_description_content = Command(
        [
            "xacro ",
            urdf_file,
        ]
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {
                "robot_description": ParameterValue(
                    robot_description_content, value_type=str
                )
            }
        ],
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            ParameterFile(parameters_file),
        ],
        output="screen",
        on_exit=Shutdown(),
    )
    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
            "--param-file",
            parameters_file,
        ],
    )
    joint_trajectory_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_trajectory_controller",
            "--controller-manager",
            "/controller_manager",
            "--param-file",
            parameters_file,
        ],
    )
    rviz_node = Node(
        package="rviz2",
        condition=IfCondition(LaunchConfiguration("launch_rviz")),
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
    )

    return LaunchDescription(
        [
            robot_state_publisher_node,
            control_node,
            joint_state_broadcaster,
            joint_trajectory_controller,
            rviz_node,
        ]
        + arguments
    )
