.. _newsim:

Adding a New Simulation
***********************

Adding a new simulation consists of the following steps:

1.  Setting up your simulation.
2.  Adding the simulation to the slurm docker.
3.  Configuring the webservice.

Setting up your simulation:
===========================
In order to run your simulation using the sim-city stack it needs to adhere to a few conventions.

One command
    Your simulation needs to be able to be run with one command. If your simulation requires
    several commands to be called in succession you should use a bash script to call the commands
    one after the other.

One json input file
    The simcity webservice will supply your simulation with one json input file. This input file will be
    placed in an input directory. This input directory is available as an environment variable *$SIMCITY_IN*, or can be supplied
    as an argument to your script if set up correctly in the webservice.

One output directory
    Any output of your simulation should be put in the designated output directory, avaiable as an environment variable: *$SIMCITY_OUT*.
    As with the input directory the webservice can be set up so this is provided as an input to the simulation command.

Temp directory
    A temporary directory for the job will be created and is available through the environment variable *$SIMCITY_TMP*. Again this can
    also be supplied as an argument to the command.

GeoJson output
    Any output that is geo-spatial information that you would like to display on the map using the frontend should be in geojson format.
    For more information check out the `geojson website <http://geojson.org/>`__.


In general the following environment variables are available for your script:
    ===============     ==============================      ===================================
    variable            Description                         Example
    ===============     ==============================      ===================================
    $SIMCITY_JOBID      Unique identifier for this job      job_slurm-4321
    $SIMCITY_IN         Input directory                     /home/xenon/in/task_1234
    $SIMCITY_OUT        Output directory                    /home/xenon/out/task_1234
    $SIMCITY_TMP        Tmp directory                       /tmp/task_1234
    $SIMCITY_PARAMS     Path of the input.json file         /home/xenon/in/task_1234/input.json
    ===============     ==============================      ===================================

Adding to Slurm docker
======================
Add the code of your simulation to the *simcity-slurm/simulations* directory. Preferably in an seperate subdirectory, for instance
*simcity-slurm/simulations/mysim*.

This directory is copied during building the docker image into */home/xenon/simulations/* inside the docker image.
E.g. your simulation will be available from the path */home/xenon/simulations/mysim/* when you ssh into the docker container.

If your simulation depends on certain libraries to be installed you need to edit the *simcity-slurm/Dockerfile*.
In the Dockerfile you will find the following snippet:

.. code: docker

    # Add the dependencies for your simulation here
    USER root
    RUN export DEBIAN_FRONTEND=noninteractive && apt-get install -y openjdk-7-jre

This line installs the java 7 jre. If your simulation does not use java you can remove it here and replace it with other ubuntu packages.
If you use python I would suggest to create a virtual environment and use pip to install your requirements, for instance from a requirements.txt.

.. code:: docker

    RUN cd /home/xenon/mysim \ 
        && virtualenv mysim \
        && . mysim/bin/activate \
        && pip install -U pip \
        && pip install -r requirements.txt

For more information on running commands in a dockerfile please refer to the `dockerfile manual <https://docs.docker.com/engine/reference/builder/#/run>`__.

Configuring the webservice
==========================

To configure the webservice you will need to ad a json file to the webservice docker that describes the input to the simulation.
This serves the purpose of letting the front end know which fields to display for input and enables us to validate the input parameters
before sending it to the simulation.

The description of the input parameters for your simulation should be in `json schema format <http://json-schema.org/>`__.
We render the input form using `Angular schema form <http://schemaform.io/>`__. More detail is given in section Simulation json.

Furthermore the description of the simulation points to a *resourceTypeUrl*, this is a file that is served by the webservice as well
that describes the geojson output of your simulation so the front-end can display it nicely. This is discussed in section Resource type json.

Simulation json:
----------------
Similar to adding your code to the slurm docker image you create a json file in the *simcity-webservice/simulations* directory.
This json file should have the following layout:

.. code:: json

    {
        "latest": "0.2",    # latest and stable are two standard labels that you should include 
        "stable": "0.1",    # the default label for the webservice is 'latest'
        "mylabel": "two",   # You can define any label you like however and link it to one of the
                            # full definitions below
        "0.1": {            # Each version should be a complete description of the input for your
            ...             # simulation as explained below.
        },
        "0.2": {
            ...
        },
        "two":              # These are just strings, so they can be anything.
            ...             # Semantic versioning (cf. http://semver.org/) might not be a bad
                            # idea though.
        }
    }


The description of your simulation should have to the following layout. 

.. code:: json

    "0.1": {
        "command": "~/simulations/mysim/run_mysim.sh",      # The command to run the simulation
        "parallelism": "*",                                 # The number of cores the simulation uses by itself, * means all.
                                                            # this allows sim-city-client to run multiple instances of your
                                                            # simulation on the same node if the number of cores allows. 
        "resourceTypeUrl": "/explore/resource/mysim",       # Url for the resource type json file. This can be any url, but
                                                            # the next section explains how to add it to the webservice
        "form": [                                           # Optional description of how to display the form for submitting
            ...                                             # a simulation of this type. Required if using geo coordinates as
        ],                                                  # an input.
        "properties": {                                     # json-schema description of the input.
            ...
        },
        "required": [                                       # List of required fields.
            ...
        ]
    }

Properties:
~~~~~~~~~~~
The properties describe to the system which parameters your simulation uses and what their type is.
The example below shows one such a parameter called *populationSampleFactor* which is a of the number type
it has a maximum and a minimum and a default value. These are used by the system to check input before running
your simulation as well as to **render the form on the interface**.

Below are two examples of parameters, please refer to the `json schema website <http://json-schema.org/>`__ and
this `guide <https://spacetelescope.github.io/understanding-json-schema/about.html>`__.

.. code:: json

    "properties": {
        "populationSampleFactor": {         # Example of a parameter that is a number
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "default": 0.1,
            "title": "Commute factor",
            "description": "portion of the population (totalling 8.5 million) that commutes"
        },
        "fireStations": {                   # Example of an array parameter
            "title": "Fire stations",
            "minItems": 0,
            "type": "array",
            "startEmpty": true,
            "items": {                      # With an array parameter each item must be 
                "type":"object",            # described as well
                "properties": {             # Each item in this case has an x and y coordinate
                    "id": {                 # as well as an id. This is an example of a geo-
                        "type":"string"     # coordinate
                    },
                    "x": {
                        "type":"number"
                    },
                    "y": {
                        "type":"number"
                    }
                },
                "required": ["x","y"]
            },
            "description": "Please add one or more fire stations to the map",

            # This message is shown when the form does not validate on this field 
            "validationMessage": "Please add at least one fire station"
        }
    }

Form:
~~~~~
Form is an array in the description that is used by angular json schema form to render the form.
The order of this array determines the order of the fields in the form.

Below is an example. populationSampleFactor does not have any special configuration.
fireStations however is special, it has a number of configuration fields, both for the
configuration of its display as well as to let the frontend know this is a geo-coordinate input.

.. code:: json

    "form": [
        "populationSampleFactor",
        {
            "key": "fireStations",          # The key used in the form
            "startEmpty": true,             # Do not add a default first item
            "add": null,                    # Do not put an add button in the form
            "remove": null,                 # Do not put a remove button in the form
            "type": "layer",                # Special type to tell the frontend that this field
                                            # comes from a geojson layer
            "layer": "test_sim",            # The name of the layer
            "featureId": "FireStation",     # featureId of this type. See Resource type json section
            "items": [
                {
                    "type": "point2d"       # Special display of this type for each item that can be
                }                           # defined in sim-city-cs
            ]
        }
    ]



Resource type json:
-------------------

Troubleshooting
===============

My simulation does not run
    Please check if your simulation run script is executable from whithin the docker container. To do this start the sim-city stack
    with *docker-compose up --build* then ssh into the docker container using *ssh -p10022 xenon@localhost* using password javagat.
    Best is to debug your simulation now by running it inside the container in this manner.

    If your simulation is running in this manner check whether there is a problem with the paths of where simcity-client is calling
    your simulation.