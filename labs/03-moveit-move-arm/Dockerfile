# core ROS 2 desktop tools (like RViz and RQT) and the simulators (Gazebo)
FROM osrf/ros:humble-desktop-full   

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

#
# Install ROS 2 packages and colcon build tools
# moveit-config:
#   - SRDF (Semantic Robot Description Format): Defines joint groups (e.g., "manipulator"), identifies "end effectors," and specifies which parts of the robot can safely touch each other without triggering a collision alarm.
#   - Kinematics Solvers: Configuration for how the robot calculates the math ($IK/FK$) to move its joints to reach a specific coordinate in 3D space
#   - Joint Limits: Data on how fast or how far each motor can turn.
#   - Launch Files: Scripts to start the MoveIt "MoveGroup" node and the RViz planning plugin.
#   - Controllers: Links between MoveIt's high-level plans and the actual hardware drivers (like your ur_robot_driver)
RUN apt-get update && apt-get install -y \
    ros-humble-moveit \
    ros-humble-ur-robot-driver \
    ros-humble-ur-description \
    ros-humble-ur-moveit-config \
    python3-colcon-common-extensions \
    python-is-python3 \
    git \
    && rm -rf /var/lib/apt/lists/*

# home
# WORKDIR /ros2_ws/src
# RUN git clone -b humble https://github.com/ros-planning/moveit2_tutorials.git

# auto source 
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

# Set up the workspace and build
WORKDIR /ros2_ws

# # Initialize rosdep (if not already done) and install dependencies for the cloned repos
# RUN apt-get update && \
#     rosdep update && \
#     rosdep install -r --from-paths src --ignore-src --rosdistro humble -y && \
#     rm -rf /var/lib/apt/lists/*

# # Build the workspace
# # We use /bin/bash -c so we can source the existing ROS installation
# RUN /bin/bash -c "source /opt/ros/humble/setup.bash && colcon build --symlink-install"

# # Automatically source the workspace in every new terminal
# RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
#     echo "source /ros2_ws/install/setup.bash" >> /root/.bashrc

# Set the default command to bash
CMD ["bash"]