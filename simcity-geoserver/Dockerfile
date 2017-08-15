FROM kartoza/geoserver

USER root
COPY ./config.ini /home/simcity/sim-city-geoserver/config.ini
COPY ./start.sh /home/simcity/sim-city-geoserver/start.sh

RUN chown simcity:simcity /home/simcity/sim-city-geoserver/config.ini
RUN chown simcity:simcity /home/simcity/sim-city-geoserver/simulations