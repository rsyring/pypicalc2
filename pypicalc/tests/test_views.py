from __future__ import absolute_import
from __future__ import unicode_literals

import flask
import flask_webtest


class ViewBase(object):

    @classmethod
    def setup_class(cls):
        # anonymous user
        cls.ta = flask_webtest.TestApp(flask.current_app)


class TestPublic(ViewBase):

    def test_home(self):
        resp = self.ta.get('/')
        assert resp.text == 'Hello World from PyPI Calc 2!'

    def test_name(self):
        resp = self.ta.get('/Randy')
        assert resp.text == 'Hello Randy!'
        resp = self.ta.get('/Nate')
        assert resp.text == 'Hello Nate!'

    def test_ping(self):
        resp = self.ta.get('/ping')
        assert resp.text == 'pypicalc ok'
