from launch import LaunchDescription
from launch.actions import Shutdown
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterFile, ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    mujoco_config_package = FindPackageShare("ur5_workbench_mujoco_config")
    urdf_file = PathJoinSubstitution(
        [mujoco_config_package, "urdf", "ur5_workbench.mujoco_ros2_control.xacro"]
    )
    scene_file = PathJoinSubstitution(
        [mujoco_config_package, "description", "scene.xml"]
    )

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
                ),
                "use_sim_time": True,
            }
        ],
    )

    mjcf_conversion_node = Node(
        package="mujoco_ros2_control",
        executable="robot_description_to_mjcf.sh",
        output="both",
        emulate_tty=True,
        arguments=["--publish_topic", "/mujoco_robot_description", "--scene", scene_file, "-s"],
    )

    parameters_file = PathJoinSubstitution(
        [mujoco_config_package, "config", "controllers.yaml"]
    )
    mujoco_plugins_file = PathJoinSubstitution(
        [mujoco_config_package, "config", "plugins.yaml"]
    )
    rviz_config_file = PathJoinSubstitution(
        [mujoco_config_package, "rviz", "wrench.rviz"]
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
    fts_broadcaster1 = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "force_torque_sensor_broadcaster1",
            "--controller-manager",
            "/controller_manager",
            "--param-file",
            parameters_file,
        ],
    )
    fts_broadcaster2 = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "force_torque_sensor_broadcaster2",
            "--controller-manager",
            "/controller_manager",
            "--param-file",
            parameters_file,
        ],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        parameters=[{"use_sim_time": True}],
        arguments=["-d", rviz_config_file],
    )

    return LaunchDescription(
        [
            mjcf_conversion_node,
            robot_state_publisher_node,
            mujoco_ros2_control_node,
            joint_state_broadcaster,
            joint_trajectory_controller,
            fts_broadcaster1,
            fts_broadcaster2,
            rviz_node,
        ]
    )
