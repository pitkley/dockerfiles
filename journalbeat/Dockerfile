FROM golang:1.7
MAINTAINER Pit Kleyersburg <pitkley@googlemail.com>

RUN apt-get update \
    && apt-get install libsystemd-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN go get github.com/mheese/journalbeat

COPY entrypoint.sh /sbin/entrypoint

ENTRYPOINT ["/sbin/entrypoint"]
CMD ["-help"]

