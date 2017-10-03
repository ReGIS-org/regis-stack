#!/bin/sh
cd /home/regis/csweb/csWeb
npm install
bower install
gulp init
bower link
cd out/csServerComp
npm link
#
cd /home/regis/csweb/sim-city-cs
npm install
npm link csweb
cd /home/regis/csweb/sim-city-cs/public
bower install
bower link csweb
cd /home/regis/csweb/sim-city-cs
typings install
gulp init
