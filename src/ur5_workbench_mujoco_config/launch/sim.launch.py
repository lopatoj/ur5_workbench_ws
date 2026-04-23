from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler, Shutdown
from launch.event_handlers import OnProcessExit
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterFile, ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    arguments = []
    arguments.append(DeclareLaunchArgument("include_thing1", default_value="true"))
    arguments.append(DeclareLaunchArgument("include_thing2", default_value="true"))
    arguments.append(DeclareLaunchArgument("thing1_wrist_camera_model", default_value=""))
    arguments.append(DeclareLaunchArgument("thing2_wrist_camera_model", default_value=""))

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
            " include_thing1:=",
            LaunchConfiguration("include_thing1"),
            " include_thing2:=",
            LaunchConfiguration("include_thing2"),
            " thing1_wrist_camera_model:=",
            LaunchConfiguration("thing1_wrist_camera_model"),
            " thing2_wrist_camera_model:=",
            LaunchConfiguration("thing2_wrist_camera_model"),
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

    delay_rviz_after_controllers = RegisterEventHandler(
        event_handler=OnProcessExit(target_action=fts_broadcaster2, on_exit=[rviz_node])
    )

    return LaunchDescription(
        arguments + [
            mjcf_conversion_node,
            robot_state_publisher_node,
            mujoco_ros2_control_node,
            joint_state_broadcaster,
            joint_trajectory_controller,
            fts_broadcaster1,
            fts_broadcaster2,
            delay_rviz_after_controllers,
        ]
    )
