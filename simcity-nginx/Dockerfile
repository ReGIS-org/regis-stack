FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

RUN adduser -D simcity

USER simcity
RUN mkdir /home/simcity/www
COPY www/ /home/simcity/www/
# If you want to also host static content copy them to /home/simcity/www

USER root