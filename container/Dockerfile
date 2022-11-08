
# FIRST STAGE:  build the app.
FROM golang:1.16 AS build-app

RUN mkdir /app

# Set the Current Working Directory inside the container
WORKDIR /app

ADD . /app

# Build the Go app
RUN apt-get update && \
    apt-get install -y \
    git 

# Make us able to change version and repo when building
ARG MMS_VERSION=main
ARG MMS_REPO=https://github.com/metno/go-mms

RUN git clone --branch ${MMS_VERSION} ${MMS_REPO}
WORKDIR /app/go-mms

# We want to populate the module cache based on the go.{mod,sum} files.
# Dependencies are downloaded only when go.mod or go.sum changes.
RUN go mod download

RUN make edeps
RUN make statik
RUN make deps

RUN make
RUN make test

# SECOND STAGE: create the app runtime image.
FROM ubuntu

COPY --from=build-app /app  /app/

WORKDIR /app
COPY config.yaml ./go-mms
RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-setuptools
RUN apt-get -y install python3-pip
WORKDIR /app/go-mms

ARG MMD_AGENT_REPO=https://github.com/metno/mmd_agent
ARG MMD_AGENT_VERSION=main

RUN apt-get -y install git
RUN git clone --branch ${MMD_AGENT_VERSION} ${MMD_AGENT_REPO}

COPY config.yaml ./mmd_agent
RUN pip install -r mmd_agent/requirements.txt




