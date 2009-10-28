.. _gettingstarted_creating_languagelibraries:

===========================
Defining Language Libraries
===========================

Language libraries are programming code libraries that are installed using a programming language-specific tool and are therefore operating system agnostic. ``easy_install`` for python, ``gem`` for ruby, ``cpan`` for perl, and ``pear`` for PHP are all examples of these language-specific tools.

Defining a New Language Library
===============================

1. In the admin, click the **Add** button on the **Language Library** line.

   .. image:: images/add_languagelibrary.png
      :alt: Click the Add button on the Language Library line.

2. Select a programming language from the drop down menu.

3. Enter the name of the library.

4. Enter the command to install the library.

5. Enter the command to see if the library is installed.

6. Uncheck the **Must sudo** checkbox if the command does not require root privileges for installation.

   .. image:: images/add_languagelibrary_form.png
      :alt: A completed language library entry form

7. Click on the **Save** button.