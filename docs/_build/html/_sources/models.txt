.. _models:

======
Models
======

.. figure:: _static/OMG_schema_example.png
   :alt: Schema using examples

   Here is a simple diagram of the how the classes connect, using example data
   to help illustrate the connections

.. _models-service:

Services and Commands
=====================

*Services* are processes like Apache httpd, memcached and the like. A service may have *Commands* to do things like start it, stop it, and reload its configuration.

For example **Service** Apache httpd has **Command**\ s start, stop, reload, status, and config_test.

Services and commands do not include any implementation information. All implementation is done in the :ref:`ServerOS <models-serveros>`\ .


.. _models-serveros:

ServerOS, ServicePackage and ServiceCommand
===========================================

An operating system for a server. The ServerOS describes how to install system packages (using apt or yum for example), which packages are required

.. _models-servicepackage:

ServicePackage
==============
The package or packages required to install the :ref:`Service <models-service>` on to the :ref:`Server Operating System <models-serveros>`. Installation of the Service will use the package manager commands indicated in the Server Operating System.

.. _models-servicecommand:

ServiceCommand
==============
Commands for services based on the operating system.

.. _models-languagelibrary:

LanguageLibrary
===============
A library for a language, typically installed with a language-specific tool

.. _models-server:

Server
======
A machine with services and web sites.

.. _models-website:

WebSite
=======
A web site that is on one or more servers


