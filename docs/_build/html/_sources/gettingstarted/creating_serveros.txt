.. _gettingstarted_creating_serveros:

====================
Creating a Server OS
====================

The server operating system is where the implementation of services is described. It also describes how services are installed and how you can tell if a service is in fact installed.

There are three parts to defining a Server OS: :ref:`How Things are Done`, :ref:`How Services are Installed`, and :ref:`How a Service Commands are Executed`.

.. _howthingsaredone:

Defining "How Things are Done"
==============================

1. In the admin, click the **Add** button on the **ServerOSes** line.

   
   .. image:: images/add_serveros.png
      :alt: Click the Add button on the ServerOSes line.
   

2. In the top part of the form, enter the name of the operating system, the command to install a package and the command to find if a package is installed. The commands can use the placeholder ``%(package)s`` for the package name; multiple times if necessary.

   
   .. image:: images/add_serveros_form.png
      :alt: The Add ServerOS form filled out.
   

   In this case, ``Ubunutu``, the command to install a package is ``apt-get install -ym %(package)s``. The command to find whether or not a package is installed is more complex. The command to list all installed packages ``dpkg -l %(package)s`` is piped (``|``) through ``grep %(package)s`` to find the package name in the list.


.. _howservicesareinstalled:

Defining "How Services are Installed"
=====================================

1. Select the service from the popup menu in the **Service** column.

2. Type in the name of the package or packages that are required to implement this service on this ServerOS in the **Package** column. Separate packages by spaces.
   
   For example, to implement ``Apache 2.2`` on ``Ubuntu``, the packages required are: ``apache2.2-common apache2-mpm-worker apache2-utils apache2 libapache2-mod-wsgi``.
   
   .. image:: images/add_service_package.png
      :alt: Defining how a service is installed.

.. _howaservicecommandsareexecuted:

Defining "How a Service Commands are Executed"
==============================================

1. Select the service's command from the popup menu in the **Command** column.

2. Type in the command to execute it on this Server OS in the **Command string** column.

3. Make sure the checkbox in the **Must sudo** column is checked (the default) if this command must be executed with superuser privileges, or unchecked if it does not.
   
   For example to implement the ``Apache 2.2 start`` command on ``Ubuntu``, the string ``/etc/init.d/apache2 start`` must be executed with superuser privileges.
   
   .. image:: images/add_service_command.png
      :alt: Defining how this Server OS executes a command for a service.

4. Click on the **Save** button.