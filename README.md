# sim-city-stack
Full Sim-City Stack using docker files and docker-compose

First, install docker-compose. Then, run a test infrastructure with
```
docker-compose up --build -d
```
The sim-city-webservice is now available on localhost port 9098.
There is a CouchDB database running for tasks jobs on port 5784 (user simcityadmin, password simcity).
A webdav server is running on port 8080 (user webdav, password vadbew). 
And finally, a Slurm cluster is accessible over SSH on port 10022 (user `xenon`, password `javagat`).
