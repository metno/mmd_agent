
# FIRST STAGE:  build the app.
FROM golang:1.16 AS build-app

RUN mkdir /mmd-agent

# Set the Current Working Directory inside the container
WORKDIR /mmd-agent

ADD . /mmd-agent

# Build the Go app
RUN apt-get update && \
    apt-get install -y \
    git 
RUN git clone https://github.com/metno/go-mms
WORKDIR /mmd-agent/go-mms

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

COPY --from=build-app /mmd-agent  /app/

WORKDIR /app

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-setuptools
RUN apt-get -y install python3-pip

RUN pip install -r requirements.txt
