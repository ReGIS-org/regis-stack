FROM phusion/baseimage:latest
MAINTAINER Berend Weel <b.weel@esciencecenter.nl>

# Keep ssh running
RUN rm -f /etc/service/sshd/down
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

RUN apt-get update && apt-get install -y nodejs nodejs-legacy npm git libsass-dev
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install -y nodejs

RUN /usr/sbin/useradd -p $(openssl passwd simcity) -d /home/simcity -m --shell /bin/bash simcity

USER simcity

RUN mkdir /home/simcity/npm && echo "prefix = /home/simcity/npm" > /home/simcity/.npmrc && echo "export PATH=/home/simcity/npm/bin:$PATH" >> /home/simcity/.profile && . /home/simcity/.profile && echo "export PATH=/home/simcity/npm/bin:$PATH" >> /home/simcity/.bashrc
ENV PATH=/home/simcity/npm/bin:$PATH

RUN mkdir /home/simcity/simcity
WORKDIR /home/simcity/simcity
RUN git clone https://github.com/indodutch/csWeb.git
RUN git clone https://github.com/indodutch/sim-city-cs.git

WORKDIR /home/simcity/

ENV N_PREFIX=/home/simcity
RUN npm i -g npm
RUN npm i -g n
RUN ~/npm/bin/n latest
RUN npm i -g typescript bower nodemon http-server gulp node-gyp js-beautify typings
RUN npm i -g randomatic arr-flatten throat readable-stream write-file-atomic

#COPY run /etc/service/simcity/
COPY start.sh /home/simcity/

USER root
RUN chmod +x /home/simcity/start.sh
USER simcity

EXPOSE 3003

# CMD ["/sbin/my_init"]
CMD ["/home/simcity/start.sh"]
