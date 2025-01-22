FROM nvidia/cuda:12.4.1-base-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    git \
    wget \
    unzip \
    build-essential \
    libssl-dev \
    libffi-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    liblzma-dev \
    tk-dev \
    uuid-dev \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Install required dependencies and download Python
RUN wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz && \
    tar xzf Python-3.12.0.tgz && \
    cd Python-3.12.0 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.12.0 Python-3.12.0.tgz

# Install distutils for Python 3.12
RUN apt-get update && apt-get install -y python3.12-distutils

# Set Python 3.12 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 1 && \
    update-alternatives --config python3 --skip-auto

# Upgrade pip and install packages
RUN python3 -m ensurepip && python3 -m pip install --upgrade pip

# Clone the repository
ARG REPO_URL=https://github.com/OluwadareLab/EmbedTAD.git
RUN git clone $REPO_URL /workspace

WORKDIR /workspace

# Install CUDA toolkit and libraries
RUN apt-get update && apt-get install -y \
    cuda-toolkit-12-4 \
    cuda-cudart-12-4 \
    cuda-libraries-12-4 \
    cuda-nvml-dev-12-4 \
    cuda-driver-dev-12-4 \
    libcurl4-openssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python requirements
RUN if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi

ENV HOME=/workspace

CMD ["/bin/bash"]