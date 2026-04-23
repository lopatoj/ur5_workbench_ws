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
    arguments.append(DeclareLaunchArgument("thing1_robot_ip", default_value="192.168.50.1"))
    arguments.append(DeclareLaunchArgument("thing2_robot_ip", default_value="192.168.50.2"))
    arguments.append(DeclareLaunchArgument("include_thing1", default_value="true"))
    arguments.append(DeclareLaunchArgument("include_thing2", default_value="true"))
    arguments.append(DeclareLaunchArgument("thing1_wrist_camera_model", default_value=""))
    arguments.append(DeclareLaunchArgument("thing2_wrist_camera_model", default_value=""))

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

    script_filename = PathJoinSubstitution(
        [
            FindPackageShare("ur_client_library"),
            "resources",
            "external_control.urscript",
        ]
    )
    input_recipe_filename = PathJoinSubstitution(
        [FindPackageShare("ur_robot_driver"), "resources", "rtde_input_recipe.txt"]
    )
    output_recipe_filename = PathJoinSubstitution(
        [FindPackageShare("ur_robot_driver"), "resources", "rtde_output_recipe.txt"]
    )

    robot_description_content = Command(
        [
            "xacro ",
            urdf_file,
            "include_ros2_control:=true",
            "include_thing1:=",
            LaunchConfiguration("include_thing1"),
            "include_thing2:=",
            LaunchConfiguration("include_thing2"),
            "thing1_robot_ip:=",
            LaunchConfiguration("thing1_robot_ip"),
            "thing2_robot_ip:=",
            LaunchConfiguration("thing2_robot_ip"),
            "thing1_wrist_camera_model:=",
            LaunchConfiguration("thing1_wrist_camera_model"),
            "thing2_wrist_camera_model:=",
            LaunchConfiguration("thing2_wrist_camera_model"),
            "script_filename:=",
            script_filename,
            "input_recipe_filename:=",
            input_recipe_filename,
            "output_recipe_filename:=",
            output_recipe_filename,
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
