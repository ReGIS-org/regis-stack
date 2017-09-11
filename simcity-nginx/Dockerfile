FROM nginx:alpine

COPY cors /etc/nginx/cors
COPY nginx-2.conf /etc/nginx/nginx.conf

RUN adduser -D simcity

USER simcity
RUN mkdir /home/simcity/www
COPY www/ /home/simcity/www/
# If you want to also host static content copy them to /home/simcity/www

USER root
