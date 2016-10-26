#!/bin/sh

cd /home/simcity/sim-city-cs
npm install
cd /home/simcity/sim-city-cs/public && bower install
cd /home/simcity/sim-city-cs && typings install
gulp serve