FROM phusion/baseimage:latest
MAINTAINER Berend Weel <b.weel@esciencecenter.nl>

# Keep ssh running
RUN rm -f /etc/service/sshd/down
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh

RUN apt-get update && apt-get install -y nodejs nodejs-legacy npm git libsass-dev

RUN npm i -g npm
RUN npm i -g n
RUN n latest
RUN npm i -g typescript bower nodemon http-server gulp node-gyp js-beautify typings

RUN /usr/sbin/useradd -p $(openssl passwd simcity) -d /home/simcity -m --shell /bin/bash simcity

WORKDIR /home/simcity/
RUN chown simcity:simcity -R /home/simcity

USER simcity
RUN mkdir ~/npm && echo "prefix = ~/npm" > ~/.npmrc && echo "export PATH=~/npm/bin:$PATH" >> ~/.profile && . ~/.profile

#COPY run /etc/service/simcity/
COPY start.sh /home/simcity/

USER root
RUN chmod +x /home/simcity/start.sh
RUN apt-get install dos2unix
#RUN dos2unix /etc/service/simcity/run

EXPOSE 3003

USER root
CMD ["/sbin/my_init"]