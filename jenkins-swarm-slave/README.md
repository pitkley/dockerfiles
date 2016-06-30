# Jenkins swarm slave

Based on [`csanchez/jenkins-swarm-slave`](https://hub.docker.com/r/csanchez/jenkins-swarm-slave/).
Available on Docker Hub as [`pitkley/jenkins-swarm-slave`](https://hub.docker.com/r/pitkley/jenkins-swarm-slave/).

A [Jenkins swarm](https://wiki.jenkins-ci.org/display/JENKINS/Swarm+Plugin) slave.

## Running

To run a Docker container passing [any parameters](https://wiki.jenkins-ci.org/display/JENKINS/Swarm+Plugin#SwarmPlugin-AvailableOptions) to the slave

    docker run pitkley/jenkins-swarm-slave -master http://jenkins:8080 -username jenkins -password jenkins -executors 1

Linking to the Jenkins master container there is no need to use `--master`

    docker run -d --name jenkins -p 8080:8080 pitkley/jenkins-swarm
    docker run -d --link jenkins:jenkins pitkley/jenkins-swarm-slave -username jenkins -password jenkins -executors 1


# Building

    docker build -t jenkins-swarm-slave .
