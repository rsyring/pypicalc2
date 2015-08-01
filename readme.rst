.. default-role:: code

Book Orders Demo Application
######################################

Created as a companion application for DB Testing prsentation at PyOhio 2015.

Environment Assumptions
=======================

- You have a PostgreSQL server available, preferrably with user/password/db setup according to
  `bookorders.conf:TestProfile`
- You have a recent version of Tox installed at the system or user level.

Running Tests
=============

- Make sure your DB settings match what is in `config.py:TestProfile` OR see next section.
- Run `tox` in the source directory.

Local Configuration Changes
===========================

In order to set configuration for your local environment, create
    `<project root>/bookorders-config.py` as below, changing db creds as needed::

    DEFAULT_PROFILE = 'DevProfile'


    class DevProfile(object):
        # secret key for Flask (fill it in with something random)
        SECRET_KEY = ''

        KEG_KEYRING_ENABLE = False

        SQLALCHEMY_DATABASE_URI = 'postgresql://bookorders:bookorders@localhost/bookorders'


    class TestProfile(object):
        SQLALCHEMY_DATABASE_URI = 'postgresql://test:test@localhost/test'


Python 3 Gotchyas
=================

Since this is a Python 3 project, take note of the following:

    * The wheelhouse uses the "pip" executable.  You will likely have to be in a virtualenv for this
      to work since "pip" will usually point to the python 2 system version of pip.


Virtualenv Setup
=================

This project uses a wheelhouse.  Therefore, you should consider virtualenvs temporary.  In order
to easily get a virtualenv setup when you are ready to work on the project, run::

    source scripts/make-env-vex.sh

