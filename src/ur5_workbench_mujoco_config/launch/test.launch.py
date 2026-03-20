from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, Shutdown
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterFile


def generate_launch_description():
    mujoco_config_package = FindPackageShare("ur5_workbench_mujoco_config")
    description_package = FindPackageShare("ur5_workbench_description")
    urdf_file = PathJoinSubstitution(
        [mujoco_config_package, "urdf", "ur5_workbench.mujoco_ros2_control.xacro"]
    )

    robot_state_publisher_launch = IncludeLaunchDescription(
        PathJoinSubstitution(
            [description_package, "launch", "robot_state_publisher.launch.py"]
        ),
        launch_arguments={"urdf_file": urdf_file}.items(),
    )

    parameters_file = PathJoinSubstitution(
        [mujoco_config_package, "config", "controllers.yaml"]
    )
    mujoco_plugins_file = PathJoinSubstitution(
        [mujoco_config_package, "config", "plugins.yaml"]
    )


    mujoco_ros2_control_node = Node(
        package="mujoco_ros2_control",
        executable="ros2_control_node",
        emulate_tty=True,
        output="both",
        parameters=[
            {"use_sim_time": True},
            ParameterFile(parameters_file),
            ParameterFile(mujoco_plugins_file),
        ],
        on_exit=Shutdown()
    )
    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager", "--param-file", parameters_file],
    )
    position_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["position_controller", "--controller-manager", "/controller_manager", "--param-file", parameters_file],
    )

    return LaunchDescription([
        robot_state_publisher_launch,
        mujoco_ros2_control_node,
        joint_state_broadcaster,
        position_controller,
    ])
