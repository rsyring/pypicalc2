from __future__ import absolute_import
from __future__ import unicode_literals

import logging

import flask

public = flask.Blueprint('public', __name__,)
log = logging.getLogger(__name__)


@public.route('/')
@public.route('/<name>')
def home(name=None):
    # Using this if statement instead of a default value above to demonstrate
    # code coverage.
    if name is None:
        say_hello_to = 'World from PyPI Calc 2'
    else:
        say_hello_to = name
    return 'Hello {}!'.format(say_hello_to)
