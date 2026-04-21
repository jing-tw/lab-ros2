# core ROS 2 desktop tools (like RViz and RQT) and the simulators (Gazebo)
FROM osrf/ros:humble-desktop-full   

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Use Taiwan mirror for faster downloads
RUN sed -i 's/archive.ubuntu.com/tw.archive.ubuntu.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/tw.archive.ubuntu.com/g' /etc/apt/sources.list
RUN rm -fr /var/lib/apt/lists/*
RUN apt-get clean


RUN apt-get update && apt-get install -y \
    sudo \
    lsb-release \
    wget \
    curl \
    git \
    vim \
    ca-certificates \
    build-essential \
    cmake \

    python3-colcon-common-extensions \
    python3 python3-pip python3-venv \

    ros-humble-moveit \
    ros-humble-ur-robot-driver \
    ros-humble-ur-description \
    ros-humble-ur-moveit-config \
    && rm -rf /var/lib/apt/lists/*

# Auto source ROS
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc

# Set up the workspace and build
WORKDIR /ros2_ws

# (Optional) Add a non-root user for security
# RUN useradd -m jing
# USER jing

# Set the default command
CMD ["/bin/bash"]

# Pinocchio installation
ARG SCRIPT_NAME=install_pinocchio.sh
ARG SCRIPT_PATH=/usr/local/bin
COPY ${WORKDIR}/src/mysrc/panda_ik/${SCRIPT_NAME} ${SCRIPT_PATH}/${SCRIPT_NAME}
RUN chmod +x ${SCRIPT_PATH}/${SCRIPT_NAME}
RUN ${SCRIPT_PATH}/${SCRIPT_NAME}

