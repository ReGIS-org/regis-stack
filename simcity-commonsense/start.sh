#!/bin/sh

cd /home/simcity/sim-city-cs
npm install
npm link csweb
cd /home/simcity/sim-city-cs/public
bower install
bower link csweb
cd /home/simcity/sim-city-cs
typings install
gulp serve
