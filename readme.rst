.. default-role:: code

PyPi Calc 2
######################################

.. image:: https://circleci.com/gh/rsyring/pypicalc2.svg?&style=shield
    :target: https://circleci.com/gh/rsyring/pypicalc2

.. image:: https://coveralls.io/repos/rsyring/bookorders/badge.svg?branch=master
    :target: https://coveralls.io/r/rsyring/bookorders?branch=master


Created as a companion application for `Testing Application Boundaries`__ presentation at
Code PaLOUsa 2016.

.. __: http://www.codepalousa.com/Sessions/679

Environment Assumptions
=======================

- You have a PostgreSQL server available, preferably with user/password/db setup according to
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

        SQLALCHEMY_DATABASE_URI = 'postgresql://pypicalc2:pypicalc2@localhost/pypicalc2'


    class TestProfile(object):
        SQLALCHEMY_DATABASE_URI = 'postgresql://test:test@localhost/test'


Python 3 Gotchas
=================

Since this is a Python 3 project, take note of the following:

    * The wheelhouse uses the "pip" executable.  You will likely have to be in a virtualenv for this
      to work since "pip" will usually point to the python 2 system version of pip.


Virtualenv Setup
=================

This project uses a wheelhouse.  Therefore, you should consider virtualenvs temporary.  In order
to easily get a virtualenv setup when you are ready to work on the project, run::

    source scripts/make-env-vex.sh

