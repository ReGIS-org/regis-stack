#!/bin/sh
cd /home/simcity/simcity/csWeb
npm install
bower install
gulp init
bower link
cd out/csServerComp
npm link
#
cd /home/simcity/simcity/sim-city-cs
npm install
npm link csweb
cd /home/simcity/simcity/sim-city-cs/public
bower install
bower link csweb
cd /home/simcity/simcity/sim-city-cs
typings install
gulp init
sleep 5s
gulp serve
