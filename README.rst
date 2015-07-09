Requirements
============

OSCM Prototype requires:

* Python==3.4.2
* Django==1.7.3
* django-extensions==1.4.9
	- six [required: >=1.2, installed: 1.9.0]
* mysqlclient==1.3.6
* wheel==0.24.0


Usage
=====

Enter the project and take a look around::

.. code-block:: console

	$ cd smsystem/
	$ ls

Create a GitHub repo and push it there::

.. code-block:: console

	$ git init
	$ git add .
	$ git commit -m "first commit"
	$ git remote add origin ssh://git@pm.ti.bfh.ch/smsystem.git
	$ git push -u origin master

Now take a look at your repo. Don't forget to carefully look at the generated README.

MySQL and SQLite databases are supported.

Getting up and running
======================

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv (see below)
* MySQL (replace your configurations in the setting files)


Development and Testing
=======================

Dependencies for developing OSCM are listed in requirements.txt.
Use of a virtual environment is strongly recommended.

First make sure to create and activate a virtualenv_, then open a terminal at the project root and install the requirements for local development::

.. code-block:: console

	$ virtualenv .
	$ source bin/activate

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

.. code-block:: console

	(env)$ pip install -r requirements.txt
	(env)$ pip install -e .

For Django >= 1.7, create the database tables with Django's ``makemigrations``, ``migrate`` and create a superuser with ``createsuperuser``.

.. code-block:: console

	(env)$ python manage.py makemigrations
	(env)$ python manage.py migrate
	(env)$ python manage.py createsuperuser

Check your setup by starting a Web server on your local machine:

.. code-block:: console

	(env)$ python manage.py runserver

Direct your browser to the ``Django`` ``/admin`` and log in.

.. code-block:: console

	127.0.0.1:8000/admin

Support
=======

Bugs may be reported at https://pm.ti.bfh.ch/projects/smsystem/issues/new
