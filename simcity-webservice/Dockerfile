FROM indodutch/sim-city-webservice

USER root
COPY ./config.ini /home/simcity/sim-city-webservice/config.ini

RUN rm /home/simcity/sim-city-webservice/simulations/*.min.json || true
COPY ./simulations /home/simcity/sim-city-webservice/simulations/

RUN chown simcity:simcity /home/simcity/sim-city-webservice/config.ini
RUN chown simcity:simcity /home/simcity/sim-city-webservice/simulations

USER simcity