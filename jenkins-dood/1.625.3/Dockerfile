FROM jenkins:1.625.3
MAINTAINER Pit Kleyersburg <pitkley@googlemail.com>

USER root

RUN apt-get update \
    && apt-get install -y libapparmor1 sudo \
    && rm -rf /var/lib/apt/lists/*

RUN echo "jenkins ALL=NOPASSWD: /usr/bin/docker-host *" >> /etc/sudoers
COPY docker /usr/bin/docker
COPY docker-slave /usr/bin/docker-slave

USER jenkins
