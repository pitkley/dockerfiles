FROM evarga/jenkins-slave
MAINTAINER Pit Kleyersburg <pitkley@googlemail.com>

# This docker-file is pretty much a carbon copy of Leonardo Di Donato's
# image `leodido/texlive`, just based on `evarga:jenkins-slave` and thus
# adapted to `apt-get`.

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install git

ENV TL install-tl-2015
RUN mkdir -p $TL

RUN wget -nv -O $TL.tar.gz http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
RUN tar -xzf $TL.tar.gz -C $TL --strip-components=1
ADD full.profile $TL/

RUN cd $TL/ && ./install-tl --persistent-downloads --profile full.profile

ENV PATH $PATH:/usr/local/texlive/2015/bin/x86_64-linux

RUN rm $TL.tar.gz && rm -r $TL

RUN [ -f $(kpsewhich -var-value TEXMFSYSVAR)/fonts/conf/texlive-fontconfig.conf ] && cp $(kpsewhich -var-value TEXMFSYSVAR)/fonts/conf/texlive-fontconfig.conf /etc/fonts/conf.d/09-texlive.conf || :
RUN fc-cache -fsv

