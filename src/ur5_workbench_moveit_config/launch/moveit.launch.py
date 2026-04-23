from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    ur5_workbench_moveit_config = FindPackageShare("ur5_workbench_moveit_config")

    arguments = []
    arguments.append(DeclareLaunchArgument(
        "rviz_config",
        default_value=ur5_workbench_moveit_config / "rviz/moveit.rviz",
    ))
    arguments.append(DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
    ))

    use_sim_time = LaunchConfiguration("use_sim_time")

    moveit_config = MoveItConfigsBuilder("ur5_workbench", package_name="ur5_workbench_moveit_config").to_moveit_configs()

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="both",
        parameters=[
            {"use_sim_time": use_sim_time},
            moveit_config.to_dict(),
        ],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        output="log",
        respawn=False,
        arguments=["-d", LaunchConfiguration("rviz_config")],
        parameters=[
            {"use_sim_time": use_sim_time},
            moveit_config.planning_pipelines,
            moveit_config.robot_description_kinematics,
            moveit_config.joint_limits,
        ],
    )

    return LaunchDescription(
        arguments + [
            rviz_node,
            move_group_node,
        ]
    )
