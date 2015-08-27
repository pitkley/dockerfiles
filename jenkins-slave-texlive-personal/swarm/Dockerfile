FROM pitkley/jenkins-slave-texlive:swarm
MAINTAINER Pit Kleyersburg <pitkley@googlemail.com>

USER root

RUN apt-get update
RUN apt-get -y upgrade
RUN tlmgr update --all

RUN apt-get -y install gnuplot make ghostscript
RUN apt-get -y install python-setuptools
RUN easy_install pip
RUN pip install pygments

RUN sed -i "s/^#\(.*\)StrictHostKeyChecking.*$/\1StrictHostKeyChecking no/g" /etc/ssh/ssh_config

USER jenkins-slave

