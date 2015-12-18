FROM jenkins:latest
MAINTAINER Pit Kleyersburg <pitkley@googlemail.com>

USER root

RUN apt-get update \
    && apt-get install -y libapparmor1 sudo \
    && rm -rf /var/lib/apt/lists/*

RUN echo "jenkins ALL=NOPASSWD: /usr/bin/docker *" >> /etc/sudoers

USER jenkins
