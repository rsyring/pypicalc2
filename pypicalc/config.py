from __future__ import absolute_import
from __future__ import unicode_literals

import pathlib

project_dpath = pathlib.Path(__file__).parent


class DefaultProfile(object):
    """
        These values will apply to all configuration profiles.
    """
    # It's tempting to turn this off to avoid the warning, but if you are storing passwords
    # in your settings, leave this enabled and setup a keyring.  See the app's keyring related
    # commands for help.
    KEG_KEYRING_ENABLE = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestProfile(object):
    KEG_KEYRING_ENABLE = False
    # Default creds for CI testing.
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@database/testdb'
    MAIL_DEFAULT_SENDER = 'fakesender@example.com'
