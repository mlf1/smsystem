##########################################
Deploy and install on the test environment
##########################################


Connect to the test server
==========================

.. code-block:: console

    $ ssh saitis.bfh.ch

Installation (requirements)
===========================

.. code-block:: console

    $ sudo -i (pwd=bfh)

* Install Python (3.4.2):
    .. code-block:: console

        $ apt-get install python3-setuptools
        $ apt-get install python3-dev

* Install Pip (7.0.3):
    .. code-block:: console

        $ easy_install-3.4 -U pip OR apt-get install python3-pip

* Install Virtualenv (13.0.1):
    .. code-block:: console

        $ easy_install-3.4 -U virtualenv

* Install Git (2.1.4):
    .. code-block:: console

        $ apt-get install git

* Install GetText for Ubuntu:
    .. code-block:: console

        $ apt-get install get text

* Install MySql server (5.5.43):
    .. code-block:: console

        $ apt-get install mysql-server mysql-client libmysqlclient-dev python-dev

* Install GCC:
    .. code-block:: console

        $ apt-get install gcc

In the following steps we’ll use the *"myproject"* directory for the base folder of the project, location: *"/home/sysadmin/myproject"*

Create a virtual environment, following the command lines below:
================================================================

.. code-block:: console

   $ cd /home/sysadmin/myproject
   $ virtualenv myenv

Activate the virtual environment:

.. code-block:: console

    $ source /home/sysadmin/myproject/myenv/bin/activate
    (myenv) $

Deactivate the virtual environment:

.. code-block:: console

    (myenv) $ deactivate
    $

SMTP server:
============

You can use Postfix (on *Linux*) or create a test *SMTP* server with *Django* just run this command via the *python shell* you had set up.
It will not send the email buy as you run tests you will be able to see the content of your email display in the *shell* window.

.. code-block:: console

    (myenv) $ python -m smtpd -n -c DebuggingServer localhost:1025

You can create a specific alias about it:

.. code-block:: console

    (myenv) $ alias mailserve='python -m smtpd -n -c DebuggingServer localhost:1025'

You must now configure email in the *settings file* of *Django* (*local, test, dev,...*):

.. code-block:: python

    # Email setup (example)
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'someone@bfh.ch'
    EMAIL_HOST_PASSWORD = 'the_password'
    EMAIL_PORT = 587
    DEFAULT_FROM_EMAIL = 'some.mail@bfh.ch'

Tools
=====

Create a *".bash_aliases"* file in home directory and set the following commands:

.. code-block:: sh

    alias ll=‘ls -Al’

    # Go to OSCM directory
    alias oscm=‘cd /home/sysadmin/myproject/smsystem’

    # Activate the virtual environment
    alias myenv=’source /home/sysadmin/myproject/myenv/bin/activate’

Use the following command line to directly activate the new aliases:

.. code-block:: console

    (myenv) $ source .bashrc

Git
---

Go to the base directory project and retrieve the *"Testing"* branch:
    Requirements : activate https on the repository (*in Redmine*)

.. code-block:: console

    (myenv) $ git clone —branch Testing "https://pm.ti.bfh.ch/projects/smsystem/settings/repositories/smsystem.git"

Pip
---

Install the dependencies of the *OSCM* application:

.. code-block:: console

    (myenv) $ cd /home/sysadmin/myproject/smsystem
    (myenv) $ pip install -r requirements.txt

Logs
----

Create the *"logs"* directory:

.. code-block:: console

    (myenv) $ mkdir -r /home/sysadmin/myproject/smsystem/oscm/logs

Set logger in *info* level for the *OSCM* application (in the *settings* file):

.. code-block:: python

    DEBUG = False
    ...
    TEMPLATE_DEBUG = False
    ...
    ALLOWED_HOSTS = ['*’] <— set at least a allowed host and use it
    ...
        'oscm_app': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(
                LOG_BASE_DIR,
                'oscm_app.log'),
            'formatter': 'simple',
            'filters': ['require_debug_false’],
        }

Database
--------

Build db:

.. code-block:: console

    (myenv) $ cd /home/sysadmin/smsystem/oscm
    (myenv) $ python manage.py makemigrations
    (myenv) $ python manage.py migrate
    (myenv) $ python manage.py createoscmsuperuser

Translation files
-----------------

Where ?

The *translation* files (*django.po* files) are in the following directory ordered by language (*de, en, fr*):

.. code-block:: console

    (myenv) $ cd /home/sysadmin/smsystem/oscm/oscm_app/core/locale

Retrieve all translations (*old and new*) from the source code (*py* files and *html* files):

.. code-block:: console

    (myenv) $ python manage.py makemessages -a

Create the *translation* files (*django.mo* files):

.. code-block:: console

    (myenv) $ python manage.py compilemessages

Static files
------------

Where ?

The *static* files (*pictures, css* files) are in the following directory:

.. code-block:: console

    (myenv) $ cd /home/sysadmin/smsystem/oscm/oscm_app/core/static

Create the static directory and collect the specific files:

.. code-block:: console

    (myenv) $ python manage.py collectstatic

The server
==============

How to launch the server ?

.. code-block:: console

    (myenv) $ python manage.py runserver 0.0.0.0:8000 --settings=oscm_system.settings.test --insecure

How to test it ?

You must launch a browser:

.. code-block:: html

    http://saitis.bfh.ch:8000