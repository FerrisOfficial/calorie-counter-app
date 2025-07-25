FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/opt/android-sdk
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV ANDROID_NDK_HOME=/opt/android-ndk
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_NDK_HOME

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    git \
    zip \
    unzip \
    openjdk-8-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    build-essential \
    ccache \
    curl \
    wget \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Create a non-root user
RUN useradd -m -s /bin/bash builder && \
    echo "builder ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Switch to non-root user
USER builder
WORKDIR /home/builder

# Install buildozer and dependencies as non-root user
RUN pip3 install --user --upgrade pip
RUN pip3 install --user buildozer cython

# Add local bin to PATH
ENV PATH="/home/builder/.local/bin:$PATH"

# Create app directory
RUN mkdir -p /home/builder/app
WORKDIR /home/builder/app

# Copy app files
COPY --chown=builder:builder . /home/builder/app

# Build APK (with automatic yes to root warning)
CMD echo "y" | buildozer android debug
