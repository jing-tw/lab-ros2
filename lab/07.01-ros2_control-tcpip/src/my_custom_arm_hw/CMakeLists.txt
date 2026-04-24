cmake_minimum_required(VERSION 3.8)
project(my_custom_arm_hw)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source filestarget_link_libraries
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()
add_library(my_custom_arm_hw SHARED
  src/custom_tcp_hardware.cpp
)

target_include_directories(my_custom_arm_hw PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/my_custom_arm_hw>
)



ament_target_dependencies(my_custom_arm_hw
  hardware_interface
  pluginlib
  rclcpp
  rclcpp_lifecycle
)

# 匯出 plugin
pluginlib_export_plugin_description_file(hardware_interface my_custom_arm_hw.xml)

install(
  TARGETS my_custom_arm_hw
  DESTINATION lib
)

install(
  DIRECTORY include/
  DESTINATION include/
)

install(
  DIRECTORY urdf config launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
