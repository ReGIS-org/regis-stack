# sim-city-stack
Full Sim-City Stack using docker files and docker-compose.

The goal of this stack is to set up a development infrastructure of the sim-city stack
it is not meant for production deployment!

The full documentation is available at http://sim-city-stack.readthedocs.io/

First, install docker and docker-compose.

Check out the [sim-city-cs](https://github.com/indodutch/sim-city-cs) repository in the same directory as
this repo.
Put your simulation scripts in the simcity-slurm/simulations/ directory with their respective .json description
in the simcity-webservice/simulations/ directory. Check the documentation for more information on adding simulations
to the system. 

Then, run a test infrastructure with
```
docker-compose up --build
```
The sim-city frontend is now available on localhost.

The sim-city-webservice is now available on localhost/explore/
There is a CouchDB database running for tasks jobs on on localhost/couchdb/
A webdav server is running on localhost/webdav/

These parts are strung together using nginx that is also running in a docker container.

Finally, a slurm cluster is running to run simulations.

# The Docker Components

## simcity-commonsense
This docker container runs the front end. The directory sim-city-cs is mounted into the docker image
in /home/simcity/sim-city-cs. You can edit typescript and html files in this directory from outside the
docker, which will trigger a recompilation of the files and a restart of the server using nodemon.

The sim-city-cs docker is accessible over SSH on port 30022 (user `simcity`, password `simcity`).

## simcity-webservice
This docker hosts the simcity-webservice. The simulations directory is copied into the docker when it is built.
Changing the files in this directory therefore requires rebuilding the docker image.

The sim-city-webservice docker is accessible over SSH on port 20022 (user `simcity`, password `simcity`).

## simcity-slurm
This docker hosts a slurm cluster with 2 nodes. The simulations directory is copied into the docker when it is built
into /home/xenon/simulations. Changing the files in this directory therefore requires rebuilding the docker image.

It is running an toned down version of ubuntu 14.04.
All simulations are run as the xenon user. If your simulation depends on certain software add it to the Dockerfile.

The slurm docker is accessible over SSH on port 10022 (user `xenon`, password `javagat`).

## simcity-couchdb
This docker hosts the couchdb. It is a standard couchdb install with a little local configuration.
It runs on port 5784 with user `simcityadmin`, password `simcity`

## simcity-webdav
This docker hosts a webdav server on port 8080. The user is `webdav` with password `vadbew`

## simcity-nginx
This docker hosts the nginx http server. Its configuration links the different docker components together.
It also hosts static content on localhost/www/. You can add your own static content in the www directory,
which gets copied into the docker image when it is built.
