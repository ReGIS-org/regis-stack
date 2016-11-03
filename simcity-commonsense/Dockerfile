FROM indodutch/csweb
MAINTAINER Berend Weel <b.weel@esciencecenter.nl>

RUN apt-get install dos2unix

USER simcity
WORKDIR /home/simcity/

COPY run /etc/service/simcity/
COPY start.sh /home/simcity/


USER root
RUN dos2unix /etc/service/simcity/run


EXPOSE 3003
