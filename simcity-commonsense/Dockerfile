FROM indodutch/csweb
MAINTAINER Berend Weel <b.weel@esciencecenter.nl>

USER simcity
WORKDIR /home/simcity/

COPY run /etc/service/simcity/
COPY start.sh /home/simcity/


USER root
RUN chmod +x /home/simcity/start.sh
RUN apt-get install dos2unix
RUN dos2unix /etc/service/simcity/run


EXPOSE 3003
