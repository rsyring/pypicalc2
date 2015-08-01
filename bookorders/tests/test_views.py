from __future__ import absolute_import
from __future__ import unicode_literals

import flask
from flask.ext.webtest import TestApp


class ViewBase(object):

    @classmethod
    def setup_class(cls):
        # anonymous user
        cls.ta = TestApp(flask.current_app)


class TestPublic(ViewBase):

    def test_home(self):
        resp = self.ta.get('/')
        assert resp.text == 'Hello World from BookOrders!'

    def test_ping(self):
        resp = self.ta.get('/ping')
        assert resp.text == 'bookorders ok'
