FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Denver

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

RUN ln -s /usr/bin/python3.8 /usr/bin/python
RUN python3.8 -m pip install --upgrade pip
WORKDIR /embedtad
COPY . /embedtad
RUN pip install --no-cache-dir -r requirements.txt