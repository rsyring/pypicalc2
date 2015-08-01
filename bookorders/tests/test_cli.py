from __future__ import absolute_import
from __future__ import unicode_literals

from keg.testing import CLIBase

from bookorders.app import BookOrders


class TestCLI(CLIBase):
    app_cls = BookOrders

    def test_hello(self):
        result = self.invoke(cmd_name='hello')
        assert 'Hello World\n' == result.output
