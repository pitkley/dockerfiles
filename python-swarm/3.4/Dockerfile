FROM csanchez/jenkins-swarm-slave
MAINTAINER Pit Kleyersburg <pitkley@googlemail.com>

USER root
RUN apt-get update \
    && apt-get install -y python3.4 python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

RUN easy_install3 pip \
    && chown -R jenkins-slave:staff /usr/local/lib/python* \
    && rm -rf /tmp/*

USER jenkins-slave
