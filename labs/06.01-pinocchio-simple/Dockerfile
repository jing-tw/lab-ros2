# Layer 1: OS (Ubuntu 22.04 LTS)
FROM ubuntu:22.04

# Avoid prompts from apt during build
ENV DEBIAN_FRONTEND=noninteractive

# Layer 2: Dependencies
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
    python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /workspace

# (Optional) Add a non-root user for security
# RUN useradd -m jing
# USER jing

# Set the default command
CMD ["/bin/bash"]

# Pinocchio installation
ARG SCRIPT_NAME=install_pinocchio.sh
ARG SCRIPT_PATH=/usr/local/bin
COPY ${WORKDIR}/src/${SCRIPT_NAME} ${SCRIPT_PATH}/${SCRIPT_NAME}
RUN chmod +x ${SCRIPT_PATH}/${SCRIPT_NAME}
RUN ${SCRIPT_PATH}/${SCRIPT_NAME}

