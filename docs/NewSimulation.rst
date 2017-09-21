.. _newsim:

Adding a New Simulation
***********************

Adding a new simulation consists of the following steps:

1.  Setting up your simulation.
2.  Adding the simulation to the slurm docker.
3.  Configuring the webservice.

Setting up your simulation
==========================
In order to run your simulation using the sim-city stack it needs to adhere to a few conventions.

One command
    Your simulation needs to be able to be run with one command. If your simulation requires
    several commands to be called in succession you should use a bash script to call the commands
    one after the other.

One json input file
    The simcity webservice will supply your simulation with one json input file. This input file will be
    placed in an input directory. This input directory is available as an environment variable *$SIMCITY_IN*, or can be supplied
    as an argument to your script if set up correctly in the webservice. For more information on the standards of GIS data, see :ref:`input-formats`.

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

Simulation json
---------------
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

Properties
~~~~~~~~~~
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

Form
~~~~
Form is an array in the description that is used by angular json schema form to render the form.
The order of this array determines the order of the fields in the form.

Below is an example. populationSampleFactor does not have any special configuration.
fireStations however is special, it has a number of configuration fields, both for the
configuration of its display as well as to let the frontend know this is a geo-coordinate input.

Most important here is that its type is "layer", this means the front-end expects this input to
be given on a special layer. The name of this layer is given in the "layer" field, this layer is
created automatically when this simulation is selected for the front-end.

This in combination with the resourceType description the front-end creates drag-and-drop buttons
to add this feature to the input layer.

.. code:: json

    "form": [
        "populationSampleFactor",
                ...
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


.. _resource-type-json:

Resource type json
------------------
The resource type description is also a json file. This json file describes the various types of data that are used in your
simulation, both in the input and the output.

Only properties that are defined in the *propertyTypeData* and are in the *propertyTypeKeys* of a featureType are available
for non-admin users to display and filter on.

Below is an example resource type description which describes three different feature types: FireStations, Fires and Wards.
FireStations and Fires are used for the input to the simulation, while wards is the output of the simulation.

The FireStation and Fire feature types describe a unique id and name for these types, as well as some *propertyTypeKeys*,
these keys reference the *propertyTypeData* section lower in the file.
The style description tells the front end how to display this feature type, which is also used to drag-and-drop these
features on the map. In this case it defines a "point" drawing mode using an icon as a display.

The Ward feature type also describes a unique id, a name and a number of *propertyTypeKeys*. In this case the drawing
mode is "polygon" which means a shape on the map. The most obvious options for drawing modes are: Point, MultiPoint, Polygon,
MultiPolygon, Line and PolyLine.

The *propertyTypeData* section describes the features properties, this is used in the display of the features properties
in the right sidebar in the user interface. As said before, describing your features here is crucial to allow non-admin
users to display and filter different properties.

.. code:: json

    {
        "id": "matsim",
        "title": "matsim",
        "featureTypes": {
            "FireStation": {
                "id": "SimCity#firestation",
                "name": "FireStation",
                "style": {
                    "drawingMode": "Point",
                    "iconUri": "images/brandweerposten/Brandweerkazerne.png",
                    "cornerRadius": 50,
                    "fillColor": "#ffffff",
                    "iconWidth": 30,
                    "iconHeight": 30,
                    "strokeColor": "#ffffff"
                },
                "propertyTypeKeys": "title,notes",
                "u": "bower_components/csweb/dist-bower/images/marker.png"
            },
            "Fire": {
                "id": "SimCity#fire",
                "name": "Fire",
                "style": {
                    "drawingMode": "Point",
                    "iconUri": "data/images/fire.png",
                    "cornerRadius": 50,
                    "fillColor": "#ffffff",
                    "iconWidth": 30,
                    "iconHeight": 30,
                    "strokeColor": "#ffffff"
                },
                "propertyTypeKeys": "title,notes",
                "u": "bower_components/csweb/dist-bower/images/marker.png"
            },
            "Ward": {
                "id": "SimCity#Ward",
                "name": "Ward",
                "style": {
                    "nameLabel": "ward_name",
                    "drawingMode": "Polygon",
                    "cornerRadius": 50,
                    "fillColor": "#999999",
                    "iconWidth": 30,
                    "iconHeight": 30,
                    "strokeColor": "#ffffff"
                },
                "propertyTypeKeys": "ward_name;ward_no;cmc_mc_nm;tot_p;first_responder;second_responder",
                "u": "bower_components/csweb/dist-bower/images/marker.png"
            }
        },
        "propertyTypeData": {
            "ward_no": {
                "label": "ward_no",
                "type": "text",
                "title": "Ward Number",
                "visibleInCallOut": true,
                "canEdit": false,
                "isSearchable": true,
                "section": "Metadata"
            },
            "ward_name": {
                "label": "Name",
                "type": "text",
                "title": "Name",
                "visibleInCallOut": true,
                "canEdit": false,
                "isSearchable": true,
                "section": "Metadata"
            },
            "cmc_mc_nm": {
                "label": "cmc_mc_nm",
                "type": "number",
                "title": "City Name",
                "canEdit": false,
                "isSearchable": true,
                "visibleInCallOut": true,
                "section": "Metadata"
            },
            "first_responder": {
                "label": "first_responder",
                "type": "number",
                "title": "First Responder",
                "canEdit": false,
                "isSearchable": true,
                "visibleInCallOut": true
            },
            "second_responder": {
                "label": "second_responder",
                "type": "number",
                "title": "Second Responder",
                "canEdit": false,
                "isSearchable": true,
                "visibleInCallOut": true
            },
            "tot_p": {
                "label": "tot_p",
                "type": "number",
                "title": "Total Population",
                "canEdit": false,
                "isSearchable": true,
                "visibleInCallOut": true
            }
        },
        "isDynamic": false
    }


Troubleshooting
===============

My simulation does not run
    Please check if your simulation run script is executable from whithin the docker container. To do this start the sim-city stack
    with *docker-compose up --build* then ssh into the docker container using *ssh -p10022 xenon@localhost* using password javagat.
    Best is to debug your simulation now by running it inside the container in this manner.

    If your simulation is running in this manner check whether there is a problem with the paths of where simcity-client is calling
    your simulation.
