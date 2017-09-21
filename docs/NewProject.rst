.. _newproject:

Creating a New Project
**********************

This document describes the steps necesarry to create a new project within the sim-city web interface.

Before you start
================

In this document we assume that you have the sim-city webinterface and its prerequisites installed
and running, if not see :ref:`installation`

Create Project
==============
In the following examples we will call the new project MyProject, replace this with your own project name.

Creating your project consists of 3 steps:

* Creating a project directory
* Add your project to the projects.json file.
* Creating a project.json

Project Location
----------------
Projects in the sim-city-cs framework are located in public/data/projects/

Create a project directory
--------------------------
Create your project directory in the public/data/projects directory

From the sim-city-cs directory:

.. code:: shell

    cd public/data/projects
    mkdir MyProject

Add the project to the projects.json file
-----------------------------------------
Open the projects.json file located in public/data/projects

At the bottom of this json file you will find a key called *projects*.
This is a list of project objects. Add your project here with the following template:

.. code:: json

    "projects": [
        ...
        {
        "title": "MyProject",
        "url": "data/projects/MyProject/project.json"
        }
        ...
    ]

Create a project.json
---------------------
Use the project.json at the end of this page as a basis for your new project.
Below I go into the several parts of the project.json.

`Please note that json does not support comments. If you want to copy and paste
parts of the commented sections be sure to remove the comments. Also keep in mind
that parts are sometimes ommitted for readability.`

Main Structure
''''''''''''''
Below is the main general structure for a project in the sim-city-cs framework.

.. code:: json

    {
        "title": "MyProject",                       # The project Title. Any string
        "description": "Description for MyProject", # The project Description. Any string
        "url": "https://github.com/MyProject",      # Url of the project, if any
        "isDynamic": true,                          # isDyanamic means the changes to the
                                                    # project that are made using the user
                                                    # interface are saved to the disk
        "expertMode": 3,                            # Level of expertise of the use.
                                                    # For the simcity example project 3 is used
                                                    # Beginner     = 1
                                                    # Intermediate = 2
                                                    # Expert       = 3
                                                    # Admin        = 4
        "userPrivileges": {
            "mca": {                                # Set expert mode for Multi-Criteria Analysis
                "expertMode": true
            },
            "heatmap": {                            # Set expert mode for Heatmap
                "expertMode": true
            }
        },
        "baselayers": {},                           # Extra Baselayers to include
                                                    # see the section on baselayers
        "dashboards": [],                           # List of dashboards for the project
                                                    # see the section on dashboards
        "groups": [],                               # A list of layer groups
                                                    # see the section on groups
        "simAdmin": {                               # Extra data for the simulation administrator
            "webserviceUrl": "/explore",            # The url for the sim-city-webservice
                                                    # Using the docker stack this is /explore
                                                    # which is short for http://localhost/explore
            "simulationName": "MySimulation",       # The name of the default simulation
            "simulationVersion": "latest"           # The name of the default version
        }
    }


.. _input-formats:

Input Format
''''''''''
Re-GIS works with GeoJSON or JSON input files. Other GIS standards include GML, SHP, KML, CSV.
For more information, see, e.g. `<https://www.datavizforall.org/transform/>`_.


Dashboards
''''''''''
The *dashboards* section describes which dashboards a project has, it is a list of dashboard objects.
Each dashboard can hold one or more widgets described in the widgets subsection.

The sim-city example project has two dashboards: The Home dashboard and the Job Monitor dashboard.

.. code:: json

    "dashboards": [{
        "id": "home",                   # ID of the dashboard
        "name": "Home",                 # Name of the dashboard
        "editMode": false,              # Whether it starts in edit mode
        "showMap": true,                # Whether to show the map
        "showTimeline": false,          # Whether to show the timeline
        "showLeftmenu": true,           # Whether to show the menu on the left
        "showLegend": true,             # Whether to show the legend
        "showBackgroundImage": false,   # Whether to show the background layers
        "visiblelayers": [              # List of layers that are visible by default
            "fireresponse"              # This is a list of layerids
        ],                              # These layers are defined further in the document
        "widgets": [                    # List of widgets on the dashboard, explained below
            ...
        ],
        "visibleLeftMenuItems": [       # Which of the menu items in the left menu start
            "!lm-layers"                # as visible. Default is layers
        ]
    },
    ...
    ]

Widgets
"""""""

The *widgets* section is a list of widgets included in the *dashboard*.
In the simcity example project the home dashboard has a *buttonwidget* to allow the user the drag and drop features for the simulation
on the map and a *simulation-form* widget for the form to submit a simulation.

.. code:: json

    "widgets": [{
            "id": "1086ec94-4c54-4d84-dc04-9d3673df6d35",   # The id of the widget,
                                                            # must be unique to the project
            "directive": "buttonwidget",                    # Which angular directive to use
            "enabled": true,                                # Enabled by default?
            "style": "transparent",                         # The display style
            "left": "435px",                                # How far from the left to display it
            "right": "",                                    # How far from the right to display it
            "top": "82px",                                  # How far from the top to display it
            "width": "300px",                               # The width of the widget
            "data": {                                       # Data that will be passed to the widget
                "layerGroup": "MyProject",
                "buttons": []
            },
            "collapse": false                               # Whether or not to hide the widget
                                                            # at the start
        },
        ...
        ]

Groups
''''''

A group is a set of layers grouped together under a common name.
These groups are displayed under a collapsable name in the left menu under layers.


.. code:: json


    {
        "id": "MyLayer",                                    # The id of the layer group
        "languages": {                                      # There is some support for multiple
                                                            # languages
            "en": {
                "title": "My Layer",                        # The name of the layer gropu in english
                "description": "My Awesome Layer"           # Description of the layer group
            }
        },
        "layers": [                                         # List of layers to include
			...
        ]
    },
    ...

Example Layer
"""""""""""""

.. code:: json

    {
        "id": "MyLayer",                                    # id of the layer
        "reference": "mylayer",                             # Reference name
        "languages": {
            "en": {
                "title": "My Layer",                        # Layer name
                "description": "My Description"             # Layer description
            }
        },
        "type": "GeoJson",                                  # Type of the data in the layer
                                                            # GeoJSON (default), TopoJSON, or WMS

        "url": "resources/myData.json",                     # Location of the data. Can be a url
                                                            # or a path relative to the public folder

        "typeUrl": "resources/myTypes.json",                # Location of the resource type
                                                            # description. For more information on
                                                            # this see the resource type
                                                            # documentation.

        "enabled": false,                                   # Whether the layer is enabled by default

        "opacity": 50                                       # The opacity (e.g. inverse transparancy)
                                                            # of the layer
    },

More about resource type JSON, see section :ref:`resource-type-json`.

It is also possible to define a layergroup where the layers are taken from an external server. For instance using ows:

.. code:: json

    {
        ...
        "clustering": true,                                 # Clustering means the features of
                                                            # different layers are combined and
                                                            # stored in one big list

        "layers": [],                                       # Layers can be empty

        "owsurl": "http://my.url.to/an/ows/server",         # Url of the ows server

        "owsgeojson": true                                  # Let the system know this is an OWS
                                                            # layer group
    }

Baselayers
''''''''''
You can include extra baselayers on top of those defined in the projects.json file.
Below is an example for OpenStreetMap (which is already defined in the projects.json file, this is only to illustrate).

.. code:: json

    {
        "title": "OpenStreetMap HOT",
        "subtitle": "Road",
        "url": "http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
        "isDefault": false,
        "minZoom": 0,
        "maxZoom": 19,
        "cesium_url": "http://c.tile.openstreetmap.fr/hot/",
        "cesium_maptype": "openstreetmap",
        "subdomains": ["a", "b", "c"],
        "attribution": "Tiles courtesy of <a href='http://hot.openstreetmap.org/' target='_blank'>Humanitarian OpenStreetMap Team</a>",
        "preview": "http://b.tile.openstreetmap.fr/hot/11/1048/675.png"
    }


Full Project json file
''''''''''''''''''''''

.. code:: json

    {
        "title": "MyProject",
        "description": "Description for MyProject",
        "url": "https://github.com/MyProject",
        "isDynamic": true,
        "expertMode": 3,
        "userPrivileges": {
            "mca": {
                "expertMode": true
            },
            "heatmap": {
                "expertMode": true
            }
        },
        "baselayers": {},
        "dashboards": [{
            "id": "home",
            "name": "Home",
            "editMode": false,
            "showMap": true,
            "showTimeline": false,
            "showLeftmenu": true,
            "showLegend": true,
            "showBackgroundImage": false,
            "visiblelayers": [
                "fireresponse"
            ],
            "widgets": [{
                "id": "1086ec94-4c54-4d84-dc04-9d3673df6d35",
                "directive": "buttonwidget",
                "enabled": true,
                "style": "transparent",
                "left": "435px",
                "right": "",
                "top": "82px",
                "width": "300px",
                "data": {
                    "layerGroup": "MyProject",
                    "buttons": []
                }
            },
            {
                "id": "simulation-form",
                "directive": "sim-form",
                "enabled": true,
                "style": "transparent",
                "left": "435px",
                "right": "",
                "top": "180px",
                "bottom": "25px",
                "width": "450px",
                "data": {
                    "layerGroup": "MyProject"
                },
                "collapse": true
            }],
            "visibleLeftMenuItems": [
                "!lm-layers"
            ]
        },
        {
            "id": "monitor",
            "name": "Job Monitor",
            "editMode": false,
            "showMap": false,
            "showTimeline": false,
            "showLeftmenu": false,
            "showLegend": false,
            "showBackgroundImage": true,
            "visiblelayers": [
            ],
            "widgets": [{
                "id": "9086ec94-4c54-4d84-dc04-9d3673df6d35",
                "directive": "sim-summary",
                "enabled": true,
                "style": "transparent",
                "left": "50px",
                "right": "",
                "top": "82px",
                "width": "300px"
            },
            {
                "id": "cb86ec94-4c54-4d84-dc04-9d3673df6d35",
                "directive": "sim-job",
                "enabled": true,
                "style": "transparent",
                "left": "375px",
                "right": "",
                "top": "82px"
            }
            ],
            "visibleLeftMenuItems": []
        }
        ],
        "groups": [
        {
            "id": "MyProject",
            "languages": {
                "en": {
                    "title": "MyProject",
                    "description": "MyProject layers manipulation buttons"
                }
            },
            "layers": []
        }],
        "simAdmin": {
            "webserviceUrl": "/explore",
            "simulationName": "MySim",
            "simulationVersion": "latest"
        }
    }
