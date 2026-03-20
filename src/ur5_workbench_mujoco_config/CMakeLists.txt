cmake_minimum_required(VERSION 3.8)
project(ur5_workbench_mujoco_config)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY
    config
    description
    launch
    urdf
  DESTINATION
    share/${PROJECT_NAME}
)

ament_package()
