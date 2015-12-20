FROM csanchez/jenkins-swarm-slave
MAINTAINER Pit Kleyersburg <pitkley@googlemail.com>

USER root
RUN apt-get update \
    && apt-get install -y python3.4 \
    && rm -rf /var/lib/apt/lists/*

USER jenkins-slave
