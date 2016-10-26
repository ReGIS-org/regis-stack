FROM indodutch/csweb
MAINTAINER Berend Weel <b.weel@esciencecenter.nl>

USER simcity
WORKDIR /home/simcity/

COPY run /etc/service/simcity/
COPY start.sh /home/simcity/

USER root
EXPOSE 3003
