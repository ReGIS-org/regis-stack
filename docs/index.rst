.. Sim-City-CS documentation master file, created by
   sphinx-quickstart on Thu Sep 15 11:56:58 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Sim-City Documentation
=======================================
The SIM-CITY Common Sense project is the front-end for the sim-city simulation framework.
It is based on the `csWeb framework <https://github.com/TNOCS/csWeb>`__.

Before You Start
----------------
The SIM-CITY Common Sense project is the front-end for the sim-city assisted decision support framework.

This framework consists of multiple components that work together:

The web-interface
    The web interface displays geo-spatial data and allows for filtering and colouring of the data.
    It also provides an easy interface for scenario exploration through running simulations.

The webservice
    The webservice is the middleware between the web-interface and the task scheduling tool Barbeque.
    The web interface communicates with the webservice using REST calls which return json documents.

Sim-city-client
    The sim-city-client is a task scheduling tool that takes care of scheduling simulations to be run on compute
    infrastructure such as Lisa or DAS-5.

CouchDB
    Barbeque stores the tasks in a couchdb database. The web-service also redirects to the couchdb to
    provide some json documents to the front-end.

Webdav
    Webdav is used to store the results of the simulations. The easiest way to use webdav is to create
    an account at `beehub <https://beehub.nl/system/>`__. According to `this page <https://userinfo.surfsara.nl/systems/beehub/new-users>`__
    the first 100GB of storage here is free.

NginX
    `Nginx <https://www.nginx.com/resources/wiki/>`__ is a http server that allows for easy configuration of
    which url redirects where. This is needed to prevent cross-site access issues.


In order to use the web-interface therefore these services need to be set up. Depending on your usage scenario
you can use docker images or install locally.

Contents:
---------
.. toctree::
   :maxdepth: 2

   installation
   NewProject

