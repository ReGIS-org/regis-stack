#!/bin/bash
source /home/xenon/simcity/bin/activate
python /home/xenon/simulations/mysim/makeCircle.py $SIMCITY_IN/input.json > $SIMCITY_OUT/test.geojson
