FROM golang:1.19

RUN apt-get update && apt-get install -y make gcc zip
RUN wget https://github.com/filecoin-project/bacalhau/archive/refs/heads/main.zip
RUN unzip main.zip
WORKDIR bacalhau-main
RUN go build