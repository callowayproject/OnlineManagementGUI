GETTING SET UP FOR THE FIRST TIME
---------------------------------

1. Bootstrap your environment. This only needs to be done once:

    ./setup/_bootstrap.sh


2. Create a virtual environment (it doesn't need to be named omg,
   but name it something you'll remember):

    mkvirtualenv omg


3. Install the "pip" Python package manager in the new virtual environment:

    easy_install pip


4. Upgrade to the latest version of the packages:

    ./bin/install.sh




WHAT YOU SHOULD DO EVERY DAY
----------------------------

1. Switch to the correct virtual environment:

    workon omg

2. Upgrade to the latest code:

    ./bin/upgrade.sh

3. Start your local development server:

    ./manage.py runserver 0.0.0.0:8000