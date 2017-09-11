#!/bin/sh
cd csWeb
npm install
bower install
gulp init
bower link
cd out/csServerComp
npm link
cd ../../..
#
cd sim-city-cs
npm install
npm link csweb
cd public
bower install
bower link csweb
cd ..
typings install
gulp init
