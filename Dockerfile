# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Denver

# Update the package list and install necessary packages
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
	&& apt-get install libcurl4-openssl-dev -y \
    python3.8 \
    python3.8-venv \
    python3.8-dev \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a symbolic link to make python3.8 the default python
RUN ln -s /usr/bin/python3.8 /usr/bin/python

# Upgrade pip
RUN python3.8 -m pip install --upgrade pip

# Set the working directory in the container
WORKDIR /embedtad

# Copy the current directory contents into the container at /embedtad
COPY . /embedtad

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
