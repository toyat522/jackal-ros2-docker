# Start from ubuntu
FROM ubuntu:jammy

# Update so we can download packages
RUN apt-get update && apt-get upgrade -y


#Set the ROS distro
ENV ROS_DISTRO humble
ARG DEBIAN_FRONTEND=noninteractive


# Add the ROS deb repo to the apt sources list
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
		curl \
		wget \
		gnupg2 \
		lsb-release \
		ca-certificates \
        console-setup \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null


# Set up ROS
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-setuptools 

# Install ros2 packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
		ros-${ROS_DISTRO}-desktop \
		python3-colcon-common-extensions \
        ros-dev-tools \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean


# Set up ROS2
RUN rosdep init
RUN rosdep update --include-eol-distros


# Set up locales
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean
RUN locale-gen en_US en_US.UTF-8 && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV PYTHONIOENCODING=utf-8


# Install additional required packages for ROS
RUN apt update && apt install -y \
    ros-$ROS_DISTRO-tf2-geometry-msgs \
    ros-$ROS_DISTRO-tf-transformations \
    ros-$ROS_DISTRO-ament-cmake-auto \
    ros-$ROS_DISTRO-rtcm-msgs \
    ros-$ROS_DISTRO-nmea-msgs \
    ros-$ROS_DISTRO-xacro \
    ros-$ROS_DISTRO-librealsense2 \
    ros-$ROS_DISTRO-diagnostic-updater \
    ros-$ROS_DISTRO-microstrain-inertial-driver \
    python3-requests \
    libpcap0.8-dev \
    libasio-dev \
    python3-serial \
    build-essential


# Install some cool programs
RUN apt update && apt install -y \
    sudo \
    vim \
    emacs \
    nano \
    gedit \
    screen \
    tmux \
    iputils-ping


# Create a user
RUN useradd -ms /bin/bash sparklab
RUN echo 'sparklab:sparklab' | chpasswd
RUN usermod -aG sudo sparklab
USER sparklab
WORKDIR /home/sparklab
