from __future__ import absolute_import
from __future__ import unicode_literals

import logging

import flask

public = flask.Blueprint('public', __name__,)
log = logging.getLogger(__name__)


@public.route('/')
@public.route('/<name>')
def home(name='World from PyPI Calc 2'):
    return 'Hello {}!'.format(name)
