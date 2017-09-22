.. _installation:

Installation
============
The installation of Re-GIS consists of six steps. Re-GIS relies on the external programs ``docker``, ``docker-compose`` and ``git``. If you already have these programs on your computer, you may skip the three first steps.

1) Install ``docker``. The docker documentation explains how to `install docker <https://docs.docker.com/engine/getstarted/>`__.

2) Install ``docker-compose``. The docker-compose documentation outlines how to  `install docker-compose <https://docs.docker.com/compose/install/>`__.

3) Install ``git``. The git webiste explains how to `install git <https://git-scm.com/downloads>`__.

4) Download Re-GIS from the git website:

.. code:: shell

    git clone https://github.com/ReGIS-org/regis-stack.git

This creates a new directory with the name ``regis-stack`` with all Re-GIS software

5) Start Re-GIS server via docker-compose:

.. code:: shell

   cd regis-stack
   docker-compose up --build

The server can stopped by pressing  ``ctrl-c`` in the same window

6) Examine Re-GIS in a webbrowser:

.. code:: shell

    open http://localhost:8008

An alternative is to open the address http://localhost:8008 in a webbrowser.
