.. _installation:

Installation
============
Installing the sim-city-web stack locally for development relies on docker.
We will go over getting all the parts step by step. If you are an advanced user
the README.md file gives a shorter overview of the installation. 

Installing Docker and docker-compose
------------------------------------
The installation for docker and docker-compose is best explained by the docker people.

To install docker see `the docker documentation <https://docs.docker.com/engine/getstarted/>`__.
For docker-compose `see here <https://docs.docker.com/compose/install/>`__.


Getting the code
----------------
First download sim-city-stack and sim-city-cs from github using:

.. code:: shell

    git clone https://git@github.com/indodutch/sim-city-stack.git
    cd sim-city-stack

    git clone https://git@github.com/indodutch/sim-city-cs.git

Running the infrastructure
--------------------------
To run the infrastructure use the following command:

.. code:: shell

    docker-compose up --build

You can stop it by pressing ctrl-c.
