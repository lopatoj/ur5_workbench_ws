from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    description_package = FindPackageShare("ur5_workbench_description")

    robot_state_publisher_launch = IncludeLaunchDescription(
        PathJoinSubstitution(
            [description_package, "launch", "robot_state_publisher.launch.py"]
        )
    )

    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui",
    )

    rviz_config_file = PathJoinSubstitution([description_package, "rviz", "view.rviz"])

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", rviz_config_file],
    )

    return LaunchDescription(
        [joint_state_publisher_gui_node, robot_state_publisher_launch, rviz_node]
    )
