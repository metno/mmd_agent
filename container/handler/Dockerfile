FROM ubuntu

RUN mkdir /app

# Set the Current Working Directory inside the container
WORKDIR /app

ADD . /app

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-setuptools
RUN apt-get -y install python3-pip

ARG MMD_AGENT_REPO=https://github.com/metno/mmd_agent
ARG MMD_AGENT_VERSION=main

RUN apt-get -y install git
RUN git clone --branch ${MMD_AGENT_VERSION} ${MMD_AGENT_REPO}

RUN pip install -r mmd_agent/requirements.txt
WORKDIR /app/mmd_agent