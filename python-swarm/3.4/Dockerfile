FROM csanchez/jenkins-swarm-slave
MAINTAINER Pit Kleyersburg <pitkley@googlemail.com>

USER root
# Install py3.4
RUN apt-get update \
    && apt-get install -y python3.4 python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

# Install pip
RUN easy_install3 pip \
    && chown -R jenkins-slave:staff /usr/local/lib/python* \
    && rm -rf /tmp/*

# Allow all ssh-hosts (for git-cloning)
RUN sed -i "s/^#\(.*\)StrictHostKeyChecking.*$/\1StrictHostKeyChecking no/g" /etc/ssh/ssh_config

USER jenkins-slave
